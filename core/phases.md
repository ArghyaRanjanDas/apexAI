# Phase Specifications

Eight phases from data acquisition to final publication. Each phase
produces artifacts, undergoes review, and must clear a gate before
advancing. Every number comes from code on data -- never from recalled
knowledge.

---

## Phase 0 -- ACQUIRE

**Goal.** Obtain collision data and record provenance.
**Agent.** Data Engineer.
**Skip when:** user provides local ROOT/parquet files (verify they open).

### Tasks

1. **Identify the data source.** Search open-data portals for the
   relevant experiment and process (`techniques/data_sources.md`):

   | Portal | URL | Experiments |
   |--------|-----|-------------|
   | CERN Open Data | opendata.cern.ch | CMS, ATLAS, ALICE, LHCb, LEP |
   | HEPData | hepdata.net | Published measurements (any) |
   | DPHEP | dphep.org | Preserved datasets |

2. **Download one file first.** Validate before bulk fetch:
   ```python
   import uproot
   f = uproot.open("downloaded_file.root")
   tree = f[tree_name]
   print(tree.keys(), tree.num_entries)
   df = tree.arrays(library="pd", entry_stop=100)
   print(df.describe())
   ```

3. **Record provenance** in `data_manifest.md`: portal, DOI, URL,
   retrieval date, SHA-256, event count, file size, tree/branch info.

4. **Fetch remaining files** and verify each opens with the expected
   tree structure.

### Deliverables
- `data/` directory, `data_manifest.md`, verification log

### Review tier
Self-check. Escalate to Investigator if files fail to open.

---

## Phase 1 -- STRATEGY

**Goal.** Identify the dataset (experiment, units, structure) and
commit to an analysis plan before writing any analysis code.
**Agent.** Executor (orient) then Orchestrator (plan + review).

### Tasks

#### 1a. Orient

5. **Map branches to experiment conventions:**

   | Pattern | Experiment | Format |
   |---------|------------|--------|
   | `nMuon`, `Muon_pt`, `Jet_btagDeepFlavB` | CMS | NanoAOD |
   | `el_pt`, `jet_jvt`, `mcChannelNumber` | ATLAS | PHYSLITE |
   | `nTracks`, `thrust`, `R2` | LEP | Custom |
   | `foxWolframR2`, `nCDCHits` | Belle/II | basf2 |

   ```python
   branches = tree.keys()
   cms_markers = {"nMuon", "nElectron", "nJet", "MET_pt", "HLT_"}
   overlap = set(branches) & cms_markers
   ```

6. **Detect units.** Sample 1000 events; if median leading-object pT
   exceeds 1000, the file is in MeV. Record and convert consistently.

   | Quantity | GeV range | MeV range |
   |----------|-----------|-----------|
   | Lepton pT | 5--200 | 5k--200k |
   | Jet pT | 20--500 | 20k--500k |

7. **Identify collision type/energy** from metadata branches or
   filenames. Record: collision system, sqrt(s), luminosity, MC flag.

8. **Log orientation** in experiment log: experiment, format, units,
   collision type, energy, luminosity, tree name, branch count, events.

#### 1b. Plan

9. **Analysis type.** Search (new signal) or measurement (known
   process)? Governs blinding and statistical treatment throughout.

10. **Enumerate conventions.** For each convention in `conventions/`,
    state "Will implement" or "Not applicable" with justification.

11. **Select primary technique.** Counting, template fit, sideband,
    ABCD, unfolding, etc. Justify against physics and statistics.
    See `techniques/signal_extraction.md`, `techniques/fitting.md`.

12. **Two qualitatively different selection approaches** (both carried
    through Phase 3). "Cut-based vs MVA" qualifies; "tight vs loose"
    does not.

13. **Systematic catalog.** Every source with: name, category
    (experimental/theoretical/modeling), evaluation method, expected
    magnitude, references. Sources to consider: luminosity, trigger,
    lepton ID/iso, JES/JER, b-tag, pileup, PDF, QCD scale, parton
    shower, MC generator, signal/background modeling, MC statistics.

