# Statistical Methods

## Significance and Hypothesis Testing

In HEP, a measurement tests the null hypothesis H0 (background only) against an alternative H1 (signal + background).

- **p-value**: probability of observing data at least as extreme as measured, assuming H0 is true
- **Significance (sigma)**: number of standard deviations in a one-sided Gaussian tail corresponding to the p-value

### Conventions

| Threshold | Sigma | p-value | Meaning |
|---|---|---|---|
| Evidence | 3.0 | 1.35e-3 | Interesting but not conclusive |
| Observation/Discovery | 5.0 | 2.87e-7 | Established beyond reasonable doubt |

### Conversion Code

```python
from scipy.stats import norm

def p_to_sigma(p):
    """Convert p-value to significance in sigma (one-sided)."""
    return norm.isf(p)  # inverse survival function

def sigma_to_p(sigma):
    """Convert significance in sigma to p-value (one-sided)."""
    return norm.sf(sigma)  # survival function = 1 - CDF
```

## Likelihood Ratio Test (Wilks' Theorem)

When comparing nested models (H0 is a special case of H1), the test statistic is:

q = 2 * (NLL_H0 - NLL_H1)

where NLL is the negative log-likelihood. Under H0, q is asymptotically chi2-distributed with degrees of freedom equal to the difference in number of parameters.

```python
from scipy.stats import chi2

def likelihood_ratio_test(nll_h0, nll_h1, delta_npar):
    """Likelihood ratio test using Wilks' theorem.
    nll_h0: negative log-likelihood of null model
    nll_h1: negative log-likelihood of alternative model
    delta_npar: number of additional parameters in H1
    """
    q = 2.0 * (nll_h0 - nll_h1)
    p_value = chi2.sf(q, delta_npar)
    return q, p_value
```

## Counting Significance (Asimov Approximation)

For counting experiments where you observe s signal events over b background events, use the Asimov formula instead of naive s/sqrt(b):

```python
import numpy as np

def asimov_significance(s, b):
    """Asimov significance for counting experiment.
    More accurate than s/sqrt(b) when s is not << b.
    Returns significance in sigma.
    """
    if b <= 0 or s <= 0:
        return 0.0
    q = 2.0 * ((s + b) * np.log(1.0 + s / b) - s)
    return np.sqrt(q)
```

Note: s/sqrt(b) is the limiting case when s << b. Always prefer the Asimov formula.

## Look-Elsewhere Effect

When searching over a range for a signal, the probability of finding a fluctuation anywhere is higher than at a specific pre-defined location.

```python
def global_significance(local_p, search_range, resolution):
    """Approximate global significance accounting for look-elsewhere effect.

    local_p: p-value at the most significant point
    search_range: total range searched (e.g., mass window in GeV)
    resolution: typical signal width (e.g., detector resolution in GeV)
    """
    n_independent_trials = search_range / resolution
    global_p = 1.0 - (1.0 - local_p) ** n_independent_trials
    # For small local_p, this simplifies to:
    # global_p ~ local_p * n_independent_trials
    return global_p
```

The number of independent trials is approximate. For a rigorous treatment, see the Gross-Vitells method (Eur.Phys.J. C70 (2010) 525) which uses the upcrossing approach.

## Confidence Intervals

### From Fit Covariance (Symmetric)

```python
import numpy as np

def symmetric_confidence_interval(popt, pcov, param_index, cl=0.6827):
    """Confidence interval from fit covariance matrix.
    cl: confidence level (0.6827 for 1-sigma, 0.9545 for 2-sigma)
    """
    from scipy.stats import norm
    n_sigma = norm.isf((1.0 - cl) / 2.0)
    val = popt[param_index]
    err = np.sqrt(pcov[param_index, param_index])
    return val - n_sigma * err, val + n_sigma * err
```

### Profile Likelihood (Asymmetric)

When errors are asymmetric, scan the negative log-likelihood as a function of the parameter of interest, profiling (minimizing) over all other parameters.

```python
def profile_likelihood_interval(nll_func, best_val, scan_range, npoints=200, cl=0.6827):
    """Profile likelihood confidence interval.

    nll_func: function of parameter of interest returning profiled NLL
    best_val: best-fit value of parameter
    scan_range: (low, high) range to scan
    npoints: number of scan points

    Thresholds (delta NLL from minimum):
      68% CL: 0.5  (1-sigma)
      95% CL: 1.92 (approximately chi2.isf(0.05, 1) / 2)
    """
    from scipy.stats import chi2
    threshold = chi2.isf(1.0 - cl, 1) / 2.0
    # threshold = 0.5 for 68%, 1.92 for 95%

    vals = np.linspace(scan_range[0], scan_range[1], npoints)
    nlls = np.array([nll_func(v) for v in vals])
    nll_min = np.min(nlls)
    delta_nll = nlls - nll_min

    # Find crossings
    inside = delta_nll <= threshold
    if not np.any(inside):
        return None, None
    indices = np.where(inside)[0]
    return vals[indices[0]], vals[indices[-1]]
```

### Bootstrap (Model-Free)

```python
def bootstrap_confidence_interval(data, statistic_func, n_bootstrap=1000, cl=0.6827):
    """Bootstrap confidence interval for any statistic.

    data: array of observations
    statistic_func: function(data) -> scalar statistic
    """
    n = len(data)
    bootstrap_stats = np.empty(n_bootstrap)
    for i in range(n_bootstrap):
        resample = data[np.random.randint(0, n, size=n)]
        bootstrap_stats[i] = statistic_func(resample)

    alpha = (1.0 - cl) / 2.0
    lo = np.percentile(bootstrap_stats, 100 * alpha)
    hi = np.percentile(bootstrap_stats, 100 * (1.0 - alpha))
    return lo, hi
```

