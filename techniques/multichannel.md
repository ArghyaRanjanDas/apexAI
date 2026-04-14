# Multi-Channel Analysis

## Overview

A multi-channel analysis splits events into orthogonal categories (channels) that are analyzed independently and then combined for maximum sensitivity. Each channel targets a distinct final state or kinematic regime.

## Phase 1: Channel Decomposition

- Enumerate all orthogonal channels based on the decay modes or event topologies under study
- Define the signal region for each channel with non-overlapping selection criteria
- Verify orthogonality: no event should appear in more than one channel
- Document the expected signal composition and dominant backgrounds for each channel

## Phase 2-3: Per-Channel Analysis

Each channel proceeds through variable survey, selection optimization, and background estimation independently:

- **Variable survey:** Identify the most discriminating variables for each channel separately, since different backgrounds dominate in different channels
- **Selection optimization:** Optimize cuts or BDT working points per channel to maximize that channel's sensitivity
- **Background estimation:** Use channel-appropriate methods (sideband, ABCD, template fits) since background compositions differ across channels

## Shared Sub-Analyses

Some calibrations and measurements apply across multiple channels and should be performed once:

- **b-tagging efficiency:** Measured in dedicated control regions, applied as scale factors to all channels using b-jets
- **Lepton identification scale factors:** Tag-and-probe measurements in Z->ll events, applied to all channels with that lepton flavor
- **Trigger efficiency:** Measured per trigger path, shared by all channels using the same trigger
- **Jet energy corrections:** Common calibration applied uniformly

These shared calibrations reduce redundant work and ensure consistency.

## Phase 4: Statistical Combination

Combine all channels into a single statistical model:

- Build a joint likelihood as the product of per-channel likelihoods
- The signal strength parameter (mu) is shared across all channels
- Each channel contributes its own set of observed data, signal expectation, and background expectation
- The combined sensitivity is greater than any single channel alone

```
L_combined(mu, theta) = product over channels c of L_c(mu, theta_c, theta_shared)
```

where theta_c are channel-specific nuisance parameters and theta_shared are correlated nuisance parameters.

### Building a joint model with pyhf

```python
import pyhf
import numpy as np

# Per-channel observed data and expectations
channels = {
    "tauhtauh": {
        "data": [15, 22, 18, 12],
        "signal": [3.2, 5.1, 4.0, 2.1],
        "background": [11.5, 17.0, 14.2, 10.0],
    },
    "taumutauh": {
        "data": [8, 14, 10],
        "signal": [1.8, 3.2, 2.0],
        "background": [6.5, 11.0, 8.2],
    },
}

# Build multi-channel workspace
spec = {
    "channels": [],
    "observations": [],
    "measurements": [
        {
            "name": "combined_fit",
            "config": {
                "poi": "mu",
                "parameters": [
                    # Correlated: same modifier name across channels
                    {"name": "lumi", "bounds": [[0.9, 1.1]]},
                    {"name": "jes", "bounds": [[0.8, 1.2]]},
                ],
            },
        }
    ],
    "version": "1.0.0",
}

for ch_name, ch_data in channels.items():
    n_bins = len(ch_data["data"])
    spec["channels"].append(
        {
            "name": ch_name,
            "samples": [
                {
                    "name": "signal",
                    "data": ch_data["signal"],
                    "modifiers": [
                        {"name": "mu", "type": "normfactor", "data": None},
                        # Correlated across channels (same name)
                        {"name": "lumi", "type": "normsys",
                         "data": {"hi": 1.02, "lo": 0.98}},
                    ],
                },
                {
                    "name": "background",
                    "data": ch_data["background"],
                    "modifiers": [
                        # Correlated: jet energy scale
                        {"name": "jes", "type": "normsys",
                         "data": {"hi": 1.05, "lo": 0.95}},
                        # Uncorrelated: per-channel bkg norm
                        {"name": f"bkg_norm_{ch_name}", "type": "normsys",
                         "data": {"hi": 1.10, "lo": 0.90}},
                        # Uncorrelated: MC stat per bin
                        {"name": f"staterror_{ch_name}",
                         "type": "staterror",
                         "data": [np.sqrt(b) for b in ch_data["background"]]},
                    ],
                },
            ],
        }
    )
    spec["observations"].append(
        {"name": ch_name, "data": ch_data["data"]}
    )

ws = pyhf.Workspace(spec)
model = ws.model()
data = ws.data(model)
```