14. **Reference analysis table.** 3+ published analyses of the same
    or similar process: citation, technique, dataset, key result.

15. **~6 flagship figures.** Title, observable, expected content,
    producing phase, AN location.

16. **Label constraints.** Tag every element:
    **[A]** Assumption, **[L]** Limitation, **[D]** Decision.

### Deliverables
- Strategy document (items 9-16), orientation log (items 5-8)
- Systematic catalog, reference table, flagship figure list

### Review tier
**4-bot.** Physics + Critical + Constructive -> Arbiter. A-items block
advancement. The strategy is binding -- departures require re-review.

---

## Phase 2 -- EXPLORATION

**Goal.** Plot every variable, detect features, form physics
hypotheses, assess data quality -- before any selection.
**Agent.** Executor.

### Tasks

#### 2a. Survey

17. **1D distributions for every branch** (linear + log-y, 100 bins,
    overflow/underflow displayed):
    ```python
    for branch in tree.keys():
        arr = tree[branch].array(library="np")
        if arr.dtype.kind not in ("f", "i", "u"):
            continue
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        ax1.hist(arr, bins=100); ax1.set_title(f"{branch} (linear)")
        ax2.hist(arr, bins=100); ax2.set_yscale("log")
        fig.savefig(f"plots/survey/{branch}.png", dpi=150)
        plt.close()
    ```

18. **Summary statistics** per variable: count, mean, std, min,
    percentiles (1/25/50/75/99), max, fraction zero/NaN. Store as CSV.

19. **Invariant mass for all object pairs** (same-type and
    cross-type). Separate OS and SS for charged particles:
    ```python
    def invariant_mass(pt1, eta1, phi1, m1, pt2, eta2, phi2, m2):
        E1 = np.sqrt((pt1 * np.cosh(eta1))**2 + m1**2)
        E2 = np.sqrt((pt2 * np.cosh(eta2))**2 + m2**2)
        px1, py1, pz1 = pt1*np.cos(phi1), pt1*np.sin(phi1), pt1*np.sinh(eta1)
        px2, py2, pz2 = pt2*np.cos(phi2), pt2*np.sin(phi2), pt2*np.sinh(eta2)
        M2 = (E1+E2)**2 - (px1+px2)**2 - (py1+py2)**2 - (pz1+pz2)**2
        return np.sqrt(np.maximum(M2, 0))
    ```

20. **Derived observables:** delta-R (all pairs), HT (scalar jet-pT
    sum), MET, transverse mass (lepton+MET), correlation matrices.

#### 2b. Feature detection

21. **Automated peak finding** on invariant mass and pT distributions:
    ```python
    from scipy.signal import find_peaks
    counts, edges = np.histogram(mass_array, bins=200)
    centers = 0.5 * (edges[:-1] + edges[1:])
    median = np.median(counts)
    mad = np.median(np.abs(counts - median))
    peaks, props = find_peaks(counts, height=median + 3*mad,
                              prominence=0.05*counts.max(), distance=5)
    ```

22. **Outlier bins** with z-score > 5 vs. sliding-window median.

23. **Multimodality** via KDE mode counting.

24. **Discovery log.** Record each feature in `discovery_log.md`:
    variable, bin range, type (peak/edge/excess/deficit/correlation),
    significance, candidate interpretation.

#### 2c. Physics interpretation

25. **Compare peaks to the mass table:**

    | Particle | Mass (GeV) | Decays |
    |----------|-----------|--------|
    | pi0 | 0.135 | gamma gamma |
    | eta | 0.548 | gamma gamma, 3pi |
    | rho/omega | 0.77/0.78 | pi pi / 3pi |
    | phi | 1.020 | KK |
    | J/psi | 3.097 | ll |
    | Y(1S) | 9.460 | mu mu |
    | W | 80.38 | l nu, qq |
    | Z | 91.19 | ll, qq |
    | H | 125.25 | bb, WW, tautau, gamgam |
    | top | 172.7 | Wb |

    Peak within 3% of a known mass -> strong candidate. Otherwise
    evaluate instrumental artifacts (trigger turn-on, detector gaps,
    reconstruction zeros, combinatorics) and statistical fluctuations
    (below 3 sigma -> require confirmation in independent subsamples).

