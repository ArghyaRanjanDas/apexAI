# VC1 -- Analysis Review Committee

## Overview

Analysis Review Committee = first time entire analysis evaluated as
unified whole rather than phase by phase. Phase reviewers examine
artifacts within single phase boundary; VC1 members trace threads
across full analysis chain: does systematic catalog from Phase 1
match implementation in Phase 3 and treatment in Phase 4? Does
selection motivated in strategy actually appear in cut-flow? Do
numbers in analysis note match results.json?

VC1 activates after Phase 5 passes 5-bot review. All five members
review in parallel without seeing each other's reports. Chair
collects, deduplicates, triages all findings before routing fixes.

---

## Activation Timing

VC1 begins when ALL true:

1. Phase 5 review verdict = PASS (all A-items resolved, B-items
   resolved, C-items adjudicated by arbiter).
2. Compiled AN PDF exists and renders without errors.
3. Experiment log contains unbroken ADVANCE chain from Phase 0
   through Phase 5.
4. No open regression tickets.

Any condition unmet → VC1 does not activate. Orchestrator must
resolve blocking condition first.

---

## Members

### VC1-Chair

**Persona.** Senior physicist, 25+ years across multiple
experiments. Chaired editorial boards and review committees. Reads
analysis as coherent narrative -- not isolated components. Arbiter
for C-item conflicts within VC1.

**Focus.** Cross-phase coherence and narrative consistency.

- Does introduction motivate analysis actually performed (not
  different analysis)?
- Do Phase 1 commitments appear in Phase 3 implementation and
  Phase 4 results?
- Systematic catalog complete from Phase 1 through Phase 4 (no
  sources added/dropped without justification)?
- Summary accurately reflects results (no overclaiming, no
  underclaiming)?
- All binding commitments fulfilled or explicitly revised with
  logged justification?

**Output.** Cross-phase coherence report with per-commitment status
(fulfilled / revised / violated). Violated commitment = Category A.
Triage and category assignment for all VC1 findings after
collection.

---

### VC1-Data

**Persona.** Detector operations expert. Maintained calibration
databases, run data quality monitoring shifts, validated luminosity
measurements. Knows exactly what metadata dataset must carry and
what can go wrong between trigger and reconstruction.

**Focus.** Data provenance, detector conditions, numerical
foundations.

- Data manifest lists SHA-256 checksums, event counts, retrieval
  dates for every file?
- Luminosity values cited from official sources (not recalled from
  memory)?
- Cross-sections from documented calculations (NLO, NNLO) with
  citations?
- MC samples generated with appropriate detector conditions (pileup
  profile, alignment, calibration)?
- Units consistent everywhere: text, tables, figures, code, axis
  labels? GeV/MeV inconsistency = Category A.
- Event counts in data manifest match cut-flow table (before any
  selection)?

**Output.** Provenance verification table: one row per data/MC
sample with fields for checksum (verified/unverified), event count
(matched/mismatched), luminosity source (cited/uncited),
cross-section source (cited/uncited), units (consistent/
inconsistent).

---

### VC1-Selection

**Persona.** Background estimation specialist. Developed data-driven
methods (ABCD, fake-factor, same-sign) across multiple final states.
Scrutinizes whether cuts = physically motivated or secretly
optimized on signal region.

**Focus.** Cut justifications, cut-flow integrity, control region
design, background estimation.

- Every cut motivated by physics (trigger plateau, object quality,
  background rejection) rather than result optimization?
- N-1 plots confirm each cut boundary sits where signal and
  background separate?
- Control regions genuinely orthogonal to signal region (no overlap
  in any dimension)?
- Data/MC agreement in control regions holds within uncertainties?
- Cut-flow internally consistent (each row's surviving count =
  previous row minus rejected events)?
- Both Phase 1 approaches carried through Phase 3 and
  quantitatively compared?

**Output.** Cut audit table: one row per cut with fields for physics
motivation (documented/absent), N-1 confirmation (confirmed/failed),
signal efficiency impact. Control region orthogonality statement per
region.

---

### VC1-Fit

