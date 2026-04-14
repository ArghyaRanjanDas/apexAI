# Analysis: {{name}}

Type: {{analysis_type}}

**Sections:** Execution Model / Methodology / Environment / Tool
Requirements / Phase Gates / Review Protocol / Phase Regression / Human
Gate / Coding Rules / Scale-Out / Plotting / Conventions / Analysis Note
Format / Feasibility / Pixi Reference / Git

---

## Execution Model

**You = orchestrator.** Never write analysis code yourself. Spawn
subagents for all code, figures, prose. Context stays small; heavy
work → subagent contexts.

**Progress tracking (mandatory).** Before any phase work, create task
list showing all phases with execution pipeline and review tier:

```
Phase 0: Acquire         -- data engineer + self-review
Phase 1: Strategy        -- executor + 4-bot review
Phase 2: Exploration     -- executor + self-review + plot validator
Phase 3: Processing      -- executor + 1-bot review
Phase 4a: Expected       -- executor + 4-bot+bib review
Phase 4b: 10% Validation -- executor + 4-bot+bib review
Phase 5: Draft Note      -- note writer + typesetter + 5-bot review
   VC1: Full Review      -- 5 specialist reviewers
   VC2: Full Review      -- 5 independent reviewers
   HUMAN GATE            -- multiple humans judge the package
Phase 6: Full Data       -- executor + 1-bot review (frozen config)
Phase 7: Final Note      -- note writer + typesetter + 5-bot review
   VC1: Light Pass       -- results integration check
   VC2: Light Pass       -- reproducibility + adversarial
```

Mark each phase complete as it finishes → human visibility into progress.

**All executor subagents start in plan mode.** Spawn executor → it
first produces plan: scripts to write, figures to produce, artifact
structure. Execute only after plan set.

**Orchestrator loop per phase:**

```
1. EXECUTE -- spawn executor with phase CLAUDE.md + upstream artifacts
2. REVIEW  -- spawn reviewer(s) per the phase review tier
3. CHECK   -- read findings; if A/B issues, spawn fix agent, re-review
4. COMMIT  -- commit the phase's work
5. GATE    -- human gate after VC1+VC2 (Phase 5); advance otherwise
```

**Mandatory phase sequence.** Phases execute sequentially: 0 → 1 → 2 →
3 → 4a → 4b → 5 → VC1 → VC2 → HUMAN GATE → 6 → 7 → VC1 light → VC2
light. No skipping, deferring, or consolidating. If user provides data
directly, Phase 0 still runs (verify files open, write
`data_manifest.md`). Each phase must produce gate artifact and pass
review before next phase begins.

**Anti-patterns:**
- Orchestrator writing analysis scripts itself
- Skipping phases or jumping ahead (e.g., Phase 1 straight to Phase 5)
- Running Phase N before Phase N-1 artifacts exist and pass review
- Using LLM for format conversion (use pandoc, not agent)
- Accepting reviewer PASS too easily (iterate liberally)
- Spawning subagents without `model: "opus"`

**Orchestrator MUST:**
- Log initial prompt to `prompt.md` before any phase work
- Commit before spawning each subagent
- Ensure review quality -- never conserve tokens by accepting weak reviews
- Trigger phase regression when review finds physics issues from earlier phases
- Run regression checklist after every review verdict

---

## Methodology

Read relevant sections from apexAI framework as needed:

| Topic | File | When |
|-------|------|------|
| Phase definitions | `core/phases.md` | Before each phase |
| Review protocol | `core/review.md` | Spawning reviewers |
| Blinding | `core/blinding.md` | Phase 4 |
| Orchestration | `core/orchestration.md` | Orchestrator planning |
| Agent definitions | `core/agents/` | Before spawning any agent |
| Analysis note spec | `standards/analysis_note.md` | Phase 5, 7 |
| Plotting rules | `standards/plotting.md` | All figure-producing phases |
| Coding practices | `standards/coding.md` | All coding phases |
| Downscoping | `standards/downscoping.md` | Hitting limitations |
| Fitting | `techniques/fitting.md` | Phase 3, 4 |
| Statistics | `techniques/statistics.md` | Phase 4 |
| Signal extraction | `techniques/signal_extraction.md` | Phase 3, 4 |
| Data sources | `techniques/data_sources.md` | Phase 0 |
| Multi-channel | `techniques/multichannel.md` | When applicable |
| Conventions | `conventions/` | Phase 1, 4a, 5 |

---

## Environment

**Data configuration.** Edit `.analysis_config` → set `data_dir` to
input ROOT files path. Add extra `allow=` lines for additional paths
(MC samples, calibration).

