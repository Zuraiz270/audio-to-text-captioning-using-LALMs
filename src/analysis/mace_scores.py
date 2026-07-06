"""MACE (Dixit et al., arXiv:2411.00321) on the poly/mono subsets — secondary RQ2 metric.

Runs the reference implementation (github.com/satvik-dixit/mace, cloned at
_mace_repo/) unmodified: method='combined' = CLAP audio-text + text-text
cosine with a FENSE-style fluency penalty. Backend: MS-CLAP-2023 (msclap),
NOT laion-clap — verified from the repo source.

Scope (timebox discipline): the three LALMs on the poly and mono subsets,
sharing one CLAP instance across calls so the model loads once. Audio
embeddings are recomputed per call by the reference implementation; we accept
that cost rather than modify validated code.

Runs in .venv-mace (dependency-light: stdlib + the repo's own deps):
  .venv-mace/Scripts/python.exe -m src.analysis.mace_scores [--models af3 salmonn qwen_omni]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MACE_DIR = REPO / "_mace_repo" / "mace_metric"
AUDIO_DIR = REPO / "data/clotho_v2.1/clotho_audio_evaluation/evaluation"


def _load_subset(path: Path) -> set[str]:
    return {ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs="+", default=["af3", "salmonn", "qwen_omni"])
    parser.add_argument("--subsets", nargs="+", default=["poly", "mono"])
    parser.add_argument("--out", type=Path, default=Path("results/mace_scores.json"))
    args = parser.parse_args()

    sys.path.insert(0, str(MACE_DIR))
    from mace import mace  # noqa: E402  (repo is flat-module style)
    from msclap import CLAP  # noqa: E402

    print("[mace] loading MS-CLAP-2023 once ...", file=sys.stderr)
    clap = CLAP(version="2023", use_cuda=False)

    out_path = REPO / args.out
    results: dict = {}
    if out_path.exists():  # resumable
        results = json.loads(out_path.read_text(encoding="utf-8"))

    subsets = {s: _load_subset(REPO / f"subsets/{s}.txt") for s in args.subsets}

    for model in args.models:
        pred = json.loads((REPO / f"results/{model}_eval.json").read_text(encoding="utf-8"))
        results.setdefault(model, {})
        for sname, keep in subsets.items():
            if sname in results[model]:
                print(f"[skip] {model}/{sname} already done", file=sys.stderr)
                continue
            items = [it for it in pred["items"] if it["file_name"] in keep]
            print(f"[mace] {model}/{sname}: {len(items)} clips ...", file=sys.stderr)
            t0 = time.time()
            # Chunked calls: msclap encodes ALL reference sentences of a call in
            # one forward pass (5 refs x 709 clips ~ 3.35 GB activation -> host
            # OOM). MACE's per-item scores are independent, so chunking and
            # averaging per-item scores is mathematically exact.
            import numpy as np
            per_item: dict[str, list[float]] = {}
            CHUNK = 100
            for i in range(0, len(items), CHUNK):
                chunk = items[i:i + CHUNK]
                # Clamp candidates to 30 words: msclap pads text to 77 GPT2
                # tokens but never truncates, so anything longer crashes its
                # collate. 30 words stays safely under 77 tokens; the clamp
                # touches 3/3135 captions total (incl. one degenerate 515-word
                # Qwen repetition loop). Uniform rule across models.
                _corpus, sents = mace(
                    method="combined",
                    candidates=[" ".join(it["prediction"].split()[:30]) for it in chunk],
                    mult_references=[it["references"] for it in chunk],
                    audio_paths=[str(AUDIO_DIR / it["file_name"]) for it in chunk],
                    clap_model=clap, device="cpu", batch_size=8,
                    return_all_scores=True, verbose=0,
                )
                for k, v in sents.items():
                    # some entries come back 0-dim; atleast_1d keeps extend valid
                    per_item.setdefault(k, []).extend(np.atleast_1d(np.asarray(v)).tolist())
                print(f"  [{min(i+CHUNK, len(items))}/{len(items)}]", file=sys.stderr)
            scores = {k: float(np.mean(v)) for k, v in per_item.items()}
            results[model][sname] = {"n_items": len(items), "scores": scores,
                                     "elapsed_sec": round(time.time() - t0, 1)}
            out_path.write_text(json.dumps(results, indent=1), encoding="utf-8")
            print(f"[done] {model}/{sname} in {time.time()-t0:.0f}s: {scores}", file=sys.stderr)

    print(f"[all done] -> {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
