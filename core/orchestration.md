# Orchestrator Coordination Guide

## What the Orchestrator Does

The orchestrator is a thin coordinator. Its job is strictly:

1. **Hold state**: the current prompt, phase summaries, and agent verdicts.
2. **Spawn subagents**: with curated context, never raw conversation history.
3. **Read verdicts**: parse each subagent's structured output.
4. **Commit artifacts**: write validated outputs to the repository.
5. **Track commitments**: carry forward binding statements from earlier phases.
6. **Maintain the experiment log**: append every decision, never edit prior entries.

## What the Orchestrator Does NOT Do

- **Never writes analysis code.** Not a single line. Code is produced by specialist agents.
- **Never interprets physics results.** It routes results to the appropriate reviewer.
- **Never holds full subagent context.** After a subagent finishes, its working
  context is discarded. The orchestrator retains only the summary and verdict.
- **Never overrides a specialist verdict.** If a validator says FAIL, the
  orchestrator acts on that verdict; it does not second-guess it.
- **Never skips the human gate.** Phase transitions that require human approval
  (see blinding.md) are blocking.
- **Never skips a phase.** The full sequence is mandatory:
  0 → 1 → 2 → 3 → 4a → 4b → 5 → VC1 → VC2 → HUMAN GATE → 6 → 7 →
  VC1 light → VC2 light. Each phase must produce its gate artifact and
  pass review before the next begins. If data is pre-provided, Phase 0
  still runs (verify + manifest).

---

## Context Assembly

Every subagent receives exactly three layers of context, assembled by the
orchestrator before spawn. Nothing more, nothing less.

### Layer 1: Bird's-Eye Framing

A short paragraph stating:
- What analysis this is (process, channel, dataset).
- What phase we are in.
- What this agent's specific task is within that phase.

### Layer 2: Relevant Methodology Sections

Cherry-picked sections from the phase CLAUDE.md that apply to this agent's
task. The orchestrator does not dump the entire methodology document. It selects
only the sections the agent needs.

### Layer 3: Upstream Artifacts

Concrete outputs from prior phases or parallel agents that this agent must
consume. Examples: a skim file path, a cut table, a BDT model path, a
systematic variation list.

### Phase CLAUDE.md

Each phase has a CLAUDE.md file. This is the single document that agents read at
runtime. The orchestrator assembles it before the phase begins by combining
methodology references, task definitions, and artifact paths. Agents treat it
as their complete specification.

---

## Session Identity

Every subagent session gets a random human-readable name (e.g., "cedar-fox",
"slate-heron"). Naming conventions:

- Format: `{adjective}-{noun}` or `{material}-{animal}`.
- Names are unique within a phase.
- The experiment log references sessions by name, not by internal IDs.
- Session names appear in artifact commit messages for traceability.

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

Key points:
- The subagent's working memory is ephemeral. Once it returns, all intermediate
  state is gone. The orchestrator must not assume it can ask follow-up questions
  to the same session.
- The verdict is a structured object (PASS/FAIL/PARTIAL + summary + issues).
- On FAIL, the orchestrator spawns a new session with the failure summary
  included in Layer 3 as upstream context.

---

## Parallelism Patterns

### When to Parallelize

Agents are independent when they:
- Read from the same upstream artifacts but do not write to each other's outputs.
- Operate on disjoint channels or systematics.
- Perform validation checks that do not depend on each other's verdicts.

### When to Serialize

Agents must run sequentially when:
- Agent B consumes Agent A's output artifact.
- A validator must see a producer's output before the next producer starts.
- A human gate stands between two phases.

### Scaling Rules

1. **Estimate processing time** before choosing serial vs. parallel. A 2-minute
   task does not need parallelism. A 30-minute-per-channel task across 3
   channels does.
2. **Calibrate on a small sample first.** Before launching N parallel agents,
   run one agent on a reduced sample to verify the task definition is correct.
   Fix issues cheaply before scaling.
3. **Cap concurrent agents.** No more than 5 parallel subagents at once. Beyond
   that, the orchestrator's ability to track verdicts degrades.

### Concrete Patterns

**Pattern: VC1 (Validation Campaign 1)**
All 5 validators launch in parallel. Each validates one independent aspect
(selection, background model, systematics, signal extraction, limit setting).
The orchestrator waits for all 5 verdicts before proceeding.

**Pattern: VC2 (Validation Campaign 2)**
Same as VC1 but for a different phase milestone. Same 5-parallel structure,
different validation criteria loaded via Layer 2.

**Pattern: Phase 7 Validator with Sub-Agents**
The Phase 7 validator itself spawns 3 sub-agents (one per channel: tauhtauh,
taumutauh, tauetauh). The validator collects sub-verdicts and synthesizes a
single verdict for the orchestrator. The orchestrator sees one verdict, not
three.

**Pattern: Serial Producer Chain**
Skim agent -> Selection agent -> BDT agent -> Limit agent. Each waits for
the previous to finish and pass.

---

## Binding Commitment Tracking

Any definitive statement made in Phase N is a **binding commitment** in all
subsequent phases. Examples:
- "We use DeepTau v2p5 as the tau ID discriminant." (Phase 1)
- "QCD is estimated from data using the ABCD method." (Phase 2)
- "The bb invariant mass window is [90, 150] GeV." (Phase 3)

Tracking rules:
1. The orchestrator maintains a list of binding commitments, tagged by the
   phase and session that produced them.
2. At each phase transition, the orchestrator checks: are all prior commitments
   still fulfilled in the current artifacts?
3. An unfulfilled commitment is a **Category A defect**: the phase cannot
   proceed until it is resolved (either the commitment is fulfilled or
   explicitly revised with justification logged).
4. Revising a commitment requires re-validation of all downstream phases that
   depended on it.

---

## Experiment Log

The experiment log is the single source of truth for what happened, when, and
why. It is append-only.

Each entry contains:
- Timestamp
- Session name
- Phase
- Action taken
- Verdict (if applicable)
- Rationale (one sentence)

Rules:
- **Append-only.** No edits to prior entries. If a decision is reversed, a new
  entry records the reversal and references the original entry.
- **Every spawn is logged.** Including the context layers provided.
- **Every verdict is logged.** Including FAIL verdicts and the subsequent
  corrective action.
- **Human gate decisions are logged verbatim.** The arbiter's exact response
  (APPROVE / ITERATE / REGRESS(N) / PAUSE) and any accompanying notes.

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
