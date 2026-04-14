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
