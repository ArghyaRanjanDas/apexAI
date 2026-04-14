# VC2 -- Publication Committee

## Overview

Publication Committee = final gate before analysis declared
complete. Where VC1 evaluates analysis as coherent whole, VC2
attacks it. Five independent reviewers attempt to break analysis
through reproduction, adversarial perturbation, independent
reanalysis, bias auditing, and external-referee scrutiny. Unanimous
PASS required -- no arbiter can overrule single VC2 FAIL verdict.

VC2 activates after VC1 PASS. Defining feature = strict isolation:
VC2 reviewers have no knowledge of VC1 findings, no access to
analysis process history, and in some cases deliberately restricted
access to analysis products.

---

## Activation

VC2 begins when ALL true:

1. VC1 verdict = PASS (all 5 members).
2. All VC1 fixes merged, no regression tickets open.
3. Final AN PDF compiled with all VC1-mandated changes.
4. Code repository in clean, tagged state.

---

## Independence Requirements

Four absolute rules. Violation of any → entire VC2 review
invalidated, must restart from scratch with new reviewers.

### Rule 1: No VC1 access

VC2 reviewers see NONE of: VC1 findings, VC1 discussion, VC1 member
identities, VC1 fix descriptions, VC1 iteration history.
Orchestrator must ensure complete information separation.

### Rule 2: No shared context

VC2 receives AN (PDF + source), code repository, data files. VC2
does NOT receive: experiment log, orchestrator reasoning, inter-agent
messages, phase CLAUDE.md files, binding commitment lists, or any
process artifact.

### Rule 3: CrossAnalyst gets raw data only

VC2-CrossAnalyst receives ONLY raw data files and one-sentence
physics question (e.g., "Measure Z boson mass in dimuon channel" or
"Search for HH -> bbtautau in scouting data"). No AN, no code, no
results, no cut values, no systematic list. Must produce independent
analysis from scratch.

### Rule 4: Blind sequence

VC2-Blind evaluates in strict sequence: selection methodology first,
then systematic treatment, then fit methodology, ONLY THEN sees fit
result and final numbers. Orchestrator enforces by providing
materials in stages. Blind reviewer's methodology assessment
recorded before result revealed → prevents retroactive
rationalization.

---

## Members

### VC2-Reproduce

**Persona.** Build engineer and reproducibility specialist. Set up
CI/CD pipelines for analysis preservation. "It works on my machine"
= Category A. Code must run in clean environment and produce
identical results, or analysis = not reproducible.

**Focus.** Exact reproduction of every number in AN from provided
code and data.

**Protocol.**

1. Set up clean environment (fresh pixi install, no cached state,
   no pre-existing outputs).
2. Execute every script referenced in AN in workflow order.
3. Capture all numerical outputs: yields, efficiencies, fit
   parameters, systematic effects, final results.
4. Compare each output against corresponding AN value. Relative
   difference threshold: 1e-6 for exact quantities (event counts,
   fit parameter values), 1e-3 for derived quantities (efficiencies,
   uncertainties) where floating-point ordering may differ.
5. Verify every figure: re-generated must be visually identical to
   AN figures (pixel-level diff, allowing minor rendering
   differences from different backends).
6. Verify results.json matches AN text for all quoted numbers.

**PASS criterion.** Every number reproduces within threshold. Every
figure reproduces. Every script executes without error.

**FAIL triggers.**
- Script fails to execute = Category A.
- Numerical discrepancy beyond threshold = Category A.
- Figure discrepancy (different data, not just rendering) =
  Category A.
- Missing script (referenced in AN but not in repository) =
  Category A.
- Undocumented dependencies (script requires files not in
  repository or data manifest) = Category B.

---

### VC2-Adversarial

**Persona.** Red-team specialist who has broken analyses passing all
other review stages. Designs attacks targeting known failure modes:
sensitivity to noise, label dependence, signal assumption, momentum
calibration, classifier memorization, signal injection recovery.
Does not accept "analysis is robust" without quantitative adversarial
evidence.

