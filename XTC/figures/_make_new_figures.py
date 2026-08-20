"""
Generate publication-quality figures for sections 5.7 (AMT human eval),
5.8 (cross-vendor judge), and 5.9 (IFEval) of the XTC paper.

Output: fig44_human_eval_amt.pdf, fig45_cross_vendor_judge.pdf, fig46_ifeval_degradation.pdf
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent

# ---- House style ----------------------------------------------------------
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "axes.labelweight": "regular",
    "axes.titleweight": "bold",
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "legend.frameon": False,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.8,
    "axes.edgecolor": "#444444",
    "xtick.color": "#444444",
    "ytick.color": "#444444",
    "axes.labelcolor": "#222222",
    "axes.titlecolor": "#222222",
    "xtick.direction": "out",
    "ytick.direction": "out",
    "xtick.major.size": 3.0,
    "ytick.major.size": 3.0,
    "xtick.major.width": 0.7,
    "ytick.major.width": 0.7,
    "grid.color": "#cccccc",
    "grid.linewidth": 0.5,
    "grid.alpha": 0.7,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
    "pdf.fonttype": 42,
    "text.usetex": False,
})

# Use small caps via plain capital letters for "XTC" in figures
XTC_LBL  = "XTC"

XTC_GREEN = "#2A9D8F"     # XTC Strong
TIE_GRAY  = "#B8B8B8"     # ties
BASE_RED  = "#E76F51"     # baseline
ACCENT    = "#264653"     # dark teal accent
GPT_BLUE  = "#3D7EA6"     # gpt-4o color
CLAUDE_O  = "#9B5DE5"     # Claude Opus color


# =============================================================================
# Figure 44: AMT Human Evaluation — preference stacked bars
# =============================================================================
def fig_human_eval():
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.4),
                             gridspec_kw={"width_ratios": [1.05, 0.95],
                                          "wspace": 0.30})

    # ---- LEFT panel: stacked horizontal preference bars
    ax = axes[0]
    axes_labels = ["Creativity\n& Interest", "General Quality\n& Fluency"]
    xtc_wins  = [62.3, 41.1]
    ties      = [16.7, 43.3]
    base_wins = [21.0, 15.6]

    y = np.arange(len(axes_labels))
    h = 0.55
    ax.barh(y, xtc_wins, height=h, color=XTC_GREEN,
            label=f"{XTC_LBL} Strong wins", edgecolor="white", linewidth=1.0)
    ax.barh(y, ties, height=h, left=xtc_wins, color=TIE_GRAY,
            label="Tie", edgecolor="white", linewidth=1.0)
    ax.barh(y, base_wins, height=h,
            left=np.array(xtc_wins) + np.array(ties),
            color=BASE_RED, label="Baseline wins",
            edgecolor="white", linewidth=1.0)

    # In-bar labels
    for i, (x, t, b) in enumerate(zip(xtc_wins, ties, base_wins)):
        ax.text(x / 2, y[i], f"{x:.1f}%", ha="center", va="center",
                color="white", fontsize=10, fontweight="bold")
        if t > 8:
            ax.text(x + t / 2, y[i], f"{t:.1f}%", ha="center", va="center",
                    color="#333333", fontsize=9, fontweight="bold")
        else:
            ax.text(x + t / 2, y[i], f"{t:.1f}%", ha="center", va="center",
                    color="#333333", fontsize=8)
        ax.text(x + t + b / 2, y[i], f"{b:.1f}%", ha="center", va="center",
                color="white", fontsize=10, fontweight="bold")

    ax.set_yticks(y)
    ax.set_yticklabels(axes_labels, fontsize=9.5)
    ax.set_xlim(0, 100)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"])
    ax.set_xlabel(r"Preference share (n=100 prompts $\times$ 3 annotators)")
    ax.invert_yaxis()
    ax.set_title("(a) AMT preference rates", loc="left")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.20),
              ncol=3, handlelength=1.0, columnspacing=1.2)
    ax.spines["left"].set_visible(False)
    ax.tick_params(left=False)

    # ---- RIGHT panel: net preference (XTC-minus-Baseline) with significance
    ax = axes[1]
    net = np.array(xtc_wins) - np.array(base_wins)  # +41.3, +25.5
    pvals = [r"$p<10^{-4}$", r"$p<10^{-3}$"]
    kappa = [0.58, 0.44]

    bars = ax.bar(np.arange(2), net, width=0.55,
                  color=[XTC_GREEN, ACCENT], edgecolor="white", linewidth=1.0)
    ax.axhline(0, color="#444", linewidth=0.7)
    for i, (b, p, k) in enumerate(zip(bars, pvals, kappa)):
        ax.text(b.get_x() + b.get_width() / 2,
                b.get_height() + 1.2,
                f"+{net[i]:.1f} pp\n{p}",
                ha="center", va="bottom", fontsize=9, fontweight="bold")
        ax.text(b.get_x() + b.get_width() / 2, 1.5,
                rf"$\kappa={k:.2f}$",
                ha="center", va="bottom", fontsize=9, color="white",
                fontweight="bold")

    ax.set_xticks(np.arange(2))
    ax.set_xticklabels(["Creativity", "Quality"])
    ax.set_ylim(0, 55)
    ax.set_ylabel(f"Net preference for {XTC_LBL} (pp)")
    ax.set_title(r"(b) Net win rate & Fleiss' $\kappa$", loc="left")
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    ax.set_axisbelow(True)

    fig.suptitle("Human evaluation on Amazon Mechanical Turk "
                 "(Gemma 3 27B q4, blinded A/B, 150 Master raters)",
                 fontsize=11, y=1.04)

    fig.savefig(OUT / "fig44_human_eval_amt.pdf")
    fig.savefig(OUT / "fig44_human_eval_amt.png", dpi=240)
    plt.close(fig)


# =============================================================================
# Figure 45: LLM-as-judge — Claude Opus 4.7 + GPT-4o cross-vendor control
# =============================================================================
def fig_cross_vendor():
    fig, ax = plt.subplots(figsize=(8.6, 3.8))

    criteria = ["Repetition", "Creativity", "Lexical\ndiversity",
                "Coherence", "Fluency", "Relevance", "Overall\nquality"]

    # paired deltas (XTC - Baseline) on Gemma 3 27B q4 (n=24).
    # Opus values are computed from the per-prompt judge CSVs.
    # GPT-4o values are the cross-vendor replication.
    judges = [
        ("Claude Opus 4.7",      "#7B3EA8",
         [+0.45, +0.09, +0.23, +0.00, +0.00, +0.00, -0.09],
         [+0.14, -0.18, +0.00, -0.20, -0.18, -0.20, -0.41],
         [+0.77, +0.36, +0.45, +0.20, +0.18, +0.20, +0.23]),
        ("GPT-4o (cross-vendor)", GPT_BLUE,
         [+0.51, +0.39, +0.28, +0.05, +0.02, +0.10, +0.05],
         [+0.22, +0.11, +0.04, -0.18, -0.20, -0.15, -0.15],
         [+0.78, +0.65, +0.50, +0.28, +0.22, +0.32, +0.28]),
    ]

    x = np.arange(len(criteria))
    w = 0.34
    n = len(judges)

    for j, (name, color, m, lo, hi) in enumerate(judges):
        m, lo, hi = map(np.array, (m, lo, hi))
        err = [m - lo, hi - m]
        offset = (j - (n - 1) / 2) * w
        ax.bar(x + offset, m, width=w, color=color, edgecolor="white",
               linewidth=0.7, yerr=err, capsize=2.4,
               error_kw=dict(elinewidth=0.9, ecolor="#333"),
               label=name)
        for i, (lo_i, m_i, hi_i) in enumerate(zip(lo, m, hi)):
            if lo_i > 0 or hi_i < 0:
                top = m_i + (hi_i - m_i) + 0.04 if m_i >= 0 else m_i - (m_i - lo_i) - 0.04
                ax.text(x[i] + offset, top, r"$\star$", ha="center",
                        va="bottom" if m_i >= 0 else "top",
                        color=color, fontsize=12, fontweight="bold")

    ax.axhline(0, color="#444", linewidth=0.7)
    ax.set_xticks(x)
    ax.set_xticklabels(criteria, fontsize=11)
    ax.set_ylabel(r"Paired $\Delta$ vs. baseline (1--5 scale)", fontsize=12)
    ax.set_ylim(-0.65, 1.00)
    ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=5))
    ax.tick_params(axis="y", labelsize=10)
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    ax.set_axisbelow(True)

    ax.text(0.99, 0.97, r"$\star$ = 95% CI excludes zero",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=9, color="#444",
            bbox=dict(facecolor="white", edgecolor="#cccccc",
                      boxstyle="round,pad=0.3"))

    ax.legend(loc="upper right", bbox_to_anchor=(1.0, -0.18), ncol=2,
              fontsize=10, columnspacing=1.4, handlelength=1.2,
              frameon=False)

    fig.savefig(OUT / "fig45_cross_vendor_judge.pdf")
    fig.savefig(OUT / "fig45_cross_vendor_judge.png", dpi=240)
    plt.close(fig)


# =============================================================================
# Figure 46: IFEval pass-rate degradation - XTC vs. Temperature
# =============================================================================
def fig_ifeval():
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 3.5),
                             gridspec_kw={"width_ratios": [1.05, 0.95],
                                          "wspace": 0.32})

    # ---- LEFT panel: bar chart of conditions
    ax = axes[0]
    conditions = ["Baseline\n(T=1.0)",
                  f"{XTC_LBL} Light\n" + r"($\rho{=}0.25$)",
                  f"{XTC_LBL} Medium\n" + r"($\rho{=}0.50$)",
                  "Temperature\n(T=1.15)"]
    scores = [81.2, 80.8, 79.5, 72.4]
    deltas = [0.0, -0.4, -1.7, -8.8]

    palette = ["#7f8c8d", XTC_GREEN, "#1B7A6E", BASE_RED]
    bars = ax.bar(np.arange(4), scores, width=0.62,
                  color=palette, edgecolor="white", linewidth=1.0)
    ax.set_ylim(65, 86)
    ax.set_ylabel("IFEval prompt-level strict accuracy (%)")
    ax.axhline(81.2, color="#888", linestyle="--", linewidth=0.8,
               alpha=0.7)
    ax.text(3.45, 81.5, "baseline",
            color="#888", va="bottom", ha="left", fontsize=8.5)

    for b, s, d in zip(bars, scores, deltas):
        ax.text(b.get_x() + b.get_width() / 2,
                b.get_height() + 0.3,
                f"{s:.1f}%", ha="center", va="bottom",
                fontsize=10, fontweight="bold")
        if d != 0:
            color_text = "white"
            ax.text(b.get_x() + b.get_width() / 2,
                    b.get_height() - 1.4,
                    rf"$\Delta\,{d:+.1f}$",
                    ha="center", va="top", color=color_text,
                    fontsize=9.5, fontweight="bold")

    ax.set_xticks(np.arange(4))
    ax.set_xticklabels(conditions, fontsize=9)
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_title("(a) IFEval pass rate (Llama 3.3 70B q4)", loc="left")

    # ---- RIGHT panel: diversity gain vs IF cost scatter
    ax = axes[1]
    methods = [f"{XTC_LBL} Light",
               f"{XTC_LBL} Medium",
               "Temperature 1.15"]
    div_gain = np.array([+8.0, +13.5, +14.0])  # approx Distinct-2 % gain
    if_loss  = np.array([0.4, 1.7, 8.8])       # IFEval pp loss
    colors = [XTC_GREEN, "#1B7A6E", BASE_RED]
    offsets = [(8, 4), (8, -8), (-8, 8)]
    ha_list = ["left", "left", "right"]
    va_list = ["center", "top", "center"]

    for m, dg, il, c, off, ha, va in zip(methods, div_gain, if_loss, colors,
                                          offsets, ha_list, va_list):
        ax.scatter(dg, il, s=180, color=c, edgecolor="white",
                   linewidth=1.2, zorder=3,
                   label=m)
        ax.annotate(m, (dg, il), textcoords="offset points",
                    xytext=off, fontsize=9, ha=ha, va=va)

    # Pareto-frontier guide line
    ax.plot([0, 16], [0, 0], color="#bbb", linestyle=":", linewidth=0.8)
    ax.invert_yaxis()
    ax.set_xlim(0, 17)
    ax.set_ylim(11, -1)
    ax.set_xlabel("Distinct-2 gain over baseline (%)")
    ax.set_ylabel(r"IFEval cost (pp lost) $\downarrow$")
    ax.set_title("(b) Diversity gain vs. instruction-following cost",
                 loc="left")
    ax.grid(linestyle=":", alpha=0.5)
    ax.set_axisbelow(True)

    # "Better" indicator placed in the bottom-left clear zone, well away
    # from the XTC Medium scatter point.
    ax.text(1.0, 9.5,
            "better\n" + r"$\rightarrow$ more diversity" + "\n" +
            r"$\uparrow$ less IF cost",
            fontsize=8.2, color="#1d6c5e", ha="left", va="bottom",
            bbox=dict(facecolor="white", edgecolor="#cccccc",
                      boxstyle="round,pad=0.35"))

    fig.suptitle(f"Instruction-following preservation: {XTC_LBL} vs. "
                 f"temperature scaling at matched Distinct-2 gain",
                 fontsize=11, y=1.03)

    fig.savefig(OUT / "fig46_ifeval_degradation.pdf")
    fig.savefig(OUT / "fig46_ifeval_degradation.png", dpi=240)
    plt.close(fig)


# =============================================================================
# Figure 04: Design ablation — regenerated with readable axis labels.
# Replaces the original fig04 whose x-tick labels overlapped each other.
# =============================================================================
def fig_design_ablation():
    metrics = [
        ("Distinct-2 $\\uparrow$",
         [0.307, 0.434, 0.494, 0.420, 0.422],
         [0.058, 0.057, 0.075, 0.062, 0.072]),
        ("Self-BLEU-4 $\\downarrow$",
         [0.387, 0.341, 0.311, 0.311, 0.336],
         [0.054, 0.054, 0.061, 0.054, 0.057]),
        ("Repeat trigram rate $\\downarrow$",
         [0.446, 0.330, 0.288, 0.336, 0.342],
         [0.080, 0.066, 0.073, 0.072, 0.067]),
        ("Embedding cos. dist. $\\uparrow$",
         [0.328, 0.348, 0.358, 0.350, 0.345],
         [0.046, 0.043, 0.038, 0.044, 0.044]),
        ("Cluster entropy $\\uparrow$",
         [2.02, 2.18, 2.30, 2.16, 2.21],
         [0.25, 0.18, 0.10, 0.18, 0.18]),
    ]

    methods = ["Baseline",
               "Drop Top-1",
               "Keep Least (XTC)",
               "Keep Random",
               "Keep Second"]
    colors  = ["#7f8c8d", "#E07AB1", XTC_GREEN, "#C04A41", "#3D7EA6"]

    fig, axes = plt.subplots(1, 5, figsize=(14.0, 4.2),
                             gridspec_kw={"wspace": 0.34, "bottom": 0.30})
    x = np.arange(len(methods))

    for ax, (title, vals, errs) in zip(axes, metrics):
        bars = ax.bar(x, vals, width=0.66, color=colors,
                      edgecolor="white", linewidth=0.9,
                      yerr=errs, capsize=2.5,
                      error_kw=dict(elinewidth=0.9, ecolor="#333333"))
        bars[2].set_edgecolor("#0e3a33")
        bars[2].set_linewidth(1.8)
        ax.set_title(title, fontsize=11, pad=6)
        ax.set_xticks(x)
        ax.set_xticklabels(methods, rotation=40, ha="right", fontsize=10)
        ax.grid(axis="y", linestyle=":", alpha=0.5)
        ax.set_axisbelow(True)
        ax.tick_params(axis="x", pad=1)

    fig.suptitle("Design ablation: comparing token-exclusion strategies "
                 "(Gemma 3 27B q4, $\\rho{=}1.0$, $\\tau{=}0.1$)",
                 fontsize=12, y=0.99)
    fig.savefig(OUT / "fig04_design_ablation.pdf")
    fig.savefig(OUT / "fig04_design_ablation.png", dpi=240)
    plt.close(fig)


# =============================================================================
# Figure 05: Structured quality retention (rebuilt without the code-exactness
# panel that previously dominated the left side of the original figure).
# =============================================================================
def fig_quality_safety():
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    conditions = ["Baseline\n(T=1.0)", "Temp 0.80",
                  f"{XTC_LBL} Light", f"{XTC_LBL} Medium"]
    metrics = {
        "Eval pass rate $\\uparrow$":
            ([0.611, 0.583, 0.640, 0.611],
             [0.069, 0.075, 0.060, 0.073]),
        "Field match rate $\\uparrow$":
            ([0.795, 0.741, 0.758, 0.738],
             [0.065, 0.075, 0.075, 0.075]),
        "JSON valid rate $\\uparrow$":
            ([0.833, 0.778, 0.778, 0.778],
             [0.080, 0.080, 0.080, 0.080]),
    }
    palette = ["#3D7EA6", "#E78F2A", XTC_GREEN]

    x = np.arange(len(conditions))
    w = 0.26
    for i, (name, (vals, errs)) in enumerate(metrics.items()):
        ax.bar(x + (i - 1) * w, vals, width=w,
               color=palette[i], edgecolor="white", linewidth=0.9,
               yerr=errs, capsize=2.4,
               error_kw=dict(elinewidth=0.9, ecolor="#333333"),
               label=name)

    ax.set_xticks(x)
    ax.set_xticklabels(conditions, fontsize=9.5)
    ax.set_ylabel("Rate")
    ax.set_ylim(0.40, 1.00)
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_title("Structured quality retention "
                 f"({XTC_LBL} preserves fidelity on JSON extraction "
                 "and constrained rewriting)", loc="left", fontsize=10.5)
    ax.legend(loc="upper right", bbox_to_anchor=(1.0, -0.16),
              ncol=3, handlelength=1.2)

    fig.savefig(OUT / "fig05_quality_safety.pdf")
    fig.savefig(OUT / "fig05_quality_safety.png", dpi=240)
    plt.close(fig)


# =============================================================================
# Figure 47: 70B-scaling LLM-as-judge mini panel (replaces appendix table 9)
# =============================================================================
def fig_judge_70b():
    fig, ax = plt.subplots(figsize=(6.6, 3.0))

    metrics = ["Creativity", "Lexical\ndiversity", "Repetition",
               "Overall\nquality"]
    # 70B q4 LLM-judge panel restricted to Opus 4.7 (the cross-vendor
    # control judge was not run on this scaling configuration).
    judges = [
        ("Claude Opus 4.7", "#7B3EA8",
         [+0.38, +0.21, +0.21, +0.04],
         [+0.08, +0.04, -0.04, -0.08],
         [+0.67, +0.38, +0.46, +0.17]),
    ]

    x = np.arange(len(metrics))
    w = 0.46
    for j, (name, color, m, lo, hi) in enumerate(judges):
        m, lo, hi = map(np.array, (m, lo, hi))
        err = [m - lo, hi - m]
        ax.bar(x, m, width=w, color=color, edgecolor="white",
               linewidth=0.7, yerr=err, capsize=2.6,
               error_kw=dict(elinewidth=1.0, ecolor="#333"),
               label=name)
        for i, (lo_i, m_i, hi_i) in enumerate(zip(lo, m, hi)):
            if lo_i > 0 or hi_i < 0:
                top = m_i + (hi_i - m_i) + 0.04
                ax.text(x[i], top, r"$\star$", ha="center",
                        va="bottom", color=color, fontsize=12,
                        fontweight="bold")

    ax.axhline(0, color="#444", linewidth=0.7)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=11)
    ax.set_ylim(-0.25, 0.80)
    ax.set_ylabel(r"Paired $\Delta$ vs. baseline", fontsize=12)
    ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=5))
    ax.tick_params(axis="y", labelsize=10)
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    ax.set_axisbelow(True)

    ax.text(0.99, 0.97, r"$\star$ = 95% CI excludes zero",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=9, color="#444",
            bbox=dict(facecolor="white", edgecolor="#cccccc",
                      boxstyle="round,pad=0.3"))

    fig.savefig(OUT / "fig47_judge_70b.pdf")
    fig.savefig(OUT / "fig47_judge_70b.png", dpi=240)
    plt.close(fig)


if __name__ == "__main__":
    fig_human_eval()
    fig_cross_vendor()
    fig_ifeval()
    fig_design_ablation()
    fig_quality_safety()
    fig_judge_70b()
    print("Wrote:", *sorted(p.name for p in OUT.glob("fig*_*.png") if p.stat().st_mtime > 0))
