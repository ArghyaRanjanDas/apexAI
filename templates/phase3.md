# Phase 3: Processing -- {{name}}

Type: {{analysis_type}}

---

## Objective

Implement selection, background estimation, corrections. Carry both
Phase 1 approaches through quantitative comparison. Validate with
closure and stress tests. Implement systematic variations.

---

## Tasks

### 3a. Selection

1. **Baseline cuts:** trigger (document prescales and turn-on curves),
   object multiplicity, loose PID, geometric acceptance, overlap removal.
   Document every cut with physics motivation.

2. **Analysis-specific selection** for both Phase 1 approaches.
   Start loose, tighten incrementally. Never optimize toward known
   answer.

3. **Cut-flow tables** per approach:

   | Cut | Events | Relative eff. | Cumulative eff. | Signal eff. | Bkg rejection |
   |-----|-------:|-------------:|----------------:|------------:|--------------:|
   | ... | ... | ... | ... | ... | ... |

4. **N-1 plots.** Per cut variable, plot with all other cuts applied.
   Vertical dashed line at threshold. Show signal and background
   separately. Verify boundary sits where signal/background separate.

5. **Control regions.** One per major background, orthogonal to signal
   region. Validate data/MC agreement in each CR.

### 3b. Approach Comparison

6. **Quantitative comparison** of both approaches on common metric
   (expected significance, S/sqrt(B), or sensitivity). Select primary;
   secondary → Phase 4 cross-check.

### 3c. Validation

7. **Closure test.** Full chain on MC pseudo-data with known truth.
   Must recover injected signal: chi2/ndf < 3, p > 0.05.

8. **Stress test.** Reweight MC kinematics, verify recovery. Tests
   robustness against data/MC modeling differences.

9. **Failure remediation.** If either test fails, follow remediation
   protocol (at least 3 distinct attempts):
   1. Check formula (dimensional consistency, limiting cases)
   2. Check inputs (correct branches, units, weights)
   3. Alternative binning (coarser and finer)
   4. Different regularization/fit config
   5. Different MC generator or tune
   6. Different method (secondary approach from Phase 1)
   All attempts exhausted → document quantitatively, escalate.

### 3d. MVA (if applicable)

10. **Train** using only modeling-checked variables from Phase 2
    (chi2/ndf < 5). Required diagnostics: overtraining KS test (p > 0.05),
    ROC + AUC, score distributions (train/test overlay), feature importance.

11. **Hyperparameter scan** (2+ parameters with performance curves).

### 3e. Systematic Variations

12. **Implement every variation** from Phase 1 systematic catalog.
    Per source: up/down variation, rerun selection, record effect on
    yield and shape.

13. **Organize by category** (experimental/theoretical/modeling) in
    format Phase 4 can ingest into statistical model.

---

## Deliverables

- Selection code (both approaches) in `src/`
- Cut-flow tables, N-1 plots in `outputs/figures/`
- Control region data/MC comparisons
- Approach comparison table with quantitative metric
- Closure and stress test results with chi2/ndf and p-values
- MVA diagnostics (if applicable)
- Systematic variation tables organized by category
- `outputs/SELECTION.md` -- synthesis of all processing results

## Review Tier

**1-bot.** Critical Reviewer + Plot Validator.

## References

- `core/phases.md` -- validation failure remediation protocol
- `conventions/` -- applicable conventions for systematics
