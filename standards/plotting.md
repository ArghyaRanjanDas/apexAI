# Figure Production Standards

All figures produced in an apexAI analysis must follow these rules. They are
non-negotiable. Any deviation requires an explicit, documented justification
in the experiment log. The rules prevent broken aspect ratios, mangled labels,
clipped content, and inconsistent styling that have plagued past analyses.

---

## Base Template

Every plotting script starts from this skeleton:

```python
import matplotlib.pyplot as plt
import mplhep as mh
import numpy as np

np.random.seed(42)
mh.style.use("CMS")

# --- Single plot ---
fig, ax = plt.subplots(figsize=(10, 10))

# --- Ratio plot ---
# fig, (ax, rax) = plt.subplots(
#     2, 1, figsize=(10, 10),
#     gridspec_kw={"height_ratios": [3, 1]},
#     sharex=True,
# )
# fig.subplots_adjust(hspace=0)

# --- Your plotting code here ---

# --- Experiment label (required on every independent axes) ---
mh.label.exp_label(
    exp="<EXPERIMENT>",
    text="",
    loc=0,
    data=True,
    llabel="Open Data",    # or "Open Simulation" for MC
    rlabel=None,           # custom right-side annotation if needed
    ax=ax,
)

fig.savefig("output.pdf", bbox_inches="tight", dpi=200, transparent=True)
fig.savefig("output.png", bbox_inches="tight", dpi=200, transparent=True)
plt.close(fig)
```

---

## Mandatory Rules (Category A if Violated)

### Font sizes are LOCKED

Do not pass absolute numeric `fontsize=` values to ANY matplotlib call
(`set_xlabel`, `set_ylabel`, `set_title`, `tick_params`, `annotate`, `text`).
The CMS stylesheet sets all font sizes correctly for the 10x10 figure size.
Relative string sizes (`'small'`, `'x-small'`, `'xx-small'`) are allowed
where needed (dense legends, annotation text).

### Figure size is LOCKED at (10, 10)

Do not use any other figure size. The CMS stylesheet font sizes are calibrated
for this canvas. For ratio plots: `figsize=(10, 10)` with `height_ratios=[3, 1]`.
For MxN subplots: scale to 10 per subplot dimension (2x2 -> (20, 20),
1x3 -> (30, 10)).

### Legends via mpl_magic

The default approach is to scale the y-axis to accommodate the legend:

```python
from mplhep.plot import mpl_magic
ax.legend(fontsize="x-small")
mpl_magic(ax)
```

Call `mpl_magic(ax)` after all plotting is done. It extends the y-range so
the legend sits in empty space above the data. Manual placement (`loc=`,
`bbox_to_anchor`) is allowed only when the plot has a genuinely empty region.

Legend-data overlap is Category A. Visual inspection of rendered figures is
required, not just checking `loc=` in the script.

### Colorbars: make_square_add_cbar or cbarextend

For ANY 2D plot with a colorbar, use one of:
- `mh.hist2dplot(H, cbarextend=True)` (preferred)
- `cax = mh.utils.make_square_add_cbar(ax)` then `fig.colorbar(im, cax=cax)`
- `cax = mh.utils.append_axes(ax, extend=True)` then `fig.colorbar(im, cax=cax)`

**Never use** `fig.colorbar(im)`, `fig.colorbar(im, ax=ax)`,
`fig.colorbar(im, ax=ax, shrink=...)`, or `plt.colorbar(...)`. These steal
space from the main axes and break the square aspect ratio. Applies to ALL
2D plots: correlation matrices, migration matrices, response matrices,
efficiency maps.

### Ratio plots: sharex=True and hspace=0

Ratio plots MUST use `sharex=True` in `plt.subplots()` AND
`fig.subplots_adjust(hspace=0)`. Without `sharex=True`, the upper panel shows
a redundant x-axis label ("Axis 0"). Without `hspace=0`, a visible gap
appears between the main and ratio panels. Both are Category A.

