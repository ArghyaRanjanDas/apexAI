# Review Protocol

Every finding needs evidence: file path, line number, value, or plot.
"Looks reasonable" = rejected. Bar: publication-ready, not "good enough."

---

## 1. Review Philosophy

**Evidence-based.** Finding without cite (plot, chi2/ndf, bin, code line) = not a finding. Returned for evidence.

**Traceable.** Every number → script:line. Correct number, no provenance = B. Number from recalled knowledge = A.

**Adversarial.** Assume executor may exhibit motivated reasoning. Red flags: huge uncertainties hiding poor central value, calibration assuming answer, tautological validation (fit vs. own training data). Ask: "Is this narrative self-serving?"

---

## 2. Finding Classification

| Cat | Meaning | Action |
|-----|---------|--------|
| **A** | Blocks advancement | Fix, re-review by FRESH reviewer. No downstream work until resolved. |
| **B** | Must fix before PASS | Fix, present to same reviewer. Reviewer may upgrade to A. |
| **C** | Style/preference | Arbiter (or VC1 Chair) decides. Never blocks advancement. |

**Escalation.** Reviewer may upgrade B→A. Only arbiter/Chair may downgrade A (documented justification).

**Dismissal.** Cannot dismiss "out of scope" if fix < ~1 hour. Upstream-dependent findings batch into one regression ticket.

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

**Arbiter:** Reads all reports, resolves C-conflicts, issues PASS/ITERATE/REGRESS. No new findings. Disagreement on category → arbiter assigns final with justification.

**Independence.** Reviewers write without seeing each other's reports. Arbiter/Chair sees full set first.

---

## 4. Per-Phase Review Focus

Out-of-scope findings → regression tickets (Section 6), don't block current phase.

**Phase 0 (Self):** Files open in uproot. Provenance: portal, DOI, SHA-256, event count. Tree matches experiment format.

**Phase 1 (4-bot):** Physics: analysis type, two genuinely different approaches, systematic catalog completeness, reference analyses. Critical: flagship figures defined, [A]/[L]/[D] labels, consistency, catalog gaps. Constructive: improvements without plan change. Arbiter: strategy binding once approved.

**Phase 2 (Self + PV):** All branches plotted (linear + log-y, 100 bins, overflow). Summary CSV. Mass spectra (OS/SS). Peaks vs. mass table. Variable ranking. MVA input check (chi2/ndf > 5 = flagged). PV: axis labels, units, overflow bins.

**Phase 3 (1-bot):** Cut-flow both approaches. N-1 plots confirm boundaries. Control regions orthogonal. Closure (chi2/ndf < 3, p > 0.05) + stress tests pass — if not, remediation (3+ attempts). MVA diagnostics if applicable (KS p > 0.05, ROC, importance). Systematics per catalog.

**Phase 4a (4-bot+bib):** Systematic completeness (missing = A). Fit converges (Hesse + Minos, nuisances ±2 sigma, none constrained >50%). Formula audit. Perturbation tests. Fit init from data shape. Citations resolve. PDG pull >3 sigma = A.

**Phase 4b (4-bot+bib):** 10% subsample (fixed seed). Identical 4a config. Central value compatible within sqrt(10)-inflated uncertainty. Unblinding checklist complete. Produces human gate materials.

**Phase 5 (5-bot):** AN per `standards/analysis_note.md`. Every number → `[code:script.py:LN]`. Figures per `standards/plotting.md`. PDF clean (margins, refs, captions, 50-100 pages). Rendering + BibTeX checks. Last automated review before VC1.

**Phase 6 (1-bot):** Methodology frozen. Review = execution only. Config identical to 4b. Post-fit diagnostics on full data. Robustness (fit range, binning, cuts, primary vs. secondary). Anomaly >2 sigma → auto-escalate to 4-bot. Documented with quantitative 4b comparison.

**Phase 7 (5-bot):** Final AN with full observed results. Figures = full-data versions. Same Phase 5 standards. Methodology sections must be unchanged from Phase 5 draft — discrepancy = A.

**VC1 light (ARC):** All 5 review. Scope = results integration only: full-data numbers inserted, figures updated, methodology unchanged. Methodology change = A. No re-review of selection/fit/systematics unless results raise concerns.

**VC2 light (Pub):** Reproduce re-executes Phase 6-7 scripts, diffs outputs. Adversarial re-runs 6 attacks on full data. CrossAnalyst verifies compatibility. Blind checks no post-hoc steering. Referee confirms journal standards. Unanimous PASS required.

---

## 5. Iteration and Escalation

| Tier | Warn | Strong warn | Hard cap |
|------|------|-------------|----------|
| 4/5-bot | 3 | 5 | 10 (potential Phase 1 regression) |
| 1-bot | 2 | 3 | Escalate to 4-bot |
| Self | -- | -- | Escalate to 1-bot |

**Warn:** log recurring issue. **Strong warn:** evaluate deeper problem, may file regression. **Hard cap:** tier escalates; 4/5-bot cap → mandatory Phase 1 plan review.

**Fresh reviewer rule.** A-item re-review = different reviewer. Gets: finding, fix, artifacts — not original assessment.

**Arbiter escalation.** Unresolvable disagreement → orchestrator invokes consultation or regresses.

---

## 6. Phase Regression

### Mandatory triggers

1. **Validation failure without remediation** — test fails, <3 documented attempts.
2. **Dominant systematic** — single source >80% of total.
3. **GoF inconsistency** — toys inconsistent with observed GoF.
4. **Excessive exclusion** — >50% bins excluded from fit.
5. **Tautological comparison** — validation against same data used to derive result.