### Fitting and extracting results

```python
# Maximum likelihood fit
pyhf.set_backend("numpy", "minuit")
result = pyhf.infer.mle.fit(data, model, return_uncertainties=True)
bestfit, uncertainties = result

poi_index = model.config.poi_index
mu_hat = bestfit[poi_index]
mu_err = uncertainties[poi_index]
log.info(f"Combined mu = {mu_hat:.3f} +/- {mu_err:.3f}")

# Expected and observed upper limits (CLs)
obs_limit, exp_limit_band = pyhf.infer.hypotest(
    1.0, data, model, test_stat="qtilde", return_expected_set=True
)
```

## Correlated vs. Uncorrelated Systematics

Correctly classifying systematic uncertainties as correlated or uncorrelated across channels is essential for a valid combination.

**Correlated (shared nuisance parameter across channels):**
- Luminosity uncertainty -- affects all channels equally
- Theory cross-section uncertainties -- same for all channels of the same process
- Jet energy scale -- common calibration
- b-tagging scale factors -- same measurement applied everywhere
- PDF uncertainties -- same source affects all channels

**Uncorrelated (independent nuisance parameter per channel):**
- Channel-specific background normalization -- different control regions
- Statistical uncertainty of MC templates -- independent per channel
- Channel-specific trigger efficiency -- different trigger paths
- Data-driven background estimates -- method is channel-dependent

Misclassifying a correlated systematic as uncorrelated will underestimate the combined uncertainty. Misclassifying an uncorrelated systematic as correlated will overestimate it.

## Channel Consistency Check

Before combining, verify that per-channel results are compatible:

- Fit each channel independently and extract the signal strength (mu) with its uncertainty
- Per-channel results should be statistically compatible within their uncertainties
- Compute a compatibility chi-squared: chi2 = sum_c ((mu_c - mu_combined) / sigma_c)^2
- A large chi2 (p-value < 0.05) indicates tension between channels that must be investigated before combination
- Possible causes of tension: mismodeled backgrounds in one channel, incorrect systematic correlations, signal model issues

Only proceed with the combination after the consistency check passes.

### Per-channel fit and compatibility test

```python
from scipy import stats

# Fit each channel independently
per_channel_mu = {}
for ch_name in channels:
    ch_ws = ws.prune(channels=[ch_name])  # single-channel workspace
    ch_model = ch_ws.model()
    ch_data = ch_ws.data(ch_model)
    ch_result = pyhf.infer.mle.fit(
        ch_data, ch_model, return_uncertainties=True
    )
    ch_bestfit, ch_unc = ch_result
    poi_idx = ch_model.config.poi_index
    per_channel_mu[ch_name] = (ch_bestfit[poi_idx], ch_unc[poi_idx])
    log.info(f"  {ch_name}: mu = {ch_bestfit[poi_idx]:.3f} "
             f"+/- {ch_unc[poi_idx]:.3f}")

# Compatibility chi-squared
chi2 = sum(
    ((mu - mu_hat) / sigma) ** 2
    for mu, sigma in per_channel_mu.values()
)
ndf = len(per_channel_mu) - 1
p_value = stats.chi2.sf(chi2, ndf)
log.info(f"Compatibility: chi2/ndf = {chi2:.1f}/{ndf}, p = {p_value:.3f}")

if p_value < 0.05:
    log.warning("Channel tension detected (p < 0.05). "
                "Investigate before combining.")
```

### Combined significance

```python
# Discovery significance (background-only hypothesis)
obs_p = pyhf.infer.hypotest(
    0.0, data, model,
    test_stat="q0",
    return_expected=False,
)
significance = stats.norm.isf(obs_p)
log.info(f"Observed significance: {significance:.2f} sigma")
```
