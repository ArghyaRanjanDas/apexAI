# Fit Model Catalog

## Model Selection Decision Tree

```
Is there a visible peak in the distribution?
|
+-- NO --> Use background-only model (exponential, polynomial)
|
+-- YES --> Is the peak narrow (width < 5% of peak position)?
    |
    +-- NO --> Try Gaussian + background (broad features)
    |
    +-- YES --> Is the peak symmetric?
        |
        +-- YES --> Is the peak from a resonance with natural width?
        |   |
        |   +-- NO --> Gaussian + background
        |   |
        |   +-- YES --> Voigt profile + background
        |        (or Breit-Wigner if resolution << natural width)
        |
        +-- NO --> Crystal Ball + background
             (asymmetric tail from detector effects)
```

## Background Shape Guide

| Observed shape | Model | When to use |
|---|---|---|
| Flat | Constant | Combinatorial backgrounds in narrow windows |
| Falling | Exponential or power law | Most invariant mass distributions above threshold |
| Rising then falling | Phase space function | Near kinematic thresholds |
| Linear trend | Polynomial degree 1 | Slowly varying backgrounds in small windows |

## Model Implementations

### 1. Gaussian + poly1

```python
import numpy as np

def gaussian_poly1(x, amp, mu, sigma, c0, c1):
    """Gaussian signal over linear background."""
    gauss = amp * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
    bg = c0 + c1 * x
    return gauss + bg
```

### 2. Breit-Wigner + poly1

```python
def breitwigner_poly1(x, amp, M, Gamma, c0, c1):
    """Relativistic Breit-Wigner signal over linear background."""
    bw = amp * Gamma**2 / ((x**2 - M**2)**2 + (M * Gamma)**2)
    bg = c0 + c1 * x
    return bw + bg
```

### 3. Voigt + poly1

```python
from scipy.special import voigt_profile

def voigt_poly1(x, amp, mu, sigma, gamma, c0, c1):
    """Voigt profile (Gaussian convolved with Lorentzian) over linear background.
    sigma: Gaussian width (detector resolution)
    gamma: Lorentzian half-width (natural width)
    """
    vp = amp * voigt_profile(x - mu, sigma, gamma)
    bg = c0 + c1 * x
    return vp + bg
```

### 4. Crystal Ball + poly1

```python
def crystalball_poly1(x, amp, mu, sigma, alpha, n, c0, c1):
    """Crystal Ball function over linear background.
    alpha: transition point (in sigma units)
    n: power-law tail exponent
    """
    t = (x - mu) / sigma
    abs_alpha = abs(alpha)
    A = (n / abs_alpha)**n * np.exp(-0.5 * abs_alpha**2)
    B = n / abs_alpha - abs_alpha

    sig = np.where(
        t > -abs_alpha,
        amp * np.exp(-0.5 * t**2),
        amp * A * (B - t)**(-n)
    )
    bg = c0 + c1 * x
    return sig + bg
```

### 5. Double Gaussian + poly1

```python
def double_gaussian_poly1(x, amp1, mu, sigma1, amp2, sigma2, c0, c1):
    """Two Gaussians sharing a mean over linear background.
    Use when single Gaussian residuals show structure.
    """
    g1 = amp1 * np.exp(-0.5 * ((x - mu) / sigma1) ** 2)
    g2 = amp2 * np.exp(-0.5 * ((x - mu) / sigma2) ** 2)
    bg = c0 + c1 * x
    return g1 + g2 + bg
```

### 6. Exponential (background-only)

```python
def exponential_bg(x, A, lam):
    """Falling exponential background. lam should be negative."""
    return A * np.exp(lam * x)
```

## Parameter Estimation from Data

NEVER guess initial parameters from physics knowledge.
Estimate directly from data.

