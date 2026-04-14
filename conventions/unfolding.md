# Unfolding / detector correction conventions

## When this applies

Any analysis that corrects a measured distribution from detector level
to particle level (or parton level). Includes differential cross-section
measurements, normalized distributions, and double-differential spectra.
Applies regardless of whether the correction uses bin-by-bin factors,
matrix inversion, iterative Bayesian, SVD, or ML-based methods.

## Standard configuration

- **Particle-level definition**: must be stated explicitly with a
  complete object and phase-space definition before any correction is
  applied. This fiducial definition should be close to the detector-level
  selection to minimize model dependence.
- **Correction procedure**: the default is regularized matrix inversion.
  A second independent method (e.g. iterative Bayesian or bin-by-bin)
  must be performed as a cross-check. If the two methods disagree by more
  than half the statistical uncertainty in any bin, investigate before
  proceeding.
- **Covariance matrix**: the full statistical covariance matrix of the
  unfolded result must be provided. Construct it from pseudo-experiments
  (bootstrap or toy MC), not from the diagonal of the response matrix
  alone.
- **Regularization**: the regularization strength must be chosen by a
  data-driven criterion (e.g. L-curve, minimizing the average global
  correlation coefficient). The choice and its sensitivity must be
  documented.

## Required systematic sources

- **Response matrix statistics**: finite MC sample size in each cell of
  the response matrix. Propagate via bootstrap of the response matrix.
- **Physics model dependence**: reweight the MC used to build the
  response matrix to an alternative truth spectrum and repeat the
  unfolding. The difference is a systematic.
- **Detector systematics**: JES, JER, lepton scale factors, b-tagging,
  pileup -- propagate each through the full unfolding chain (not just
  through the efficiency correction).
- **Background subtraction**: vary each background within its uncertainty
  before unfolding and propagate the effect.
- **Regularization strength**: vary the regularization parameter within
  a reasonable range and include the variation as a systematic.

## Quality gates

1. **Closure test** -- unfold the MC detector-level distribution using
   the response matrix built from the same MC. The unfolded result must
   match the particle-level truth within statistical precision. This
   validates the machinery only.
2. **Stress test** -- reweight the MC truth to a significantly different
   shape (e.g. multiply by a linear slope) and verify the unfolding
   recovers the reweighted truth. This tests sensitivity to model
   assumptions.
3. **Prior dependence** -- for iterative methods, vary the prior (number
   of iterations, initial spectrum shape) and verify the result is stable.
   For matrix methods, this corresponds to varying the regularization.
4. **Covariance validation** -- draw pseudo-experiments from the unfolded
   result and its covariance matrix, refold them, and verify the chi2
   distribution with the original detector-level data is consistent with
   expectations.
5. **Data/MC input validation** -- before unfolding, compare the
   detector-level data with the folded MC prediction in every bin. Large
   disagreements (beyond the total systematic envelope) indicate that
   the response matrix may be unreliable in that region.

## Known pitfalls

### Normalizing before correcting

Normalizing the detector-level distribution before applying the
unfolding. Normalization changes the statistical correlations and
invalidates the response matrix. Always unfold the absolute
distribution first, then normalize the unfolded result.

### Confusing closure with validation

A closure test that succeeds only proves the linear algebra works. It
does not validate that the response matrix is appropriate for the data.
The stress test is the actual validation.

### Flat systematic estimates

Assigning a flat (bin-independent) systematic uncertainty to a
correction that is strongly bin-dependent. Each source must be
evaluated bin-by-bin through the full unfolding chain.

### Double-counting model dependence

Using the same MC variation to assess both the response matrix
systematic and the background subtraction systematic. These are the
same variation propagated through different parts of the chain. Choose
one path and document it.

### Wrong matching strategy

Using a response matrix built with a different particle-level object
matching strategy (e.g. geometric vs ghost-matching for jets) than what
the fiducial definition implies. The matching in the response matrix
must be consistent with the published fiducial definition.
