# Conventions

Living domain-knowledge documents for specific analysis techniques. Encode what senior physicist expects in well-executed analysis.

## Role in workflow

Consulted at three points:

- **Phase 1 (Strategy)** -- enumerate required systematic sources + validation checks. Agent must state "Will implement" for each required item or document "Not applicable because [reason]". Enumeration = binding.
- **Phase 4a (Expected results)** -- verify systematic completeness against convention checklist before proceeding to data.
- **Phase 5 / Phase 7 (Analysis note)** -- ensure methodology + results sections address every convention requirement.

## When updated

After each completed analysis, executor and reviewers may propose additions from lessons learned. Proposals follow suggestion framework in `infrastructure/suggestions.md`. Accepted changes merged into relevant convention document.

## Document structure

Every convention document follows this layout:

1. **When this applies** -- conditions triggering this convention.
2. **Standard configuration** -- default choices unless justified otherwise.
3. **Required systematic sources** -- categorized list. Each item must be addressed in strategy phase.
4. **Required validation checks** -- quality gates that must pass before results = trustworthy.
5. **Known pitfalls** -- failure modes from prior analyses, with why they are dangerous.

## Binding obligation

Required systematic sources and validation checks = not suggestions. Agents must produce response for every listed item:

- "Will implement: [brief plan]"
- "Not applicable because: [physics or procedural reason]"

Skipping item without explanation = Category A review finding.

## Current conventions

| Document | Analysis type |
|----------|---------------|
| `extraction.md` | Counting experiments and efficiency/scale-factor extraction |
| `search.md` | Searches for new physics and limit setting |
| `unfolding.md` | Detector-level to particle-level corrections |

New convention documents added as framework encounters additional analysis types.
