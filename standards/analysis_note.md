# Analysis Note Specification

The analysis note (AN) is the permanent, self-contained record of a complete
HEP measurement or search. It is not a journal paper, not an executive
summary, and not a slide deck with equations. It is the document from which
every number, every figure, and every methodological decision can be
understood and reproduced without access to the code.

## The Gold Standard

A physicist who has never seen the analysis must be able to reproduce every
number from the AN alone. This is the completeness test. Apply it literally:

- If a reader needs to look at the code to understand a selection choice,
  the AN has a gap.
- If a reader cannot tell how a systematic was evaluated without reading
  the script, the AN has a gap.
- If a reader cannot reconstruct the event selection from the AN text and
  figures, the AN has a gap.
- If a reader cannot determine how the final result was extracted from the
  equations and description in the AN, the AN has a gap.

Every gap is a defect. The AN exists to eliminate gaps.

## Versioning

The AN is a living document that evolves across analysis phases. Each phase
produces a phase-stamped version; no version is ever overwritten.

| Phase | Content | File naming |
|-------|---------|-------------|
| 4a (expected) | Complete AN with ALL detail using Asimov/MC results only | `ANALYSIS_NOTE_4a_v{N}.md` |
| 4b (partial data) | Updated from latest 4a; numbers replaced with 10% data | `ANALYSIS_NOTE_4b_v{N}.md` |
| 5 (draft) | Prose polish, typesetting, flagship figure quality pass | `ANALYSIS_NOTE_v{N}.md` |
| 7 (final) | Updated from Phase 5 draft; full observed results from Phase 6 | `ANALYSIS_NOTE_FINAL_v{N}.md` |

Review/fix cycles within a phase increment the version number (v1, v2, ...).
All versions are preserved on disk for audit and comparison. A reviewer can
diff any two versions to see exactly what changed.

## Page Count

The AN is a complete record. Typical length: 50--100 rendered pages for a
standard measurement.

**Under 30 pages means detail is missing.** This is a Category A defect at
Phase 5 review unless the reviewer confirms the analysis is genuinely simple
(single observable, fewer than 5 systematic sources, no MVA, no unfolding)
AND the completeness test still passes.

Common causes of thin ANs:
- Missing per-cut distribution plots (before and after each cut)
- Missing per-systematic impact figures
- Missing cross-check result plots (just "PASS" without showing the comparison)
- Missing MVA diagnostics when a classifier is used
- Summary tables without supporting figures
- Methods described in one sentence instead of full paragraphs with equations

## Number Consistency Gate

Every numerical value in the AN must originate from a machine-readable
artifact (JSON, NPZ, CSV) produced by the analysis scripts. Numbers are
never hand-transcribed from terminal output or plots.

The `results/*.json` files are the single source of truth. The AN is a
rendering of those values into prose. A per-section table that contradicts
the summary table is Category A regardless of which one is correct -- the
inconsistency itself is the problem.

Rules:
- Every number must cite the script that produced it.
- Every number must appear consistently wherever it is quoted (section tables,
  summary tables, prose, derived quantities, appendix tables).
- When a fix cycle changes a result, ALL instances must be updated.
- Rounding must be consistent: if the abstract says +/-0.01 and a table says
  +/-0.011, choose one precision and use it everywhere.
- When displaying component uncertainties and a total, verify that the
  quadrature sum matches the displayed total to the displayed precision.

## Notation Consistency

Every physical quantity must use a single, consistent symbol throughout the
AN. Define symbols at first use and maintain the convention. The same variable
appearing under different names in different sections is Category A.

When adopting notation from a reference paper, note explicitly if it differs
from notation used earlier in the AN. When a primary operating point or
configuration changes between phases (e.g., Phase 4a uses kappa=0.5 but
Phase 4b uses kappa=0.3), state the change explicitly in the relevant
results section and update or annotate every earlier occurrence of the old
label.

---

## Required Sections

The following 13 sections must appear in this order. No section may be empty.
Every section heading must be followed by at least one paragraph of prose
before any figures or tables.

### 1. Title

The title must contain the measured quantity, the final state or channel,
the dataset, and the center-of-mass energy. Use plain text in the YAML title
field (not LaTeX math). Use Unicode for mathematical symbols.

### 2. Author List

List all contributors who materially contributed to the analysis or the note.

