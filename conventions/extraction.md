# Extraction measurement conventions

## When this applies

Any analysis measuring efficiency, scale factor, cross-section by counting, or calibration quantity from collision data. Tag-and-probe, ABCD methods, template fits for purity extraction, similar techniques all fall under this convention.

## Standard configuration

- **Pseudo-data**: MC pseudo-data with Poisson fluctuations for all development work. Never fit real data before strategy = frozen.
- **Random seeds**: fixed and recorded. Every pseudo-experiment must be reproducible from seed alone.
- **Granularity**: per-subperiod (e.g. per-era or per-fill-range). Must produce results at this granularity even if final result combines subperiods.
- **Calibration origin**: data-derived whenever possible. MC-derived calibrations require explicit justification documenting why data-driven approach fails and what residual bias = expected.

## Required systematic sources

### Efficiency modeling

- Tag selection bias: vary tag criteria → assess probe contamination.
- Probe definition stability: tighten and loosen probe requirements.
- Signal model shape: alternative signal templates (e.g. different MC generator or analytic shape).
- Background model shape: alternative background templates or functional forms; envelope of reasonable models.
- Fit range dependence: vary fit window boundaries → assess stability of extracted quantity.

### Background contamination

- Same-sign or anti-isolated control regions → estimate non-prompt contamination.
- Prompt background subtraction using MC or sideband extrapolation.
- Charge misidentification rate from data-driven estimate.

### MC model dependence

- Generator comparison: at least two generators for signal process.
- Parton shower variation: compare nominal with alternative shower model.
- Higher-order corrections: NLO vs LO shape effects on measurement.

### Sample composition

- Pileup reweighting uncertainty: vary minimum-bias cross-section by its uncertainty.
- Luminosity uncertainty: propagated to any MC-derived component.
- Beam conditions: per-subperiod variations in instantaneous luminosity and detector occupancy.

## Required validation checks

1. **Closure test** -- apply full extraction procedure to MC truth. Extracted value must be consistent with known input. Validates method, not physics.
2. **Parameter sensitivity** -- vary each nuisance parameter by +/- 1 sigma individually → verify extracted quantity shifts within quoted systematic.
3. **Operating point stability** -- repeat measurement at alternative working points (e.g. different MVA thresholds). Large variations → inadequate systematic coverage.
4. **Per-subperiod consistency** -- extract quantity independently in each subperiod. Chi-squared compatibility test must yield p > 0.01.
5. **Diagnostic sensitivity** -- inject known bias into pseudo-data → verify procedure detects it. Method that cannot detect 2x bias in dominant systematic = insufficiently sensitive.

## Known pitfalls

### Tautological comparison

Comparing extracted value to MC input used to derive background model. If background model trained on same MC → agreement proves nothing. Comparison must use independent sample or orthogonal region.

### Self-consistent closure

Closure test using same functional form for generation and extraction will always close. Must use different model for truth than for extraction.

### MVA-induced correlations

If MVA used in selection → training sample and measurement sample must not overlap. Even with disjoint samples, MVA can introduce hidden correlations between systematic categories. Verify by checking nuisance parameter profile with and without MVA cut.

### Circular luminosity

Do not use luminosity measurement that itself depends on efficiency you are extracting. Document luminosity calibration chain → verify no circular dependency.
