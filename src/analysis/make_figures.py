"""Generate every figure and LaTeX table for the term paper from results/*.json.

Nothing in the paper is hand-typed: tables are emitted as .tex includes and
figures as PDFs, all derived from the frozen results files. Re-running this
script reproduces the paper's numbers exactly.

Inputs it tolerates missing (skips with a note): subset scores (Table 2),
chair_audio.json (Table 3), hypothesis_tests.json (Table 4).

Usage (in .venv):  python -m src.analysis.make_figures
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parents[2]
PAPER = REPO / "deliverables/paper"
FIGS = PAPER / "figures"
TABLES = PAPER / "tables"

MODELS = [  # (results key, display name, kind, published SPIDEr-FL anchor or None)
    # Anchors: CNN14 0.261 = official DCASE 2023 Task 6A baseline result;
    # EnCLAP-base 0.291 = SPIDEr-FL measured for the released checkpoint with
    # the same aac-metrics toolkit (Kim et al., EnCLAP++, DCASE 2024 Workshop,
    # arXiv:2409.01201 Table 1). The ICASSP 2024 EnCLAP paper itself reports
    # SPIDEr 0.294/0.295 (no SPIDEr-FL).
    ("ast", "AST (tag template)", "floor", None),
    ("qwen_omni", "Qwen2.5-Omni-7B", "lalm", None),
    ("salmonn", "SALMONN-13B", "lalm", None),
    ("cnn14", "CNN14+BART (DCASE'23)", "trained", 0.261),
    ("enclap", "EnCLAP-base", "trained", 0.291),
    ("af3", "Audio Flamingo 3", "lalm", None),
]
KIND_COLOR = {"floor": "#9e9e9e", "lalm": "#1f77b4", "trained": "#d62728"}


def _scores(name: str) -> dict | None:
    p = REPO / f"results/{name}.json"
    if not p.exists():
        print(f"[skip] {p.name} missing", file=sys.stderr)
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def fig1_spider_bar() -> None:
    rows = [(disp, _scores(f"{key}_eval_scores")["metrics"]["spider_fl"], kind, pub)
            for key, disp, kind, pub in MODELS]
    rows.sort(key=lambda r: r[1])
    fig, ax = plt.subplots(figsize=(5.0, 2.8))
    names = [r[0] for r in rows]
    vals = [r[1] for r in rows]
    colors = [KIND_COLOR[r[2]] for r in rows]
    bars = ax.barh(names, vals, color=colors)
    for bar, (disp, v, kind, pub) in zip(bars, rows):
        ax.text(v + 0.004, bar.get_y() + bar.get_height() / 2, f"{v:.3f}",
                va="center", fontsize=8)
        if pub is not None:
            ax.plot([pub], [bar.get_y() + bar.get_height() / 2], marker="|",
                    markersize=14, color="black")
    ax.set_xlabel("SPIDEr-FL (Clotho-eval, 1045 clips)")
    ax.set_xlim(0, max(vals) * 1.18)
    handles = [plt.Rectangle((0, 0), 1, 1, color=KIND_COLOR[k]) for k in ("floor", "lalm", "trained")]
    ax.legend(handles, ["tagging floor", "zero-shot LALM", "trained captioner"],
              fontsize=7, loc="lower right")
    fig.tight_layout()
    fig.savefig(FIGS / "fig1_spider_bar.pdf")
    plt.close(fig)
    print("[fig1] written", file=sys.stderr)


def table1_full_metrics() -> None:
    metrics = [("spider_fl", "SPIDEr-FL"), ("cider_d", "CIDEr-D"),
               ("spice", "SPICE"), ("meteor", "METEOR"), ("fer", "FER $\\downarrow$")]
    lines = [
        "\\begin{tabular}{lccccc}", "\\toprule",
        "Model & " + " & ".join(m[1] for m in metrics) + " \\\\", "\\midrule",
    ]
    for key, disp, kind, pub in MODELS:
        s = _scores(f"{key}_eval_scores")["metrics"]
        cells = " & ".join(f"{s[m]:.3f}" for m, _ in metrics)
        name = f"\\textbf{{{disp}}}" if key == "af3" else disp
        lines.append(f"{name} & {cells} \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    (TABLES / "table1_full.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("[table1] written", file=sys.stderr)


def fig2_table2_poly_mono() -> None:
    rows = []
    for key, disp, kind, pub in MODELS:
        poly = _scores(f"{key}_eval_scores_poly")
        mono = _scores(f"{key}_eval_scores_mono")
        if poly is None or mono is None:
            return
        rows.append((disp, kind, poly["metrics"]["spider_fl"], mono["metrics"]["spider_fl"],
                     poly["n_items"], mono["n_items"]))

    lines = [
        "\\begin{tabular}{lccc}", "\\toprule",
        "Model & poly & mono & $\\Delta$(poly$-$mono) \\\\", "\\midrule",
    ]
    for disp, kind, p, m, np_, nm in rows:
        lines.append(f"{disp} & {p:.3f} & {m:.3f} & {p - m:+.3f} \\\\")
    lines += ["\\bottomrule", "\\end{tabular}",
              f"% n_poly={rows[0][4]}, n_mono={rows[0][5]}"]
    (TABLES / "table2_polymono.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")

    fig, ax = plt.subplots(figsize=(5.0, 2.6))
    names = [r[0] for r in rows]
    deltas = [r[2] - r[3] for r in rows]
    colors = [KIND_COLOR[r[1]] for r in rows]
    ax.barh(names, deltas, color=colors)
    ax.axvline(0, color="black", lw=0.8)
    ax.set_xlabel("$\\Delta$ SPIDEr-FL (polyphonic $-$ monophonic)")
    fig.tight_layout()
    fig.savefig(FIGS / "fig2_poly_mono.pdf")
    plt.close(fig)
    print(f"[fig2/table2] written (n_poly={rows[0][4]}, n_mono={rows[0][5]})", file=sys.stderr)


def table3_chair() -> None:
    chair = _scores("chair_audio")
    if chair is None:
        return
    lines = [
        "\\begin{tabular}{lccc|c}", "\\toprule",
        "Model & \\multicolumn{3}{c|}{CHAIR-s at $\\tau$} & coverage \\\\",
        " & 0.20 & \\textbf{0.25} & 0.30 & ($\\tau{=}0.25$) \\\\", "\\midrule",
    ]
    for key, disp, kind, pub in MODELS:
        m = chair["models"].get(key)
        if not m:
            continue
        lines.append(
            f"{disp} & {m['0.20']['chair_s']:.3f} & \\textbf{{{m['0.25']['chair_s']:.3f}}} "
            f"& {m['0.30']['chair_s']:.3f} & {m['0.25']['coverage']:.2f} \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    (TABLES / "table3_chair.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("[table3] written", file=sys.stderr)


def table4_mace() -> None:
    mace = _scores("mace_scores")
    if mace is None:
        return
    order = [("af3", "Audio Flamingo 3"), ("salmonn", "SALMONN-13B"),
             ("qwen_omni", "Qwen2.5-Omni-7B")]
    lines = [
        "\\begin{tabular}{lccc}", "\\toprule",
        "Model & MACE poly & MACE mono & $\\Delta$(poly$-$mono) \\\\", "\\midrule",
    ]
    for key, disp in order:
        p = mace[key]["poly"]["scores"]["mace"]
        m = mace[key]["mono"]["scores"]["mace"]
        lines.append(f"{disp} & {p:.3f} & {m:.3f} & {p - m:+.3f} \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    (TABLES / "table4_mace.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("[table4] written", file=sys.stderr)


_LATEX_SPECIALS = {"&": "\\&", "%": "\\%", "$": "\\$", "#": "\\#",
                   "_": "\\_", "{": "\\{", "}": "\\}"}


def _latex_escape(text: str) -> str:
    return "".join(_LATEX_SPECIALS.get(c, c) for c in text)


# Verbatim caption examples pulled from the predictions JSONs; clips chosen to
# show the register differences discussed in the RQ1/RQ3 text (tag list vs
# report framing vs Clotho-style, incl. AF3's unsupported "zipper").
EXAMPLE_CLIPS = ["20070819.fjord.beach.00.wav", "creaky.wav"]


def table5_examples() -> None:
    preds = {}
    for key, _, _, _ in MODELS:
        data = _scores(f"{key}_eval")
        if data is None:
            return
        preds[key] = {it["file_name"]: it for it in data["items"]}
    lines = [
        "\\begin{tabular}{lp{6.6cm}p{6.6cm}}", "\\toprule",
        "System & " + " & ".join(
            f"\\texttt{{{_latex_escape(c)}}}" for c in EXAMPLE_CLIPS) + " \\\\",
        "\\midrule",
    ]
    ref_cells = " & ".join(
        _latex_escape(preds["af3"][c]["references"][0]) for c in EXAMPLE_CLIPS)
    lines.append(f"Human reference (1 of 5) & {ref_cells} \\\\")
    lines.append("\\midrule")
    for key, disp, kind, pub in MODELS:
        cells = " & ".join(
            _latex_escape(preds[key][c]["prediction"]) for c in EXAMPLE_CLIPS)
        lines.append(f"{disp} & {cells} \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    (TABLES / "table5_examples.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("[table5] written", file=sys.stderr)


def main() -> int:
    FIGS.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    fig1_spider_bar()
    table1_full_metrics()
    fig2_table2_poly_mono()
    table3_chair()
    table4_mace()
    table5_examples()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
