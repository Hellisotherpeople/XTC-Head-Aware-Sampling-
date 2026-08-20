"""
Generate the main method-explainer figure for XTC.
3 panels:
  (a) Input distribution p_t with eligibility threshold tau
  (b) Eligible set E_t identified; dominant choices marked for removal,
      weakest plausible alternative kept
  (c) Renormalized distribution q_t
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.8,
    "axes.edgecolor": "#444",
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
    "pdf.fonttype": 42,
})

XTC_GREEN = "#2A9D8F"
DROP_RED  = "#E76F51"
TAIL_GRAY = "#B8B8B8"
HEAD_BLUE = "#3D7EA6"

tokens = ["once", "the", "a",  "an",  "one", "in"]
probs  = np.array([0.34, 0.28, 0.18, 0.07, 0.05, 0.08])
tau    = 0.10

eligible_mask = probs >= tau
eligible_idx  = np.where(eligible_mask)[0]
weakest_in_E  = eligible_idx[np.argmin(probs[eligible_idx])]
removed_idx   = [i for i in eligible_idx if i != weakest_in_E]

YMAX = 0.55


def panel_a(ax):
    colors = [HEAD_BLUE if eligible_mask[i] else TAIL_GRAY
              for i in range(len(tokens))]
    bars = ax.bar(tokens, probs, color=colors, edgecolor="white", linewidth=1.0)
    ax.axhline(tau, color="#444", linestyle="--", linewidth=1.0)
    ax.text(len(tokens) - 0.4, tau + 0.012,
            r"$\tau = 0.10$", color="#444", ha="right", fontsize=10)
    ax.set_ylim(0, YMAX)
    ax.set_ylabel(r"$p_t(v)$")
    ax.set_title(r"(a) Input $p_t$:  identify eligible set $E_t$")
    ax.text(2.5, YMAX - 0.03,
            r"$E_t = \{v : p_t(v) \geq \tau\}$",
            color=HEAD_BLUE, fontsize=11, ha="center")
    for b, p, in_E in zip(bars, probs, eligible_mask):
        if in_E:
            ax.text(b.get_x() + b.get_width()/2, p + 0.008,
                    f"{p:.2f}", ha="center", va="bottom", fontsize=9,
                    color=HEAD_BLUE, fontweight="bold")


def panel_b(ax):
    colors = []
    for i in range(len(tokens)):
        if i in removed_idx:
            colors.append(DROP_RED)
        elif i == weakest_in_E:
            colors.append(XTC_GREEN)
        else:
            colors.append(TAIL_GRAY)
    bars = ax.bar(tokens, probs, color=colors, edgecolor="white", linewidth=1.0)
    ax.axhline(tau, color="#444", linestyle="--", linewidth=1.0)
    ax.set_ylim(0, YMAX)
    ax.set_title(r"(b) Remove dominant; keep weakest eligible (underdog)")
    for i in removed_idx:
        ax.text(i, probs[i] / 2, "remove", ha="center", va="center",
                color="white", fontsize=9, fontweight="bold", rotation=90)
    ax.text(weakest_in_E, probs[weakest_in_E] + 0.012,
            "keep", ha="center", va="bottom",
            color=XTC_GREEN, fontsize=10, fontweight="bold")
    ax.set_yticks([])


def panel_c(ax):
    q = probs.copy()
    for i in removed_idx:
        q[i] = 0.0
    q = q / q.sum()
    colors = [XTC_GREEN if i == weakest_in_E
              else (DROP_RED if i in removed_idx else TAIL_GRAY)
              for i in range(len(tokens))]
    bars = ax.bar(tokens, q, color=colors, edgecolor="white", linewidth=1.0)
    ax.set_ylim(0, YMAX)
    ax.set_title(r"(c) Renormalize $\Rightarrow q_t$")
    ax.set_yticks([])
    for i, p in enumerate(q):
        if p > 0:
            ax.text(i, p + 0.008, f"{p:.2f}", ha="center", va="bottom",
                    fontsize=9, color="#222", fontweight="bold")


fig, axes = plt.subplots(1, 3, figsize=(12.0, 3.2),
                         gridspec_kw={"wspace": 0.20})
panel_a(axes[0])
panel_b(axes[1])
panel_c(axes[2])

for ax in axes:
    ax.set_xlabel("vocabulary token $v$")

fig.savefig(OUT / "fig_method_schematic.pdf")
fig.savefig(OUT / "fig_method_schematic.png", dpi=240)
plt.close(fig)
print("Wrote fig_method_schematic.{pdf,png}")