#### 2d. Data quality and variable ranking

26. **Overlay with published distributions** from Phase 1 references
    (normalized to area). Note discrepancies.

27. **Rank variables by separation power.** Signal/background chi2/ndf
    per variable. chi2/ndf > 5 -> investigate (powerful discriminant
    or poor modeling).

28. **MVA input check.** Data/MC chi2/ndf > 5 in any control region
    -> variable flagged, cannot enter MVA without remediation.

### Deliverables
- `plots/survey/` (all 1D distributions), summary CSV
- Invariant mass spectra (OS/SS), derived observables
- `discovery_log.md`, variable ranking table, data quality assessment

### Review tier
**Self-check** + **Plot Validator** (axis labels, units, overflow).

---

## Phase 3 -- PROCESSING

**Goal.** Implement selection, background estimation, corrections.
Carry two approaches through quantitative comparison. Validate with
closure and stress tests.
**Agent.** Executor.

### Tasks

#### 3a. Selection

29. **Baseline cuts:** trigger (document prescales, turn-on; see
    "Trigger and efficiency scales"), object multiplicity, loose PID,
    geometric acceptance, overlap removal.

30. **Analysis-specific selection** for both Phase 1 approaches.
    Document every cut with physics motivation. Start loose, tighten
    incrementally. Never optimize toward a known answer.

31. **Cut-flow tables** per approach: cut name, surviving events,
    cumulative efficiency, signal efficiency, background rejection.

32. **N-1 plots.** For each cut variable, plot with all other cuts
    applied. Verifies the boundary sits where signal/background
    separate.

33. **Control regions.** One per major background, orthogonal to the
    signal region. Validate data/MC agreement in each.

#### 3b. Approach comparison

34. **Quantitative comparison** of both approaches on a common metric
    (expected significance or sensitivity). Select primary; secondary
    becomes a Phase 4 cross-check.

#### 3c. Validation

35. **Closure test.** Full chain on MC pseudo-data with known truth.
    Must recover injected signal: chi2/ndf < 3, p > 0.05.

36. **Stress test.** Reweight MC kinematics and verify recovery. Tests
    robustness against data/MC modeling differences.

37. **Failure remediation.** If either test fails, follow the
    remediation protocol below. Never skip a failing test.

#### 3d. MVA (if applicable)

38. **Train** using only modeling-checked variables (Phase 2, chi2/ndf
    < 5). Required diagnostics: overtraining KS test (p > 0.05), ROC
    + AUC, score distributions, feature importance.

39. **Hyperparameter scan** (2+ parameters with performance curves).

#### 3e. Systematics

40. **Implement every variation** from Phase 1 catalog. Per source:
    up/down variation, rerun selection, record effect.

41. **Organize by category** (experimental/theoretical/modeling) in a
    format Phase 4 can ingest into the statistical model.

### Deliverables
- Selection code (both approaches), cut-flow tables, N-1 plots
- Control regions + data/MC comparisons
- Approach comparison table, closure/stress test results
- MVA diagnostics (if applicable), systematic variation tables

### Review tier
**1-bot.** Critical Reviewer + Plot Validator.

---

## Phase 4 -- INFERENCE

**Goal.** Extract the expected result on simulation and validate on
10% data. No human gate here -- the analysis proceeds to draft
documentation before human review.
See `core/blinding.md`.

### Phase 4a -- Expected Result

**Agent.** Executor.

42. **Build the statistical model** (template fit, counting, etc.)
    from Phase 3 predictions. See `techniques/fitting.md`.

43. **Systematic completeness table.** Every Phase 1 source must
    appear. Missing source = A-level finding:

    | Source | In catalog | Implemented | Effect |
    |--------|-----------|-------------|--------|
    | JES | Yes | Yes | +2.3/-1.8% |
    | Lumi | Yes | Yes | +/-1.6% |