**Axis 0 workaround.** After calling `exp_label(ax=ax_main, loc=0)`,
suppress the artifact on the ratio panel:
```python
for txt in rax.texts:
    if "Axis" in txt.get_text():
        txt.remove()
```
Or use `loc=2` (upper left) to avoid triggering the bug.

### Histograms via mh.histplot

When plotting histograms from raw event data, always use `mh.histplot()`.
Never use `ax.step()`, `ax.bar()`, or `ax.fill_between()` for these.

| Data type | Correct | Wrong |
|-----------|---------|-------|
| Raw counts (error bars) | `mh.histplot(h, histtype="errorbar")` | `ax.errorbar()` without yerr |
| MC prediction (filled) | `mh.histplot(h, histtype="fill")` | `ax.fill_between()`, `ax.bar()` |
| Stacked MC | `mh.histplot([h1,h2], stack=True)` | `ax.bar(..., bottom=...)` |
| Theory curve (continuous) | `ax.plot(x, y)` | (correct -- not binned) |

### Derived quantities: explicit yerr

When plotting any quantity that is NOT a raw event count (normalized
distributions, correction factors, ratios, efficiencies, systematic shifts),
you MUST pass explicit `yerr=`. Without it, mplhep computes sqrt(bin content),
which is meaningless for non-count values.

**The test:** Did you fill the histogram with `h.fill(raw_values)`? Then
auto sqrt(N) is correct. Did you assign values with `h.view()[:] = ...` or
compute from a formula? Then `yerr=` is mandatory.

### No ax.text or ax.annotate

Use `mh.label.add_text(text, ax=ax)` for all text annotations. This respects
mplhep styling and positioning. Includes panel labels like (a), (b) in grids.

### No titles

Never `ax.set_title()`. Captions go in the analysis note. Additional info
can go into `ax.legend(title="...")` or `mh.label.add_text()`.

### Both PDF and PNG

Save every figure in both formats:
```python
fig.savefig("output.pdf", bbox_inches="tight", dpi=200, transparent=True)
fig.savefig("output.png", bbox_inches="tight", dpi=200, transparent=True)
```
PDF for the analysis note, PNG for quick inspection. Always `bbox_inches="tight"`.

### No tight_layout

Never use `tight_layout()` or `constrained_layout=True` with mplhep. They
conflict with mplhep label positioning. Use `bbox_inches="tight"` at save
time instead.

### Close figures

`plt.close(fig)` after saving to prevent memory leaks in long scripts.

---

## Per-Experiment Labels

### ATLAS Open Data
```python
mh.style.use("ATLAS")
mh.atlas.label(label="Open Data", data=True, lumi=<val>, com=13, loc=0, ax=ax)
```
- Units in files: **MeV**. Convert to GeV for all plots (divide by 1000).

### CMS Open Data
```python
mh.style.use("CMS")
mh.cms.label(label="Open Data", data=True, lumi=<val>, com=13, loc=0, ax=ax)
```
- Units in NanoAOD: **GeV**. No conversion needed.

### CMS (Collaboration)
```python
mh.style.use("CMS")
mh.cms.label(label="Preliminary", data=True, lumi=<val>, com=13, loc=0, ax=ax)
```

### LEP Experiments (ALEPH, DELPHI, L3, OPAL)

Use the mplhep generic label system with CMS style as base:
```python
mh.style.use("CMS")
mh.label.exp_label(
    exp="ALEPH", data=True, llabel="Open Data",
    rlabel=r"$\sqrt{s} = 91.2$ GeV", ax=ax,
)
```
Units vary by experiment -- always verify from data (check pT magnitude).

### Belle / BaBar
```python
mh.label.exp_label(
    exp="Belle", data=True, llabel="Open Data",
    rlabel=r"$\sqrt{s} = 10.58$ GeV", ax=ax,
)
```

### Label Stacking Pitfall