## Upper Limits

### CLs Method (Standard HEP)

```python
def cls_upper_limit(observed, background, signal_scale_range=(0, 10), npoints=100, cl=0.95):
    """CLs upper limit on signal strength.
    Scan signal strength mu, compute CLs = p_{s+b} / p_b.
    Exclude mu where CLs < 1 - cl.
    """
    from scipy.stats import poisson

    mu_values = np.linspace(signal_scale_range[0], signal_scale_range[1], npoints)
    cls_values = np.empty(npoints)

    for i, mu in enumerate(mu_values):
        expected_sb = background + mu
        expected_b = background

        # p_{s+b}: probability of observing <= observed under s+b hypothesis
        p_sb = poisson.cdf(observed, expected_sb)
        # p_b: probability of observing <= observed under b-only hypothesis
        p_b = poisson.cdf(observed, expected_b)

        cls_values[i] = p_sb / max(p_b, 1e-15)

    # Find where CLs crosses 1 - cl
    target = 1.0 - cl
    crossings = np.where(cls_values < target)[0]
    if len(crossings) == 0:
        return mu_values[-1]  # limit beyond scan range
    return mu_values[crossings[0]]
```

### Bayesian with Flat Prior

```python
def bayesian_upper_limit(observed, background, mu_max=20.0, npoints=1000, cl=0.95):
    """Bayesian upper limit with flat prior on signal strength."""
    from scipy.stats import poisson

    mu_values = np.linspace(0, mu_max, npoints)
    # Likelihood: Poisson(observed | mu + background)
    likelihood = poisson.pmf(observed, mu_values + background)
    # Flat prior, so posterior proportional to likelihood
    posterior = likelihood / np.trapz(likelihood, mu_values)
    # Cumulative posterior
    cdf = np.cumsum(posterior) * (mu_values[1] - mu_values[0])
    # Find mu where CDF reaches cl
    idx = np.searchsorted(cdf, cl)
    if idx >= len(mu_values):
        return mu_values[-1]
    return mu_values[idx]
```

## Goodness of Fit

### Chi-Squared Test

```python
from scipy.stats import chi2

def chi2_goodness_of_fit(observed, expected, npar):
    """Chi-squared goodness of fit.
    observed: array of observed bin counts
    expected: array of expected bin counts from model
    npar: number of fitted parameters
    """
    errors = np.sqrt(np.maximum(expected, 1.0))
    chi2_val = np.sum(((observed - expected) / errors) ** 2)
    ndf = len(observed) - npar
    chi2_ndf = chi2_val / ndf
    p_value = chi2.sf(chi2_val, ndf)
    return chi2_val, ndf, chi2_ndf, p_value
```

| chi2/ndf | Interpretation |
|---|---|
| ~1.0 | Good fit |
| > 2.0 | Poor fit; model does not describe data |
| < 0.5 | Suspiciously good; errors likely overestimated |

### Kolmogorov-Smirnov Test

```python
from scipy.stats import ks_2samp

def ks_test(data1, data2):
    """Two-sample KS test. Returns (statistic, p-value).
    p-value > 0.05: cannot reject that samples come from same distribution.
    """
    return ks_2samp(data1, data2)
```

## Error Propagation

### Analytic (Jacobian Method)

If a derived quantity f depends on fitted parameters theta with covariance C, then:

Var(f) = J @ C @ J^T

where J is the Jacobian (partial derivatives of f with respect to theta).

```python
def propagate_errors_analytic(jacobian, covariance):
    """Propagate errors through a function using the Jacobian.

    jacobian: array of shape (n_outputs, n_params), partial derivatives df_i/dtheta_j
    covariance: array of shape (n_params, n_params), parameter covariance matrix

    Returns: covariance matrix of shape (n_outputs, n_outputs) for derived quantities
    """
    J = np.atleast_2d(jacobian)
    return J @ covariance @ J.T
```

### Numerical (Toy MC)

When the function is complex or non-linear, sample parameter variations from the covariance matrix.

```python
def propagate_errors_toys(func, popt, pcov, n_toys=1000):
    """Propagate errors by sampling parameter variations.

    func: function(params) -> scalar or array
    popt: best-fit parameters
    pcov: parameter covariance matrix
    """
    samples = np.random.multivariate_normal(popt, pcov, size=n_toys)
    results = np.array([func(s) for s in samples])
    return np.mean(results, axis=0), np.std(results, axis=0)
```

## Systematic Uncertainties

### Evaluation Procedure

For each systematic source:

1. Vary the source by +1 sigma and -1 sigma from its nominal value
2. Re-run the full analysis chain with the varied input
3. Take the difference from the nominal result as the systematic uncertainty

### Combining Systematics

```python
def combine_systematics(syst_list):
    """Combine independent systematic uncertainties in quadrature.
    syst_list: list of (up_variation, down_variation) tuples
    Returns: (total_up, total_down)
    """
    up = np.sqrt(sum(max(u, 0)**2 for u, d in syst_list))
    down = np.sqrt(sum(min(d, 0)**2 for u, d in syst_list))
    return up, -down
```

### Common Systematic Sources in HEP

| Source | Typical size | Notes |
|---|---|---|
| Energy/momentum scale | 1-2% | Shift reconstructed energies up/down |
| Energy/momentum resolution | 1-5% | Smear reconstructed energies by additional amount |
| Selection efficiency | ~20% | Vary selection cuts; use data-driven scale factors |
| Background model | varies | Try alternative background parameterizations |
| Luminosity | 1-3% | Affects all rate measurements equally |
| Fit range | varies | Repeat fit with modified range boundaries |
| Binning | varies | Repeat analysis with different bin widths |
| Pileup | 1-5% | Vary pileup reweighting |
| PDF uncertainty | 1-5% | Use PDF error sets |