44. **Asimov/MC extraction.** Verify: fit converges (Hesse + Minos),
    post-fit nuisances within +/-2 sigma, none constrained >50%,
    post-fit chi2/ndf < 3.

45. **Formula audit.** Dimensional analysis, limiting cases (zero
    signal, zero systematics, background-only), Phase 1 traceability.

46. **Operating point.** Scan tunable parameters, document sensitivity
    vs. each. See "Operating point stability" below.

47. **Perturbation tests:**
    - Scale pT x1.02 -> mass shifts ~2%
    - Drop 50% events -> uncertainty grows ~sqrt(2)
    - Inject fake peak at 75 GeV -> fit must find it
    Each has a PASS criterion. Failure triggers investigation.

48. **Fit initialization from data shape.** Peak from max bin, width
    from FWHM, yield from peak-region integral. Never from textbook.
    Quality: chi2/ndf in [0.5, 3.0].

49. **`results.json`** with phase, type, central value, stat/syst
    uncertainties, chi2/ndf, event counts, operating point.

**Review (4a):** 4-bot+bib (Physics, Critical, Constructive, Plot
Validator, BibTeX, Arbiter). A-items block 4b.

### Phase 4b -- 10% Validation

50. **10% subsample** via fixed random seed (chosen before seeing data).

51. **Full inference chain** with identical 4a configuration.

52. **Compare with 4a.** Central value compatible within 4b statistical
    uncertainty (inflated by sqrt(10) vs. full data).

53. **Unblinding checklist:**
    - [ ] Fit converges
    - [ ] Nuisance parameters in range
    - [ ] Post-fit distributions reasonable
    - [ ] 4b consistent with 4a
    - [ ] No pulls |pull| > 3
    - [ ] Perturbation tests pass
    - [ ] Control region agreement maintained

54. **`results.json`** updated with `"phase":"4b"`, `"type":"10pct"`,
    comparison with 4a documented.

**Review (4b):** 4-bot+bib (same panel as 4a). A-items block Phase 5.

---

## Phase 5 -- DRAFT NOTE

**Goal.** Produce a complete, publication-quality draft analysis note
containing full methodology and 10% validation results. This draft
undergoes internal review, VC1, VC2, and human gate before any full
data unblinding. Humans see a fully AI-attested, VC-endorsed package.
**Agent.** Note Writer (draft), Typesetter (compile), Orchestrator.

### Tasks

55. **Draft AN** per `standards/analysis_note.md`:
    1. Introduction (motivation, prior work, overview)
    2. Dataset and simulation (samples, generators, xsec, luminosity)
    3. Object reconstruction (trigger, ID, b-tag, overlap removal)
    4. Event selection (regions, cut-flow, N-1, efficiencies)
    5. Background estimation (methods, control regions, data-driven)
    6. Systematics (source-by-source, method, impact, correlations)
    7. Results (expected from 4a, 10% validation from 4b,
       perturbation and robustness tests, operating point scans)
    8. Summary (findings so far, methodology validation, outlook
       for full unblinding)

56. **Code traceability.** Every number references `[code:script.py:LN]`.
    Note Writer verifies each reference resolves.

57. **Flagship figures** at publication quality per `standards/plotting.md`:
    labels with units, experiment/lumi annotation, ratio panels,
    consistent colors, PDF + PNG. Include all figures from Phases 2-4b.

58. **Compile to PDF:** markdown -> pandoc -> LaTeX postprocess ->
    tectonic. Verify every figure, table, equation, cross-reference.

59. **Rendering check:** no margin overflow, clean page breaks,
    correct equations, resolved references, complete captions, 50-100
    page count.

### Deliverables
- Draft AN source + compiled PDF, all figures (PDF+PNG)
- BibTeX file, code traceability index
- 10% validation results integrated in results chapter

