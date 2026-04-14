# Analysis Note Specification

Analysis note (AN) = permanent, self-contained record of complete HEP measurement or search. Not journal paper, not executive summary, not slide deck with equations. Document from which every number, figure, and methodological decision can be understood and reproduced without code access.

## Gold Standard

Physicist who never saw analysis must reproduce every number from AN alone. Completeness test -- apply literally:

- Reader needs code to understand selection choice → AN has gap.
- Reader can't tell how systematic was evaluated without reading script → gap.
- Reader can't reconstruct event selection from AN text and figures → gap.
- Reader can't determine how final result was extracted from equations/description → gap.

Every gap = defect. AN exists to eliminate gaps.

## Versioning

AN = living document evolving across analysis phases. Each phase produces phase-stamped version; no version ever overwritten.

| Phase | Content | File naming |
|-------|---------|-------------|
| 4a (expected) | Complete AN with ALL detail using Asimov/MC results only | `ANALYSIS_NOTE_4a_v{N}.md` |
| 4b (partial data) | Updated from latest 4a; numbers replaced with 10% data | `ANALYSIS_NOTE_4b_v{N}.md` |
| 5 (draft) | Prose polish, typesetting, flagship figure quality pass | `ANALYSIS_NOTE_v{N}.md` |
| 7 (final) | Updated from Phase 5 draft; full observed results from Phase 6 | `ANALYSIS_NOTE_FINAL_v{N}.md` |

Review/fix cycles within phase increment version number (v1, v2, ...). All versions preserved on disk for audit and comparison. Reviewer can diff any two versions.

## Page Count

AN = complete record. Typical length: 50--100 rendered pages for standard measurement.

**Under 30 pages → detail missing.** Category A defect at Phase 5 review unless reviewer confirms genuinely simple analysis (single observable, fewer than 5 systematic sources, no MVA, no unfolding) AND completeness test still passes.

Common causes of thin ANs:
- Missing per-cut distribution plots (before and after each cut)
- Missing per-systematic impact figures
- Missing cross-check result plots (just "PASS" without showing comparison)
- Missing MVA diagnostics when classifier used
- Summary tables without supporting figures
- Methods described in one sentence instead of full paragraphs with equations

## Number Consistency Gate

Every numerical value in AN must originate from machine-readable artifact (JSON, NPZ, CSV) produced by analysis scripts. Numbers never hand-transcribed from terminal output or plots.

`results/*.json` = single source of truth. AN = rendering of those values into prose. Per-section table contradicting summary table = Category A regardless of which one correct -- inconsistency itself = problem.

Rules:
- Every number must cite producing script.
- Every number must appear consistently wherever quoted (section tables, summary tables, prose, derived quantities, appendix tables).
- Fix cycle changes result → ALL instances must update.
- Rounding must be consistent: abstract says +/-0.01 and table says +/-0.011 → choose one precision, use everywhere.
- Component uncertainties + total displayed → verify quadrature sum matches displayed total to displayed precision.

## Notation Consistency

Every physical quantity must use single, consistent symbol throughout AN. Define symbols at first use, maintain convention. Same variable under different names in different sections = Category A.

When adopting notation from reference paper, note explicitly if differs from earlier AN notation. When primary operating point changes between phases (e.g., Phase 4a uses kappa=0.5 but Phase 4b uses kappa=0.3), state change explicitly in relevant results section and update/annotate every earlier occurrence.

---

## Required Sections

Following 13 sections must appear in this order. No section may be empty. Every section heading must have at least one paragraph of prose before any figures or tables.

### 1. Title

Must contain: measured quantity, final state/channel, dataset, center-of-mass energy. Plain text in YAML title field (not LaTeX math). Unicode for mathematical symbols.

### 2. Author List

All contributors who materially contributed to analysis or note.

### 3. Abstract (unnumbered, before Table of Contents)

4--5 sentences. Must state: what was measured, which data used, extraction method, key result with uncertainties, comparison to reference value. Not a numbered section.

### 4. Table of Contents

Immediately after abstract.

### 5. Change Log (unnumbered, before Introduction)

