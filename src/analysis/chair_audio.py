"""CHAIR-audio: closed-vocabulary caption-hallucination rates (RQ3).

Adapts CHAIR (Rohrbach et al., EMNLP 2018) from vision to audio. Vision CHAIR
counts caption objects absent from the image against a FIXED 80-class list; we
do the same against the 527-class AudioSet vocabulary (the ontology both our
SED tagger and AST use), so the metric stays deterministic and reproducible —
no learned NLP components.

Dual criterion (per the preregistration): an entity mentioned in a model's
caption is HALLUCINATED iff it appears in NEITHER
  (a) the union of the 5 human reference captions (matched with the same rule),
NOR
  (b) the audio's SED tag set = AudioSet classes whose framewise max prob >= tau
      (read from results/sed_framewise_summary.json; no extra inference).

Reported per model and per tau in {0.20, 0.25, 0.30} (0.25 primary, prereg
threshold-sensitivity bracket):
  CHAIR-i  = hallucinated entity mentions / all entity mentions
  CHAIR-s  = captions with >= 1 hallucinated entity / all captions
  coverage = captions with >= 1 matched entity / all captions

Known limitation (disclosed in the paper): vocabulary misses (synonyms outside
AudioSet surface forms) inflate rates uniformly across models; the paired
AF3-vs-SALMONN comparison (H4) largely cancels this bias.

Usage (in .venv):
  python -m src.analysis.chair_audio --out results/chair_audio.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TAUS = ("0.20", "0.25", "0.30")
MODELS = ("af3", "salmonn", "qwen_omni", "enclap", "cnn14", "ast")
# Generic AudioSet surface forms that match almost any caption ("sound",
# "noise", "speech" alternatives are kept — they are real event words) — we
# only drop pure structural words that would match every Clotho caption, plus
# the "etc." pseudo-alternative some labels carry.
_STOP_FORMS = {"sound", "audio", "background", "inside", "outside", "etc."}


def _clean(label: str) -> str:
    """Same rule as src/models/ast_tagging.py: drop parentheticals, lowercase."""
    return re.sub(r"\s*\([^)]*\)", "", label).strip().lower()


def build_vocab(labels: list[str]) -> dict[str, str]:
    """Map surface form -> canonical cleaned label.

    AudioSet display names carry comma-separated alternatives ("Domestic
    animals, pets"); each alternative becomes its own surface form pointing to
    the same canonical label.
    """
    vocab: dict[str, str] = {}
    for raw in labels:
        canonical = _clean(raw)
        for alt in canonical.split(","):
            form = alt.strip()
            if form and form not in _STOP_FORMS:
                vocab.setdefault(form, canonical)
    return vocab


def compile_matcher(vocab: dict[str, str]):
    """Word-boundary regex per surface form, longest-first.

    Uniform morphological variants only (no hand-curated synonyms): plural
    -s/-es and progressive -ing (with optional dropped final 'e', so "bark"
    matches "barking" and "whistle" matches "whistling").
    """
    patterns = []
    for form in sorted(vocab, key=len, reverse=True):
        stem = re.escape(form)
        # Dropped-e progressive ("whistle" -> "whistling") only for stems long
        # enough to stay unambiguous; short forms like "bee" would otherwise
        # collapse to "be" and match "being".
        if form.endswith("e") and len(form) >= 5:
            stem = re.escape(form[:-1]) + "e?"
        pat = re.compile(r"\b" + stem + r"(?:e?s|ing)?\b")
        patterns.append((pat, vocab[form]))

    def match(text: str) -> set[str]:
        text = text.lower()
        found: set[str] = set()
        for pat, canonical in patterns:
            if pat.search(text):
                found.add(canonical)
        return found

    return match


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", type=Path, default=Path("results/sed_framewise_summary.json"))
    parser.add_argument("--out", type=Path, default=Path("results/chair_audio.json"))
    args = parser.parse_args()

    from panns_inference import labels as audioset_labels

    repo = Path(__file__).resolve().parents[2]
    vocab = build_vocab(list(audioset_labels))
    match = compile_matcher(vocab)

    summary = json.loads((repo / args.summary).read_text(encoding="utf-8"))
    # audio tag sets per clip per tau, canonicalized like the caption entities
    audio_tags: dict[str, dict[str, set[str]]] = {}
    for clip in summary["clips"]:
        audio_tags[clip["file_name"]] = {
            tau: {_clean(a["label"]) for a in clip["per_tau"][tau]["active_labels"]}
            for tau in TAUS
        }

    out: dict = {"vocab_size": len(vocab), "taus": list(TAUS), "models": {}}
    indicators: dict = {}  # model -> tau -> {file_name: 0/1} (H4 input)

    for model in MODELS:
        pred = json.loads((repo / f"results/{model}_eval.json").read_text(encoding="utf-8"))
        rows = []
        for it in pred["items"]:
            ents = match(it["prediction"])
            ref_ents = set()
            for ref in it["references"]:
                ref_ents |= match(ref)
            rows.append((it["file_name"], ents, ref_ents))

        per_tau = {}
        indicators[model] = {}
        for tau in TAUS:
            n_mentions = n_halluc = n_caps_matched = n_caps_halluc = 0
            flags: dict[str, int] = {}
            for fn, ents, ref_ents in rows:
                tags = audio_tags.get(fn, {}).get(tau, set())
                halluc = {e for e in ents if e not in ref_ents and e not in tags}
                n_mentions += len(ents)
                n_halluc += len(halluc)
                n_caps_matched += bool(ents)
                n_caps_halluc += bool(halluc)
                flags[fn] = int(bool(halluc))
            n = len(rows)
            per_tau[tau] = {
                "chair_i": round(n_halluc / max(n_mentions, 1), 4),
                "chair_s": round(n_caps_halluc / n, 4),
                "coverage": round(n_caps_matched / n, 4),
                "mean_entities_per_caption": round(n_mentions / n, 3),
            }
            indicators[model][tau] = flags
        out["models"][model] = per_tau
        print(f"[{model}] " + " ".join(
            f"tau={t}: CHAIR-s={per_tau[t]['chair_s']:.3f}" for t in TAUS), file=sys.stderr)

    # per-clip indicator arrays only for the H4 pair (file size discipline)
    out["h4_indicators"] = {m: indicators[m] for m in ("af3", "salmonn")}

    out_path = repo / args.out
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[done] -> {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
