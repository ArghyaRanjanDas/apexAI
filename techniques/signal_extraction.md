# Signal Extraction Methods

## Method Selection Guide

| Situation | Recommended method | Section |
|---|---|---|
| Localized feature in smooth spectrum | Sideband estimation | 1 |
| Natural control sample available | Control sample subtraction | 2 |
| Two uncorrelated discriminating variables | ABCD method | 3 |
| Known shapes for signal and background components | Template decomposition | 4 |
| None of the above apply | Fit-based extraction | 5 |

When in doubt, apply multiple methods and check that they give consistent results. Disagreement between methods reveals systematic effects.

---

## 1. Sideband Estimation

Estimate the background under a signal peak using data from adjacent regions (sidebands) where signal contamination is negligible.

**Procedure:**
1. Define signal region around the feature of interest
2. Define sideband regions on both sides, away from the signal
3. Fit or interpolate the background shape using sideband data
4. Extrapolate the background into the signal region
5. Subtract the estimated background from data in the signal region

```python
import numpy as np
from scipy.optimize import curve_fit

def sideband_subtraction(bin_centers, bin_counts, signal_window, sideband_windows):
    """Estimate and subtract background using sidebands.

    bin_centers: array of bin center positions
    bin_counts: array of counts per bin
    signal_window: (low, high) defining signal region
    sideband_windows: list of (low, high) tuples defining sideband regions
    """
    # Select sideband bins
    sideband_mask = np.zeros(len(bin_centers), dtype=bool)
    for lo, hi in sideband_windows:
        sideband_mask |= (bin_centers >= lo) & (bin_centers <= hi)

    x_sb = bin_centers[sideband_mask]
    y_sb = bin_counts[sideband_mask]

    # Fit background model to sidebands (linear example)
    def bg_model(x, c0, c1):
        return c0 + c1 * x

    popt, _ = curve_fit(bg_model, x_sb, y_sb, sigma=np.sqrt(np.maximum(y_sb, 1.0)))

    # Extrapolate into signal region
    bg_estimate = bg_model(bin_centers, *popt)

    # Signal = data - background
    signal = bin_counts - bg_estimate

    # Signal region mask
    sig_mask = (bin_centers >= signal_window[0]) & (bin_centers <= signal_window[1])

    return signal, bg_estimate, sig_mask
```

**Requirements:**
- Sidebands must be free of signal contamination
- Background shape must be smooth enough to interpolate reliably
- Sidebands should be on both sides of the signal region when possible

---

## 2. Control Sample Subtraction

Subtract a control sample that captures the background but not the signal.

**Cross-domain examples:**

| Domain | Signal sample | Control sample | What cancels |
|---|---|---|---|
| HEP (di-lepton) | Opposite-sign lepton pairs (OS) | Same-sign lepton pairs (SS) | Combinatorial/fake backgrounds |
| HEP (isolation) | Isolated leptons | Anti-isolated leptons | QCD multijet |
| Astronomy | On-source region | Off-source region | Instrumental + sky background |
| Genomics | Treated sample | Untreated control | Baseline expression |

```python
def control_subtraction(data_signal, data_control, scale_factor=1.0):
    """Subtract scaled control sample from signal sample.

    data_signal: array of counts in signal sample bins
    data_control: array of counts in control sample bins
    scale_factor: normalization ratio (e.g., from sideband normalization)

    Returns: background-subtracted signal, statistical error
    """
    subtracted = data_signal - scale_factor * data_control
    # Error: quadrature sum of Poisson errors
    error = np.sqrt(data_signal + scale_factor**2 * data_control)
    return subtracted, error
```

**Requirements:**
- Control sample must have the same background composition as the signal sample
- Signal contamination in the control sample must be negligible
- The scale factor must be determined from a signal-free region or from first principles

---

## 3. ABCD Method

Estimate background in a signal region using two uncorrelated discriminating variables to define four regions in a 2D plane.

```
         Variable Y
            |
     B      |      A (signal region)
            |
   ---------+----------
            |
     C      |      D
            |
        Variable X
```

The key relation: if X and Y are uncorrelated for background,

    N_D_background = N_B * N_C / N_A_background

Equivalently, the background in the signal region A is:

    N_A_background = N_B * N_D / N_C

```python
def abcd_method(n_a_observed, n_b, n_c, n_d):
    """ABCD background estimation.

    n_a_observed: observed events in signal region A
    n_b, n_c, n_d: observed events in control regions B, C, D

    Returns: estimated background in A, signal estimate, statistical error on background
    """
    if n_c == 0:
        raise ValueError("Region C has zero events; ABCD method undefined")

    bg_estimate = n_b * n_d / n_c

    # Error propagation (Poisson errors on B, C, D)
    # d(bg)/dB = D/C, d(bg)/dC = -B*D/C^2, d(bg)/dD = B/C
    dbg_dB = n_d / n_c
    dbg_dC = -n_b * n_d / n_c**2
    dbg_dD = n_b / n_c
    bg_error = np.sqrt(dbg_dB**2 * n_b + dbg_dC**2 * n_c + dbg_dD**2 * n_d)

    signal_estimate = n_a_observed - bg_estimate

    return bg_estimate, signal_estimate, bg_error
```