### 3. Abstract (unnumbered, before Table of Contents)

The abstract is 4--5 sentences and must state: what was measured, which data
were used, the method used for extraction, the key result with uncertainties,
and the comparison to a reference value. It must not be a numbered section.

### 4. Table of Contents

Immediately after the abstract.

### 5. Change Log (unnumbered, before Introduction)

Maintained in reverse chronological order. Entries grouped by phase/version
with bulleted summaries describing what changed and why. The change log must
not exceed 1 rendered page. For multi-iteration analyses, condense earlier
phases to one-line summaries and keep full detail only for the last 2
versions. Move the full change history to an appendix if needed.

The change log is a navigation aid, not a process diary. Internal phase
labels, finding numbers, and debug details do not belong here.

### 6. Introduction

Must cover: physics motivation, precise definition of the observable,
prior measurements with citations, and the role of the present analysis.

**Cross-experiment context is mandatory.** Cite at least 2 measurements of
the same or closely related observable from other experiments (LEP, Tevatron,
LHC, B-factories) where they exist. For a first measurement, cite the
closest precursor measurements and explain what is new.

### 7. Data Samples

Must document: experiment, collision type, center-of-mass energy, integrated
luminosity, MC generators, event counts before and after preselection, file
format, tree name.

**Structured tables are mandatory** (not free-form prose or file listings):

**Data summary table** -- one row per data-taking era/period. Integrated
luminosity is mandatory for every period. If luminosity is not published
for archived/open data, estimate from the hadronic cross-section and event
count and state the method.

| Period | sqrt(s) [GeV] | Events (pre-sel) | Luminosity [pb^-1] |
|--------|---------------|------------------|---------------------|
| ...    | ...           | ...              | ...                 |

**MC sample table** -- one row per physics process:

| Process | Generator | Cross-section [nb] | N_gen | k-factor | Notes |
|---------|-----------|---------------------|-------|----------|-------|
| ...     | ...       | ...                 | ...   | ...      | ...   |

These are summary-level tables. For archived data, document what is known
and mark unknowns explicitly.

### 8. Event Selection

Every cut must have: motivation, distribution plot (N-1 preferred), efficiency
(per-cut and cumulative), sensitivity to cut variation (+/-10% shift).

**Cut-flow table is mandatory:**

| Selection step | Events | Relative eff. | Cumulative eff. |
|----------------|-------:|-------------:|----------------:|
| ...            | ...    | ...          | ...             |

Rule of thumb: every selection cut needs a before/after distribution plot.

### 9. Kinematic Distributions

Survey plots for basic kinematics, invariant-mass spectra, opposite-sign vs
same-sign comparisons, and derived quantities used later. Every plot must be
discussed in short, factual paragraphs.

### 10. Signal Extraction / Corrections / Unfolding

Must include: candidate model set, justification for the nominal model,
parameter initialization from data, fit results, nominal fit plot with
residuals or pulls.

**Key equations must be displayed** as `$$...$$`. The correction formula,
the likelihood or chi-squared used for fitting, and the systematic
propagation formula must all be shown. A reader must be able to implement
the method from the equations alone.

**Equations for every method.** When a method is described, the governing
equation must accompany it. "The correction is applied bin-by-bin" without
showing the explicit formula is incomplete. "A BDT is trained on signal
and background" without the loss function and input features is incomplete.

**Interpretive paragraphs.** Every result, figure, and table must be
accompanied by a paragraph interpreting the finding. What does the result
mean? Is it consistent with expectations? What are the implications?

**Resolving power statement.** Every extraction must state what level of
deviation from the SM the measurement can distinguish at 2 sigma, given
the total uncertainty. This tells the reader whether the measurement is
a precision test or an exploratory observation.

### 11. Systematic Uncertainties

One subsection per source, following this 4-part template:

1. **Physical origin** (1--2 sentences: what physical effect causes this)
2. **Evaluation method** (how the variation is defined, what is varied,
   through what chain it propagates; cite the formula or reference; state
   the variation size and justify it with a measurement or published
   uncertainty)
3. **Numerical impact** (table row + impact figure showing how the result
   shifts bin-by-bin; flat shifts on shape measurements require explanation)
4. **Interpretation** (dominant? subdominant? correlated with other sources?
   what would reduce it?)