```python
def estimate_parameters(bin_centers, bin_counts):
    """Estimate signal + linear background parameters from histogram data."""

    # Background: average of first and last 10% of bins
    n_side = max(1, len(bin_centers) // 10)
    bg_left = np.mean(bin_counts[:n_side])
    bg_right = np.mean(bin_counts[-n_side:])
    c0_est = bg_left
    c1_est = (bg_right - bg_left) / (bin_centers[-1] - bin_centers[0])

    # Background estimate at each bin
    bg_est = c0_est + c1_est * bin_centers

    # Signal after background subtraction
    signal_est = bin_counts - bg_est

    # Peak position: location of maximum in background-subtracted data
    i_peak = np.argmax(signal_est)
    mu_est = bin_centers[i_peak]

    # Amplitude: height above background at the peak
    amp_est = signal_est[i_peak]

    # Width: full width at half maximum
    half_max = amp_est / 2.0
    above_half = signal_est >= half_max
    if np.any(above_half):
        indices = np.where(above_half)[0]
        fwhm = bin_centers[indices[-1]] - bin_centers[indices[0]]
        sigma_est = fwhm / 2.355  # FWHM = 2.355 * sigma
    else:
        sigma_est = (bin_centers[-1] - bin_centers[0]) / 10.0

    return {
        "amp": amp_est,
        "mu": mu_est,
        "sigma": sigma_est,
        "c0": c0_est,
        "c1": c1_est,
    }
```

## Performing Fit

```python
from scipy.optimize import curve_fit

def perform_fit(model_func, bin_centers, bin_counts, p0):
    """Fit a model to histogram data with proper error handling."""

    # Bin errors: Poisson, with floor of 1 to avoid zero-error bins
    errors = np.sqrt(np.maximum(bin_counts, 1.0))

    popt, pcov = curve_fit(
        model_func,
        bin_centers,
        bin_counts,
        p0=p0,
        sigma=errors,
        absolute_sigma=True,
        maxfev=10000,
    )

    # Parameter uncertainties from covariance diagonal
    perr = np.sqrt(np.diag(pcov))

    # Chi-squared
    residuals = bin_counts - model_func(bin_centers, *popt)
    chi2 = np.sum((residuals / errors) ** 2)
    ndf = len(bin_centers) - len(popt)
    chi2_ndf = chi2 / ndf

    return popt, perr, pcov, chi2_ndf
```

## Fit Quality Assessment

| chi2/ndf | Interpretation | Action |
|---|---|---|
| 0.5 -- 2.0 | Acceptable fit | Report results |
| > 2.0 | Poor fit | Try a more complex model or different background |
| < 0.5 | Suspiciously good | Errors are likely overestimated; review error assignment |

## Iteration Strategy

When fit = unsatisfactory, follow this order:

1. **Try different background shape** -- poly1 → exponential or poly2
2. **Try different signal shape** -- Gaussian → Crystal Ball or Voigt
3. **Restrict fit range** -- exclude regions with unexpected structure
4. **Check for secondary features** -- second peak possible; try double Gaussian

Do not iterate more than 3-4 times on same distribution.
No model gives chi2/ndf in 0.5-2.0 → report best fit, note limitation.

## Anti-Hallucination Rule

**NEVER** set initial parameters from physics knowledge (e.g., "Z boson mass = 91.2 GeV").
Always derive initial estimates from data itself using procedure above.
Physics knowledge = ONLY for hypothesis generation AFTER fit completes.

## Mass Reference Table (for hypothesis generation ONLY)

For interpreting fit results. Do NOT use as fit inputs.

| Particle | Mass (GeV) |
|---|---|
| pi0 | 0.135 |
| eta | 0.548 |
| rho | 0.775 |
| omega | 0.783 |
| phi | 1.019 |
| J/psi | 3.097 |
| psi(2S) | 3.686 |
| Upsilon(1S) | 9.460 |
| Upsilon(2S) | 10.023 |
| Upsilon(3S) | 10.355 |
| Z boson | 91.188 |
| W boson | 80.377 |
| Higgs boson | 125.25 |
| top quark | 172.69 |