**Critical requirement:** You MUST verify that the two variables X and Y are uncorrelated in background-dominated samples before using this method. Check correlation in simulation or in a control region. If X and Y are correlated, the estimate will be biased.

---

## 4. Template Decomposition

Decompose observed data into a weighted sum of shape templates (e.g., from simulation or control samples), fitting the normalizations.

The data histogram is modeled as:

    data_i = sum_j (f_j * template_j_i)

where f_j are the fractions/normalizations to be fitted, and template_j_i is the expected count from component j in bin i.

```python
from scipy.optimize import minimize

def template_fit(data, templates, template_names=None):
    """Fit data as a sum of shape templates using Poisson likelihood.

    data: array of observed counts per bin
    templates: list of arrays, each an expected-count template (same binning as data)
    template_names: optional list of names for each template

    Returns: fitted fractions, covariance matrix
    """
    n_templates = len(templates)
    templates = [np.asarray(t, dtype=float) for t in templates]

    def neg_log_likelihood(fracs):
        """Poisson negative log-likelihood."""
        fracs_pos = np.abs(fracs)  # enforce positive fractions
        expected = sum(f * t for f, t in zip(fracs_pos, templates))
        expected = np.maximum(expected, 1e-10)  # avoid log(0)
        # -sum(data * log(expected) - expected)
        return -np.sum(data * np.log(expected) - expected)

    # Initial guess: equal fractions normalized to data
    total_data = np.sum(data)
    f0 = np.full(n_templates, total_data / n_templates / np.mean([np.sum(t) for t in templates]))

    result = minimize(neg_log_likelihood, f0, method="L-BFGS-B")
    fracs_fit = np.abs(result.x)

    # Covariance from inverse Hessian
    from scipy.optimize import approx_fprime
    def hessian_diag(x):
        eps = 1e-5
        h = np.zeros((len(x), len(x)))
        for i in range(len(x)):
            def fi(xi):
                xc = x.copy()
                xc[i] = xi
                return neg_log_likelihood(xc)
            for j in range(i, len(x)):
                def fj(xj):
                    xc = x.copy()
                    xc[j] = xj
                    return neg_log_likelihood(xc)
                # Numerical second derivative
                h[i, j] = (neg_log_likelihood(x + eps * (np.eye(len(x))[i] + np.eye(len(x))[j]))
                           - neg_log_likelihood(x + eps * np.eye(len(x))[i])
                           - neg_log_likelihood(x + eps * np.eye(len(x))[j])
                           + neg_log_likelihood(x)) / eps**2
                h[j, i] = h[i, j]
        return h

    hess = hessian_diag(fracs_fit)
    try:
        cov = np.linalg.inv(hess)
    except np.linalg.LinAlgError:
        cov = np.full((n_templates, n_templates), np.nan)

    return fracs_fit, cov
```

**Requirements:**
- Templates must represent the actual shapes of each component (from simulation or data-driven methods)
- Templates should be normalized to unit area or to expected yields before fitting
- Check that the fitted fractions are physically reasonable (non-negative, sum makes sense)

---

## 5. Fit-Based Extraction

Fit the observed distribution with a signal + background model and extract the signal yield from the fit parameters.

This is described in detail in [techniques/fitting.md](fitting.md).

The signal yield is obtained by integrating the signal component of the fitted model:

```python
def extract_signal_yield(signal_func, popt_signal, x_range, n_points=1000):
    """Integrate the signal component to get the yield.

    signal_func: the signal-only part of the model (e.g., Gaussian without background)
    popt_signal: parameters for the signal function
    x_range: (low, high) integration range
    """
    x = np.linspace(x_range[0], x_range[1], n_points)
    y = signal_func(x, *popt_signal)
    yield_est = np.trapz(y, x)
    return yield_est
```

**Requirements:**
- The model must describe the data well (check chi2/ndf; see fitting.md)
- Signal and background components must be clearly separable in the model
- Report the signal yield with its uncertainty from the fit covariance

---

## General Principles

- **Blinding:** In searches, finalize the analysis strategy on simulation or sidebands BEFORE looking at data in the signal region.
- **Closure tests:** Apply the method to simulation where the true signal is known, and verify that the extracted signal matches the truth.
- **Cross-checks:** Use at least two methods when feasible. If results disagree, investigate the source of the discrepancy before choosing one.