### Review tier
**5-bot.** Physics, Critical, Constructive, Plot Validator, BibTeX,
Rendering + Arbiter. A-items block VC1.

### Post-review: VC1 Full Review

VC1 (5 specialist reviewers) conduct a full analysis review of the
draft note. Scope covers methodology, statistical treatment,
systematic evaluation, physics interpretation, and presentation.
See `core/review.md`.

### Post-review: VC2 Full Review

VC2 (5 independent reviewers, no VC1 access) conduct a full
adversarial review. Includes cross-analyst reproduction, blind
re-analysis, independent systematic evaluation, and presentation
critique. See `core/review.md`. A-items from VC1 or VC2 block the
human gate.

### HUMAN GATE

Orchestrator halts. Humans receive the complete package:
- Draft AN with full methodology and 10% results
- All Phase 2-4b figures and diagnostics
- 5-bot internal review report (resolved)
- VC1 specialist review attestation
- VC2 independent review attestation

Human chooses: **APPROVE** (advance to full unblinding),
**ITERATE** (repeat phase -- revise draft, re-review),
**REGRESS** (earlier phase -- methodology change required),
**PAUSE** (halt for external input or collaboration review).

No automated bypass. Decision logged in experiment log.

**Approval freezes methodology.** Once the human gate clears, the
analysis configuration (selection, fit model, systematic treatment,
operating points) is locked. Phase 6 runs the frozen chain on full
data. Any methodology change after approval requires regression to
Phase 3 or earlier and re-traversal of Phases 4-5.

---

## Phase 6 -- FULL DATA

**Goal.** Execute the human-approved, methodology-frozen analysis on
the full dataset. No configuration changes permitted.
**Agent.** Executor.

### Tasks

60. **Full dataset, frozen configuration.** No changes to selection,
    fit model, systematic treatment, or operating points after the
    Phase 5 human gate. Configuration hash verified against the
    approved version.

61. **Post-fit diagnostics:** pre/post-fit overlays, nuisance pulls,
    parameter correlations, GoF (chi2/ndf, p-value, saturated model),
    yields per region.

62. **Robustness checks:** vary fit range +/-10%, halve/double bins,
    tighten/loosen each cut, compare primary vs. secondary approach.
    Result must be stable within systematics.

63. **Anomaly assessment:** unexpected features, |pull| > 3, tension
    with cross-checks, >3 sigma excesses/deficits. All documented.

64. **Final significance/limits** per `techniques/statistics.md`:
    measurements (value +/- stat +/- syst) or searches (95% CL limits,
    p-value, local significance).

65. **`results.json`:** `"phase":"6"`, `"type":"observed"`, full
    systematic breakdown, comparison with 4a expected and 4b 10%
    validation.

### Anomaly Escalation

If observed result deviates from expected (Phase 4a) by more than
2 sigma:
- Automatic escalation from 1-bot to 4-bot review
- Detailed investigation of data/MC differences required
- Cross-check with secondary approach mandatory
- Pull distribution analysis across all regions
- Human notification with anomaly report before proceeding to Phase 7

### Deliverables
- Full observed result with complete uncertainty breakdown
- Post-fit diagnostic plots (pre/post overlays, pulls, correlations)
- Robustness check table, anomaly assessment
- Updated `results.json` with observed values

### Review tier
**1-bot.** Critical Reviewer + Plot Validator. Methodology already
approved at Phase 5 human gate; focus is on execution correctness and
result integrity.

**Escalation:** if anomalous (>2 sigma from expected), automatically
escalates to **4-bot** (Physics, Critical, Constructive, Plot
Validator + Arbiter) with mandatory anomaly investigation.

---

## Phase 7 -- FINAL NOTE

**Goal.** Update the Phase 5 draft AN with full observed results,
produce flagship figures at publication quality, and compile the
final PDF. The methodology sections are unchanged (frozen at human
gate); only results, figures, and summary are updated.
**Agent.** Note Writer (update), Typesetter (compile), Orchestrator.

### Tasks

