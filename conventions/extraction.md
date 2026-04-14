# Extraction measurement conventions

## When this applies

Any analysis that measures an efficiency, scale factor, cross-section by
counting, or calibration quantity from collision data. Tag-and-probe,
ABCD methods, template fits for purity extraction, and similar techniques
all fall under this convention.

## Standard configuration

- **Pseudo-data**: MC pseudo-data with Poisson fluctuations for all
  development work. Never fit real data before the strategy is frozen.
- **Random seeds**: fixed and recorded. Every pseudo-experiment must be
  reproducible from the seed alone.
- **Granularity**: per-subperiod (e.g. per-era or per-fill-range). The
  analysis must be capable of producing results at this granularity even
  if the final result combines subperiods.
- **Calibration origin**: data-derived whenever possible. MC-derived
  calibrations require an explicit justification documenting why the
  data-driven approach fails and what residual bias is expected.

## Required systematic sources

### Efficiency modeling

- Tag selection bias: variation of tag criteria to assess probe
  contamination.
- Probe definition stability: tighten and loosen probe requirements.
- Signal model shape: alternative signal templates (e.g. different MC
  generator or analytic shape).
- Background model shape: alternative background templates or functional
  forms; envelope of reasonable models.
- Fit range dependence: vary the fit window boundaries and assess
  stability of the extracted quantity.

### Background contamination

- Same-sign or anti-isolated control regions to estimate non-prompt
  contamination.
- Prompt background subtraction using MC or sideband extrapolation.
- Charge misidentification rate from data-driven estimate.

### MC model dependence

- Generator comparison: at least two generators for the signal process.
- Parton shower variation: compare nominal with alternative shower model.
- Higher-order corrections: NLO vs LO shape effects on the measurement.

### Sample composition

- Pileup reweighting uncertainty: vary the minimum-bias cross-section
  by its uncertainty.
- Luminosity uncertainty: propagated to any MC-derived component.
- Beam conditions: per-subperiod variations in instantaneous luminosity
  and detector occupancy.

## Required validation checks

1. **Closure test** -- apply the full extraction procedure to MC truth.
   The extracted value must be consistent with the known input. This test
   validates the method, not the physics.
2. **Parameter sensitivity** -- vary each nuisance parameter by +/- 1
   sigma individually and verify the extracted quantity shifts within the
   quoted systematic.
3. **Operating point stability** -- repeat the measurement at alternative
   working points (e.g. different MVA thresholds). Large variations
   indicate inadequate systematic coverage.
4. **Per-subperiod consistency** -- extract the quantity independently in
   each subperiod. A chi-squared compatibility test must yield p > 0.01.
5. **Diagnostic sensitivity** -- inject a known bias into the
   pseudo-data and verify the procedure detects it. A method that cannot
   detect a 2x bias in a dominant systematic is insufficiently sensitive.

## Known pitfalls

### Tautological comparison

Comparing the extracted value to the MC input used to derive the
background model. If the background model was trained on the same MC,
agreement proves nothing. The comparison must use an independent sample
or an orthogonal region.

### Self-consistent closure

A closure test that uses the same functional form for generation and
extraction will always close. The closure test must use a different
model for truth than for extraction.

### MVA-induced correlations

If an MVA is used in the selection, the training sample and the
measurement sample must not overlap. Even with disjoint samples, the
MVA can introduce hidden correlations between systematic categories.
Verify by checking the profile of nuisance parameters with and without
the MVA cut.

### Circular luminosity

Do not use a luminosity measurement that itself depends on the
efficiency you are extracting. Document the luminosity calibration
chain and verify no circular dependency exists.
