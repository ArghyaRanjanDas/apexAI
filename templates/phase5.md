# Phase 5-7: Draft Note, Full Data, Final Note -- {{name}}

Type: {{analysis_type}}

This template covers Phases 5, 6, and 7 since they share the documentation
pipeline. The executing phase determines which section applies.

---

## Phase 5: Draft Analysis Note

### Objective

Produce a complete, publication-quality draft analysis note containing
full methodology and 10% validation results (from Phase 4b). This draft
undergoes 5-bot internal review, VC1, VC2, and the human gate before
any full data unblinding.

### Tasks

1. **Draft AN** per `standards/analysis_note.md`. Required sections:
   1. Introduction (motivation, prior work, overview)
   2. Dataset and simulation (samples, generators, xsec, luminosity)
   3. Object reconstruction (trigger, ID, b-tag, overlap removal)
   4. Event selection (regions, cut-flow, N-1, efficiencies)
   5. Background estimation (methods, control regions, data-driven)
   6. Systematic uncertainties (per-source: origin, method, impact,
      interpretation)
   7. Results (expected from 4a, 10% validation from 4b, perturbation
      tests, robustness, operating point scans)
   8. Summary (findings so far, methodology validation, outlook for
      full unblinding)

2. **Code traceability.** Every number references `[code:script.py:LN]`.
   Verify each reference resolves to an actual line of code.

3. **Flagship figures** at publication quality per `standards/plotting.md`:
   - Labels with units on every axis
   - Experiment/lumi annotation via mplhep
   - Ratio panels where applicable
   - Consistent colors across the AN
   - Both PDF and PNG output
   - Include all figures from Phases 2 through 4b

4. **Compile to PDF:** markdown -> pandoc -> LaTeX postprocess -> tectonic.
   ```bash
   pixi run build-pdf
   ```
   Verify every figure, table, equation, and cross-reference renders.

5. **Rendering check:** no margin overflow, clean page breaks, correct
   equations, resolved cross-references, complete captions, 50-100 pages.

### Deliverables (Phase 5)

- `outputs/ANALYSIS_NOTE.md` -- complete draft source
- `outputs/ANALYSIS_NOTE.pdf` -- compiled PDF
- All figures in `outputs/figures/` (PDF + PNG)
- BibTeX file (`outputs/references.bib`)
- Code traceability index

### Review (Phase 5)

**5-bot.** Physics + Critical + Constructive + Plot Validator + BibTeX +
Rendering -> Arbiter. A-items block VC1.

After 5-bot PASS:
- **VC1 full review** (5 specialist reviewers)
- **VC2 full review** (5 independent reviewers, no VC1 access)
- **HUMAN GATE** -- multiple humans judge the complete, AI-verified,
  VC-endorsed package

---

## Phase 6: Full Data (after Human Gate APPROVE)

### Objective

Execute the human-approved, methodology-frozen analysis on the full
dataset. No configuration changes permitted.

### Tasks

6. **Full dataset, frozen configuration.** No changes to selection, fit
   model, systematic treatment, or operating points. Configuration hash
   verified against the approved version.

7. **Post-fit diagnostics:**
   - Pre/post-fit distribution overlays
   - Nuisance parameter pulls and constraints
   - Parameter correlation matrix
   - GoF: chi2/ndf, p-value, saturated model test
   - Yields per region

8. **Robustness checks:** vary fit range +/-10%, halve/double bins,
   tighten/loosen each cut, compare primary vs. secondary approach.
   Result must be stable within systematics.

9. **Anomaly assessment:** unexpected features, |pull| > 3, tension with
   cross-checks, >3 sigma excesses or deficits. All documented.

10. **Final significance/limits** per `techniques/statistics.md`:
    - Measurements: value +/- stat +/- syst
    - Searches: 95% CL limits, p-value, local significance

11. **Update `results.json`:** `"phase":"6"`, `"type":"observed"`,
    full systematic breakdown, comparison with 4a expected and 4b 10%.

### Deliverables (Phase 6)

- `outputs/results.json` with observed values
- Post-fit diagnostic plots
- Robustness check table
- Anomaly assessment document

### Review (Phase 6)

**1-bot.** Critical + Plot Validator. Escalates to **4-bot** if
observed result deviates >2 sigma from expected (Phase 4a).

---

## Phase 7: Final Analysis Note

### Objective

Update the Phase 5 draft AN with full observed results, produce flagship
figures at publication quality, and compile the final PDF. Methodology
sections are unchanged (frozen at human gate); only results, figures,
and summary are updated.

### Tasks

12. **Update AN results chapter** with full observed data:
    - Replace 10% validation results with full observed results
    - Add observed vs. expected comparison plots
    - Include post-fit diagnostics from Phase 6
    - Update significance/limits with observed values
    - Add robustness check summary table

13. **Flagship figures** at publication quality: final observed
    distributions, limit/significance plots, money plots with observed
    data overlaid. All per `standards/plotting.md`.

14. **Update summary chapter:** final findings, comparison with theory
    predictions, comparison with reference analyses from Phase 1,
    outlook and future directions.

15. **Compile final PDF.** Same toolchain as Phase 5. Verify all new
    figures, tables, and cross-references resolve. Methodology sections
    must be byte-identical to the approved draft (diff check).

16. **Final rendering check:** margin overflow, page breaks, equations,
    references, captions, page count.

### Deliverables (Phase 7)

- `outputs/ANALYSIS_NOTE_FINAL.md` -- final AN source
- `outputs/ANALYSIS_NOTE_FINAL.pdf` -- final compiled PDF
- All figures (PDF + PNG) including observed-data plots
- Updated BibTeX and code traceability index
- Machine-readable results (`results.json` + HEPData YAML)
- Diff report confirming methodology sections unchanged

### Review (Phase 7)

**5-bot.** Full panel + Rendering + Arbiter. A-items block VC passes.

After 5-bot PASS:
- **VC1 light pass** -- results integration check only
- **VC2 light pass** -- reproducibility + adversarial on full data

---

## References

- `standards/analysis_note.md` -- AN structure, completeness checklist
- `standards/plotting.md` -- figure production standards
- `techniques/statistics.md` -- significance, limits, GoF
- `techniques/fitting.md` -- fit models and validation
- `core/review.md` -- VC1/VC2 protocol
- `core/blinding.md` -- post-approval rules
