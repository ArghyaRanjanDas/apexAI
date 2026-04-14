# Review Protocol

Every finding requires specific evidence -- a file path, line number,
value, or plot. "Looks reasonable" is not acceptable. Quality bar:
publication-ready, not merely good enough to continue.

---

## 1. Review Philosophy

**Evidence-based.** A finding without a cite (plot, chi2/ndf, bin,
line of code) is not a finding. Returned to reviewer for evidence.

**Traceable.** Every number traces to script:line. Correct number
with no provenance = Category B. Number from recalled knowledge = A.

**Adversarial.** Assume the executor may exhibit motivated reasoning.
Red flags: enormous uncertainties hiding a poor central value,
calibration assuming the answer, tautological validation (comparing
a fit to its own training data). Reviewers ask: "Is this narrative
self-serving?"

---

## 2. Finding Classification

| Cat | Meaning | Action |
|-----|---------|--------|
| **A** | Blocks advancement | Fix, re-review by FRESH reviewer. No downstream work until resolved. |
| **B** | Must fix before PASS | Fix, present to same reviewer. Reviewer may upgrade to A. |
| **C** | Style/preference | Arbiter (or VC1 Chair) decides. Never blocks advancement. |

**Escalation.** Reviewer may upgrade B to A. Only arbiter/Chair may
downgrade A, with documented justification.

**Dismissal.** Cannot dismiss as "out of scope" if fix < ~1 hour.
Multiple upstream-dependent findings batch into one regression ticket.

---

## 3. Review Tiers

| Tier | Panel | Arbiter | Phases |
|------|-------|---------|--------|
| Self | Executor + Plot Validator | No | 0, 2 |
| 1-bot | Critical + Plot Validator | No | 3, 6 |
| 4-bot | Physics + Critical + Constructive | Yes | 1 |
| 4-bot+bib | Above + Plot Validator + BibTeX | Yes | 4a, 4b |
| 5-bot | Above + Rendering | Yes | 5, 7 |
| VC1 full | Chair + Data + Selection + Fit + Theory | Chair | After Phase 5 |
| VC2 full | Reproduce + Adversarial + CrossAnalyst + Blind + Referee | None (unanimous) | After VC1 full |
| -- | **HUMAN GATE** (multiple humans) | -- | After VC2 full |
| VC1 light | Same 5 members | Chair | After Phase 7 |
| VC2 light | Same 5 members | None (unanimous) | After VC1 light |

**Arbiter behavior.** Reads all reports, resolves C-item conflicts,
issues verdict: PASS / ITERATE / REGRESS. Does not generate new
findings. If reviewers disagree on category for the same issue, the
arbiter assigns the final category with justification.

**Independence.** Reviewers write findings without seeing each
other's reports. Arbiter (or Chair) is the first to see the full set.

---

## 4. Per-Phase Review Focus

Findings outside scope are valid but filed as regression tickets
(Section 6) rather than blocking the current phase.

**Phase 0 (Self):** Files open in uproot. Provenance: portal, DOI,
SHA-256, event count. Tree matches experiment format.

**Phase 1 (4-bot):** Physics: analysis type, two genuinely different
approaches, systematic catalog completeness, reference analyses.
Critical: flagship figures defined, [A]/[L]/[D] labels, internal
consistency, catalog gaps. Constructive: improvements without plan
change. Arbiter: strategy is binding once approved.

**Phase 2 (Self + PV):** All branches plotted (linear + log-y, 100
bins, overflow). Summary CSV. Mass spectra (OS/SS). Peaks vs. mass
table. Variable ranking. MVA input check (chi2/ndf > 5 = flagged).
PV: axis labels, units, overflow bins.

**Phase 3 (1-bot):** Cut-flow for both approaches. N-1 plots confirm
boundaries. Control regions orthogonal. Closure (chi2/ndf < 3,
p > 0.05) and stress tests pass -- if not, remediation protocol
followed (3+ attempts). MVA diagnostics if applicable (KS p > 0.05,
ROC, importance). Systematics per catalog.

**Phase 4a (4-bot+bib):** Systematic completeness (missing = A). Fit
converges (Hesse + Minos, nuisances within +/-2 sigma, none
constrained > 50%). Formula audit. Perturbation tests. Fit init from
data shape. Citations resolve. PDG pull > 3 sigma = Category A.

**Phase 4b (4-bot+bib):** 10% subsample (fixed seed, pre-chosen).
Identical 4a config. Central value compatible within sqrt(10)-inflated
uncertainty. Unblinding checklist complete. Produces materials for
human gate.

**Phase 5 (5-bot):** AN per `standards/analysis_note.md`. Every
number traced to `[code:script.py:LN]`. Figures per
`standards/plotting.md`. PDF clean (margins, refs, captions, 50-100
pages). Rendering check. BibTeX check. Last automated review before
VC1.

