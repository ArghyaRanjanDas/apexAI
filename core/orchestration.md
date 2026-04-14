# Orchestrator Coordination Guide

## What Orchestrator Does

Orchestrator = thin coordinator. Jobs:

1. **Hold state**: prompt, phase summaries, agent verdicts.
2. **Spawn subagents**: curated context, never raw conversation.
3. **Read verdicts**: parse structured output.
4. **Commit artifacts**: validated outputs to repo.
5. **Track commitments**: carry forward binding statements.
6. **Maintain experiment log**: append every decision, never edit.

## What Orchestrator Does NOT Do

- **Never writes code.** Not one line. Specialists produce all code.
- **Never interprets physics.** Routes results to reviewer.
- **Never holds subagent context.** After return, context discarded. Retains summary + verdict only.
- **Never overrides verdict.** FAIL = FAIL. No second-guessing.
- **Never skips human gate.** Blocking per blinding.md.
- **Never skips a phase.** Mandatory sequence:
  0 → 1 → 2 → 3 → 4a → 4b → 5 → VC1 → VC2 → HUMAN GATE → 6 → 7 →
  VC1 light → VC2 light. Each phase produces gate artifact + passes
  review before next begins. Pre-provided data → Phase 0 still runs
  (verify + manifest).

---

## Phase Execution Loop

Core coordination algorithm. Runs for each phase in sequence.

```
SEQUENCE = [0, 1, 2, 3, 4a, 4b, 5, VC1_full, VC2_full,
            HUMAN_GATE, 6, 7, VC1_light, VC2_light]

for phase in SEQUENCE:

    # 1. PRE-CHECK
    Verify prior phase artifact exists and review verdict = PASS.
    If not, halt with error (never skip a missing gate).

    # 2. SPAWN EXECUTOR
    Assemble 3-layer context (see Context Assembly below).
    Spawn executor subagent with phase CLAUDE.md + upstream artifacts.
    Executor produces artifact + structured verdict.

    # 3. REVIEW
    Spawn reviewer(s) per phase review tier (see core/review.md):
      Phase 0, 2       → Self + Plot Validator
      Phase 1           → 4-bot (Physics + Critical + Constructive + Arbiter)
      Phase 3, 6        → 1-bot (Critical + Plot Validator)
      Phase 4a, 4b      → 4-bot+bib (above + Plot Validator + BibTeX)
      Phase 5, 7        → 5-bot (above + Rendering)
      VC1 full/light    → 5 ARC specialists (parallel)
      VC2 full/light    → 5 independent reviewers (parallel, isolated)
    Reviewers produce findings with A/B/C categories.

    # 4. FIX LOOP
    while A-items or B-items remain:
        Spawn Fixer with finding + artifact.
        Re-review: A-items by FRESH reviewer, B by same reviewer.
        Respect iteration caps (review.md Section 5):
          4/5-bot: warn@3, strong-warn@5, hard-cap@10
          1-bot:   warn@2, escalate@3
        If hard cap hit → file regression ticket, regress to earlier phase.

    # 5. COMMIT
    Commit phase artifacts to repository.
    Append to experiment log: phase, session, verdict, rationale.

    # 6. GATE CHECK
    If phase = VC2_full → halt for HUMAN GATE.
      Present package (see core/blinding.md).
      Wait for APPROVE / ITERATE / REGRESS / PAUSE.
      Only APPROVE advances to Phase 6.
    If phase = VC2_light → analysis complete. Produce final deliverables.
    Otherwise → advance to next phase in SEQUENCE.

    # 7. REGRESSION CHECK
    After every review verdict, check regression triggers (review.md
    Section 6). If triggered:
      Investigator traces root cause → REGRESSION_TICKET.md
      Fixer re-runs target phase
      All downstream phases re-execute and re-review
      Resume at triggering phase
```

### Post-Review Decision Tree

```
Verdict = PASS, no A/B items?
  → COMMIT, advance to next phase.

Verdict has B-items only?
  → Spawn Fixer, re-review by same reviewer, loop.

Verdict has A-items?
  → Spawn Fixer, re-review by FRESH reviewer, loop.

Hard cap reached?
  → File regression ticket, regress to earlier phase.

Regression trigger matched?
  → Investigator traces, fix at origin, cascade downstream.

Phase = HUMAN GATE and response = REGRESS(N)?
  → Return to Phase N, re-traverse to gate.
```

---

## Context Assembly

Subagents get exactly 3 context layers. No more.

