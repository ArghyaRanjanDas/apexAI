# Multi-Channel Analysis

## Overview

Multi-channel analysis splits events into orthogonal categories (channels), analyzed independently then combined for maximum sensitivity. Each channel targets distinct final state or kinematic regime.

## Phase 1: Channel Decomposition

- Enumerate all orthogonal channels based on decay modes or event topologies
- Define signal region for each channel with non-overlapping selection criteria
- Verify orthogonality: no event in more than one channel
- Document expected signal composition and dominant backgrounds per channel

## Phase 2-3: Per-Channel Analysis

Each channel proceeds through variable survey, selection optimization, background estimation independently:

- **Variable survey:** Identify most discriminating variables per channel separately; different backgrounds dominate in different channels
- **Selection optimization:** Optimize cuts or BDT working points per channel → maximize that channel's sensitivity
- **Background estimation:** Use channel-appropriate methods (sideband, ABCD, template fits); background compositions differ across channels

## Shared Sub-Analyses

Some calibrations apply across multiple channels → perform once:

- **b-tagging efficiency:** Measured in dedicated control regions, applied as scale factors to all channels using b-jets
- **Lepton identification scale factors:** Tag-and-probe in Z->ll events, applied to all channels with that lepton flavor
- **Trigger efficiency:** Measured per trigger path, shared by all channels using same trigger
- **Jet energy corrections:** Common calibration applied uniformly

Shared calibrations → reduced redundancy, ensured consistency.

## Phase 4: Statistical Combination

Combine all channels into single statistical model:

- Build joint likelihood = product of per-channel likelihoods
- Signal strength parameter (mu) shared across all channels
- Each channel contributes own observed data, signal expectation, background expectation
- Combined sensitivity > any single channel alone

```
L_combined(mu, theta) = product over channels c of L_c(mu, theta_c, theta_shared)
```

theta_c = channel-specific nuisance parameters, theta_shared = correlated nuisance parameters.

### Building joint model with pyhf

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

Correctly classifying systematic uncertainties as correlated or uncorrelated across channels = essential for valid combination.

**Correlated (shared nuisance parameter across channels):**
- Luminosity uncertainty -- affects all channels equally
- Theory cross-section uncertainties -- same for all channels of same process
- Jet energy scale -- common calibration
- b-tagging scale factors -- same measurement applied everywhere
- PDF uncertainties -- same source affects all channels

**Uncorrelated (independent nuisance parameter per channel):**
- Channel-specific background normalization -- different control regions
- Statistical uncertainty of MC templates -- independent per channel
- Channel-specific trigger efficiency -- different trigger paths
- Data-driven background estimates -- method = channel-dependent

Misclassifying correlated as uncorrelated → underestimated combined uncertainty. Misclassifying uncorrelated as correlated → overestimated.

## Channel Consistency Check

Before combining, verify per-channel results compatible:

- Fit each channel independently → extract signal strength (mu) with uncertainty
- Per-channel results should be statistically compatible within uncertainties
- Compute compatibility chi-squared: chi2 = sum_c ((mu_c - mu_combined) / sigma_c)^2
- Large chi2 (p-value < 0.05) → tension between channels, must investigate before combination
- Possible causes: mismodeled backgrounds in one channel, incorrect systematic correlations, signal model issues

Only proceed with combination after consistency check passes.

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
