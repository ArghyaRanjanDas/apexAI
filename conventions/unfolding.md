# Unfolding / detector correction conventions

## When this applies

Any analysis correcting measured distribution from detector level to particle level (or parton level). Includes differential cross-section measurements, normalized distributions, double-differential spectra. Applies regardless of correction method: bin-by-bin factors, matrix inversion, iterative Bayesian, SVD, or ML-based.

## Standard configuration

- **Particle-level definition**: must be stated explicitly with complete object and phase-space definition before any correction applied. Fiducial definition should be close to detector-level selection → minimize model dependence.
- **Correction procedure**: default = regularized matrix inversion. Second independent method (e.g. iterative Bayesian or bin-by-bin) required as cross-check. If two methods disagree by more than half statistical uncertainty in any bin → investigate before proceeding.
- **Covariance matrix**: full statistical covariance matrix of unfolded result must be provided. Construct from pseudo-experiments (bootstrap or toy MC), not from diagonal of response matrix alone.
- **Regularization**: strength chosen by data-driven criterion (e.g. L-curve, minimizing average global correlation coefficient). Choice and sensitivity must be documented.

## Required systematic sources

- **Response matrix statistics**: finite MC sample size in each cell. Propagate via bootstrap of response matrix.
- **Physics model dependence**: reweight MC used to build response matrix to alternative truth spectrum → repeat unfolding. Difference = systematic.
- **Detector systematics**: JES, JER, lepton scale factors, b-tagging, pileup -- propagate each through full unfolding chain (not just efficiency correction).
- **Background subtraction**: vary each background within its uncertainty before unfolding → propagate effect.
- **Regularization strength**: vary regularization parameter within reasonable range → include variation as systematic.

## Quality gates

1. **Closure test** -- unfold MC detector-level distribution using response matrix from same MC. Unfolded result must match particle-level truth within statistical precision. Validates machinery only.
2. **Stress test** -- reweight MC truth to significantly different shape (e.g. multiply by linear slope) → verify unfolding recovers reweighted truth. Tests sensitivity to model assumptions.
3. **Prior dependence** -- for iterative methods, vary prior (number of iterations, initial spectrum shape) → verify result stable. For matrix methods = varying regularization.
4. **Covariance validation** -- draw pseudo-experiments from unfolded result and its covariance matrix, refold them → verify chi2 distribution with original detector-level data = consistent with expectations.
5. **Data/MC input validation** -- before unfolding, compare detector-level data with folded MC prediction in every bin. Large disagreements (beyond total systematic envelope) → response matrix may be unreliable in that region.

## Known pitfalls

### Normalizing before correcting

Normalizing detector-level distribution before applying unfolding. Normalization changes statistical correlations → invalidates response matrix. Always unfold absolute distribution first, then normalize unfolded result.

### Confusing closure with validation

Closure test success only proves linear algebra works. Does not validate that response matrix = appropriate for data. Stress test = actual validation.

### Flat systematic estimates

Assigning flat (bin-independent) systematic uncertainty to correction that is strongly bin-dependent. Each source must be evaluated bin-by-bin through full unfolding chain.

### Double-counting model dependence

Using same MC variation to assess both response matrix systematic and background subtraction systematic. Same variation propagated through different parts of chain. Choose one path, document it.

### Wrong matching strategy

Using response matrix built with different particle-level object matching strategy (e.g. geometric vs ghost-matching for jets) than what fiducial definition implies. Matching in response matrix must be consistent with published fiducial definition.
