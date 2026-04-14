# VC2 -- Publication Committee

## Overview

The Publication Committee is the final gate before an analysis is
declared complete. Where VC1 evaluates the analysis as a coherent
whole, VC2 attacks it. Five independent reviewers attempt to break
the analysis through reproduction, adversarial perturbation,
independent reanalysis, bias auditing, and external-referee
scrutiny. Unanimous PASS is required -- no arbiter can overrule a
single VC2 FAIL verdict.

VC2 activates after VC1 PASS. Its defining feature is strict
isolation: VC2 reviewers have no knowledge of VC1 findings, no
access to the analysis process history, and in some cases
deliberately restricted access to the analysis products themselves.

---

## Activation

VC2 begins when ALL of the following are true:

1. VC1 verdict is PASS (all 5 members).
2. All VC1 fixes are merged and no regression tickets are open.
3. The final AN PDF is compiled with all VC1-mandated changes.
4. The code repository is in a clean, tagged state.

---

## Independence Requirements

These four rules are absolute. Violation of any rule invalidates
the entire VC2 review, which must restart from scratch with new
reviewers.

### Rule 1: No VC1 access

VC2 reviewers see NONE of the following: VC1 findings, VC1
discussion, VC1 member identities, VC1 fix descriptions, or VC1
iteration history. The orchestrator must ensure complete
information separation.

### Rule 2: No shared context

VC2 receives the AN (PDF + source), the code repository, and the
data files. VC2 does NOT receive: the experiment log, orchestrator
reasoning, inter-agent messages, phase CLAUDE.md files, binding
commitment lists, or any artifact of the analysis process.

### Rule 3: CrossAnalyst gets raw data only