A subsection that only states a number without explaining the propagation
chain is incomplete.

After the per-source subsections:

**Summary budget table** (source vs. variation on observable).

**Systematic breakdown figure** (waterfall, horizontal bar, or stacked bar
chart showing relative contribution of each source). A summary table alone
is insufficient.

**Error budget narrative** (mandatory paragraph):
(a) which sources dominate and why,
(b) whether the measurement is statistically or systematically limited,
(c) what concrete improvements could reduce the dominant sources,
(d) the measurement's resolving power.

### 12. Cross-Checks

Each cross-check belongs within the section it validates (not standalone).
Each must include: what was tested, criterion for success, observed outcome,
comparison plot (overlay/ratio/pull -- not just pass/fail), chi-squared/p-value,
interpretation. Large cross-checks go to appendix with forward reference.

### 13. Statistical Method, Results, Comparison, Conclusions, Future Directions, Known Limitations

**Statistical Method** -- likelihood construction, fit validation, GoF.

**Results** -- final value with full uncertainties (stat + syst separated),
per-bin tables for differential measurements.

**Mandatory comparison overlay.** At least one figure overlaying this
measurement with published values on the SAME axes: published data points
with uncertainties, this measurement with total uncertainty band, a ratio
or pull panel, and a chi-squared/ndf annotation. A results section without
this overlay is Category B. A results section that says "consistent with
published values" without showing the comparison is Category A.

**Comparison to Prior Results** -- quantitative, not qualitative. Every
comparison must state chi-squared/ndf, pull in sigma, or ratio with
uncertainty. Must address: (a) comparison to best published measurement,
(b) whether precision is competitive/comparable/exploratory, (c) what the
comparison tells us about method validity.

**Conclusions** -- result, precision, dominant limitations. No new numbers.

**Future Directions** -- items must be genuinely infeasible now. See
the downscoping standard for the feasibility test.

**Known Limitations** -- 3--5 most significant open issues with: what the
limitation is, whether it was attempted, quantitative impact, what would
fix it. This is the physicist-facing narrative (distinct from the
Limitation Index appendix).

---

## Appendices

### Appendix A: Reproduction Contract

The exact command sequence to reproduce the full analysis from raw data to
final result. Must include: environment setup, pixi task sequence in
execution order, workflow diagram showing the execution DAG, any manual
steps, expected runtime estimates. Sufficient for a physicist who has never
seen the analysis to reproduce every number by following commands verbatim.

### Appendix B: Figure Index

Table of all figures with figure number, file path, short description,
and main section.

### Appendix C: Limitation Index

Complete registry of all constraints [A1], limitations [L1], and design
decisions [D1]. Each entry: label, one-line description, where introduced,
impact on result, mitigation.

### Appendix D: Covariance Matrices

Per-source correlation matrices (one panel per component, same color scale),
total covariance and correlation matrices (state max off-diagonal
correlation), recommendation for downstream use.

### Appendix E: Extended Tables

Per-bin systematic tables, extended cutflow, auxiliary plots.

### Appendix F: Review History

Summary per review round: reviewer role, main issues raised, resolutions,
unresolved items.

---

## Statistical Methodology Standards

These are Category A if violated.

**Full covariance is mandatory.** When a covariance matrix exists, ALL
chi-squared tests must use the full covariance:
$$\chi^2 = (\mathbf{d} - \mathbf{m})^T C^{-1} (\mathbf{d} - \mathbf{m})$$
Diagonal-only chi-squared may be reported alongside but must not be
the primary metric. If the covariance matrix is ill-conditioned
(condition number > 10^8), note this and report both metrics with caveats.

**Pull distribution diagnostics.** State the expected number of bins
with |pull| > 2 sigma (= 4.6%) and > 3 sigma (= 0.27%). If actual >>
expected: uncertainties are underestimated or there is a genuine data-MC
difference -- state which. If actual << expected or pull RMS < 0.7:
uncertainties are overestimated. Pull RMS must be quoted: 1.0 +/- 0.1 is
healthy; < 0.7 is overcoverage; > 1.3 is undercoverage.

**Goodness-of-fit.** The primary extraction must have chi-squared/ndf < 3
(p > 0.01). A primary result with p < 0.01 requires: (a) source of poor
GoF identified, (b) demonstrated not to bias the extracted parameter,
(c) a configuration with acceptable GoF shown as cross-check.

