# Figure Production Standards

All figures in apexAI analysis must follow these rules. Non-negotiable. Deviation requires explicit, documented justification in experiment log. Rules prevent broken aspect ratios, mangled labels, clipped content, inconsistent styling.

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

### Font sizes LOCKED

No absolute numeric `fontsize=` values to ANY matplotlib call (`set_xlabel`, `set_ylabel`, `set_title`, `tick_params`, `annotate`, `text`). CMS stylesheet sets all font sizes correctly for 10x10 figure size. Relative string sizes (`'small'`, `'x-small'`, `'xx-small'`) allowed where needed (dense legends, annotation text).

### Figure size LOCKED at (10, 10)

No other figure size. CMS stylesheet font sizes calibrated for this canvas. Ratio plots: `figsize=(10, 10)` with `height_ratios=[3, 1]`. MxN subplots: scale to 10 per subplot dimension (2x2 → (20, 20), 1x3 → (30, 10)).

### Legends via mpl_magic

Default approach = scale y-axis to accommodate legend:

```python
from mplhep.plot import mpl_magic
ax.legend(fontsize="x-small")
mpl_magic(ax)
```

Call `mpl_magic(ax)` after all plotting done. Extends y-range so legend sits in empty space above data. Manual placement (`loc=`, `bbox_to_anchor`) allowed only when plot has genuinely empty region.

Legend-data overlap = Category A. Visual inspection of rendered figures required, not just checking `loc=` in script.

### Colorbars: make_square_add_cbar or cbarextend

For ANY 2D plot with colorbar, use one of:
- `mh.hist2dplot(H, cbarextend=True)` (preferred)
- `cax = mh.utils.make_square_add_cbar(ax)` then `fig.colorbar(im, cax=cax)`
- `cax = mh.utils.append_axes(ax, extend=True)` then `fig.colorbar(im, cax=cax)`

**Never use** `fig.colorbar(im)`, `fig.colorbar(im, ax=ax)`, `fig.colorbar(im, ax=ax, shrink=...)`, or `plt.colorbar(...)`. These steal space from main axes → break square aspect ratio. Applies to ALL 2D plots: correlation matrices, migration matrices, response matrices, efficiency maps.

### Ratio plots: sharex=True and hspace=0

Ratio plots MUST use `sharex=True` in `plt.subplots()` AND `fig.subplots_adjust(hspace=0)`. Without `sharex=True` → upper panel shows redundant x-axis label ("Axis 0"). Without `hspace=0` → visible gap between main and ratio panels. Both = Category A.

**Axis 0 workaround.** After calling `exp_label(ax=ax_main, loc=0)`, suppress artifact on ratio panel:
```python
for txt in rax.texts:
    if "Axis" in txt.get_text():
        txt.remove()
```
Or use `loc=2` (upper left) to avoid triggering bug.

### Histograms via mh.histplot

When plotting histograms from raw event data, always use `mh.histplot()`. Never use `ax.step()`, `ax.bar()`, or `ax.fill_between()`.

| Data type | Correct | Wrong |
|-----------|---------|-------|
| Raw counts (error bars) | `mh.histplot(h, histtype="errorbar")` | `ax.errorbar()` without yerr |
| MC prediction (filled) | `mh.histplot(h, histtype="fill")` | `ax.fill_between()`, `ax.bar()` |
| Stacked MC | `mh.histplot([h1,h2], stack=True)` | `ax.bar(..., bottom=...)` |
| Theory curve (continuous) | `ax.plot(x, y)` | (correct -- not binned) |

### Derived quantities: explicit yerr

When plotting any quantity NOT raw event count (normalized distributions, correction factors, ratios, efficiencies, systematic shifts), MUST pass explicit `yerr=`. Without it, mplhep computes sqrt(bin content) → meaningless for non-count values.

**Test:** Filled histogram with `h.fill(raw_values)`? Auto sqrt(N) correct. Assigned values with `h.view()[:] = ...` or computed from formula? `yerr=` mandatory.

### No ax.text or ax.annotate

Use `mh.label.add_text(text, ax=ax)` for all text annotations. Respects mplhep styling and positioning. Includes panel labels like (a), (b) in grids.

### No titles

Never `ax.set_title()`. Captions go in analysis note. Additional info → `ax.legend(title="...")` or `mh.label.add_text()`.

### Both PDF and PNG

Save every figure in both formats:
```python
fig.savefig("output.pdf", bbox_inches="tight", dpi=200, transparent=True)
fig.savefig("output.png", bbox_inches="tight", dpi=200, transparent=True)
```
PDF for analysis note, PNG for quick inspection. Always `bbox_inches="tight"`.

### No tight_layout

Never use `tight_layout()` or `constrained_layout=True` with mplhep. Conflicts with mplhep label positioning. Use `bbox_inches="tight"` at save time instead.

