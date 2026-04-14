# Phase 6: Full Data -- {{name}}

Type: {{analysis_type}}

**METHODOLOGY IS FROZEN.** Human gate approved the analysis at the end
of Phase 5. No changes to selection, fit model, systematic treatment,
binning, or operating points. Configuration hash must match the
approved version. Any methodology change requires returning through
the human gate.

---

## Objective

Execute the human-approved, methodology-frozen analysis on the full
dataset. Produce observed results, diagnostics, and anomaly assessment.

## Tasks

1. **Full dataset, frozen configuration.** Run the identical analysis
   pipeline from Phase 4b on the complete dataset. Configuration hash
   verified against the approved version before execution begins.

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
   10% validation results.

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
methodology was already approved.

**Escalation:** if observed result deviates > 2 sigma from expected
(Phase 4a), review automatically escalates to **4-bot** (Physics +
Critical + Constructive + Arbiter).

## What you MUST NOT do

- Change any selection cut, fit model, or systematic treatment
- Re-optimize operating points or binning
- Add or remove systematic sources
- Modify the background estimation method
- Change the signal model or interpretation

If any of the above is needed, the analysis must return to the human
gate with a regression ticket.

## References

- `core/blinding.md` -- post-approval rules
- `core/review.md` -- review tiers and escalation
- `techniques/statistics.md` -- significance, limits, GoF
- `techniques/fitting.md` -- fit diagnostics