**Phase 6 (1-bot):** Methodology frozen by human approval; review
checks execution only. Configuration identical to 4b. Post-fit
diagnostics on full data. Robustness checks (fit range, binning,
cuts, primary vs. secondary approach). Any anomaly > 2 sigma from
expected triggers automatic escalation to 4-bot. Anomalies documented
with quantitative comparison to 4b results.

**Phase 7 (5-bot):** Final AN updated with full observed results.
Figures replaced with full-data versions. Flagship figures finalized.
Same standards as Phase 5: every number traced, figures per plotting
standards, PDF clean. Rendering and BibTeX checks. Methodology
sections must be unchanged from Phase 5 draft -- any discrepancy is
Category A.

**VC1 light (ARC):** All 5 specialists review. Scope limited to
results integration: full-data numbers correctly inserted, figures
updated, methodology sections unchanged. Any methodology change from
the approved draft is Category A. No re-review of selection logic,
fit model, or systematics unless results raise new concerns.

**VC2 light (Pub):** Reproduce re-executes Phase 6-7 scripts in clean
environment, diffs outputs. Adversarial re-runs all 6 attacks on full
data. CrossAnalyst verifies independent analysis compatible with full
results. Blind checks no post-hoc result steering. Referee confirms
final AN meets journal standards. Unanimous PASS required.

---

## 5. Iteration and Escalation

| Tier | Warn | Strong warn | Hard cap |
|------|------|-------------|----------|
| 4/5-bot | 3 | 5 | 10 (potential Phase 1 regression) |
| 1-bot | 2 | 3 | Escalate to 4-bot |
| Self | -- | -- | Escalate to 1-bot |

**Warn:** log recurring issue. **Strong warn:** orchestrator evaluates
for deeper problem, may file regression ticket. **Hard cap:** tier
escalates; 4/5-bot cap triggers mandatory review of Phase 1 plan.

**Fresh reviewer rule.** A-item re-review uses a different reviewer.
Fresh reviewer gets: finding, fix description, artifacts -- but not
the original reviewer's assessment.

**Arbiter escalation.** Unresolvable disagreement escalates to
orchestrator, which may invoke consultation or regress.

---

## 6. Phase Regression

### Mandatory triggers

1. **Validation failure without remediation** -- test fails, < 3
   documented remediation attempts.
2. **Dominant systematic** -- single source > 80% of total budget.
3. **GoF inconsistency** -- toy studies inconsistent with observed
   GoF statistic.
4. **Excessive exclusion** -- > 50% bins excluded from fit.
5. **Tautological comparison** -- validation against the same data
   used to derive the result.

### Procedure

1. **Investigator traces** root cause to originating phase.
2. **REGRESSION_TICKET.md** written: triggering finding, root cause
   phase, affected phases, artifacts to regenerate, remediation plan.
3. **Fixer re-runs** target phase. Stale artifacts marked (not
   deleted).
4. **Downstream cascade.** All phases between target and current
   re-execute and re-review sequentially.
5. **Resume** normal review at the triggering phase.

### Scope

| Target | Invalidates | Approval |
|--------|-------------|----------|
| Phase 0 | Everything | Orchestrator |
| Phase 1 | All subsequent | Orchestrator |
| Phase 2 | Phases 3-5 + VCs | Automatic |
| Phase 3 | Phases 4-5 + VCs | Automatic |
| Within Phase 4 | Resets human gate | Automatic |
| Phase 5 | Documentation only | Automatic |
| Phase 6 | Phase 7 + VC light passes | Automatic (config frozen) |
| Phase 7 | VC light passes | Automatic (methodology frozen) |

---

## 7. Human Gate

After VC2 full PASS, before Phase 6. Single mandatory human
intervention. No automated bypass.

**Presented:** draft AN (VC-endorsed, all methodology final with 10%
results), unblinding checklist, 4a expected result, 4b validation
result + 4a comparison, all review findings/resolutions, VC1 and VC2
attestation reports, open B-items, perturbation results, control
region plots.

| Option | Effect |
|--------|--------|
| APPROVE | Phase 6 begins, methodology frozen |
| ITERATE | Fix within draft scope, re-review, re-present |
| REGRESS | Target phase specified, triggers Section 6 |
| PAUSE | Analysis halts until human resumes |

Decision logged. After APPROVE, any methodology change requires
returning through the gate.

---

## 8. VC1 -- Analysis Review Committee

Activates after Phase 5 PASS. Five parallel specialist reviewers.

### Members