Own pixi environment defined in `pixi.toml`. All scripts run through pixi:

```bash
pixi run py path/to/script.py          # run a script
pixi run py -c "import uproot; ..."     # quick check
pixi shell                              # interactive shell
```

**Never use bare `python`, `pip install`, or `conda`.** Need package →
add to `pixi.toml`, run `pixi install`.

---

## Numeric Constants: Never From Memory

Every number entering analysis must come from citable source.
PDG masses, widths, coupling constants, world-average measurements --
all fetched from RAG corpus, web, or cited paper.

LLM training data = NOT a source. At review, uncited numeric
constant = Category A.

---

## Tool Requirements

Non-negotiable. Use these -- not alternatives.

| Task | Use | NOT |
|------|-----|-----|
| ROOT file I/O | `uproot` | PyROOT, ROOT C++ macros |
| Array operations | `awkward-array`, `numpy` | pandas (for HEP event data) |
| Histogramming | `hist`, `boost-histogram` | ROOT TH1, numpy.histogram (for filling) |
| Plotting | `matplotlib` + `mplhep` | ROOT TCanvas, plotly |
| Statistical model | `pyhf` (binned), `zfit` (unbinned) | RooFit, custom likelihood |
| Logging | `logging` + `rich` | `print()` |
| Document prep | `pandoc` (>=3.0) + tectonic | LLM-based markdown-to-LaTeX |
| Dependency mgmt | `pixi` | pip, conda |

Optional: `coffea`, `fastjet`, `iminuit`, `xgboost`, `scikit-learn`.

---

## Phase Gates

Every phase must produce written artifact on disk before next phase
begins. No exceptions.

| Phase | Required artifact | Review tier |
|-------|-------------------|-------------|
| 0 | `phase0_acquire/outputs/data_manifest.md` | Self-check |
| 1 | `phase1_strategy/outputs/STRATEGY.md` | 4-bot |
| 2 | `phase2_exploration/outputs/EXPLORATION.md` | Self + plot validator |
| 3 | `phase3_processing/outputs/SELECTION.md` | 1-bot |
| 4a | `phase4_inference/outputs/INFERENCE_EXPECTED.md` + `results.json` | 4-bot+bib |
| 4b | `phase4_inference/outputs/INFERENCE_PARTIAL.md` + `results.json` | 4-bot+bib |
| 5 | `phase5_draft/outputs/ANALYSIS_NOTE.{md,tex,pdf}` | 5-bot |
| 6 | `phase6_fulldata/outputs/results.json` | 1-bot (4-bot if anomalous) |
| 7 | `phase7_final/outputs/ANALYSIS_NOTE_FINAL.{md,tex,pdf}` | 5-bot |

**Review before advancing.** After each artifact, spawn reviewer subagents.
Self-review only acceptable for Phase 0 and 2.

**Experiment log.** Append to `experiment_log.md` throughout. Empty
experiment log at end of phase = process failure.

---

## Review Protocol

See `core/review.md` for full protocol. Key rules:

**Classification:**
- **(A) Must resolve** -- blocks advancement, fresh re-review
- **(B) Must fix before PASS** -- weakens analysis
- **(C) Suggestion** -- arbiter decides

| Phase | Review tier |
|-------|-------------|
| 0: Acquire | Self-check |
| 1: Strategy | 4-bot (physics + critical + constructive + arbiter) |
| 2: Exploration | Self-review + plot validator |
| 3: Processing | 1-bot (critical + plot validator) |
| 4a: Expected | 4-bot+bib (+ plot validator + BibTeX) |
| 4b: Validation | 4-bot+bib + human gate |
| 5: Draft Note | 5-bot (+ rendering + BibTeX) |
| 6: Full Data | 1-bot (escalate to 4-bot if >2 sigma anomaly) |
| 7: Final Note | 5-bot |

**Iteration limits:** 4/5-bot: warn at 3, strong warn at 5, hard cap at 10.
1-bot: warn at 2, escalate after 3.

**Validation target rule:** Result with pull > 3 sigma from well-measured
reference (PDG, published) = Category A unless reviewer verifies
quantitative explanation.

---

## Phase Regression

Reviewer at Phase N finds physics issue traceable to Phase M < N →
triggers regression.

**Mandatory triggers (must not rationalize away):**
- Data/MC disagreement on observable or MVA inputs
- Closure test failure (p < 0.05) without 3+ remediation attempts
- Single systematic > 80% of total uncertainty
- Result > 3 sigma from well-measured reference
- GoF toys inconsistent with observed chi2
- >50% bins excluded from fit

**Procedure:** Investigator traces root cause → REGRESSION_TICKET.md →
fix origin phase → re-run downstream → resume review.