Reverse chronological order. Entries grouped by phase/version with bulleted summaries describing what changed and why. Must not exceed 1 rendered page. Multi-iteration analyses → condense earlier phases to one-line summaries, keep full detail only for last 2 versions. Move full history to appendix if needed.

Change log = navigation aid, not process diary. Internal phase labels, finding numbers, debug details don't belong here.

### 6. Introduction

Must cover: physics motivation, precise observable definition, prior measurements with citations, role of present analysis.

**Cross-experiment context mandatory.** Cite at least 2 measurements of same or closely related observable from other experiments (LEP, Tevatron, LHC, B-factories) where they exist. First measurement → cite closest precursor measurements, explain what's new.

### 7. Data Samples

Must document: experiment, collision type, center-of-mass energy, integrated luminosity, MC generators, event counts before/after preselection, file format, tree name.

**Structured tables mandatory** (not free-form prose or file listings):

**Data summary table** -- one row per data-taking era/period. Integrated luminosity mandatory for every period. Luminosity not published for archived/open data → estimate from hadronic cross-section and event count, state method.

| Period | sqrt(s) [GeV] | Events (pre-sel) | Luminosity [pb^-1] |
|--------|---------------|------------------|---------------------|
| ...    | ...           | ...              | ...                 |

**MC sample table** -- one row per physics process:

| Process | Generator | Cross-section [nb] | N_gen | k-factor | Notes |
|---------|-----------|---------------------|-------|----------|-------|
| ...     | ...       | ...                 | ...   | ...      | ...   |

Summary-level tables. Archived data → document what's known, mark unknowns explicitly.

### 8. Event Selection

Every cut must have: motivation, distribution plot (N-1 preferred), efficiency (per-cut and cumulative), sensitivity to cut variation (+/-10% shift).

**Cut-flow table mandatory:**

| Selection step | Events | Relative eff. | Cumulative eff. |
|----------------|-------:|-------------:|----------------:|
| ...            | ...    | ...          | ...             |

Rule of thumb: every selection cut needs before/after distribution plot.

### 9. Kinematic Distributions

Survey plots for basic kinematics, invariant-mass spectra, opposite-sign vs same-sign comparisons, derived quantities used later. Every plot discussed in short, factual paragraphs.

### 10. Signal Extraction / Corrections / Unfolding

Must include: candidate model set, justification for nominal model, parameter initialization from data, fit results, nominal fit plot with residuals or pulls.

**Key equations must be displayed** as `$$...$$`. Correction formula, likelihood or chi-squared used for fitting, systematic propagation formula -- all shown. Reader must implement method from equations alone.

**Equations for every method.** Method described → governing equation must accompany. "Correction applied bin-by-bin" without explicit formula = incomplete. "BDT trained on signal and background" without loss function and input features = incomplete.

**Interpretive paragraphs.** Every result, figure, table must have paragraph interpreting finding. What does result mean? Consistent with expectations? Implications?

**Resolving power statement.** Every extraction must state what deviation level from SM measurement can distinguish at 2 sigma, given total uncertainty. Tells reader whether measurement = precision test or exploratory observation.

### 11. Systematic Uncertainties

One subsection per source, following 4-part template:

1. **Physical origin** (1--2 sentences: what physical effect causes this)
2. **Evaluation method** (how variation defined, what varied, propagation chain; cite formula or reference; state variation size, justify with measurement or published uncertainty)
3. **Numerical impact** (table row + impact figure showing bin-by-bin result shift; flat shifts on shape measurements require explanation)
4. **Interpretation** (dominant? subdominant? correlated with other sources? what would reduce it?)

Subsection stating only number without explaining propagation chain = incomplete.

After per-source subsections:

**Summary budget table** (source vs. variation on observable).

**Systematic breakdown figure** (waterfall, horizontal bar, or stacked bar chart showing relative contribution of each source). Summary table alone = insufficient.

**Error budget narrative** (mandatory paragraph):
(a) which sources dominate and why,
(b) measurement statistically or systematically limited,
(c) concrete improvements to reduce dominant sources,
(d) measurement's resolving power.

### 12. Cross-Checks

Each cross-check belongs within section it validates (not standalone). Each must include: what tested, success criterion, observed outcome, comparison plot (overlay/ratio/pull -- not just pass/fail), chi-squared/p-value, interpretation. Large cross-checks → appendix with forward reference.

