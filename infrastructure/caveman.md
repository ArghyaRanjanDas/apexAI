# Caveman -- terse communication style

## Core pattern

```
[thing] [action] [reason]. [next step].
```

Every message follows this skeleton. No preamble, no hedging, no filler.

## Rules

- Drop articles, drop fillers, drop pleasantries.
- Sentence fragments are fine.
- Technical terms are never abbreviated -- write "pseudorapidity" not
  "prap", write "transverse momentum" not "pT" on first use.
- Numbers always include units.
- Uncertainty always accompanies a measurement.

## Where it applies

- Agent-to-user chat messages.
- Status updates and progress logs.
- Internal reasoning traces.
- Agent-to-agent messages (sub-agent calls, review comments in chat).

## Where it does NOT apply

Caveman style is suspended for deliverables and formal outputs:

- Analysis notes (Phase 5, 7) -- full academic prose.
- `results.json` -- structured data format.
- Plot axis labels and legends -- standard notation.
- Git commit messages -- conventional format.
- Review documents (VC1, VC2 findings) -- complete sentences for clarity.
- Security warnings -- unambiguous full sentences.

## Examples

**Bad**: "I've gone ahead and looked at the distribution of the
invariant mass of the two b-jets, and it seems like the peak is
located around 125 GeV, which is consistent with what we'd expect
from the Higgs boson decay."

**Good**: "mbb peaks at 125 GeV, consistent with H->bb. Next: fit
signal+background model."

**Bad**: "Sure! I'd be happy to help with that. Let me start by
checking the trigger efficiency for the ditau path."

**Good**: "Checking ditau trigger efficiency."

**Bad**: "The closure test has been completed successfully and all
bins agree within statistical uncertainty."

**Good**: "Closure passes, all bins within stat uncertainty. Moving
to stress test."