### Procedure

1. Investigator traces root cause → originating phase.
2. REGRESSION_TICKET.md: trigger, root phase, affected phases, artifacts to regen, remediation plan.
3. Fixer re-runs target phase. Stale artifacts marked (not deleted).
4. Downstream cascade: all phases between target and current re-execute + re-review.
5. Resume normal review at triggering phase.

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

After VC2 full PASS, before Phase 6. Single mandatory human intervention. No bypass.

**Presented:** Draft AN (VC-endorsed, methodology final, 10% results), unblinding checklist, 4a expected, 4b validation + 4a comparison, all findings/resolutions, VC1+VC2 attestations, open B-items, perturbation results, control region plots.

| Option | Effect |
|--------|--------|
| APPROVE | Phase 6 begins, methodology frozen |
| ITERATE | Fix in draft scope → re-review → re-present |
| REGRESS | Target phase → triggers Section 6 |
| PAUSE | Halts until human resumes |

Decision logged. Post-APPROVE methodology change → return through gate.

---

## 8. VC1 — Analysis Review Committee

Activates after Phase 5 PASS. 5 parallel specialists.

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

1. **Collect** — all 5 submit independently (no shared reports).
2. **Triage** — Chair deduplicates, assigns A/B/C.
3. **Route** — assign to owner via fix routing table.
4. **Fix parallel** — each fix: change, evidence, script:line.
5. **Re-review** — A→fresh reviewer, B→original, C→Chair resolves.
6. **Iterate** until all 5 PASS. No partial advancement.

### Fix routing

| Issue | Owner |
|-------|-------|
| Data/units/luminosity | Data Engineer |
| Cuts/backgrounds/selection | Executor |
| Fit/statistics/systematics | Executor |
| Interpretation/theory | Executor + Note Writer |
| Documentation/figures | Note Writer |

### Anti-hallucination checklist

Each failure = Category A.

- [ ] Every number → `[code:script.py:LN]` that resolves
- [ ] No textbook values as fit inputs (init from data shape)
- [ ] Perturbation tests passed (pT scale, event drop, fake injection)
- [ ] Parameters from fits to data, not prior knowledge
- [ ] Uncertainties from fit or documented procedure, not assumed
- [ ] Units consistent: text, tables, figures, code, axes
- [ ] Post-hoc comparisons labeled as such

---

## 9. VC2 — Publication Committee

Activates after VC1 PASS. 5 independent reviewers, strict isolation. Unanimous PASS required — no arbiter override.

### Independence rules (absolute)

1. **No VC1 access.** VC2 sees no VC1 findings/discussion.
2. **No process context.** VC2 gets AN + code + data. No experiment log, no orchestrator reasoning, no inter-agent messages.
3. **CrossAnalyst: raw data only.** No AN, no code, no results. Physics question only.
4. **Blind sequence.** Blind reviewer evaluates methodology before seeing fit result.

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
| 1 | **Noise** — Gaussian (0.1 × resolution) on all inputs, rerun | Result shifts < 0.5 sigma |
| 2 | **Label swap** — swap signal/background, retrain MVA | AUC drops to ~0.5 |
| 3 | **Peak removal** — mask signal window, fit sidebands | Background extrapolates smoothly, residuals consistent with fluctuation |
| 4 | **Momentum scale** — shift momenta +1%, rerun | Mass peak shifts ~1% as expected |
| 5 | **Memorization** — permute event labels, retrain MVA | AUC drops to ~0.5 |
| 6 | **Injection** — fake signal at different location/strength | Recovered within 2 sigma of injected |

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

Two VC checkpoints: **full review** of draft (before humans) and **light pass** after full data.

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

**Phases 0-3:** Building. Lightweight review (Self, 1-bot) for fast iteration. Exception = Phase 1: full 4-bot because strategy is binding. Post-approval departures → re-review at same tier.

**Phases 4a-4b:** Inference on partial data. 4-bot+bib examines statistical machinery, systematic budget, fit behavior. Validation target rule: PDG pull >3σ = automatic A.

**Phase 5:** Heaviest automated review (5-bot). Complete doc — full methodology, all systematics, all validation, all figures — with 10% results.

**VC1 full:** Entire analysis reviewed as unified whole. Chair enforces cross-phase coherence. Anti-hallucination checklist verifies provenance. A/B/C + fix routing.

**VC2 full:** Adversarial validation under strict isolation. VC2 sees only work product + data — no VC1 findings, no process history. CrossAnalyst builds independent analysis from raw data. Adversarial runs 6 attacks. Blind evaluates methodology before results. Unanimous PASS.

**HUMAN GATE.** Humans receive complete AI-verified, VC-endorsed package. Judge whether AI self-review was rigorous enough. APPROVE → methodology frozen permanently.

**Phase 6:** Lightweight (1-bot). Methodology human-approved → execution focus only. Config frozen. Anomaly >2σ → auto-escalate to 4-bot.

**Phase 7:** Update draft with full results, flagship figures, final PDF. 5-bot ensures publication-ready.

**VC1 light:** Same 5 check results integration only. Methodology sections must be unchanged.

**VC2 light:** Reproduce re-executes scripts. Adversarial re-runs attacks on full data. CrossAnalyst verifies compatibility. Methodology already endorsed.

### Final Deliverables

Post-VC2 light: AN (PDF) with VC response appendices, code repo, `results.json`, HEPData YAML, experiment log, regression tickets + resolutions. Complete audit trail.

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
