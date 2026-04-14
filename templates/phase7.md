# Phase 7: Final Analysis Note -- {{name}}

Type: {{analysis_type}}

**METHODOLOGY IS FROZEN.** Only results, figures, summary sections
updated. Methodology sections must be byte-identical to human-approved
Phase 5 draft. Discrepancy = Category A.

---

## Objective

Update Phase 5 draft with full observed results from Phase 6. Produce
flagship figures at publication quality. Compile final PDF. Last writing
phase before VC light passes.

## Tasks

1. **Update AN results chapter** with full observed data:
   - Replace 10% validation with full observed results
   - Add observed vs. expected comparison plots
   - Include post-fit diagnostics from Phase 6
   - Update significance/limits with observed values
   - Add robustness check summary table

2. **Flagship figures** at publication quality: final observed
   distributions, limit/significance plots, money plots with observed
   data overlaid. All per `standards/plotting.md`.

3. **Update summary chapter:** final findings, comparison with theory
   predictions, comparison with Phase 1 reference analyses, outlook
   and future directions.

4. **Methodology diff check.** Diff Phase 5 vs Phase 7 methodology
   sections. Only permitted changes:
   - Results values updated (10% → full)
   - Figures replaced with full-data versions
   - Summary/conclusions updated for full results
   Any other change = Category A → return through human gate.

5. **Compile final PDF.** Same toolchain as Phase 5:
   ```bash
   pixi run build-pdf
   ```
   Verify all new figures, tables, cross-references resolve.

6. **Final rendering check:** margin overflow, page breaks, equations,
   references, captions, page count (50-100 pages).

7. **Prepare HEPData submission:** machine-readable results in YAML
   with systematic breakdown.

## Deliverables

- `outputs/ANALYSIS_NOTE_FINAL.md` -- final AN source
- `outputs/ANALYSIS_NOTE_FINAL.pdf` -- final compiled PDF
- All figures (PDF + PNG) including observed-data plots
- Updated BibTeX and code traceability index
- Machine-readable results (`results.json` + HEPData YAML)
- Diff report confirming methodology sections unchanged

## Review

**5-bot.** Full panel (Physics + Critical + Constructive + Plot
Validator + BibTeX + Rendering) + Arbiter. A-items block VC passes.

After 5-bot PASS:
- **VC1 light pass** -- results integration check only
  (see `core/agents/vc1.md` Light Pass Mode)
- **VC2 light pass** -- reproducibility + adversarial on full data
  (see `core/agents/vc2.md` Light Pass Mode)

After VC2 light PASS: analysis complete.

## What you MUST NOT do

- Modify any methodology section (selection, background, systematics)
- Re-interpret analysis based on observed results
- Add post-hoc comparisons without labeling as such
- Change figure styling inconsistently with Phase 5

## References

- `standards/analysis_note.md` -- AN structure, completeness checklist
- `standards/plotting.md` -- figure production standards
- `techniques/statistics.md` -- significance, limits, GoF
- `core/review.md` -- VC1/VC2 protocol, light pass scope
- `core/agents/vc1.md` -- VC1 light pass definition
- `core/agents/vc2.md` -- VC2 light pass definition
