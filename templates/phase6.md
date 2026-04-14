# Phase 6: Full Data -- {{name}}

Type: {{analysis_type}}

**METHODOLOGY IS FROZEN.** Human gate approved analysis at end of
Phase 5. No changes to selection, fit model, systematic treatment,
binning, or operating points. Configuration hash must match approved
version. Methodology change → return through human gate.

---

## Objective

Execute human-approved, methodology-frozen analysis on full dataset.
Produce observed results, diagnostics, anomaly assessment.

## Tasks

1. **Full dataset, frozen configuration.** Run identical pipeline from
   Phase 4b on complete dataset. Configuration hash verified against
   approved version before execution.

2. **Post-fit diagnostics:**
   - Pre/post-fit distribution overlays
   - Nuisance parameter pulls and constraints
   - Parameter correlation matrix
   - GoF: chi2/ndf, p-value, saturated model test
   - Yields per region

3. **Robustness checks:** vary fit range +/-10%, halve/double bins,
   tighten/loosen each cut, compare primary vs. secondary approach.
   Result must be stable within systematics.

4. **Anomaly assessment:** unexpected features, |pull| > 3, tension
   with cross-checks, >3 sigma excesses or deficits. All documented
   with quantitative comparison to Phase 4a expected and Phase 4b
   10% validation.

5. **Final significance/limits** per `techniques/statistics.md`:
   - Measurements: value +/- stat +/- syst
   - Searches: 95% CL limits, p-value, local significance

6. **Update `results.json`:** `"phase":"6"`, `"type":"observed"`,
   full systematic breakdown, comparison with 4a expected and 4b 10%.

## Deliverables

- `outputs/results.json` with observed values
- Post-fit diagnostic plots in `outputs/figures/`
- Robustness check table
- Anomaly assessment document
- Configuration hash verification log

## Review

**1-bot.** Critical + Plot Validator. Checks execution only --
methodology already approved.

**Escalation:** observed result deviates > 2 sigma from expected
(Phase 4a) → review auto-escalates to **4-bot** (Physics + Critical +
Constructive + Arbiter).

## What you MUST NOT do

- Change any selection cut, fit model, or systematic treatment
- Re-optimize operating points or binning
- Add or remove systematic sources
- Modify background estimation method
- Change signal model or interpretation

Any of above needed → return to human gate with regression ticket.

## References

- `core/blinding.md` -- post-approval rules
- `core/review.md` -- review tiers and escalation
- `techniques/statistics.md` -- significance, limits, GoF
- `techniques/fitting.md` -- fit diagnostics