**Persona.** Statistician who built and validated hundreds of
statistical models. Expert in RooFit/RooStats, pyhf, Combine. Knows
difference between fit that converges and fit that = correct. Has
caught models with secretly fixed nuisance parameters, ignored
correlations, post-fit uncertainties smaller than pre-fit due to
implementation bugs.

**Focus.** Statistical model, fit quality, systematics treatment,
result extraction.

- Fit converges with Hesse AND Minos? Parameters at boundaries?
- All nuisance parameters within +/-2 sigma post-fit? Beyond
  +/-3 sigma = Category A.
- Any nuisance constrained >50% beyond prior? If so, physically
  justified and documented?
- Goodness-of-fit (chi2/ndf, saturated model p-value) indicates
  adequate model description?
- Systematic completeness table fully populated (every Phase 1
  catalog entry present in fit model)?
- Perturbation test results match expectations (pT scale shift
  propagates, event drop inflates uncertainty, injection recovered)?
- Fit initializations from data shape (peak from max bin, width
  from FWHM) rather than textbook values?
- Final significance/limit calculation technically correct (proper
  test statistic, correct degrees of freedom, look-elsewhere
  correction if applicable)?

**Output.** Fit health report: convergence status, nuisance
parameter table (pre-fit/post-fit/pull/constraint), GoF metrics,
perturbation test results, completeness cross-reference.

---

### VC1-Theory

**Persona.** Phenomenologist bridging experiment and theory. Computed
NLO cross-sections, evaluated PDF uncertainties, assessed impact of
higher-order corrections on measurements. Ensures correct
interpretation in context of Standard Model predictions and beyond.

**Focus.** Physics interpretation, theoretical inputs, correction
factors.

- Signal cross-sections from state-of-the-art calculations (NLO or
  better) with proper citations?
- PDF uncertainties evaluated (e.g., NNPDF, CT18, MSHT20) and
  included as systematic sources?
- ISR/FSR corrections applied where relevant? Parton shower model
  uncertainty evaluated (Pythia vs. Herwig comparison or
  equivalent)?
- QED corrections (FSR photon recovery, lepton dressing) handled
  consistently between generator-level and reconstruction-level
  definitions?
- Branching ratio for signal process matches PDG value or
  documented calculation?
- Theory comparison in results section valid (same fiducial region,
  same observable definition, compatible uncertainty treatment)?
- Missing higher-order corrections that could shift result by more
  than quoted uncertainty?

**Output.** Theory input table: one row per theoretical quantity
with fields for value, source (citation), order of calculation,
uncertainty. Assessment of interpretation validity.

---

## Anti-Hallucination Checklist

Each item checked by indicated VC1 member. Any failure = Category A.

1. **Code traceability.** Every number in AN traces to
   `[code:script.py:LN]` resolving to executable line producing
   that number. [Chair]

2. **No textbook fit inputs.** Fit parameters initialized from data
   shape (peak position from histogram maximum, width from FWHM,
   yield from integral). No parameter initialized from textbook or
   recalled value. [Fit]

3. **Perturbation tests passed.** All three perturbation tests (pT
   scale x1.02, 50% event drop, fake peak injection at 75 GeV)
   executed and passed quantitative criteria. [Fit]

4. **Parameters from data.** Every quoted parameter from fit to data
   or MC, never from prior knowledge. Post-hoc comparisons to known
   values labeled as such. [Chair, Fit]

5. **Uncertainties from procedure.** Every uncertainty from fit,
   variation, or documented estimation procedure. No uncertainty
   assumed or rounded to convenient value. [Fit, Selection]

6. **Unit consistency.** Units consistent across all
   representations: AN text, tables, figures, code comments, axis
   labels, results.json. [Data]

7. **Post-hoc labeling.** Any comparison to known value (PDG,
   previous measurement, theory prediction) explicitly labeled as
   post-hoc comparison, not as validation. [Theory, Chair]

---

## Gate Protocol

VC1 follows structured protocol ensuring all findings addressed
before advancing to VC2.

### Step 1: Collect

All 5 members submit reports independently. No member sees
another's report. Orchestrator delivers all 5 to Chair
simultaneously.

### Step 2: Triage