| Reviewer | Focus |
|----------|-------|
| **Chair** | Cross-phase coherence, narrative consistency. Arbiter for C-items. |
| **Data** | Provenance, units, luminosity, MC samples, cross-section sources. |
| **Selection** | Cut motivation, cut-flow consistency, control region orthogonality, efficiencies. |
| **Fit** | Model choice, convergence, nuisance behavior, systematics, significance, GoF. |
| **Theory** | Predictions, corrections, PDFs, signal model, branching ratios, interpretation. |

### Relationship to phase reviewers

| VC1 | Phase equivalent | Difference |
|-----|-----------------|------------|
| Chair | Arbiter | Cross-phase vs. within-phase |
| Data | Plot Validator + BibTeX | Substance vs. format |
| Selection | Critical | Full chain vs. single phase |
| Fit | Physics | Complete stats vs. strategy |
| Theory | Physics | Theory correctness vs. feasibility |

### Gate protocol

1. **Collect** -- all 5 submit independently (no shared reports).
2. **Triage** -- Chair deduplicates, assigns A/B/C.
3. **Route** -- assign to owner via fix routing table.
4. **Fix in parallel** -- each fix includes: change, evidence,
   script:line.
5. **Re-review** -- A-items to fresh reviewer, B to original, C
   resolved by Chair.
6. **Iterate** until all 5 PASS (no partial advancement).

### Fix routing

| Issue | Owner |
|-------|-------|
| Data/units/luminosity | Data Engineer |
| Cuts/backgrounds/selection | Executor |
| Fit/statistics/systematics | Executor |
| Interpretation/theory | Executor + Note Writer |
| Documentation/figures | Note Writer |

### Anti-hallucination checklist

Each item failure = Category A.

- [ ] Every number traces to `[code:script.py:LN]` that resolves
- [ ] No textbook values as fit inputs (init from data shape)
- [ ] Perturbation tests passed (pT scale, event drop, fake injection)
- [ ] Parameters from fits to data, not prior knowledge
- [ ] Uncertainties from fit or documented procedure, not assumed
- [ ] Units consistent: text, tables, figures, code, axes
- [ ] Post-hoc comparisons labeled as such

---

## 9. VC2 -- Publication Committee

Activates after VC1 PASS. Five independent reviewers under strict
isolation. Unanimous PASS required -- no arbiter can overrule.

### Independence rules (absolute)

1. **No VC1 access.** VC2 sees no VC1 findings or discussion.
2. **No process context.** VC2 gets AN + code + data. No experiment
   log, no orchestrator reasoning, no inter-agent messages.
3. **CrossAnalyst: raw data path only.** No AN, no code, no results.
   Physics question only.
4. **Blind sequence.** Blind reviewer evaluates methodology before
   seeing the fit result.

### Members

| Reviewer | Procedure |
|----------|-----------|
| **Reproduce** | Re-execute all scripts, diff outputs vs. AN. Discrepancy (rel. diff > 1e-6) = A. Clean environment test. |
| **Adversarial** | Six red-team attacks (below). Any failure = A. |
| **CrossAnalyst** | Independent analysis from raw data + physics question. Different methods/cuts/binning. Disagreement beyond combined uncertainties = investigate. |
| **Blind** | Evaluate selection, then systematics, then fit method, then (only then) see result. Check circular reasoning, result steering, PDG contamination. |
| **Referee** | Journal-referee standards: clarity, completeness, novelty, comparison to existing measurements, justified precision. |

### Adversarial attacks

| # | Attack | PASS criterion |
|---|--------|----------------|
| 1 | **Noise** -- Gaussian (0.1 x resolution) on all inputs, rerun | Result shifts < 0.5 sigma |
| 2 | **Label swap** -- swap signal/background, retrain MVA | AUC drops to ~0.5 |
| 3 | **Peak removal** -- mask signal window, fit sidebands | Background extrapolates smoothly, residuals consistent with fluctuation |
| 4 | **Momentum scale** -- shift momenta +1%, rerun | Mass peak shifts ~1% as expected |
| 5 | **Memorization** -- permute event labels, retrain MVA | AUC drops to ~0.5 |
| 6 | **Injection** -- fake signal at different location/strength | Recovered within 2 sigma of injected |

### Response document format

| Column | Content |
|--------|---------|
| Reviewer | VC2 reviewer name |
| Issue | Short title (< 10 words) |
| Category | A / B / C |
| Criticism | Full description with evidence |
| Response | Agree, disagree (with justification), or clarify |
| Action | What was done (or why nothing needed) |
| Script:Line | Code reference for fix, or N/A |

No empty fields. Appended to AN as appendix.

---

## 10. Complete Review Journey

The analysis passes through two VC checkpoints: a **full review** of the
draft (before humans see anything) and a **light pass** after full data.