**Focus.** Six targeted attacks, each with explicit PASS/FAIL
criteria.

**Protocol.** Execute all six attacks. Each modifies inputs or
configuration, reruns analysis chain, compares result to unperturbed
baseline. Record all numerical results.

---

#### Adversarial Attack Suite

**Attack 1: Noise injection**

Add Gaussian noise to all continuous input variables with sigma =
0.1x detector resolution per variable (resolution from AN or RMS of
residual distribution). Rerun full chain.

- Expected: result shifts slightly, remains within statistical
  uncertainty.
- PASS: Result shift < 0.5 sigma (total uncertainty from
  unperturbed analysis).
- FAIL: Shift >= 0.5 sigma → analysis sensitive to sub-resolution
  noise, suggesting overfitting or insufficient smoothing.

**Attack 2: Label swap**

Swap signal/background labels in training data. Retrain MVA
classifier. Evaluate on original (unswapped) test data.

- Expected: classifier loses all discriminating power.
- PASS: AUC drops to 0.50 +/- 0.02 (consistent with random
  guessing). Score distributions overlap completely.
- FAIL: AUC > 0.55 → classifier learned features correlated with
  label assignment mechanism rather than physics, or training
  sample has label leakage.

**Attack 3: Peak removal**

Mask events in signal mass window (per AN). Fit sideband regions
with background model, extrapolate into masked window.

- Expected: background model extrapolates smoothly. Residuals in
  masked window consistent with statistical fluctuation.
- PASS: Masked window residuals chi2/ndf < 2, no bin deviates >3
  sigma from extrapolation.
- FAIL: Residuals show structure (chi2/ndf >= 2) or any bin >3
  sigma → background model misspecified or signal window leaks
  into sideband fit.

**Attack 4: Momentum scale shift**

Shift all momenta by +1% (multiply all pT, px, py, pz by 1.01).
Rerun full chain. Do NOT refit -- use original fit configuration.

- Expected: invariant mass peaks shift ~1%. Other quantities shift
  proportionally.
- PASS: Mass peak shift 0.8-1.2% (allowing non-linear effects from
  cuts/acceptances). Final result shift consistent with quoted
  momentum scale systematic.
- FAIL: Peak shift outside 0.5-2.0% range, OR result shift exceeds
  quoted systematic by >2x → incorrect momentum propagation or
  underestimated systematic.

**Attack 5: Memorization test**

Randomly permute event labels (signal/background) keeping all
kinematics unchanged. Retrain MVA on permuted labels.

- Expected: classifier cannot learn (labels carry no kinematic
  information).
- PASS: AUC drops to 0.50 +/- 0.02. No quoted number matches PDG
  value to >4 significant figures (matching >4 sig figs suggests
  recalled rather than measured).
- FAIL: AUC > 0.55 (memorized individual events rather than
  learning physics), OR result matches PDG to >4 sig figs without
  explicit justification (possible hallucination).

**Attack 6: Signal injection at alternate mass**

Inject fake signal with known cross-section at 75 GeV (or mass
point well separated from actual signal if 75 GeV falls within
signal region). Injected strength = 5 sigma expected significance.

- Expected: analysis detects and correctly measures injected signal.
- PASS: Recovered mass within 2 sigma of 75 GeV. Recovered strength
  within 2 sigma of injected. Original signal result unchanged (if
  injection at different mass point).
- FAIL: Injected signal not detected, or recovered mass/strength
  outside 2 sigma, or original result shifts (cross-contamination).

---

### VC2-CrossAnalyst

**Persona.** Independent analyst, never seen this analysis before.
Receives only raw data and physics question. Designs own selection,
background estimation, signal extraction from first principles. Most
demanding check in entire framework: if two independent analyses of
same data disagree, at least one = wrong.

**Focus.** Independent reanalysis with different methodology.

**Protocol.**

1. Receive raw data files and one-sentence physics question. Nothing
   else.
