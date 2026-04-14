# Conventions

Conventions are living domain-knowledge documents for specific analysis
techniques. They encode what a senior physicist would expect to see in a
well-executed analysis of a given type.

## Role in the workflow

Conventions are consulted at three points:

- **Phase 1 (Strategy)** -- enumerate required systematic sources and
  validation checks. The agent must either state "Will implement" for each
  required item or document "Not applicable because [reason]". This
  enumeration is binding.
- **Phase 4a (Expected results)** -- verify systematic completeness against
  the convention checklist before proceeding to data.
- **Phase 5 / Phase 7 (Analysis note)** -- ensure the written methodology
  and results sections address every convention requirement.

## When they are updated

After each completed analysis, the executor and reviewers may propose
additions based on lessons learned. Proposals follow the suggestion
framework in `infrastructure/suggestions.md`. Accepted changes are merged
into the relevant convention document.

## Document structure

Every convention document follows this layout:

1. **When this applies** -- conditions that trigger this convention.
2. **Standard configuration** -- default choices unless justified otherwise.
3. **Required systematic sources** -- categorized list. Each item must be
   addressed in the strategy phase.
4. **Required validation checks** -- quality gates that must pass before
   results are considered trustworthy.
5. **Known pitfalls** -- failure modes observed in prior analyses, with
   short explanations of why they are dangerous.

## Binding obligation

The required systematic sources and validation checks are not suggestions.
Agents must produce a response for every listed item:

- "Will implement: [brief plan]"
- "Not applicable because: [physics or procedural reason]"

Skipping an item without explanation is a Category A review finding.

## Current conventions

| Document | Analysis type |
|----------|---------------|
| `extraction.md` | Counting experiments and efficiency/scale-factor extraction |
| `search.md` | Searches for new physics and limit setting |
| `unfolding.md` | Detector-level to particle-level corrections |

New convention documents may be added as the framework encounters
additional analysis types.
