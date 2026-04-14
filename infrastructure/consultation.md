# Consultation -- when and how to seek second opinions

## When to ask

- **Ambiguous features**: a distribution shows a bump or deficit that
  could be signal, fluctuation, or detector artifact.
- **Multiple valid hypotheses**: two or more explanations fit the data
  equally well and you cannot distinguish them with available information.
- **Unfamiliar detector**: working with an experiment whose detector
  geometry, reconstruction, or calibration you have not encountered before.
- **Borderline significance**: observed excess between 2 sigma and 3
  sigma where the interpretation depends heavily on systematic choices.
- **Contradictory cross-checks**: two independent cross-checks give
  inconsistent results and you cannot identify which (or both) is wrong.

## When NOT to ask

- The answer is in the data but you have not looked yet. Look first.
- You want a specific number. Run the code.
- You are confirming something you already know. Write the test instead.
- You need code syntax help. Read the documentation or the heuristics.

## Question template

When requesting consultation, structure the question as:

```
Phase: [current phase]
Dataset: [what data/MC you are working with]
What I observe: [factual description of the feature or problem]
What I've tried: [list of investigations already performed]
My hypotheses: [ranked list of possible explanations]
Specific question: [exactly what you want the consultant to address]
```

Incomplete questions will be returned for clarification.

## What to trust from a consultation

**Trust**:
- Physics reasoning and qualitative arguments.
- Methodology suggestions (e.g. "try an alternative background model").
- Sanity checks ("that cross-section is order-of-magnitude wrong").

**Do NOT trust**:
- Numerical values recalled from memory. Every number must come from
  code or a cited reference.
- Jumped conclusions ("it's obviously X"). Require the reasoning chain.
- Claims about your specific dataset that the consultant has not
  examined.

## Routing

- **Sub-agent**: preferred for physics reasoning, statistical methods,
  and analysis strategy. The sub-agent can be spawned with the relevant
  context.
- **User**: for institutional knowledge (detector quirks, analysis group
  conventions, unpublished calibrations, group policy decisions).
- **Web search**: for published measurements, PDG values, generator
  documentation, and software API references.

## After consultation

1. Log the consultation and its conclusion in the mempalace.
2. Test every suggestion with code before adopting it.
3. Do not anchor on the first answer. If the suggestion does not survive
   a quantitative test, discard it and try the next hypothesis.
