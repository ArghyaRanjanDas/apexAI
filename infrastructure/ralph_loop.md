# Ralph loop -- autonomous iteration framework

Autonomous execution loop for Phase 0-7 + VC1 + VC2 workflow. Each invocation performs one iteration, checks exit conditions, either continues or stops.

## Invocation template

```
/ralph-loop "Execute Phase <N> of <wing_name>. Current progress:
<progress_summary>. Work this iteration: <specific_task>.
Completion promise: PHASE_<N>_COMPLETE" --max-iterations <budget>
```

## Iteration budget

| Stage | Budget | Rationale |
|-------|--------|-----------|
| Phase 0 (Acquire) | 10 | Data discovery can require multiple attempts |
| Phase 1 (Strategy) | 10 | Enumeration + convention compliance |
| Phase 2 (Exploration) | 10 | Plotting, feature investigation |
| Phase 3 (Processing) | 10 | Selection tuning, closure tests |
| Phase 4 (Inference) | 10 | Fits, systematics evaluation |
| Phase 5 (Draft note) | 3 | Writing from existing results |
| VC1 full review | 8 | Five reviewers + response + iteration |
| VC2 full review | 9 | Five reviewers + response + iteration |
| Human gate | 1 | Present package, await decision |
| Phase 6 (Full data) | 3 | Methodology frozen, just run |
| Phase 7 (Final note) | 3 | Update existing draft |
| VC1 light | 3 | Results integration check |
| VC2 light | 3 | Reproducibility + adversarial |

## Progress tracking

Each iteration logs one-line status:

```
[iter 3/10] Phase 2: plotted ditau_mass, mbb, met for signal and
all backgrounds. Next: 2D correlations.
```

Progress stored in `progress.txt` at analysis root and in mempalace wing.

## Exit conditions

Loop terminates when any of these hold:

1. **Completion promise met** -- agent emits exact completion promise string → phase objective satisfied.
2. **Max iterations reached** -- budget exhausted. Agent must summarize what was accomplished and what remains.
3. **Stuck for 3 iterations** -- progress log shows no meaningful change for 3 consecutive iterations → loop exits with diagnostic explaining blockage.

## Git strategy

Commit after each completed phase or review round. Commit message format:

```
apexAI: complete Phase <N> (<short description>)
```

Do not commit mid-phase unless iteration budget about to expire and partial progress should be preserved.
