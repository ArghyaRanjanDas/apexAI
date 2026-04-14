# Phase 4: Inference -- {{name}}

Type: {{analysis_type}}

---

## Objective

Extract the expected result on simulation (4a) and validate on 10% data
(4b). Produce machine-readable results and the unblinding checklist.

---

## Sub-phase 4a: Expected Result

### Tasks

1. **Build the statistical model** (template fit, counting, etc.) from
   Phase 3 predictions. See `techniques/fitting.md` for the model catalog
   and decision tree.

2. **Systematic completeness table.** Every Phase 1 source must appear.
   Missing source = Category A finding:

   | Source | In catalog | Implemented | Effect (up/down) |
   |--------|-----------|-------------|------------------|
   | JES | Yes | Yes | +2.3/-1.8% |
   | Lumi | Yes | Yes | +/-1.6% |
   | ... | ... | ... | ... |

3. **Asimov/MC extraction.** Verify:
   - Fit converges (Hesse + Minos)
   - Post-fit nuisances within +/-2 sigma
   - No nuisance constrained >50%
   - Post-fit chi2/ndf < 3

4. **Formula audit.** Dimensional analysis, limiting cases (zero signal,
   zero systematics, background-only), Phase 1 traceability.

5. **Perturbation tests:**
   - Scale pT x1.02 -> mass shifts ~2%
   - Drop 50% events -> uncertainty grows ~sqrt(2)
   - Inject fake peak at known location -> fit must find it
   Each has a PASS criterion. Failure triggers investigation.

6. **Fit initialization from data shape.** Peak position from max bin,
   width from FWHM, yield from peak-region integral. Never from textbook.
   Quality: chi2/ndf in [0.5, 3.0].

7. **`results.json`** with:
   ```json
   {
     "phase": "4a",
     "type": "expected",
     "central_value": ...,
     "stat_uncertainty": ...,
     "syst_uncertainty": ...,
     "chi2_ndf": ...,
     "event_counts": {...},
     "operating_point": {...}
   }
   ```

### Deliverables (4a)

- `outputs/INFERENCE_EXPECTED.md`
- `outputs/results.json`
- Systematic completeness table
- Perturbation test results
- Post-fit diagnostic plots

### Review (4a)

**4-bot+bib.** Physics + Critical + Constructive + Plot Validator +
BibTeX -> Arbiter. A-items block 4b.

---

## Sub-phase 4b: 10% Validation

### Tasks

8. **10% subsample** via fixed random seed (chosen before seeing data).
   MC normalized to 10% of total luminosity.

9. **Full inference chain** with identical 4a configuration. No changes
   to selection, fit model, or systematic treatment.

10. **Compare with 4a.** Central value compatible within 4b statistical
    uncertainty (inflated by sqrt(10) vs. full data).

11. **Unblinding checklist:**
    - [ ] Fit converges
    - [ ] Nuisance parameters in range
    - [ ] Post-fit distributions reasonable
    - [ ] 4b consistent with 4a within sqrt(10)-inflated uncertainty
    - [ ] No pulls |pull| > 3
    - [ ] Perturbation tests pass
    - [ ] Control region agreement maintained

12. **Update `results.json`** with:
    ```json
    {
      "phase": "4b",
      "type": "10pct",
      "central_value": ...,
      "comparison_4a": {
        "delta": ...,
        "pull_sigma": ...
      }
    }
    ```

### Deliverables (4b)

- `outputs/INFERENCE_PARTIAL.md`
- Updated `outputs/results.json` with 4b entries
- 4a vs 4b comparison plots
- Completed unblinding checklist

### Review (4b)

**4-bot+bib.** Same panel as 4a. A-items block Phase 5.

---

## References

- `techniques/fitting.md` -- model catalog, fit code patterns
- `techniques/statistics.md` -- significance, limits, GoF, systematics
- `core/blinding.md` -- staged unblinding protocol
- `conventions/` -- applicable conventions
