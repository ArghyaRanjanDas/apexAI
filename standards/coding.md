# Code Quality Standards

These standards govern all analysis code in an apexAI project. The
overriding principle is KISS/YAGNI: scripts, not frameworks. No CLIs,
config systems, or plugin architectures. Every script is a standalone
unit that does one thing and can be run with `pixi run <task>`.

---

## Version Control

### Conventional Commits

All commit messages follow: `<type>(phase): <description>`

Types: `feat`, `fix`, `data`, `plot`, `doc`, `refactor`, `test`, `chore`.

Examples:
- `feat(phase2): add dimuon mass spectrum with OS/SS`
- `fix(phase3): correct inverted isolation cut`
- `plot(phase4a): add per-systematic impact figures`
- `data(phase1): extract reference analysis values`

### Branching

One branch per phase (`phase1_strategy`, `phase2_selection`, etc.).
Merge to main after review passes. Never force-push to main.

### Commit Frequency

Commit after every meaningful step. Commits are checkpoints. If the
process crashes, resume from the last commit. A meaningful step is:
one script working, one set of plots produced, one systematic evaluated,
one bug fixed.

---

## Code Quality

### KISS/YAGNI

Write scripts, not frameworks. No CLIs. No config files that need parsing.
No plugin architectures. No abstract base classes for "future extensibility."
The analysis is the product; the code is a tool.

A script that processes events and writes histograms to JSON is correct.
A framework with `AbstractEventProcessor`, `ConfigLoader`, and
`PluginRegistry` that does the same thing is wrong.

### Output Paths via __file__

Scripts must resolve output paths relative to the script file, not the
current working directory:

```python
HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "outputs"
FIG = OUT / "figures"
```

This ensures `pixi run py path/to/script.py` produces the same output
regardless of the shell's CWD. CWD-relative paths like
`Path("phase4_inference/outputs/figures")` break when invoked from a
different directory.

### Columnar Processing

Arrays + boolean masks, not event loops. Use awkward-array for jagged
structures, numpy for flat arrays. Named boolean masks for cuts, never
modify arrays in place.

```python
# Correct: columnar
mask_pt = events["pT"] > 25.0
mask_eta = np.abs(events["eta"]) < 2.5
selected = events[mask_pt & mask_eta]

# Wrong: event loop
for i in range(len(events)):
    if events["pT"][i] > 25.0 and abs(events["eta"][i]) < 2.5:
        selected.append(events[i])
```

### Logging, Not Printing

Use `logging` + `rich.logging.RichHandler`. No bare `print()` statements.
Ruff rule `T201` enforces this.

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

### Linting

Ruff + pre-commit for formatting and linting on every commit. The pre-commit
hook must pass before any commit lands.

---

## Analysis/Plotting Separation

Analysis code and plotting code must be independent scripts. They are never
entangled in the same file.

**Analysis scripts** process events and produce machine-readable artifacts:
JSON, NPZ, CSV. Histograms, yields, fit results, systematic shifts.

**Plotting scripts** read those artifacts and produce figures: PDF, PNG.

Benefits:
1. Plots are rerunnable. Tweaking a legend or color does not require
   re-running the analysis chain.
2. Artifacts are the handoff. If a plotting script crashes, no data is lost.
3. Review is cleaner. Analysis logic is audited without matplotlib boilerplate.

Rules:
- Analysis scripts write to `outputs/` (JSON, NPZ).
- Plotting scripts read from `outputs/` and write to `outputs/figures/`.
- Each plotting script has its own pixi task.
- Plotting scripts must NOT call `uproot.open()` or process ROOT files
  directly (exception: quick data/MC overlays during Phase 2 exploration).

---

## Pixi Task Graph

Every script maps to a pixi task. `pixi run all` reproduces the full
analysis from raw data to final result.

Requirements for `all`:
- Runs every script in the correct order
- Is idempotent (running twice produces the same output)
- Includes systematic variation reruns, not just the nominal
- Produces all figures, tables, and machine-readable outputs
- Completes without manual intervention