| Phase | Tier | Panel | Gate |
|-------|------|-------|------|
| 0 Acquire | Self | Executor | Artifacts complete |
| 1 Strategy | 4-bot | Phys + Crit + Constr + Arbiter | Arbiter PASS |
| 2 Exploration | Self+PV | Executor + PV | Self-check + PV |
| 3 Processing | 1-bot | Crit + PV | Critical PASS |
| 4a Expected | 4-bot+bib | Full panel + BibTeX + Arbiter | Arbiter PASS |
| 4b Validation | 4-bot+bib | Same as 4a | Arbiter PASS |
| 5 Draft Note | 5-bot | Full panel + Rendering + Arbiter | Arbiter PASS |
| VC1 full | ARC | Chair+Data+Selection+Fit+Theory | All 5 PASS |
| VC2 full | Pub | Reproduce+Adversarial+Cross+Blind+Referee | Unanimous PASS |
| **HUMAN GATE** | -- | **Multiple human physicists** | APPROVE/ITERATE/REGRESS/PAUSE |
| 6 Full Data | 1-bot | Crit + PV (escalate to 4-bot if >2σ anomaly) | Critical PASS |
| 7 Final Note | 5-bot | Full panel + Rendering + Arbiter | Arbiter PASS |
| VC1 light | ARC | Same 5 members | Results integration check |
| VC2 light | Pub | Same 5 members | Reproducibility + adversarial on full data |

**Phases 0-3: Building the analysis.** Review is lightweight (Self,
1-bot) for fast iteration. The exception is Phase 1, which receives
the full 4-bot panel because the strategy is binding -- departures
after approval require re-review at the same tier.

**Phases 4a-4b: Inference on partial data.** Review escalates to
4-bot+bib. The full panel examines the statistical machinery,
systematic budget, and fit behavior. The validation target rule
applies: extraction compared to PDG with pull > 3σ is automatic
Category A.

**Phase 5: Draft analysis note.** The heaviest automated review
(5-bot) ensures the draft AN meets publication standards. This is
a complete document — full methodology, all systematics, all
validation tests, all figures — with 10% data results.

**VC1 full review.** The entire analysis is reviewed as a unified
whole for the first time. The Chair enforces cross-phase coherence.
The anti-hallucination checklist verifies every number has provenance.
VC1 uses A/B/C classification with the fix routing table.

**VC2 full review.** Adversarial validation under strict isolation.
VC2 sees only the final work product and data — no VC1 findings, no
process history. The CrossAnalyst builds an independent analysis from
raw data. The Adversarial reviewer runs six attacks with quantitative
pass criteria. The Blind reviewer evaluates methodology before seeing
results. Unanimous PASS required.

**HUMAN GATE.** Multiple human physicists receive the complete,
AI-verified, VC-endorsed package: the draft AN, all VC1/VC2 review
reports, response documents, and the unblinding checklist (see
`core/blinding.md`). They judge whether the AI's self-review was
rigorous enough to trust the methodology. Approval freezes all
methodology — no changes after this point.

**Phase 6: Full data.** Review is deliberately lightweight (1-bot).
Methodology was approved by humans; Phase 6 focuses exclusively on
correct execution on full data. Configuration is frozen. Anomaly
(>2σ from expected) triggers automatic escalation to 4-bot.

**Phase 7: Final analysis note.** Update the draft with full observed
results, produce flagship figures, compile final PDF. 5-bot review
ensures the final note is publication-ready.

**VC1 light pass.** The same 5 specialists check only that full
results were correctly integrated — methodology sections are already
approved and should be unchanged.

**VC2 light pass.** Reproducibility audit on the full dataset (VC2-
Reproduce re-executes all scripts). VC2-Adversarial re-runs attacks
on full data. VC2-CrossAnalyst verifies compatibility with full
results. Light scope — methodology already endorsed.

### Final Deliverables

After VC2 light pass: AN (PDF) with VC response appendices, code
repository, `results.json`, HEPData YAML, experiment log, all
regression tickets and resolutions. This is the complete audit trail.

---

## Quick Reference

### Category decision tree

```
Is the analysis result potentially wrong because of this finding?
  YES --> A (blocks advancement, fresh re-review)
  NO  --> Could the result be misinterpreted or criticized?
            YES --> B (must fix before PASS)
            NO  --> C (style, arbiter decides)
```

### Tier selection

```
Planning?      --> 4-bot       Extracting?    --> 4-bot+bib
Exploring?     --> Self        Documenting?   --> 5-bot
Building?      --> 1-bot       Verifying?     --> VC1 then VC2
```

### Regression quick check

```
Single systematic > 80% of total?     --> Regress to Phase 1
Validation failed without 3 attempts? --> Regress to failing phase
GoF toys inconsistent?                --> Regress to Phase 4a
>50% bins excluded?                   --> Regress to Phase 3 or 4a
Tautological validation?              --> Regress to Phase 3
```