When `data=False`, mplhep auto-adds "Simulation" as the left label. Do NOT
also set `llabel` -- this produces "Simulation Open Simulation". The safe
pattern is always `data=True` with explicit `llabel`:
- `data=True, llabel="Open Data"` for data
- `data=True, llabel="Open Simulation"` for MC
- `data=True, llabel=""` for non-open contexts

---

## Unit Conversion Table

| Experiment | File units | Plot units | Conversion |
|-----------|-----------|-----------|-----------|
| ATLAS | MeV | GeV | / 1000 |
| CMS (NanoAOD) | GeV | GeV | none |
| DELPHI | varies | GeV | check data |
| ALEPH | varies | GeV | check data |
| Belle/BaBar | GeV | GeV | none |
| LEP (general) | varies | GeV | check pT magnitude |

Rule of thumb: if typical lepton pT ~ 40, units are GeV; if ~ 40000, MeV.

---

## Standard Plot Types

### Distribution plot
Data as black circles with error bars (`mh.histplot(..., histtype="errorbar")`),
MC as filled/stacked histograms. Experiment label, axis labels with units,
legend via `mpl_magic`.

### Fit result (two-panel)
Main panel: data + fit curve + background component. Ratio/pull panel below
with `sharex=True` and `hspace=0`. Pull panel shows horizontal lines at 0
and +/-2.

### Cut-flow (barh)
Horizontal bar chart with cut names on y-axis, event counts on x-axis.
Monotonically decreasing.

### N-1 plot
Apply ALL cuts except the one being shown. Vertical dashed line at the
cut threshold. Show signal and background separately.

---

## Color and Style Table

| Element | Color | Style |
|---------|-------|-------|
| Data | black | filled circles, error bars |
| Total fit | red | solid line, width 2 |
| Background component | blue | dashed line, width 1 |
| Signal component | green | dotted line |
| Systematic band | yellow or hatched | fill between |
| Control sample | open markers | gray or distinct color |
| MC simulation | colored fills | stacked histograms |

---

## Axis Label Notation

| Variable | Label |
|----------|-------|
| Transverse momentum | `$p_T$ [GeV]` |
| Invariant mass (dimuon) | `$m_{\mu\mu}$ [GeV]` |
| Invariant mass (generic) | `$m_\text{inv}$ [GeV]` |
| Energy | `$E$ [GeV]` |
| Pseudorapidity | `$\eta$` |
| Azimuthal angle | `$\phi$` |
| Delta-R | `$\Delta R$` |
| Missing ET | `$E_T^\text{miss}$ [GeV]` |
| HT | `$H_T$ [GeV]` |
| Counts | `Events / X GeV` |
| Cross-section | `$\sigma$ [pb]` |

Always include units in brackets. For y-axis bin normalization, round the
bin width to a clean value (0.01, 0.05, 0.1, 0.5, 1, 2, 5, 10, ...).
If the natural width is ugly, either adjust binning or omit the width.

---

## Sizing Rules for the Analysis Note

The pandoc preamble sets default figure height to `0.45\linewidth`.
Height-based sizing keeps the plot area consistent between 1D histograms
and 2D plots with colorbars.

| Plot type | matplotlib figsize | AN height | Notes |
|-----------|-------------------|-----------|-------|
| Single panel | (10, 10) | 0.45 linewidth (default) | Distribution, spectrum |
| Ratio plot | (10, 10) | 0.45 linewidth (default) | Data/MC with ratio |
| 2D with colorbar | (10, 10) | 0.45 linewidth (default) | Matrix, Lund plane |
| Side-by-side | Compose in LaTeX | 0.45 linewidth each | See below |
| 2x2 or 3x2 grid | Compose in LaTeX | 0.3 linewidth each | See below |

**Prefer LaTeX subfigures over matplotlib grids.** Produce individual
(10, 10) figures and compose them in the AN using pandoc-crossref subfigure
syntax. This gives better control over layout, captions, and
cross-referencing.

Exception: tightly-coupled panels sharing a physical x-axis (ratio plots,
pull panels) should be a single matplotlib figure with `sharex=True` and
`hspace=0`. If you cannot use `sharex=True`, produce separate outputs.