2. Design independent event selection (different cuts, working
   points, optimization strategy).
3. Estimate backgrounds using different method than primary (e.g.,
   primary uses ABCD → CrossAnalyst uses template fit from control
   regions, or vice versa).
4. Choose different binning for discriminant distribution.
5. Extract result using independent setup.
6. Compare with primary analysis result.

**Agreement criterion.** Two results must agree within combined
uncertainty (quadrature sum). Formally:

```
pull = |result_primary - result_cross| / sqrt(sigma_primary^2 + sigma_cross^2)
```

must be below 2.0.

**PASS criterion.** Pull < 2.0 for primary result (cross-section,
signal strength, mass, or limit).

**FAIL triggers.**
- Pull >= 2.0 = Category A. Two analyses statistically incompatible.
  Root cause investigation required before primary can proceed.
- CrossAnalyst unable to produce result (data insufficient, physics
  question ambiguous) → escalate to orchestrator. Not FAIL of
  primary, but VC2 cannot PASS without this check completing.

---

### VC2-Blind

**Persona.** Experimental psychologist turned physicist specializing
in cognitive biases in data analysis. Studied how analysts
unconsciously steer results toward expected values, how cut
optimization disguises as physics motivation, how systematic
uncertainties get cherry-picked for "reasonable" total errors.
Evaluates methodology before seeing results → prevents own bias.

**Focus.** Six bias checks, evaluated in strict sequence.

**Protocol.** Materials provided in stages by orchestrator.

- Stage 1: Selection methodology (cuts, regions, N-1 plots).
  Evaluate checks 1-2.
- Stage 2: Systematic treatment (catalog, variations, effects).
  Evaluate checks 3-5.
- Stage 3: Fit methodology (model, initialization, convergence
  criteria). Evaluate check 6 partially.
- Stage 4: Results (fit output, final numbers, interpretation).
  Complete check 6. Write final report.

Methodology assessment (Stages 1-3) recorded and sealed before
Stage 4 materials provided.

---

#### Bias Checks

**Check 1: Post-data cut optimization**

Were any cuts defined/adjusted after looking at signal region data?
Evidence: cuts absent from Phase 1 strategy, cut values changed
between Phase 3 and Phase 4, or N-1 plots where cut boundary
coincidentally maximizes apparent signal.

- PASS: All cuts traceable to Phase 1, values stable across phases,
  N-1 boundaries at physics-motivated positions.
- FAIL: Any cut appears optimized on signal region data.

**Check 2: Fit range tuning**

Was fit range chosen to produce specific result? Evidence: range
excluding regions where model describes data poorly, range changed
after seeing fit quality, or result sensitivity to range variations
exceeding quoted systematic.

- PASS: Fit range motivated by physics (kinematic boundaries,
  trigger turn-on), stable across phases, result robust to +/-10%
  range variations.
- FAIL: Range appears chosen to avoid data/model disagreement, or
  result unstable under range variation.

**Check 3: Look-elsewhere effect**

If analysis reports local significance, has look-elsewhere effect
been evaluated? For searches: trials factor from mass range scanning
must be accounted for. For measurements: not applicable unless
multiple observables examined and most significant reported.

- PASS: Look-elsewhere correction applied where required, or
  explicitly stated as not applicable with justification.
- FAIL: Local significance reported without look-elsewhere
  correction in scanning search.

**Check 4: PDG value contamination**

Does result suspiciously match PDG value? If measured quantity has
PDG entry, compare: agreement better than analysis precision
(pull < 0.1) in analysis with >5% total uncertainty suggests result
may have been steered toward known value.

- PASS: Result consistent with but not suspiciously close to PDG
  value, OR precision sufficient to explain close agreement, OR
  measured quantity has no PDG entry.
- FAIL: Result matches PDG to better than 10% of quoted uncertainty
  without physics explanation for exceptional agreement.

**Check 5: Systematic cherry-picking**