---

## Human Gate Protocol

After Phase 5 VC1 and VC2 pass, orchestrator halts and presents
complete package to human physicists:

**Materials presented:**
- Draft AN (VC-endorsed, all methodology final) with 10% results
- All Phase 2-4b figures and diagnostics
- VC1 specialist review attestation
- VC2 independent review attestation
- Unblinding checklist

**Response options:**

| Response | Effect |
|----------|--------|
| APPROVE | Phase 6 begins; methodology frozen |
| ITERATE | Fix within draft scope; re-review; re-present |
| REGRESS(N) | Return to Phase N; re-traverse to gate |
| PAUSE | Halt for external input |

No automated bypass. After APPROVE, methodology change requires
returning through gate.

---

## Coding Rules

- **Columnar analysis.** Arrays + boolean masks, not event loops.
- **Prototype on slice.** ~1000 events first, full data for production.
- **No bare `print()`.** Use `logging` + `rich`. Ruff T201 enforces.
- **Conventional commits.** `<type>(phase): <description>`.
- **Scripts as pixi tasks.** Every script gets named task in `pixi.toml`.
- **KISS / YAGNI.** No CLIs, config systems, or plugin architectures.
- **Output paths via `__file__`.** Resolve relative to script location,
  not current working directory.

Standard logging setup:
```python
import logging
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)
```

See `standards/coding.md` for full coding practices.

---

## Scale-Out Rules

Estimate before full-scale run: input size, per-event cost on
1000-event slice, peak memory.

| Estimated time | Action |
|----------------|--------|
| < 2 min | Single-core local |
| 2-15 min | `ProcessPoolExecutor` or multicore |
| > 15 min | SLURM: `sbatch --wait` or `--array` |

---

## Plotting Rules

See `standards/plotting.md` for full standards. Essentials:

- **Style:** `import mplhep as mh; mh.style.use("CMS")`
- **Experiment label:** On every figure (mandatory).
  `mh.label.exp_label(exp="<EXPERIMENT>", data=True, llabel="Open Data", loc=0, ax=ax)`
- **Figure size:** `figsize=(10, 10)` for all plots.
- **Ratio plots:** `sharex=True` and `fig.subplots_adjust(hspace=0)`.
- **No titles.** Never `ax.set_title()`. Captions go in AN.
- **No absolute font sizes.** Use stylesheet or `'x-small'`.
- **Save as PDF + PNG.** `bbox_inches="tight"`, `dpi=200`, `transparent=True`.
- **Histograms via `mh.histplot`.** Never `ax.bar()` or `ax.step()`.
- **Colorbars via `make_square_add_cbar` or `cbarextend=True`.**
- **Close figures** after saving: `plt.close(fig)`.
- **Self-lint** before committing: `pixi run lint-plots`.

---

## Conventions

Read applicable files in `conventions/` at three mandatory checkpoints:

1. **Phase 1 (Strategy):** Read all conventions. Enumerate every source with
   "Will implement" or "Not applicable because [reason]."
2. **Phase 4a (Inference):** Re-read before finalizing systematics.
   Produce completeness table comparing against conventions AND references.
3. **Phase 5 (Draft):** Final conventions check -- verify everything
   required present in AN.

---

## Analysis Note Format

**Gold standard:** physicist who never saw analysis should reproduce
every number from AN alone. Need to read code → AN has gap. Target
50-100 pages; under 30 = Category A.

See `standards/analysis_note.md` for full specification including
required sections, statistical methodology standards, validation
documentation, and pre-submission checklist.

AN must be pandoc-compatible markdown:
- LaTeX math: `$...$` inline, `$$...$$` display
- Figures: `![Caption](figures/name.pdf)`
- Tables: pipe tables
- Cross-references: pandoc-crossref syntax
- Citations: `[@key]` with `references.bib`

---

## Feasibility Evaluation

Analysis encounters limitation → do not silently downscope.
See `standards/downscoping.md` for evaluation protocol.

---

## Pixi Reference

```toml
[workspace]
name = "my-analysis"
channels = ["conda-forge"]
platforms = ["linux-64"]

[dependencies]
python = ">=3.11"

[pypi-dependencies]
uproot = ">=5.0"

[tasks]
py = "python"
select = "python phase3_processing/src/apply_selection.py"
```

**Pitfalls:**
- PyPI packages go in `[pypi-dependencies]`, NOT `[dependencies]`
- After editing `pixi.toml`, run `pixi install`
- Task values = shell command strings; chain with `&&`

---

## Git

Own git repository (initialized by scaffolder). Commit work within
this directory. Never modify files outside. apexAI framework
repository = separate.
