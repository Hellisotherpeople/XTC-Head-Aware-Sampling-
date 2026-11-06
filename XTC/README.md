# XTC NeurIPS 2026 Draft

This directory is an Overleaf-ready NeurIPS 2026 project for the XTC paper draft.

## Contents

- `main.tex`: **camera-ready copy** (`[main, final]`) with the named author block, acknowledgments, appendices, and the NeurIPS checklist. The anonymous submission copy is preserved in git history at commit `b92a882`.
- `preprint.tex`: **named preprint / arXiv copy** — same body as `main.tex`, but compiled with `\usepackage[preprint]{neurips_2026}`, with the author block filled in and the NeurIPS checklist removed.
- `neurips_2026.sty`: official NeurIPS 2026 style file copied from the official template
- `figures/`: all figures (PDF + PNG previews); `figures/_make_new_figures.py` regenerates the human-eval / cross-vendor / IFEval figures
- `refs.bib`: bibliography

## Upload to Overleaf

1. Create a new blank Overleaf project.
2. Upload the full contents of this directory.
3. Set the main file to `main.tex` if Overleaf does not detect it automatically.
4. Compile with `pdfLaTeX`.

## Two build targets

| File | Mode | Authors | Checklist |
| --- | --- | --- | --- |
| `main.tex` | `[main, final]` | named | included |
| `preprint.tex` | `[preprint]` | named | removed |

Both share `refs.bib`, `figures/`, and `neurips_2026.sty`. Body-text edits need to be
applied to both files, or diffed across them before submission.

`preprint.tex` author list, in order: Philipp Emanuel Weidmann (Independent Researcher),
Allen G. Roush (Thoughtworks), Judah Goldfeder (Columbia University), Sanjay Basu (Oracle),
Ravid Shwartz-Ziv (New York University). Weidmann and Roush are equal-contribution
co-first authors. Per-author footnotes record that Weidmann proposed the method and wrote
its original implementation (merged into text-generation-webui, PR #6335) and that Roush ran
the empirical program. The llama.cpp implementation was written by MaggotHATE (PR #9742) and
the KoboldCpp one by LostRuins (v1.74). Both are credited in the Acknowledgments.

## Mode switches

By default `main.tex` is set to anonymous main-track submission mode:

```tex
\usepackage[main]{neurips_2026}
```

For a named internal draft or arXiv-style preprint, switch to:

```tex
\usepackage[preprint]{neurips_2026}
```

For the final camera-ready version, switch to:

```tex
\usepackage[main, final]{neurips_2026}
```

## Current scope

This draft intentionally omits quantitative results, but it now includes an explicit empirical-design section covering hypotheses, comparator tuning, mechanism diagnostics, human-evaluation protocol, and an expanded diversity metric suite spanning compression, homogenization, template density, and embedding-spread measurements. The method, analysis, positioning, limitations, and checklist are all present so the paper can be edited in parallel with the ongoing empirical campaign.