---

## Additional Rules

**Suppress offset notation.** Never allow matplotlib's "1e6" offset text.
Either use `ax.ticklabel_format(axis='y', style='plain')`, absorb the
multiplier into the axis label, or use a custom formatter.

**Log scale.** Use `ax.set_yscale("log")` when the y-axis range spans more
than 2 orders of magnitude. Log y-minimum: 0.5 or 1 (never 0).

**Deterministic.** `np.random.seed(42)` if any randomness.

**2D equal-aspect.** When both axes use the same coordinate type, set
`ax.set_aspect('equal')` so bins render as squares.

**Axis limits.** Set tight to the data range. No large empty regions.

**Text labels must be publication-quality.** No code variable names or Python
identifiers in axis labels, legend entries, or tick labels. "Energy-dep.
efficiency" not "efficiency_energy_dep".

**Ratio panel tick collision.** Hide the main panel's x-axis tick labels with
`ax.tick_params(labelbottom=False)`. Set ratio panel y-limits with margin
to avoid crowding at the boundary.

**Y-axis bin width labels.** Round to clean values. Non-round bin widths in
labels are Category B.

**Ratio panel uncertainty bands.** When showing an uncertainty band, describe
it in the legend or caption. Unexplained bands are Category B. Suspiciously
flat bands (constant width) warrant investigation.

---

## Lint Script Integration

Run `pixi run lint-plots` before committing. The lint script checks:

```python
# Mandatory violations -- any match is a failure
checks = [
    ('ax.step(',    'use mh.histplot'),
    ('ax.bar(',     'use mh.histplot'),
    ('ax.text(',    'use mh.label.add_text'),
    ('tight_layout','forbidden with mplhep'),
    ('plt.colorbar','use make_square_add_cbar'),
    ('set_title(',  'use caption in AN'),
]
# Regex checks
# fontsize=<digit> -> absolute fontsize forbidden
# fig.colorbar(*, ax=) -> use cax= instead
# .view()[:] with histtype="errorbar" but no yerr= -> garbage errors
# 2D plot without make_square_add_cbar or cbarextend -> broken aspect
# legend without mpl_magic -> overlap risk
# sharex ratio plot with exp_label but no Axis 0 suppression
```

Additionally, grep all label/xlabel/ylabel strings for underscores outside
LaTeX math mode. Code variable names in rendered labels are Category A.

---

## Red Flags

These patterns in plotting scripts indicate likely defects:

- `figsize=(8, 6)` or any non-(10, 10) size
- `fontsize=14` or any absolute numeric font size
- `plt.colorbar(...)` or `fig.colorbar(im, ax=ax)`
- `ax.bar(...)` for histogram data
- `ax.text(...)` or `ax.annotate(...)`
- `tight_layout()` or `constrained_layout=True`
- `ax.set_title(...)`
- `histtype="errorbar"` without `yerr=` on derived quantities
- `data=False` combined with `llabel=` (label stacking)
- Missing `mpl_magic(ax)` after `ax.legend()`
- Missing `hspace=0` with `sharex=True`

---

## Embedding in the Analysis Note

All figures are embedded inline at the point of discussion:
```markdown
![Figure N: caption](relative/path.pdf)
```

Rules:
- Place the image immediately after the paragraph that discusses it
- Use relative paths from the analysis workspace root
- Number figures sequentially throughout the document
- PDF for the AN source, PNG for review and quick inspection
- Caption follows the format: `<Plot name>. <Context and conclusion.>`
- Captions are 2--4 sentences, self-contained
- Do not restate what is already in the legend or axis labels

---

## Output Format Summary

- Default: PNG for inspection, PDF for publication and the AN
- Resolution: dpi=200 minimum (300 for final publication)
- Always `bbox_inches="tight"`, `transparent=True`
- Filename convention: `outputs/figures/<descriptive_name>.{pdf,png}`
