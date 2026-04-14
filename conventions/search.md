# Search and limit-setting conventions

## When this applies

Any analysis that tests for the presence of a new signal and, absent
discovery, sets exclusion limits. Includes bump hunts, cut-and-count
searches, shape-based analyses with profile likelihood, and combined
searches across channels.

## Standard configuration

- **Statistical method**: CLs using the profile likelihood ratio as test
  statistic (LHC convention).
- **Approximation**: asymptotic formulae unless the expected event count
  in any bin falls below ~5, in which case use toy-based CLs.
- **Test statistic**: one-sided profile likelihood ratio with signal
  strength bounded to non-negative values.
- **Confidence level**: 95% CL for exclusion.
- **Signal injection**: inject signal at 0x, 1x, 2x, and 5x the
  predicted cross-section to validate the statistical framework before
  looking at data.
- **Blinding**: the signal region in data is not examined until the full
  analysis strategy, background model, and systematics are frozen.
  Control regions and validation regions may be examined at any time.

## Required systematic sources

### Signal modeling

- Cross-section theory uncertainty: scale variations (7-point envelope)
  and PDF uncertainty (Hessian or MC replicas).
- Signal acceptance: generator comparison, parton shower variation,
  and hadronization model.
- Signal shape: alternative MC samples to assess template shape
  uncertainty in shape-based analyses.

### Background estimation

- Data-driven backgrounds: transfer factor uncertainty from control
  region statistics and any extrapolation assumption.
- MC-driven backgrounds: normalization from theory cross-section
  uncertainty, shape from generator comparison.
- Minor backgrounds: conservative normalization uncertainty (typically
  50% or from a dedicated control region measurement).

### Detector and reconstruction

- Jet energy scale and resolution: per-source decomposition.
- Lepton efficiency: trigger, identification, isolation scale factors
  with their uncertainties.
- b-tagging: per-working-point scale factor uncertainties, including
  light-flavor mistag rate.
- Missing transverse momentum: propagation of JES/JER and unclustered
  energy.
- Pileup: minimum-bias cross-section variation.

### Theory inputs

- Luminosity uncertainty.
- PDF choice and alpha_s variation.
- Parton shower matching scale.
- Electroweak correction factors where applicable.

## Required validation checks

1. **Closure on MC** -- run the full limit-setting procedure on
   background-only MC pseudo-data. The expected limit must be consistent
   with the Asimov result.
2. **Signal injection recovery** -- inject signal at known strength and
   verify the fitted signal strength is recovered within uncertainty.
3. **Nuisance parameter pulls** -- in background-only fits, all nuisance
   parameters must be within 1 sigma of their nominal values. Pulls
   beyond 2 sigma indicate a mismodeled systematic or a fit instability.
4. **Goodness of fit** -- saturated model GoF test on background-only
   pseudo-data. The observed GoF p-value distribution should be
   approximately uniform.
5. **Look-elsewhere effect** -- if scanning over a continuous parameter
   (e.g. mass), correct for the trials factor using either the method of
   Gross and Vitells or toy-based global p-value estimation.

## Known pitfalls

### Optimizing on the signal region

Tuning selection cuts or MVA thresholds by looking at the signal region
in data. All optimization must be performed on MC or in control regions
before unblinding.

### Undercoverage from profiling

Profiling nuisance parameters can absorb genuine signal if the
systematic templates are too flexible. Verify with signal injection
that the profiled systematics do not bias the signal strength.

### Background model bias

Using a single functional form for a smooth background estimate without
testing alternatives. The spurious-signal test (fitting signal+background
to background-only pseudo-data) must return a signal strength consistent
with zero.

### Correlated systematics across channels

In combined searches, systematics that are correlated across channels
must be explicitly correlated in the statistical model. Treating them
as uncorrelated underestimates the total uncertainty.
