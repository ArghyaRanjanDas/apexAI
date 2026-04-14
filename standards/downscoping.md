# Scope Management and Downscoping

Downscoping is a last resort when the full-strength approach is genuinely
infeasible. It is not a shortcut for avoiding difficulty, and it is not the
default response to a hard problem. Every downscope weakens the analysis.
This standard ensures the weakening is documented, quantified, and justified.

---

## When to Downscope

Downscoping is justified only when the stronger approach has been attempted
and failed, or when attempting it is demonstrably infeasible (not merely
difficult or uncertain).

Concrete triggers:
- Data or MC genuinely unavailable (not "hard to use" -- unavailable)
- Insufficient MC statistics after exploring all available samples
- Compute limits that make the method impossible within the resource
  envelope (not "slower than we'd like" -- impossible)
- Missing external inputs with no viable substitute
- Method attempted and shown to fail (with documented evidence)

"The alternative might not work" or "the alternative would be harder" are
NOT sufficient justifications. If the alternative is the stronger method,
try it first.

---

## How to Downscope

### Step 0: Attempt the full-strength approach first

Before downscoping, the analyst must either:
(a) attempt the stronger method and document its failure, or
(b) document why attempting it is infeasible (not merely difficult).

"We expected it wouldn't work" is not evidence. "We tried it and it failed
because [specific reason] -- see outputs/debug/failed_svd_closure.png" is.

### Step 1: Document the constraint

Record the constraint in the experiment log with a [D] label:
`[D] SVD unfolding: co-primary -> cross-check (diagonal fraction 24.7%,
below 30% threshold)`.

### Step 2: Choose the best achievable alternative

Fall back along the complexity ladder. Examples:
- GNN -> BDT -> cut-based
- Full unfolding -> bin-by-bin correction -> efficiency correction
- Per-bin systematics -> envelope systematic -> literature value

When a method's role changes (co-primary -> cross-check, primary ->
abandoned), label the status change explicitly in the experiment log.
Silent status changes -- where a method quietly disappears or is relabeled
without documentation -- are Category A at review.

### Step 3: Quantify the impact

Estimate what the missing resource or method would contribute. State what
the analysis loses by downscoping: wider uncertainty band, reduced kinematic
coverage, coarser binning, weaker model discrimination.

### Step 4: Carry to the analysis note

Every downscoping decision must appear in the AN in three places:
- The method section (what was used instead and why)
- The systematic uncertainties table (additional uncertainty from the
  weaker method, if applicable)
- The Future Directions section (what the stronger approach would require)

A limitation that exists only in the experiment log is not properly documented.

---

## Key Scenarios

### Missing MC

If a background process has no dedicated MC sample:
- Omit if the contribution is small (< 1% of the total), with a
  quantitative justification from theory or adjacent measurements.
- Estimate from theory: use sigma x epsilon from a similar process
  at a similar energy, cite the source, and assign a conservative
  uncertainty (50--100%).
- Never silently ignore a missing background without stating its
  expected contribution.

### Low MC statistics

When available MC statistics are insufficient for the desired binning
or precision:
- Use coarser binning or merge regions.
- Switch from shape analysis to cut-and-count.
- Include MC statistical uncertainty via Barlow-Beeston lite parameters
  in the fit model.
- State the effective number of MC events per bin in the AN.

### Cannot evaluate a specific systematic from own data

When a systematic cannot be evaluated using the analysis dataset:
- Never leave the uncertainty as zero. Zero is a statement that the
  effect does not exist, which is almost never true.
- Use a literature value obtained via INSPIRE or RAG, cite the source.
- Inflate conservatively if the literature value comes from a different
  energy, detector, or selection.
- State explicitly that the value is externally sourced and why direct
  evaluation is not possible.

### Skipping approach exploration

Choosing a simpler approach (e.g., cut-based over MVA) without trying the
alternative is itself a downscope. It must follow the standard protocol:
document the constraint that prevented the stronger approach, quantify
the expected impact on sensitivity or precision, and carry the limitation
to the AN.

Concerns about the alternative's costs (increased correlations, training
difficulty, data/MC modeling requirements) are valid constraints to
document, but they do not exempt the analysis from quantifying what was
foregone.

---

## Future Directions Policy

The default response to a feasible improvement is to implement it, not to
defer it to Future Directions.

When an improvement is identified during the analysis, the question is:
"Can this be done in < 2 hours of implementation + compute?" If yes, do it
now. If no, document it in Future Directions with a specific explanation
of what makes it infeasible.

### Future Directions IS for:
- Collecting more data (requires new running periods)
- Developing a new algorithm architecture (requires R&D)
- Running full detector simulation (requires multi-day compute + expertise)
- Obtaining external inputs not yet available (requires other groups)
- Installing software that cannot be made to work in the current environment
  (after documented installation failure)

### Future Directions is NOT for:
- Running an alternative generator at particle level (~30 min)
- Trying a contamination matrix correction on an existing tagger (~1 hour)
- Decomposing a systematic into normalization vs shape components (~1 hour)
- Overlaying published measurements from a thesis (~1 hour)
- Implementing a per-hemisphere truth label using available gen-level info
  (~1 hour)
- Attempting a data-driven calibration of an uncalibrated variable (~2 hours)

These are tasks that have been deferred in past analyses and later
implemented during regression in approximately the estimated time,
producing significant improvements each time.

---

## The Litmus Test

When writing a Future Directions item, ask:

> "Did you actually try the stronger approach, or just declare it infeasible?"

And:

> "If someone reading this said 'do it now,' could it be completed within
> the current session?"

If the answer to the second question is yes, it does not belong in Future
Directions. It belongs in the current plan.

---

## Review Checks

Reviewers verify three things for every downscoping decision:

1. **Was the stronger approach attempted?** Or is infeasibility documented
   with evidence (not just assertion)?
2. **Is the quantified impact credible?** Does the stated loss from
   downscoping match what is observed in the results?
3. **Is the limitation documented in the AN?** In the method section,
   the systematic table, and Future Directions?

Downscoping without evidence of attempting the stronger method is Category A.
Downscoping documented only in the experiment log but absent from the AN is
Category B.
