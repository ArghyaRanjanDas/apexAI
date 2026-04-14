# Phase 2: Exploration -- {{name}}

Type: {{analysis_type}}

---

## Objective

Plot every variable, detect features, form physics hypotheses, and
assess data quality -- before any selection. No cuts applied in this
phase (except basic data quality if needed).

---

## Tasks

### 2a. Survey Distributions

1. **1D distribution for every branch** (linear + log-y, 100 bins,
   overflow/underflow displayed):
   ```python
   for branch in tree.keys():
       arr = tree[branch].array(library="np")
       if arr.dtype.kind not in ("f", "i", "u"):
           continue
       fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
       # linear and log-y side by side
   ```

2. **Summary statistics** per variable: count, mean, std, min,
   percentiles (1/25/50/75/99), max, fraction zero, fraction NaN.
   Store as CSV in `outputs/`.

3. **Invariant mass for all object pairs** (same-type and cross-type).
   Separate opposite-sign (OS) and same-sign (SS) for charged particles:
   ```python
   import vector
   p1 = vector.MomentumObject4D(pt=pt1, eta=eta1, phi=phi1, mass=m1)
   p2 = vector.MomentumObject4D(pt=pt2, eta=eta2, phi=phi2, mass=m2)
   m_inv = (p1 + p2).mass
   ```

4. **Derived observables:** delta-R (all pairs), HT (scalar jet-pT sum),
   MET significance, transverse mass (lepton+MET), angular correlations,
   correlation matrices for key variables.

### 2b. Feature Detection

5. **Automated peak finding** on invariant mass and pT distributions:
   ```python
   from scipy.signal import find_peaks
   counts, edges = np.histogram(mass_array, bins=200)
   centers = 0.5 * (edges[:-1] + edges[1:])
   median = np.median(counts)
   mad = np.median(np.abs(counts - median))
   peaks, props = find_peaks(
       counts, height=median + 3*mad,
       prominence=0.05*counts.max(), distance=5
   )
   ```

6. **Outlier bins** with z-score > 5 vs. sliding-window median.

7. **Multimodality** via KDE mode counting on key distributions.

8. **Document every feature** in `outputs/discovery_log.md`:
   variable, bin range, type (peak/edge/excess/deficit/correlation),
   significance estimate, candidate interpretation.

### 2c. Physics Interpretation

9. **Compare peaks to the mass table:**

   | Particle | Mass (GeV) | Decays |
   |----------|-----------|--------|
   | pi0 | 0.135 | gamma gamma |
   | rho/omega | 0.77/0.78 | pi pi / 3pi |
   | phi | 1.020 | KK |
   | J/psi | 3.097 | ll |
   | Y(1S) | 9.460 | mu mu |
   | W | 80.38 | l nu, qq |
   | Z | 91.19 | ll, qq |
   | H | 125.25 | bb, WW, tautau |
   | top | 172.7 | Wb |

   Peak within 3% of a known mass -> strong candidate. Otherwise evaluate
   instrumental artifacts (trigger turn-on, detector gaps, reconstruction
   zeros, combinatorics) and statistical fluctuations. See
   `techniques/fitting.md` for the complete mass table.

10. **Form physics hypotheses.** For each feature, propose a physics
    explanation and an instrumental explanation. Record both.

### 2d. Variable Ranking

11. **Rank variables by separation power.** Signal/background chi2/ndf
    per variable. chi2/ndf > 5 -> investigate (powerful discriminant
    or poor modeling).

12. **MVA input check.** Data/MC chi2/ndf > 5 in any control region ->
    variable flagged, cannot enter MVA without remediation.

---

## Deliverables

- `outputs/figures/survey/` -- all 1D distributions (linear + log-y)
- `outputs/summary_statistics.csv`
- Invariant mass spectra (OS/SS), derived observables
- `outputs/discovery_log.md` -- every detected feature
- Variable ranking table
- Data quality assessment
- `outputs/EXPLORATION.md` -- synthesis of all findings

## Review Tier

**Self-check** + **Plot Validator** (axis labels, units, overflow).

## References

- `techniques/fitting.md` -- mass table for peak identification
- `techniques/statistics.md` -- significance estimation