Task names are human-readable. Scripts are idempotent (fixed seeds, fixed
output paths). Split scripts exceeding ~5 min into stages with intermediate
outputs. Update `pixi.toml` whenever scripts are added or removed.

---

## Testing

Focus on structural bugs (wrong branch, wrong weight, inverted cut). These
are catastrophic because they require re-running everything and produce
plausible-looking wrong numbers.

### Always Run

- **Smoke test** per phase (~100 events, no crashes)
- **Integration test** (output files exist, correct structure, no NaN)

### Structural Checks

| Check | What it catches |
|-------|-----------------|
| Variable name -> right quantity | Plotting pT but labeling as eta |
| Cut inversion | Selecting background instead of signal |
| Efficiency consistency | Per-cut efficiency should match published |
| Cutflow monotonic | Events must decrease at each cut step |
| Systematic direction | Up variation should shift result up |
| Parallel outputs not identical | Fork/threading bug if N inputs produce N identical outputs |

### The Parallel Identity Check

If a parallel processing step produces N independent results (per-file
histograms, per-year densities), verify they are not bit-for-bit identical.
Identical outputs from independent inputs indicate a fork/threading bug
where child processes return cached data from the parent.

---

## Preferred Tools

| Capability | Tool | Notes |
|-----------|------|-------|
| ROOT file I/O | uproot | Pythonic, no ROOT install |
| Arrays | awkward-array, numpy | Columnar; awkward for jagged, numpy for flat |
| Histogramming | hist, boost-histogram | ND axes for systematic variations |
| Statistical model | pyhf, cabinetry | HistFactory JSON workspaces |
| Unbinned fits | zfit | When binned HistFactory is insufficient |
| MVA | xgboost, scikit-learn | BDTs via xgboost; sklearn for preprocessing |
| Plotting | matplotlib, mplhep | See plotting.md for all figure standards |
| Columnar model | coffea | NanoEvents, PackedSelection (optional) |
| Jet clustering | fastjet | e+e-: Durham; pp: anti-kT |
| Kinematics | vector | Lorentz vectors |
| Particle data | particle | PDG masses, widths, identifiers |
| Minimization | iminuit | Unbinned/binned fits |
| Logging | logging + rich | No bare print() |
| Documents | pandoc + tectonic | Markdown to PDF |
| Dependencies | pixi | Single source of truth for environment |

---

## Scale-Out Rules

Estimate before running: input size, per-event cost on a 1000-event slice,
peak memory.

| Estimated time | Mode |
|----------------|------|
| < 2 min | Single-core local |
| 2--15 min | `ProcessPoolExecutor` or multicore |
| > 15 min | SLURM: `sbatch --wait` or `--array` |

Prefer the simplest pattern that works. Never wait >15 min on a login node
when SLURM exists.

### Multiprocessing Safety

When using `ProcessPoolExecutor` with libraries that use OpenMP or threading
(fastjet, ROOT, numpy with MKL), always set:

```python
import multiprocessing
multiprocessing.set_start_method("forkserver", force=True)
```

The default `fork` method copies the parent's thread state into children.
Libraries with active thread pools can produce silently wrong results
where children return cached parent data instead of computing fresh values.

---

## Debug Code and Diagnostics

Debug scripts are prefixed with `debug_` or placed in `scratch/`. They are
never included in the `all` task.

But debug outputs are valuable -- preserve them:
- `outputs/` -- production artifacts (JSON, NPZ), enter the analysis chain
- `outputs/figures/` -- publication-quality figures for the AN
- `outputs/debug/` -- diagnostic figures, not in the AN, preserved and
  referenced in the experiment log
- `logs/` -- session logs, experiment log entries

Anything that informed a decision should be traceable. "I chose 8 bins
because the 12-bin version had empty bins" is only useful if the 12-bin
plot is in `outputs/debug/` and referenced in the experiment log.
