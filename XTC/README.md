# XTC NeurIPS 2026 Draft

This directory is an Overleaf-ready NeurIPS 2026 project for the XTC paper draft.

## Contents

- `main.tex`: complete paper, including all body sections, appendices, and the NeurIPS checklist (single-file layout)
- `neurips_2026.sty`: official NeurIPS 2026 style file copied from the official template
- `figures/`: all figures (PDF + PNG previews); `figures/_make_new_figures.py` regenerates the human-eval / cross-vendor / IFEval figures
- `refs.bib`: bibliography

## Upload to Overleaf

1. Create a new blank Overleaf project.
2. Upload the full contents of this directory.
3. Set the main file to `main.tex` if Overleaf does not detect it automatically.
4. Compile with `pdfLaTeX`.

## Mode switches

By default the paper is set to anonymous main-track submission mode:

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
