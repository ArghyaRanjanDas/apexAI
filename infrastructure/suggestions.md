# Suggestions -- skill evolution framework

Agents may propose improvements to the framework between analyses.
This is how the system learns and improves without compromising
scientific rigor.

## What is allowed

- **Documentation clarity**: rewriting confusing instructions, adding
  examples, fixing ambiguities.
- **Better error handling**: catching failure modes that were discovered
  during an analysis.
- **New statistical methods**: methods published in peer-reviewed
  literature or established in the field. Must include a citation.
- **Better validation**: additional cross-checks, tighter quality gates,
  new diagnostic plots.
- **Workflow efficiency**: reducing unnecessary steps, parallelizing
  independent tasks, caching intermediate results.
- **Tooling**: new tool idioms, better library usage patterns, utility
  functions.
- **New reference documents**: convention files for analysis types not
  yet covered, technique guides, experiment-specific notes.

## What is NEVER allowed

- Bypassing the discovery process (e.g. "skip Phase 2 if the channel
  is well-known").
- Skipping validation steps (e.g. "closure tests are unnecessary for
  simple counting experiments").
- Weakening anti-hallucination rules (e.g. "allow recalled cross-sections
  without citation").
- Using prior analysis results to bias a new analysis (e.g. "start with
  the cuts from the last analysis").
- Reducing verification steps in review (e.g. "VC2 is redundant if VC1
  passed").
- Hardcoding physics values (e.g. "the Higgs mass is 125.1 GeV").

## Litmus test

Before submitting a suggestion, ask:

> "Would this improvement still work correctly if the underlying physics
> were completely different from what we expect?"

If the answer is no, the suggestion encodes a physics assumption and
must be rejected.

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

Suggestions are attributed by role only (e.g. "Executor", "VC1 Chair"),
not by session or conversation identifier.

## Review process

1. Suggestions accumulate in `infrastructure/suggestions/pending/`.
2. Between analyses, the user reviews the pending suggestions.
3. Each suggestion is either accepted (moved to the relevant document)
   or rejected (moved to `suggestions/rejected/` with a reason).
4. Rejected suggestions are kept for reference -- they document ideas
   that were considered and why they were not adopted.
