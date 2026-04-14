# apexAI — Autonomous Physics Experiment with AI

An agent framework for autonomous high energy physics analysis. Given a
physics prompt and collision data (or just an experiment name), apexAI plans,
executes, reviews, and documents a publication-quality measurement or search
— from raw ROOT files to a typeset analysis note with full uncertainty budget.

## What it does

1. **Finds and acquires data** from open-data portals (ATLAS, CMS, LEP, Belle, etc.)
2. **Plans the analysis** — backgrounds, systematics, selection approaches, flagship figures
3. **Explores the data** — distributions, invariant mass spectra, feature detection
4. **Implements selection and corrections** — with closure tests, stress tests, approach comparison
5. **Extracts results** — staged unblinding (Asimov → 10% validation → full data)
6. **Writes the analysis note** — 50-100 page publication-quality document with PDF
7. **Reviews everything twice** — first through tiered multi-agent review (A/B/C classification), then through two independent verification committees (10 specialist reviewers)

Every number comes from code running on data. Never from recalled knowledge.

## Architecture

```
              ORCHESTRATOR (thin coordinator — never writes code)
                    │
    ┌───────────────┼───────────────────────────────────────┐
    ▼               ▼               ▼               ▼       ▼
 Phase 0         Phase 1-3       Phase 4          Phase 5   VC1 + VC2
 Acquire         Build           Measure           Write    Verify
 (Data Eng)      (Executor)      (4a/4b/4c)       (Scribe) (10 reviewers)
                                    │
                               HUMAN GATE
                            (after 10% validation)
```

**23 agents** organized into five groups:
- **Execution** (5): Data Engineer, Executor, Note Writer, Fixer, Investigator
- **Review** (6): Physics, Critical, Constructive, Plot Validator, BibTeX, Rendering
- **Adjudication** (2): Arbiter, Typesetter
- **VC1 — Analysis Review** (5): Chair, Data, Selection, Fit, Theory
- **VC2 — Publication Review** (5): Reproduce, Adversarial, CrossAnalyst, Blind, Referee

## Directory guide

```
apexAI/
├── SKILL.md              Skill trigger and workflow overview
├── core/                  Framework definition
│   ├── phases.md          Phase 0-5 specifications and gates
│   ├── review.md          Review tiers, VCs, regression protocol
│   ├── blinding.md        Staged unblinding protocol
│   ├── orchestration.md   How the orchestrator coordinates agents
│   └── agents/            Agent role definitions (grouped by function)
├── standards/             Quality requirements
│   ├── analysis_note.md   AN structure, versioning, completeness
│   ├── plotting.md        Figure production rules
│   ├── coding.md          Git, pixi, code quality
│   └── downscoping.md     When and how to reduce scope
├── techniques/            Analysis methods with code examples
│   ├── fitting.md         Model catalog and decision tree
│   ├── statistics.md      Hypothesis testing, limits, systematics
│   ├── signal_extraction.md  Sideband, ABCD, template methods
│   ├── data_sources.md    Open data portals and download commands
│   └── multichannel.md    Multi-channel combination
├── conventions/           Living operational knowledge per technique
├── infrastructure/        Agent tools (MemPalace, ralph-loop, etc.)
├── scripts/               Executable tooling (scaffold, lint, postprocess)
└── templates/             Analysis workspace templates (CLAUDE.md per phase)
```

## Getting started

```bash
# Scaffold a new analysis
pixi run scaffold analyses/my_analysis --type measurement
cd analyses/my_analysis

# Point to your data
echo "data_dir=/path/to/root/files" >> .analysis_config

# Install environment and launch
pixi install
claude   # pass your physics prompt
```

For autonomous iteration:
```
/ralph-loop "Execute full analysis + verification pipeline.
Phase 0-5, then VC1 and VC2. Every number from data."
--max-iterations 40
--completion-promise "Both verification committees satisfied"
```

## Provenance

apexAI synthesizes ideas from two complementary frameworks:
- An experiment-agnostic HEP discovery agent with perturbation tests, dual
  verification committees, and persistent semantic memory
- JFC (Just Furnish Context, arxiv 2603.20179) — a formal phased methodology
  with tiered multi-agent review, phase regression, and living conventions

Neither source was copied. Every file was written from scratch as a genuine
synthesis, organized by what a physicist needs rather than by where the idea
originated.

## Requirements

- [pixi](https://pixi.sh) for environment management
- [Claude Code](https://claude.ai/claude-code) as the agent runtime
- Python >= 3.11
