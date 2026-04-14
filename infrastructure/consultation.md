# Consultation -- when and how to seek second opinions

## When to ask

- **Ambiguous features**: distribution shows bump or deficit that could be signal, fluctuation, or detector artifact.
- **Multiple valid hypotheses**: two+ explanations fit data equally well, cannot distinguish with available information.
- **Unfamiliar detector**: working with experiment whose detector geometry, reconstruction, or calibration you have not encountered before.
- **Borderline significance**: observed excess between 2 sigma and 3 sigma where interpretation depends heavily on systematic choices.
- **Contradictory cross-checks**: two independent cross-checks give inconsistent results, cannot identify which (or both) = wrong.

## When NOT to ask

- Answer = in data but you have not looked yet. Look first.
- You want specific number. Run code.
- Confirming something you already know. Write test instead.
- Need code syntax help. Read documentation or heuristics.

## Question template

When requesting consultation, structure as:

```
Phase: [current phase]
Dataset: [what data/MC you are working with]
What I observe: [factual description of the feature or problem]
What I've tried: [list of investigations already performed]
My hypotheses: [ranked list of possible explanations]
Specific question: [exactly what you want the consultant to address]
```

Incomplete questions returned for clarification.

## What to trust from consultation

**Trust**:
- Physics reasoning and qualitative arguments.
- Methodology suggestions (e.g. "try alternative background model").
- Sanity checks ("that cross-section = order-of-magnitude wrong").

**Do NOT trust**:
- Numerical values recalled from memory. Every number must come from code or cited reference.
- Jumped conclusions ("it's obviously X"). Require reasoning chain.
- Claims about your specific dataset that consultant has not examined.

## Routing

- **Sub-agent**: preferred for physics reasoning, statistical methods, analysis strategy. Sub-agent can be spawned with relevant context.
- **User**: for institutional knowledge (detector quirks, analysis group conventions, unpublished calibrations, group policy decisions).
- **Web search**: for published measurements, PDG values, generator documentation, software API references.

## After consultation

1. Log consultation and conclusion in mempalace.
2. Test every suggestion with code before adopting.
3. Do not anchor on first answer. If suggestion does not survive quantitative test → discard it, try next hypothesis.