Included systematics = representative sample, or inconvenient
sources excluded? Evidence: sources in Phase 1 catalog but absent
from final fit, variations evaluated but not included (justification
amounting to "effect was small"), asymmetric systematics where only
smaller variation quoted.

- PASS: All Phase 1 catalog entries present. All evaluated
  variations included or excluded with documented, quantitative
  justification reviewed by VC1.
- FAIL: Any systematic dropped without adequate justification, or
  asymmetric treatment biased toward smaller effects.

**Check 6: Result steering**

Does analysis show patterns consistent with unconscious result
steering? Indicators: multiple methodological choices each shifting
result same direction, post-fit adjustments improving agreement with
expectation, robustness checks added after seeing result, "unplanned"
cross-checks that happen to confirm result.

- PASS: Methodological choices pre-committed (traceable to Phase 1),
  robustness checks pre-defined, cross-checks = secondary approach
  from Phase 1.
- FAIL: Pattern of choices consistently favoring particular result,
  or evidence methodology adjusted after unblinding.

---

### VC2-Referee

**Persona.** External journal referee evaluating for top-tier
journal (PRL, JHEP, EPJC). Refereed hundreds of papers, knows what
editors and readers expect: clarity, completeness, novelty, justified
precision. Reads AN as submission draft.

**Focus.** Publication readiness from external perspective.

**Protocol.**

1. Read AN as referee assignment.
2. Evaluate against journal standards:
   - **Clarity.** Can non-specialist in this subfield follow analysis
     from introduction to conclusion?
   - **Completeness.** All necessary details present for reproduction
     (without reading code)?
   - **Novelty.** What does analysis add beyond existing
     measurements? Contribution clearly stated?
   - **Comparison.** Results compared to existing measurements and
     theory predictions? Discrepancies discussed?
   - **Precision justification.** Quoted precision consistent with
     dataset size, selection efficiency, systematic treatment?
     Implausibly small uncertainties = Category A.
3. Write referee report in standard format (general comments,
   specific comments, recommendation).

**PASS criterion.** Report recommends publication (possibly with
minor revisions classified as Category B or C).

**FAIL triggers.**
- Major revision or rejection recommendation = Category A.
- Missing comparison to prior measurements = Category B.
- Unclear methodology preventing reader understanding = Category B.
- Implausibly precise result = Category A.

---

## Response Document Format

All VC2 findings compiled into response document appended to AN as
appendix. Part of permanent record.

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
fields populated. RESPONSE and ACTION fields filled after initial
criticism, during fix cycle. Document grows as issues identified and
resolved.

Unanimous PASS required. Single FAIL from any VC2 member blocks
analysis from completion. No arbiter override -- failing member's
concerns must be addressed to that member's satisfaction.

---

## Light Pass Mode

Activates after VC1 light PASS. Same 5 VC2 members, limited scope.
Methodology already endorsed by VC2 full and human gate -- not
re-reviewed.

### What each member does

| Member | Light pass procedure |
|--------|---------------------|
| **Reproduce** | Re-execute all Phase 6 and Phase 7 scripts in clean environment. Diff outputs against final AN. Discrepancy (rel. diff > 1e-6) = Category A. |
| **Adversarial** | Re-run all 6 attacks on full data (same pass criteria as full review). Any attack that passed on 10% but fails on full data = Category A. |
| **CrossAnalyst** | Verify independent analysis result compatible with full-data result within combined uncertainties. No new independent analysis required -- update existing with full data. |
| **Blind** | Check no post-hoc result steering occurred between Phase 5 and Phase 7. Methodology sections must be identical to human-approved draft. Any change = Category A. |
| **Referee** | Confirm final AN meets journal standards with full results. All figures updated. Summary and conclusions reflect full data. |

### Independence rules

Same as full review: no VC1 light findings visible to VC2 light.
No process context. CrossAnalyst works from data + physics question
only.

### Gate

Unanimous PASS required. No arbiter override. Same response document
format as full review.
