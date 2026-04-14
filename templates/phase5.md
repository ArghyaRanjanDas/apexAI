# Phase 5: Draft Analysis Note -- {{name}}

Type: {{analysis_type}}

---

## Objective

Produce complete, publication-quality draft analysis note with full
methodology and 10% validation results (from Phase 4b). Draft undergoes
5-bot internal review, VC1, VC2, and human gate before full data
unblinding.

## Tasks

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
   Verify each reference resolves to actual line of code.

3. **Flagship figures** at publication quality per `standards/plotting.md`:
   - Labels with units on every axis
   - Experiment/lumi annotation via mplhep
   - Ratio panels where applicable
   - Consistent colors across AN
   - Both PDF and PNG output
   - Include all figures from Phases 2 through 4b

4. **Compile to PDF:** markdown → pandoc → LaTeX postprocess → tectonic.
   ```bash
   pixi run build-pdf
   ```
   Verify every figure, table, equation, cross-reference renders.

5. **Rendering check:** no margin overflow, clean page breaks, correct
   equations, resolved cross-references, complete captions, 50-100 pages.

## Deliverables

- `outputs/ANALYSIS_NOTE.md` -- complete draft source
- `outputs/ANALYSIS_NOTE.pdf` -- compiled PDF
- All figures in `outputs/figures/` (PDF + PNG)
- BibTeX file (`outputs/references.bib`)
- Code traceability index

## Review

**5-bot.** Physics + Critical + Constructive + Plot Validator + BibTeX +
Rendering → Arbiter. A-items block VC1.

After 5-bot PASS:
- **VC1 full review** (5 specialist reviewers)
- **VC2 full review** (5 independent reviewers, no VC1 access)
- **HUMAN GATE** -- multiple humans judge complete, AI-verified,
  VC-endorsed package

## References

- `standards/analysis_note.md` -- AN structure, completeness checklist
- `standards/plotting.md` -- figure production standards
- `techniques/statistics.md` -- significance, limits, GoF
- `techniques/fitting.md` -- fit models and validation
- `core/review.md` -- VC1/VC2 protocol
- `core/blinding.md` -- unblinding protocol and human gate