**Closure test criteria.** Closure tests pass when chi-squared p > 0.05.
Ad hoc thresholds (e.g., "chi-squared/ndf < 5 is acceptable") are not
valid. When p < 0.01, the closure has failed and 3+ remediation attempts
are required.

## Validation Documentation Standard

Each validation test (closure, stress, flat-prior, alternative method)
must include ALL five elements:

1. **What was tested** and why
2. **Expected result**
3. **Observed result** (chi-squared/ndf, p-value, max deviation)
4. **Figure** showing the test result (not just a number)
5. **Interpretation** -- does the test pass? If not, what was tried to fix
   it (3+ attempts required)? What does this mean for the result's reliability?

"Closure test passes" without elements 1--5 is incomplete.

---

## LaTeX/PDF Pipeline

Markdown to PDF via three steps:
1. **pandoc** (>=3.0) produces a `.tex` file
2. **postprocess_tex.py** applies structural fixes (title math, abstract
   environment, references unnumbering, table spacing, float barriers,
   needspace, appendix handling, clearpage, stale label warnings)
3. **tectonic** (or xelatex) compiles to PDF

The `build-pdf` pixi task runs this pipeline. Do not modify the shared
preamble per-analysis without documented justification.

### Pandoc Pitfalls

- Never use `$\pm$`, `$<$`, `$>$`, `$-$`, `$\sim$` as standalone math.
  Use Unicode: the +/- symbol, <, >, the Unicode minus sign, ~.
- YAML title field does not render LaTeX math. Use Unicode or handle
  in postprocessing.
- Never use `\mathrm{}` in figure captions or section headers. Pandoc
  converts captions to both LaTeX and alt-text, producing errors.
- Never put `@ref` cross-references inside `$...$` math.
- Section headers must not contain complex LaTeX.

### Rendering Quality Checklist

Check after every PDF compilation:
- No orphaned section headings (heading as last line on a page)
- No figures extending beyond page margins (especially 2D + colorbar)
- Short tables (< 15 rows) not split across pages
- Captions spanning full text width
- All `@fig:`, `@tbl:`, `@eq:` references resolve
- No overfull hbox warnings involving figures or tables
- Abstract appears unnumbered before table of contents
- No table-caption collisions with preceding text
- Figure height does not exceed 0.7 textheight

---

## Literature Requirements

**Foundational citations.** The AN must cite the original theoretical papers
that defined the observable being measured. Category A if missing.

**Cross-experiment context.** Introduction must cite at least 2 measurements
from other experiments.

**Reference count diagnostic.** Fewer than 15 references in a substantial AN
is Category A. A thorough AN cites: foundational theory (3--5), reference
analyses (3--5), detector papers (2--3), methodology references (3--5),
PDG/world-average sources (3--5). Total: 15--25 typical.

**BibTeX integrity.** Never generate BibTeX entries from training data. Every
entry must be obtained from INSPIRE, DOI lookup, or the actual paper. Every
entry must include `doi`, `url`, or `eprint`. Use `unsrt`-style ordering.

---

## Pre-Submission Checklist

**Structure:**
- [ ] Section order matches this specification exactly
- [ ] Change Log is present, unnumbered, before the Introduction
- [ ] No section heading followed immediately by figure/table without prose
- [ ] Every required section is present and non-empty

**Figures and tables:**
- [ ] Every figure embedded inline and numbered sequentially
- [ ] Every caption is 2--4 sentences, self-contained
- [ ] Every selection cut has a distribution plot
- [ ] Every systematic source has an impact figure
- [ ] Every cross-check has a comparison plot (not just pass/fail)
- [ ] Systematic breakdown figure present
- [ ] Mandatory comparison overlay present in Results

**Numbers and traceability:**
- [ ] Every number cites the script that produced it
- [ ] Every final result separates stat and syst uncertainties
- [ ] Event counts consistent across all tables and text
- [ ] Rounding consistent (quadrature sums match displayed totals)
- [ ] Pull diagnostics state expected vs observed >2 sigma bins, report RMS

**Quality:**
- [ ] Every validation test documents elements 1--5
- [ ] Every limitation stated with quantitative impact
- [ ] Every post-hoc comparison labeled as such
- [ ] Every comparison to prior results is quantitative
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