66. **Update AN results chapter** with full observed data:
    - Replace 10% validation results with full observed results
    - Add observed vs. expected comparison plots
    - Include post-fit diagnostics from Phase 6
    - Update significance/limits with observed values
    - Add robustness check summary table

67. **Flagship figures** at publication quality: final observed
    distributions, limit/significance plots, money plots with
    observed data overlaid. All per `standards/plotting.md`.

68. **Update summary chapter:** final findings, comparison with
    theory predictions, comparison with reference analyses from
    Phase 1, outlook and future directions.

69. **Compile final PDF:** same toolchain as Phase 5. Verify all
    new figures, tables, and cross-references resolve. Methodology
    sections must be byte-identical to the approved draft (diff check).

70. **Final rendering check:** margin overflow, page breaks, equations,
    references, captions, page count. Final PDF is the deliverable.

### Deliverables
- Final AN source + compiled PDF
- All figures (PDF+PNG) including new observed-data plots
- Updated BibTeX, code traceability index
- Machine-readable results (`results.json` + HEPData YAML)
- Diff report confirming methodology sections unchanged

### Review tier
**5-bot.** Physics, Critical, Constructive, Plot Validator, BibTeX,
Rendering + Arbiter. A-items block VC passes.

### Post-review: VC1 Light Pass

VC1 (same 5 specialist reviewers from Phase 5) conduct a light review.
Scope is restricted to results integration only -- methodology was
already approved at Phase 5. Checklist:
- [ ] Observed results correctly integrated into AN
- [ ] Figures match `results.json` values
- [ ] No methodology sections modified
- [ ] Statistical treatment consistent with approved plan
- [ ] Summary accurately reflects observed findings

### Post-review: VC2 Light Pass

VC2 (same 5 independent reviewers from Phase 5) conduct a light
adversarial review on full data. Scope:
- [ ] Re-execute full chain with frozen configuration, verify
      reproduction of observed results
- [ ] Adversarial tests pass on full data (same tests as Phase 5
      VC2, applied to observed results)
- [ ] No evidence of post-hoc methodology tuning
- [ ] Cross-check observed anomalies (if any) against independent
      estimation

### Final sign-off
Both VC1 and VC2 light passes must clear. A-items are resolved
through the same protocol as Phase 5. Once cleared, the analysis
is complete and the final AN is ready for collaboration review
or publication.

---
---

## Cross-Cutting Protocols

### Gate Protocol

Every phase boundary requires:
1. **Artifacts complete** -- all deliverables exist and are non-empty
2. **Experiment log updated** -- structured entry of actions/findings
3. **Review conducted** -- per the tier listed for that phase
4. **A-items resolved** -- each resolution documented, reviewer confirms
5. **Advance decision** -- ADVANCE, ITERATE, or REGRESS logged

The orchestrator must not execute Phase N+1 code while Phase N gates
remain open. **Regression** (triggered by review findings, validation
failures, or VC authority) marks intervening artifacts stale (not
deleted) and re-enters the target phase with rationale logged.

### Gate Protocol Summary

| Phase | Gate type | Review tier | VC | Human |
|-------|-----------|-------------|-----|-------|
| 0 ACQUIRE | Self-check | Self | -- | -- |
| 1 STRATEGY | Full review | 4-bot | -- | -- |
| 2 EXPLORATION | Light check | Self + Plot Val | -- | -- |
| 3 PROCESSING | Focused review | 1-bot | -- | -- |
| 4a EXPECTED | Full review | 4-bot+bib | -- | -- |
| 4b 10% VALID | Full review | 4-bot+bib | -- | -- |
| 5 DRAFT NOTE | Full review + VC + Human | 5-bot | VC1 full + VC2 full | **YES** |
| 6 FULL DATA | Execution check | 1-bot (or 4-bot if anomalous) | -- | -- |
| 7 FINAL NOTE | Full review + VC light | 5-bot | VC1 light + VC2 light | -- |

---

### Validation Failure Remediation

When closure, stress, or perturbation tests fail, at least three
distinct attempts before accepting failure:

1. **Check the formula** -- dimensional consistency, limiting cases,
   off-by-one, integer division, sign conventions, factors of 2pi
2. **Check the inputs** -- correct branches, units, selection, weights,
   no double-counting
3. **Alternative binning** -- coarser and finer; some failures are
   bin-migration artifacts
4. **Different regularization/fit config** -- scan strength, document
5. **Different MC** -- alternative generator or tune; failure specific
   to one generator is a modeling issue
6. **Different method** -- attempt secondary approach from Phase 1

All attempts exhausted -> document quantitatively, escalate to
Investigator. May proceed if impact is quantified as a systematic
(requires reviewer approval as A-item).

---

### Known-Underestimate Protocol

When a systematic is obviously conservative:
1. Document why the current estimate is conservative (with references)
2. Attempt a data-driven evaluation and compare
3. Report both values; primary uses the better estimate, conservative
   quoted as cross-check

Prevents both inflated uncertainties (obscure sensitivity) and
underestimated uncertainties (false discoveries).

---

### Operating Point Stability

For any tunable threshold (BDT cut, mass window, isolation, etc.):
1. Scan range covering factor-of-2 in figure of merit
2. Plot result vs. operating point
3. Identify plateau (stable within stat uncertainty = robust;
   otherwise treat as systematic source)
4. Document choice, criterion, and local sensitivity

---

### Trigger and Efficiency Scales

1. **Tag-and-probe** for lepton triggers/ID on Z->ll (J/psi for
   low-pT). Efficiency vs. pT, eta, pileup.
2. **MC scale factors** -- data/MC ratios as per-event weights;
   propagate statistical uncertainty as systematic.
3. **Barlow-Beeston lite** -- bin-by-bin MC-stat nuisance parameters
   when MC samples are small.
4. **Turn-on curves** -- plot trigger efficiency vs. relevant variable;
   cut above the 99% plateau.

---

### Result Presentation

**Measurements:** central value +/- stat +/- syst, per-bin with
covariance (differential), integrated value, theory/prior overlay.

**Searches:** observed/expected 95% CL limits with +/-1/2 sigma bands,
local p-value/significance, obs-vs-exp comparison.

**Both:** machine-readable output (`results.json` + HEPData YAML),
source code reproducing every number, resolving-power statement where
applicable.

---

### Phase Dependency Diagram

```
Phase 0: ACQUIRE
    |
    v
Phase 1: STRATEGY  (plan, systematics, flagship figures)
    |
    v
Phase 2: EXPLORATION  (distributions, features, hypotheses, ranking)
    |
    v
Phase 3: PROCESSING  (selection, backgrounds, closure/stress)
    |
    v
Phase 4a: EXPECTED  (Asimov result, perturbation tests)
    |
    v
Phase 4b: 10% VALIDATION  (partial data, comparison with 4a)
    |
    v
Phase 5: DRAFT NOTE  (complete AN with methodology + 10% results)
    |
    v
VC1: Full Analysis Review (5 specialist reviewers)
    |
    v
VC2: Full Independent Review (5 adversarial reviewers)
    |
    === HUMAN GATE ===  (approve methodology + draft)
    |                    [methodology frozen on approval]
    v
Phase 6: FULL DATA  (observed result, frozen config)
    |
    v
Phase 7: FINAL NOTE  (update AN with observed results, final PDF)
    |
    v
VC1: Light Pass (results integration only)
    |
    v
VC2: Light Pass (reproducibility + adversarial on full data)
    |
    v
DONE
```

**Forward only.** No phase depends on later-phase deliverables. If
Phase N needs Phase N+1 information, regress to Phase 1.

**Regression.** Any phase may regress to any earlier phase. Regression
to Phase 0 requires Orchestrator approval. Regression to Phase 1
invalidates all subsequent artifacts. Regression after the Phase 5
human gate (i.e., from Phase 6 or 7) requires re-traversal of
Phases 4-5 and a new human gate approval. Methodology changes after
human approval are not permitted without full regression.