### Close figures

`plt.close(fig)` after saving → prevent memory leaks in long scripts.

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

Use mplhep generic label system with CMS style as base:
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

When `data=False`, mplhep auto-adds "Simulation" as left label. Do NOT also set `llabel` → produces "Simulation Open Simulation". Safe pattern = always `data=True` with explicit `llabel`:
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

Rule of thumb: typical lepton pT ~ 40 → units = GeV; ~ 40000 → MeV.

---

## Standard Plot Types

### Distribution plot
Data as black circles with error bars (`mh.histplot(..., histtype="errorbar")`), MC as filled/stacked histograms. Experiment label, axis labels with units, legend via `mpl_magic`.

### Fit result (two-panel)
Main panel: data + fit curve + background component. Ratio/pull panel below with `sharex=True` and `hspace=0`. Pull panel shows horizontal lines at 0 and +/-2.

### Cut-flow (barh)
Horizontal bar chart: cut names on y-axis, event counts on x-axis. Monotonically decreasing.

### N-1 plot
Apply ALL cuts except one being shown. Vertical dashed line at cut threshold. Show signal and background separately.

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

Always include units in brackets. Y-axis bin normalization → round bin width to clean value (0.01, 0.05, 0.1, 0.5, 1, 2, 5, 10, ...). Natural width ugly → adjust binning or omit width.

---

## Sizing Rules for Analysis Note

Pandoc preamble sets default figure height to `0.45\linewidth`. Height-based sizing keeps plot area consistent between 1D histograms and 2D plots with colorbars.

| Plot type | matplotlib figsize | AN height | Notes |
|-----------|-------------------|-----------|-------|
| Single panel | (10, 10) | 0.45 linewidth (default) | Distribution, spectrum |
| Ratio plot | (10, 10) | 0.45 linewidth (default) | Data/MC with ratio |
| 2D with colorbar | (10, 10) | 0.45 linewidth (default) | Matrix, Lund plane |
| Side-by-side | Compose in LaTeX | 0.45 linewidth each | See below |
| 2x2 or 3x2 grid | Compose in LaTeX | 0.3 linewidth each | See below |

**Prefer LaTeX subfigures over matplotlib grids.** Produce individual (10, 10) figures, compose in AN using pandoc-crossref subfigure syntax. Better control over layout, captions, cross-referencing.

Exception: tightly-coupled panels sharing physical x-axis (ratio plots, pull panels) should be single matplotlib figure with `sharex=True` and `hspace=0`. Can't use `sharex=True` → produce separate outputs.

---

## Additional Rules

**Suppress offset notation.** Never allow matplotlib's "1e6" offset text. Use `ax.ticklabel_format(axis='y', style='plain')`, absorb multiplier into axis label, or use custom formatter.

**Log scale.** `ax.set_yscale("log")` when y-axis range spans > 2 orders of magnitude. Log y-minimum: 0.5 or 1 (never 0).

**Deterministic.** `np.random.seed(42)` if any randomness.

**2D equal-aspect.** Both axes same coordinate type → `ax.set_aspect('equal')` so bins render as squares.

**Axis limits.** Tight to data range. No large empty regions.

**Publication-quality text labels.** No code variable names or Python identifiers in axis labels, legend entries, tick labels. "Energy-dep. efficiency" not "efficiency_energy_dep".

**Ratio panel tick collision.** Hide main panel x-axis tick labels with `ax.tick_params(labelbottom=False)`. Set ratio panel y-limits with margin to avoid crowding at boundary.

**Y-axis bin width labels.** Round to clean values. Non-round bin widths in labels = Category B.

**Ratio panel uncertainty bands.** Uncertainty band shown → describe in legend or caption. Unexplained bands = Category B. Suspiciously flat bands (constant width) warrant investigation.

---

## Lint Script Integration

Run `pixi run lint-plots` before committing. Lint script checks:

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

Also grep all label/xlabel/ylabel strings for underscores outside LaTeX math mode. Code variable names in rendered labels = Category A.

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

## Embedding in Analysis Note

All figures embedded inline at point of discussion:
```markdown
![Figure N: caption](relative/path.pdf)
```

Rules:
- Place image immediately after discussing paragraph
- Relative paths from analysis workspace root
- Number figures sequentially throughout document
- PDF for AN source, PNG for review and quick inspection
- Caption format: `<Plot name>. <Context and conclusion.>`
- Captions 2--4 sentences, self-contained
- Don't restate what's already in legend or axis labels

---

## Output Format Summary

- Default: PNG for inspection, PDF for publication and AN
- Resolution: dpi=200 minimum (300 for final publication)
- Always `bbox_inches="tight"`, `transparent=True`
- Filename convention: `outputs/figures/<descriptive_name>.{pdf,png}`
