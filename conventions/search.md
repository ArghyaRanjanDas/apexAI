# Search and limit-setting conventions

## When this applies

Any analysis testing for presence of new signal and, absent discovery, setting exclusion limits. Includes bump hunts, cut-and-count searches, shape-based analyses with profile likelihood, combined searches across channels.

## Standard configuration

- **Statistical method**: CLs using profile likelihood ratio as test statistic (LHC convention).
- **Approximation**: asymptotic formulae unless expected event count in any bin < ~5 → use toy-based CLs.
- **Test statistic**: one-sided profile likelihood ratio with signal strength bounded to non-negative values.
- **Confidence level**: 95% CL for exclusion.
- **Signal injection**: inject signal at 0x, 1x, 2x, 5x predicted cross-section → validate statistical framework before looking at data.
- **Blinding**: signal region in data not examined until full analysis strategy, background model, and systematics = frozen. Control regions and validation regions may be examined at any time.

## Required systematic sources

### Signal modeling

- Cross-section theory uncertainty: scale variations (7-point envelope) and PDF uncertainty (Hessian or MC replicas).
- Signal acceptance: generator comparison, parton shower variation, hadronization model.
- Signal shape: alternative MC samples → assess template shape uncertainty in shape-based analyses.

### Background estimation

- Data-driven backgrounds: transfer factor uncertainty from control region statistics and any extrapolation assumption.
- MC-driven backgrounds: normalization from theory cross-section uncertainty, shape from generator comparison.
- Minor backgrounds: conservative normalization uncertainty (typically 50% or from dedicated control region measurement).

### Detector and reconstruction

- Jet energy scale and resolution: per-source decomposition.
- Lepton efficiency: trigger, identification, isolation scale factors with uncertainties.
- b-tagging: per-working-point scale factor uncertainties, including light-flavor mistag rate.
- Missing transverse momentum: propagation of JES/JER and unclustered energy.
- Pileup: minimum-bias cross-section variation.

### Theory inputs

- Luminosity uncertainty.
- PDF choice and alpha_s variation.
- Parton shower matching scale.
- Electroweak correction factors where applicable.

## Required validation checks

1. **Closure on MC** -- run full limit-setting procedure on background-only MC pseudo-data. Expected limit must be consistent with Asimov result.
2. **Signal injection recovery** -- inject signal at known strength → verify fitted signal strength recovered within uncertainty.
3. **Nuisance parameter pulls** -- in background-only fits, all nuisance parameters must be within 1 sigma of nominal. Pulls beyond 2 sigma → mismodeled systematic or fit instability.
4. **Goodness of fit** -- saturated model GoF test on background-only pseudo-data. Observed GoF p-value distribution should be approximately uniform.
5. **Look-elsewhere effect** -- if scanning over continuous parameter (e.g. mass), correct for trials factor using method of Gross and Vitells or toy-based global p-value estimation.

## Known pitfalls

### Optimizing on signal region

Tuning selection cuts or MVA thresholds by looking at signal region in data. All optimization must be on MC or control regions before unblinding.

### Undercoverage from profiling

Profiling nuisance parameters can absorb genuine signal if systematic templates = too flexible. Verify with signal injection that profiled systematics do not bias signal strength.

### Background model bias

Using single functional form for smooth background estimate without testing alternatives. Spurious-signal test (fitting signal+background to background-only pseudo-data) must return signal strength consistent with zero.

### Correlated systematics across channels

In combined searches, systematics correlated across channels must be explicitly correlated in statistical model. Treating as uncorrelated → underestimates total uncertainty.