### Layer 1: Bird's-Eye Framing

Short paragraph:
- Analysis identity (process, channel, dataset).
- Current phase.
- Agent's specific task within phase.

### Layer 2: Relevant Methodology

Cherry-picked sections from phase CLAUDE.md for this agent's task.
Never dump entire doc. Select only needed sections.

### Layer 3: Upstream Artifacts

Concrete outputs from prior phases/parallel agents. Examples: skim
path, cut table, BDT model path, systematic variation list.

### Phase CLAUDE.md

Each phase has CLAUDE.md = single runtime doc. Orchestrator assembles
before phase: methodology refs + task defs + artifact paths. Agents
treat as complete spec.

---

## Session Identity

Every subagent gets random human-readable name (e.g., "cedar-fox").

- Format: `{adjective}-{noun}` or `{material}-{animal}`.
- Unique within phase.
- Experiment log references by name, not IDs.
- Names appear in commit messages for traceability.

---

## Subagent Lifecycle

```
Orchestrator                          Subagent
    |                                     |
    |-- assemble context (3 layers) ----->|
    |                                     |-- reads phase CLAUDE.md
    |                                     |-- produces artifact
    |                                     |-- produces session log
    |                                     |-- writes structured verdict
    |<--- summary + verdict --------------|
    |                                     X  (context discarded)
    |-- records in experiment log
    |-- commits artifact (if PASS)
```

- Subagent memory = ephemeral. Post-return, all state gone. No follow-up questions to same session.
- Verdict = structured (PASS/FAIL/PARTIAL + summary + issues).
- On FAIL → new session with failure summary in Layer 3.

---

## Parallelism Patterns

### Parallelize when:

- Agents read same upstream but write to disjoint outputs.
- Operating on disjoint channels or systematics.
- Validation checks independent of each other.

### Serialize when:

- Agent B consumes Agent A's output.
- Validator must see producer output before next producer starts.
- Human gate between phases.

### Scaling Rules

1. Estimate time before choosing serial vs. parallel. 2-min task = no parallelism. 30-min/channel × 3 channels = parallelize.
2. Calibrate on small sample first. Run 1 agent on reduced sample → verify task def → then scale.
3. Cap at 5 concurrent subagents. Beyond that, verdict tracking degrades.

### Concrete Patterns

**VC1:** 5 validators parallel. Each validates one aspect. Wait for all 5.

**VC2:** Same structure, different criteria via Layer 2. Strict isolation.

**Phase 7 sub-agents:** Validator spawns 3 sub-agents (one per channel). Collects sub-verdicts → single verdict to orchestrator.

**Serial chain:** Skim → Selection → BDT → Limit. Each waits for prior PASS.

---

## Binding Commitment Tracking

Definitive statement in Phase N = **binding commitment** in all subsequent phases. Examples:
- "DeepTau v2p5 as tau ID discriminant." (Phase 1)
- "QCD estimated via ABCD method." (Phase 2)
- "bb invariant mass window [90, 150] GeV." (Phase 3)

Rules:
1. Orchestrator maintains commitment list, tagged by phase + session.
2. At each transition → check all prior commitments still fulfilled.
3. Unfulfilled commitment = **Category A**. Phase blocked until resolved or explicitly revised with justification.
4. Revising commitment → re-validate all downstream phases that depend on it.

---

## Experiment Log

Single source of truth. Append-only.

Each entry: timestamp, session name, phase, action, verdict (if applicable), rationale (one sentence).

- **Append-only.** Reversals = new entry referencing original.
- **Every spawn logged.** Including context layers.
- **Every verdict logged.** Including FAILs + corrective action.
- **Human gate decisions verbatim.** Exact response + notes.

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Correct Approach |
|---|---|---|
| Orchestrator writes "just a small fix" in code | Breaks accountability; no specialist reviewed it | Spawn a specialist, even for one-liners |
| Dumping full CLAUDE.md to every agent | Wastes context window; agents hallucinate from irrelevant sections | Curate 3 layers per agent |
| Reusing a subagent session for a second task | Session context is stale and polluted | Spawn a fresh session |
| Launching parallel agents before calibrating | One broken task definition wastes all parallel runs | Run one agent on small sample first |
| Skipping commitment check at phase transition | Silent methodology drift | Always diff commitments before proceeding |
| Editing experiment log to "clean up" | Destroys audit trail | Append a correction entry instead |
| Orchestrator interprets a FAIL as "close enough" | Undermines validator authority | FAIL means FAIL; fix and re-run |