### 13. Statistical Method, Results, Comparison, Conclusions, Future Directions, Known Limitations

**Statistical Method** -- likelihood construction, fit validation, GoF.

**Results** -- final value with full uncertainties (stat + syst separated), per-bin tables for differential measurements.

**Mandatory comparison overlay.** At least one figure overlaying this measurement with published values on SAME axes: published data points with uncertainties, this measurement with total uncertainty band, ratio or pull panel, chi-squared/ndf annotation. Results section without this overlay = Category B. Results section saying "consistent with published values" without showing comparison = Category A.

**Comparison to Prior Results** -- quantitative, not qualitative. Every comparison must state chi-squared/ndf, pull in sigma, or ratio with uncertainty. Must address: (a) comparison to best published measurement, (b) precision competitive/comparable/exploratory, (c) what comparison tells about method validity.

**Conclusions** -- result, precision, dominant limitations. No new numbers.

**Future Directions** -- items must be genuinely infeasible now. See downscoping standard for feasibility test.

**Known Limitations** -- 3--5 most significant open issues with: what limitation is, whether attempted, quantitative impact, what would fix it. Physicist-facing narrative (distinct from Limitation Index appendix).

---

## Appendices

### Appendix A: Reproduction Contract

Exact command sequence to reproduce full analysis from raw data to final result. Must include: environment setup, pixi task sequence in execution order, workflow diagram showing execution DAG, manual steps, expected runtime estimates. Sufficient for physicist who never saw analysis to reproduce every number by following commands verbatim.

### Appendix B: Figure Index

Table of all figures: figure number, file path, short description, main section.

### Appendix C: Limitation Index

Complete registry of all constraints [A1], limitations [L1], design decisions [D1]. Each entry: label, one-line description, where introduced, impact on result, mitigation.

### Appendix D: Covariance Matrices

Per-source correlation matrices (one panel per component, same color scale), total covariance and correlation matrices (state max off-diagonal correlation), recommendation for downstream use.

### Appendix E: Extended Tables

Per-bin systematic tables, extended cutflow, auxiliary plots.

### Appendix F: Review History

Summary per review round: reviewer role, main issues raised, resolutions,
unresolved items.

---

## Statistical Methodology Standards

Category A if violated.

**Full covariance mandatory.** When covariance matrix exists, ALL chi-squared tests must use full covariance:
$$\chi^2 = (\mathbf{d} - \mathbf{m})^T C^{-1} (\mathbf{d} - \mathbf{m})$$
Diagonal-only chi-squared may be reported alongside but must not be primary metric. Covariance matrix ill-conditioned (condition number > 10^8) → note this, report both metrics with caveats.

**Pull distribution diagnostics.** State expected bins with |pull| > 2 sigma (= 4.6%) and > 3 sigma (= 0.27%). Actual >> expected → uncertainties underestimated or genuine data-MC difference -- state which. Actual << expected or pull RMS < 0.7 → uncertainties overestimated. Pull RMS must be quoted: 1.0 +/- 0.1 = healthy; < 0.7 = overcoverage; > 1.3 = undercoverage.

**Goodness-of-fit.** Primary extraction must have chi-squared/ndf < 3 (p > 0.01). Primary result with p < 0.01 requires: (a) poor GoF source identified, (b) demonstrated not to bias extracted parameter, (c) configuration with acceptable GoF shown as cross-check.

**Closure test criteria.** Pass when chi-squared p > 0.05. Ad hoc thresholds (e.g., "chi-squared/ndf < 5 is acceptable") = not valid. When p < 0.01, closure failed → 3+ remediation attempts required.

## Validation Documentation Standard

Each validation test (closure, stress, flat-prior, alternative method) must include ALL five elements:

1. **What was tested** and why
2. **Expected result**
3. **Observed result** (chi-squared/ndf, p-value, max deviation)
4. **Figure** showing test result (not just number)
5. **Interpretation** -- pass? If not, what tried to fix (3+ attempts required)? What does this mean for result's reliability?

"Closure test passes" without elements 1--5 = incomplete.

---

## LaTeX/PDF Pipeline