VC2-CrossAnalyst receives ONLY the raw data files and a one-
sentence physics question (e.g., "Measure the Z boson mass in the
dimuon channel" or "Search for HH -> bbtautau in scouting data").
No AN, no code, no results, no cut values, no systematic list.
The CrossAnalyst must produce an independent analysis from scratch.

### Rule 4: Blind sequence

VC2-Blind evaluates the analysis in a strict sequence: selection
methodology first, then systematic treatment, then fit methodology,
and ONLY THEN sees the fit result and final numbers. The
orchestrator enforces this by providing materials in stages. The
Blind reviewer's assessment of methodology is recorded before the
result is revealed, preventing retroactive rationalization.

---

## Members

### VC2-Reproduce

**Persona.** Build engineer and reproducibility specialist. Has
set up CI/CD pipelines for analysis preservation. Treats "it works
on my machine" as a Category A finding. If the code does not run
in a clean environment and produce identical results, the analysis
is not reproducible.

**Focus.** Exact reproduction of every number in the AN from the
provided code and data.

**Protocol.**

1. Set up a clean environment (fresh pixi install, no cached
   state, no pre-existing outputs).
2. Execute every script referenced in the AN in the order implied
   by the analysis workflow.
3. Capture all numerical outputs: yields, efficiencies, fit
   parameters, systematic effects, final results.
4. Compare each output against the corresponding value in the AN.
   Relative difference threshold: 1e-6 for exact quantities
   (event counts, fit parameter values), 1e-3 for derived
   quantities (efficiencies, uncertainties) where floating-point
   ordering may differ.
5. Verify every figure: re-generated figures must be visually
   identical to AN figures (pixel-level diff, allowing for
   minor rendering differences from different backends).
6. Verify results.json matches AN text for all quoted numbers.

**PASS criterion.** Every number reproduces within threshold.
Every figure reproduces. Every script executes without error.

**FAIL triggers.**
- Any script fails to execute: Category A.
- Any numerical discrepancy beyond threshold: Category A.
- Any figure discrepancy (different data, not just rendering):
  Category A.
- Missing script (referenced in AN but not in repository):
  Category A.
- Undocumented dependencies (script requires files not in the
  repository or data manifest): Category B.

---

### VC2-Adversarial

**Persona.** Red-team specialist who has broken analyses that
passed all other review stages. Designs specific attacks targeting
known failure modes: sensitivity to noise, label dependence,
signal assumption, momentum calibration, classifier memorization,
and signal injection recovery. Does not accept "the analysis is
robust" without quantitative evidence from adversarial testing.

**Focus.** Six targeted attacks, each with explicit PASS/FAIL
criteria.

**Protocol.** Execute all six attacks below. Each attack modifies
inputs or configuration, reruns the analysis chain, and compares
the result to the unperturbed baseline. Record all numerical
results.

---

#### Adversarial Attack Suite

**Attack 1: Noise injection**

Add Gaussian noise to all continuous input variables with
sigma = 0.1 times the detector resolution for each variable
(resolution from the AN or from the RMS of the residual
distribution). Rerun the full analysis chain.

- Expected outcome: Result shifts slightly but remains within
  statistical uncertainty.
- PASS: Result shift < 0.5 sigma (where sigma is the total
  uncertainty from the unperturbed analysis).
- FAIL: Result shift >= 0.5 sigma. Indicates the analysis is
  sensitive to noise below detector resolution, suggesting
  overfitting or insufficient smoothing.

**Attack 2: Label swap**

Swap signal and background labels in the training data. Retrain
any MVA classifier. Evaluate on the original (unswapped) test
data.

- Expected outcome: Classifier loses all discriminating power.
- PASS: AUC drops to 0.50 +/- 0.02 (consistent with random
  guessing). Score distributions for signal and background
  overlap completely.
- FAIL: AUC remains above 0.55. Indicates the classifier
  learned features correlated with the label assignment
  mechanism rather than with physics, or that the training
  sample has label leakage.

**Attack 3: Peak removal**

Mask events in the signal mass window (as defined in the AN).
Fit the sideband regions with the background model and
extrapolate into the masked window.

- Expected outcome: Background model extrapolates smoothly
  through the signal region. Residuals in the masked window
  are consistent with statistical fluctuation.
- PASS: Residuals in the masked window have chi2/ndf < 2 and
  no bin deviates by more than 3 sigma from the extrapolation.
- FAIL: Residuals show structure (chi2/ndf >= 2) or any bin
  deviates by more than 3 sigma. Indicates the background model
  is misspecified or the signal window definition leaks into
  the sideband fit.

**Attack 4: Momentum scale shift**

Shift all momenta by +1% (multiply all pT, px, py, pz by
1.01). Rerun the full analysis chain. Do NOT refit -- use the
original fit configuration.

- Expected outcome: Invariant mass peaks shift by approximately
  1%. All other quantities shift proportionally.
- PASS: Mass peak position shifts by 0.8-1.2% (allowing for
  non-linear effects from cuts and acceptances). Final result
  shifts in a direction and magnitude consistent with the
  momentum scale systematic already quoted.
- FAIL: Mass peak shift outside 0.5-2.0% range, OR final result
  shift exceeds the quoted momentum scale systematic by more
  than a factor of 2. Indicates incorrect momentum propagation
  or an underestimated systematic.

**Attack 5: Memorization test**

Randomly permute event labels (signal/background assignment)
while keeping all kinematic variables unchanged. Retrain the
MVA classifier on the permuted labels.

- Expected outcome: Classifier cannot learn because labels
  carry no information about kinematics.
- PASS: AUC drops to 0.50 +/- 0.02. No quoted number in the
  analysis matches a PDG value to more than 4 significant
  figures (matching to >4 sig figs suggests the number was
  recalled rather than measured).
- FAIL: AUC above 0.55 (classifier memorized individual events
  rather than learning physics patterns), OR any result matches
  PDG to >4 significant figures without explicit justification
  (possible hallucination of a known value).

**Attack 6: Signal injection at alternate mass**

Inject a fake signal with known cross-section at 75 GeV (or at
a mass point well separated from the actual signal, if 75 GeV
falls within the signal region). The injected signal should have
strength corresponding to 5 sigma expected significance.

- Expected outcome: The analysis detects and correctly measures
  the injected signal.
- PASS: Recovered signal mass within 2 sigma of 75 GeV.
  Recovered signal strength within 2 sigma of injected strength.
  Original signal result unchanged (if the injection is at a
  different mass point).
- FAIL: Injected signal not detected, or recovered mass/strength
  outside 2 sigma, or the original signal result shifts (cross-
  contamination between signal hypotheses).

---

### VC2-CrossAnalyst

**Persona.** Independent analyst who has never seen this analysis
before. Receives only raw data and a physics question. Designs
their own selection, background estimation, and signal extraction
from first principles. The most demanding check in the entire
framework: if two independent analyses of the same data disagree,
at least one is wrong.

**Focus.** Independent reanalysis with different methodology.

**Protocol.**

1. Receive raw data files and a one-sentence physics question.
   Nothing else.
2. Design an independent event selection (different cuts, different
   working points, different optimization strategy).
3. Estimate backgrounds using a different method than the primary
   analysis (e.g., if the primary uses ABCD, the CrossAnalyst
   uses template fit from control regions, or vice versa).
4. Choose different binning for the discriminant distribution.
5. Extract the result using the independent setup.
6. Compare with the primary analysis result.

**Agreement criterion.** The two results must agree within the
combined uncertainty (quadrature sum of both analyses'
uncertainties). Formally: the pull

```
pull = |result_primary - result_cross| / sqrt(sigma_primary^2 + sigma_cross^2)
```

must be below 2.0.

**PASS criterion.** Pull < 2.0 for the primary result (cross-
section, signal strength, mass, or limit, as appropriate).

**FAIL triggers.**
- Pull >= 2.0: Category A. The two analyses are statistically
  incompatible. Root cause investigation required before the
  primary analysis can proceed.
- CrossAnalyst unable to produce a result (data insufficient,
  physics question ambiguous): escalate to orchestrator for
  clarification. Not a FAIL of the primary analysis, but VC2
  cannot PASS without this check completing.

---

### VC2-Blind

**Persona.** Experimental psychologist turned physicist who
specializes in cognitive biases in data analysis. Has studied
how analysts unconsciously steer results toward expected values,
how cut optimization can be disguised as physics motivation, and
how systematic uncertainties get cherry-picked to produce
"reasonable" total errors. Evaluates methodology before seeing
results to prevent their own bias.

**Focus.** Six specific bias checks, evaluated in a strict
sequence.

**Protocol.** Materials are provided in stages by the orchestrator.

- Stage 1: Selection methodology (cuts, regions, N-1 plots).
  Evaluate checks 1-2.
- Stage 2: Systematic treatment (catalog, variations, effects).
  Evaluate checks 3-5.
- Stage 3: Fit methodology (model, initialization, convergence
  criteria). Evaluate check 6 partially.
- Stage 4: Results (fit output, final numbers, interpretation).
  Complete check 6. Write final report.

Assessment of methodology (Stages 1-3) is recorded and sealed
before Stage 4 materials are provided.

---

#### Bias Checks

**Check 1: Post-data cut optimization**

Were any cuts defined or adjusted after looking at the data in
the signal region? Evidence of post-data optimization: cuts that
do not appear in Phase 1 strategy, cuts whose values changed
between Phase 3 and Phase 4, or N-1 plots where the cut boundary
coincidentally maximizes the apparent signal.

- PASS: All cuts traceable to Phase 1, values stable across
  phases, N-1 boundaries at physics-motivated positions.
- FAIL: Any cut appears to have been optimized on the signal
  region data.

**Check 2: Fit range tuning**

Was the fit range chosen to produce a specific result? Evidence:
fit range that excludes regions where the model describes data
poorly, fit range that changed after seeing fit quality in those
regions, or sensitivity of the result to fit range variations
exceeding the quoted systematic.

- PASS: Fit range motivated by physics (e.g., kinematic
  boundaries, trigger turn-on), stable across phases, result
  robust to +/-10% range variations.
- FAIL: Fit range appears chosen to avoid data/model
  disagreement, or result is unstable under range variation.

**Check 3: Look-elsewhere effect**

If the analysis reports a local significance, has the look-
elsewhere effect been evaluated? For searches: the trials factor
from scanning over the mass range must be accounted for. For
measurements: not applicable unless multiple observables were
examined and the most significant was reported.

- PASS: Look-elsewhere correction applied where required, or
  explicitly stated as not applicable with justification.
- FAIL: Local significance reported without look-elsewhere
  correction in a scanning search.

**Check 4: PDG value contamination**

Does the analysis result suspiciously match a PDG value? If the
measured quantity has a PDG entry, compare: agreement to better
than the analysis precision (pull < 0.1) in an analysis with
>5% total uncertainty suggests the result may have been steered
toward the known value.

- PASS: Result is consistent with but not suspiciously close to
  the PDG value, OR the analysis precision is sufficient to
  explain close agreement, OR the measured quantity has no PDG
  entry.
- FAIL: Result matches PDG to better than 10% of the quoted
  uncertainty without a physics explanation for the exceptional
  agreement.

**Check 5: Systematic cherry-picking**

Are the included systematics a representative sample, or were
inconvenient sources excluded? Evidence: systematic sources
present in the Phase 1 catalog but absent from the final fit,
systematic variations evaluated but not included (with a
justification that amounts to "the effect was small"), or
asymmetric systematics where only the smaller variation is
quoted.

- PASS: All Phase 1 catalog entries present. All evaluated
  variations included or excluded with documented, quantitative
  justification reviewed by VC1.
- FAIL: Any systematic dropped without adequate justification,
  or asymmetric treatment biased toward smaller effects.

**Check 6: Result steering**

Does the analysis show patterns consistent with unconscious
result steering? Indicators: multiple methodological choices
that each shift the result in the same direction, post-fit
adjustments that improve agreement with expectation, robustness
checks that were added after seeing the result, or "unplanned"
cross-checks that happen to confirm the result.

- PASS: Methodological choices are pre-committed (traceable to
  Phase 1), robustness checks are pre-defined, cross-checks
  are the secondary approach from Phase 1.
- FAIL: Pattern of choices consistently favoring a particular
  result, or evidence that methodology was adjusted after
  unblinding.

---

### VC2-Referee

**Persona.** External journal referee evaluating the analysis for
publication in a top-tier journal (PRL, JHEP, EPJC). Has refereed
hundreds of papers and knows what editors and readers expect:
clarity, completeness, novelty, and justified precision. Reads the
AN as a submission draft.

**Focus.** Publication readiness from an external perspective.

**Protocol.**

1. Read the AN as if receiving it as a referee assignment.
2. Evaluate against journal standards:
   - **Clarity.** Can a non-specialist in this exact subfield
     follow the analysis from introduction to conclusion?
   - **Completeness.** Are all necessary details present for
     reproduction (without reading the code)?
   - **Novelty.** What does this analysis add beyond existing
     measurements? Is the contribution clearly stated?
   - **Comparison.** Are results compared to existing
     measurements and theory predictions? Are discrepancies
     discussed?
   - **Precision justification.** Is the quoted precision
     consistent with the dataset size, selection efficiency,
     and systematic treatment? Implausibly small uncertainties
     are Category A.
3. Write a referee report in standard format (general comments,
   specific comments, recommendation).

**PASS criterion.** The referee report recommends publication
(possibly with minor revisions classified as Category B or C).

**FAIL triggers.**
- Major revision or rejection recommendation: Category A.
- Missing comparison to prior measurements: Category B.
- Unclear methodology that prevents reader understanding:
  Category B.
- Implausibly precise result: Category A.

---

## Response Document Format

All VC2 findings are compiled into a response document that is
appended to the AN as an appendix. This document is part of the
permanent record.

```
VC2 RESPONSE DOCUMENT
Analysis: {analysis title}
Date: {review date}
Verdict: {PASS | FAIL}

===

REVIEWER: VC2-{member}
VERDICT: {PASS | FAIL}

ISSUE: {sequential number}
TITLE: {short title, <10 words}
CATEGORY: A | B | C
CRITICISM: {full description with quantitative evidence}
RESPONSE: {agree | disagree (with justification) | clarify}
ACTION: {what was done, or why nothing is needed}
SCRIPT_LINE: {file:line reference for fix, or N/A}

---

ISSUE: ...
(repeat for each issue)

===

REVIEWER: VC2-{next member}
...

===

OVERALL:
  Reproduce: {PASS|FAIL}
  Adversarial: {PASS|FAIL} ({N}/6 attacks passed)
  CrossAnalyst: {PASS|FAIL} (pull = {value})
  Blind: {PASS|FAIL} ({N}/6 bias checks passed)
  Referee: {PASS|FAIL}

FINAL VERDICT: {PASS (unanimous) | FAIL}
```

No empty fields permitted. Every ISSUE entry must have all seven
fields populated. The RESPONSE and ACTION fields are filled after
the initial criticism, during the fix cycle. The document grows
as issues are identified and resolved.

Unanimous PASS required. A single FAIL from any VC2 member blocks
the analysis from completion. There is no arbiter override -- the
failing member's concerns must be addressed to that member's
satisfaction.