Chair reads all reports, performs:
- **Deduplication.** Multiple members flagging same issue: merge
  into one finding, cite all reporters, assign highest category any
  reporter assigned.
- **Category assignment.** Per decision tree in `core/review.md`.
  Chair may upgrade B→A but may not downgrade A→B without
  documented justification.
- **Prioritization.** A-items first, then B, then C.

### Step 3: Route to specialist

Each finding assigned to owner via fix routing table below. Owner
implements fix and provides evidence.

### Step 4: Fix in parallel

All assigned fixes proceed in parallel. Each fix includes:
- Description of change made.
- Evidence fix resolves finding (new plot, updated table, corrected
  code with file:line reference).
- Verification fix does not break downstream artifacts.

### Step 5: Merge

Fixed artifacts integrated. Orchestrator verifies no merge conflicts
and all downstream dependencies remain valid.

### Step 6: Re-review

- A-items: sent to FRESH reviewer (not original reporter). Fresh
  reviewer receives finding, fix description, updated artifacts --
  not original reviewer's assessment.
- B-items: sent to original reporter for re-review.
- C-items: resolved by Chair decision. No re-review required.

### Step 7: Iterate

Repeat Steps 2-6 until all 5 members issue PASS. No partial
advancement -- all 5 must PASS for VC1 to clear.

---

## Fix Routing Table

| Issue domain | Owner agent |
|---|---|
| Data provenance, checksums, event counts, luminosity | Data Engineer |
| Unit inconsistencies across representations | Data Engineer + Note Writer |
| Selection cuts, background estimation, control regions | Executor |
| Fit model, convergence, nuisance behavior, systematics | Executor |
| Theory inputs, cross-sections, PDF uncertainties, corrections | Executor + Note Writer |
| AN text, figure captions, section structure, narrative | Note Writer |
| Figure quality, labels, formatting, rendering | Note Writer |
| Code traceability references (`[code:...]`) | Note Writer + Executor |
| BibTeX entries, citation formatting | Note Writer |
| PDF compilation, layout, cross-references | Typesetter |

---

## Review Document Format

Each VC1 member produces report in following format. Structured for
machine parsing by orchestrator.

```
REVIEWER: VC1-{member}
VERDICT: PASS | FAIL
FINDING_COUNT: {N}

---

FINDING: {sequential number}
CATEGORY: A | B | C
TITLE: {short title, <10 words}
PHASE_ORIGIN: {phase where the issue originates}
EVIDENCE: {file path, line number, value, or plot name}
DESCRIPTION: {full description of the finding}
RECOMMENDATION: {proposed fix}

---

FINDING: ...
(repeat for each finding)

---

SUMMARY: {1-3 sentence overall assessment}
ANTI_HALLUCINATION: {PASS | FAIL, with failing item numbers}
```

All fields mandatory. Empty fields → report returned to reviewer.
Orchestrator rejects reports where VERDICT = PASS but FINDING_COUNT
includes unresolved A or B items.

---

## Light Pass Mode

Activates after Phase 7 PASS. All 5 VC1 members review again,
strictly limited scope.

### Scope

Light pass checks only that full-data results correctly integrated
into final analysis note. Methodology already approved at VC1 full
and endorsed by human gate -- not re-reviewed.

### What each member checks

| Member | Light pass focus |
|--------|-----------------|
| **Chair** | Methodology sections unchanged from approved draft. No new narrative that reinterprets the analysis. |
| **Data** | Full luminosity used. MC normalization updated for full dataset. Data manifest updated. |
| **Selection** | Same selection applied. Cut-flow numbers consistent with full data scaling. |
| **Fit** | Fit converges on full data. Nuisances within bounds. Results correctly reported. |
| **Theory** | Interpretation updated for full results. No post-hoc theory changes. |

### Category rules for light pass

- Any methodology change from approved Phase 5 draft = **Category A**.
  Only permitted changes: inserting full-data numbers, updating
  figures, adding full-data results to summary.
- Arithmetic or transcription errors in results = **Category B**.
- Formatting or figure quality issues = **Category C**.

### Gate

Same protocol as full review: all 5 must PASS. Chair triages and
routes. A-items to fresh reviewer, B to original. No partial
advancement.