Markdown to PDF via three steps:
1. **pandoc** (>=3.0) produces `.tex` file
2. **postprocess_tex.py** applies structural fixes (title math, abstract environment, references unnumbering, table spacing, float barriers, needspace, appendix handling, clearpage, stale label warnings)
3. **tectonic** (or xelatex) compiles to PDF

`build-pdf` pixi task runs this pipeline. Don't modify shared preamble per-analysis without documented justification.

### Pandoc Pitfalls

- Never use `$\pm$`, `$<$`, `$>$`, `$-$`, `$\sim$` as standalone math. Use Unicode: +/- symbol, <, >, Unicode minus sign, ~.
- YAML title field doesn't render LaTeX math. Use Unicode or handle in postprocessing.
- Never use `\mathrm{}` in figure captions or section headers. Pandoc converts captions to both LaTeX and alt-text → errors.
- Never put `@ref` cross-references inside `$...$` math.
- Section headers must not contain complex LaTeX.

### Rendering Quality Checklist

Check after every PDF compilation:
- No orphaned section headings (heading as last line on page)
- No figures extending beyond page margins (especially 2D + colorbar)
- Short tables (< 15 rows) not split across pages
- Captions spanning full text width
- All `@fig:`, `@tbl:`, `@eq:` references resolve
- No overfull hbox warnings involving figures or tables
- Abstract appears unnumbered before table of contents
- No table-caption collisions with preceding text
- Figure height doesn't exceed 0.7 textheight

---

## Literature Requirements

**Foundational citations.** AN must cite original theoretical papers defining measured observable. Category A if missing.

**Cross-experiment context.** Introduction must cite at least 2 measurements from other experiments.

**Reference count diagnostic.** Fewer than 15 references in substantial AN = Category A. Thorough AN cites: foundational theory (3--5), reference analyses (3--5), detector papers (2--3), methodology references (3--5), PDG/world-average sources (3--5). Total: 15--25 typical.

**BibTeX integrity.** Never generate BibTeX entries from training data. Every entry must come from INSPIRE, DOI lookup, or actual paper. Every entry must include `doi`, `url`, or `eprint`. Use `unsrt`-style ordering.

---

## Pre-Submission Checklist

**Structure:**
- [ ] Section order matches this specification exactly
- [ ] Change Log present, unnumbered, before Introduction
- [ ] No section heading followed immediately by figure/table without prose
- [ ] Every required section present and non-empty

**Figures and tables:**
- [ ] Every figure embedded inline and numbered sequentially
- [ ] Every caption 2--4 sentences, self-contained
- [ ] Every selection cut has distribution plot
- [ ] Every systematic source has impact figure
- [ ] Every cross-check has comparison plot (not just pass/fail)
- [ ] Systematic breakdown figure present
- [ ] Mandatory comparison overlay present in Results

**Numbers and traceability:**
- [ ] Every number cites producing script
- [ ] Every final result separates stat and syst uncertainties
- [ ] Event counts consistent across all tables and text
- [ ] Rounding consistent (quadrature sums match displayed totals)
- [ ] Pull diagnostics state expected vs observed >2 sigma bins, report RMS

**Quality:**
- [ ] Every validation test documents elements 1--5
- [ ] Every limitation stated with quantitative impact
- [ ] Every post-hoc comparison labeled as such
- [ ] Every comparison to prior results quantitative
- [ ] Error budget narrative paragraph present
- [ ] Known Limitations contains 3--5 items with impact and remediation

**References:**
- [ ] 15+ references from verified sources
- [ ] No BibTeX entries from training data
- [ ] Foundational theory papers cited
- [ ] At least 2 cross-experiment citations in Introduction

**Appendices:**
- [ ] A (Reproduction Contract) complete
- [ ] B (Figure Index) present
- [ ] C (Limitation Index) present
- [ ] D (Covariance Matrices) present when applicable
- [ ] E (Extended Tables) present when applicable
- [ ] F (Review History) present

**Rendering (after PDF compilation):**
- [ ] No orphaned section headings
- [ ] No figures off-page
- [ ] No overfull hbox warnings on figures/tables
- [ ] Abstract unnumbered before ToC
- [ ] All cross-references resolve
- [ ] Document exceeds 30 pages (or genuinely simple analysis confirmed)
