# Suggestions -- skill evolution framework

Agents may propose improvements to framework between analyses. How system learns and improves without compromising scientific rigor.

## What is allowed

- **Documentation clarity**: rewriting confusing instructions, adding examples, fixing ambiguities.
- **Better error handling**: catching failure modes discovered during analysis.
- **New statistical methods**: methods published in peer-reviewed literature or established in field. Must include citation.
- **Better validation**: additional cross-checks, tighter quality gates, new diagnostic plots.
- **Workflow efficiency**: reducing unnecessary steps, parallelizing independent tasks, caching intermediate results.
- **Tooling**: new tool idioms, better library usage patterns, utility functions.
- **New reference documents**: convention files for uncovered analysis types, technique guides, experiment-specific notes.

## What is NEVER allowed

- Bypassing discovery process (e.g. "skip Phase 2 if channel = well-known").
- Skipping validation steps (e.g. "closure tests unnecessary for simple counting experiments").
- Weakening anti-hallucination rules (e.g. "allow recalled cross-sections without citation").
- Using prior analysis results to bias new analysis (e.g. "start with cuts from last analysis").
- Reducing verification steps in review (e.g. "VC2 = redundant if VC1 passed").
- Hardcoding physics values (e.g. "Higgs mass = 125.1 GeV").

## Litmus test

Before submitting, ask:

> "Would this improvement still work correctly if underlying physics were completely different from what we expect?"

If no → suggestion encodes physics assumption → must be rejected.

## Submission format

File name: `YYYY-MM-DD_<short-title>.md`

```markdown
# Suggestion: <title>

**Category**: [documentation | error-handling | statistics | validation |
               workflow | tooling | reference]
**Problem**: What current behavior is suboptimal and why.
**Proposed change**: Exact description of what to add, modify, or remove.
**Why this is safe**: Argument that this does not compromise rigor.
**Risk assessment**: What could go wrong and how to detect it.
```

Suggestions attributed by role only (e.g. "Executor", "VC1 Chair"), not by session or conversation identifier.

## Review process

1. Suggestions accumulate in `infrastructure/suggestions/pending/`.
2. Between analyses, user reviews pending suggestions.
3. Each suggestion either accepted (moved to relevant document) or rejected (moved to `suggestions/rejected/` with reason).
4. Rejected suggestions kept for reference -- document ideas considered and why not adopted.
