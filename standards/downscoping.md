# Scope Management and Downscoping

Downscoping = last resort when full-strength approach genuinely infeasible. Not shortcut for avoiding difficulty, not default response to hard problem. Every downscope weakens analysis. This standard ensures weakening documented, quantified, justified.

---

## When to Downscope

Justified only when stronger approach attempted and failed, or attempting it demonstrably infeasible (not merely difficult or uncertain).

Concrete triggers:
- Data or MC genuinely unavailable (not "hard to use" -- unavailable)
- Insufficient MC statistics after exploring all available samples
- Compute limits making method impossible within resource envelope (not "slower than we'd like" -- impossible)
- Missing external inputs with no viable substitute
- Method attempted and shown to fail (with documented evidence)

"Alternative might not work" or "alternative would be harder" = NOT sufficient justifications. Stronger method → try it first.

---

## How to Downscope

### Step 0: Attempt full-strength approach first

Before downscoping, analyst must either:
(a) attempt stronger method and document failure, or
(b) document why attempting infeasible (not merely difficult).

"Expected it wouldn't work" = not evidence. "Tried it, failed because [specific reason] -- see outputs/debug/failed_svd_closure.png" = evidence.

### Step 1: Document constraint

Record in experiment log with [D] label:
`[D] SVD unfolding: co-primary -> cross-check (diagonal fraction 24.7%, below 30% threshold)`.

### Step 2: Choose best achievable alternative

Fall back along complexity ladder. Examples:
- GNN → BDT → cut-based
- Full unfolding → bin-by-bin correction → efficiency correction
- Per-bin systematics → envelope systematic → literature value

Method's role changes (co-primary → cross-check, primary → abandoned) → label status change explicitly in experiment log. Silent status changes -- method quietly disappears or gets relabeled without documentation -- = Category A at review.

### Step 3: Quantify impact

Estimate what missing resource or method would contribute. State what analysis loses: wider uncertainty band, reduced kinematic coverage, coarser binning, weaker model discrimination.

### Step 4: Carry to analysis note

Every downscoping decision must appear in AN in three places:
- Method section (what used instead and why)
- Systematic uncertainties table (additional uncertainty from weaker method, if applicable)
- Future Directions section (what stronger approach would require)

Limitation existing only in experiment log = not properly documented.

---

## Key Scenarios

### Missing MC

Background process has no dedicated MC sample:
- Omit if contribution small (< 1% of total), with quantitative justification from theory or adjacent measurements.
- Estimate from theory: use sigma x epsilon from similar process at similar energy, cite source, assign conservative uncertainty (50--100%).
- Never silently ignore missing background without stating expected contribution.

### Low MC statistics

Available MC statistics insufficient for desired binning or precision:
- Use coarser binning or merge regions.
- Switch from shape analysis to cut-and-count.
- Include MC statistical uncertainty via Barlow-Beeston lite parameters in fit model.
- State effective MC events per bin in AN.

### Cannot evaluate specific systematic from own data

Systematic can't be evaluated using analysis dataset:
- Never leave uncertainty as zero. Zero = statement effect doesn't exist, almost never true.
- Use literature value via INSPIRE or RAG, cite source.
- Inflate conservatively if literature value from different energy, detector, or selection.
- State explicitly value externally sourced and why direct evaluation not possible.

### Skipping approach exploration

Choosing simpler approach (e.g., cut-based over MVA) without trying alternative = itself downscope. Must follow standard protocol: document constraint preventing stronger approach, quantify expected impact on sensitivity/precision, carry limitation to AN.

Concerns about alternative's costs (increased correlations, training difficulty, data/MC modeling requirements) = valid constraints to document, but don't exempt analysis from quantifying what was foregone.

---

## Future Directions Policy

Default response to feasible improvement = implement it, not defer to Future Directions.

Improvement identified during analysis → question: "Can this be done in < 2 hours of implementation + compute?" Yes → do it now. No → document in Future Directions with specific explanation of what makes it infeasible.

### Future Directions IS for:
- Collecting more data (requires new running periods)
- Developing new algorithm architecture (requires R&D)
- Running full detector simulation (requires multi-day compute + expertise)
- Obtaining external inputs not yet available (requires other groups)
- Installing software that can't work in current environment (after documented installation failure)

### Future Directions NOT for:
- Running alternative generator at particle level (~30 min)
- Trying contamination matrix correction on existing tagger (~1 hour)
- Decomposing systematic into normalization vs shape components (~1 hour)
- Overlaying published measurements from thesis (~1 hour)
- Implementing per-hemisphere truth label using available gen-level info (~1 hour)
- Attempting data-driven calibration of uncalibrated variable (~2 hours)

These = tasks deferred in past analyses, later implemented during regression in approximately estimated time, producing significant improvements each time.

---

## Litmus Test

When writing Future Directions item, ask:

> "Did you actually try stronger approach, or just declare it infeasible?"

And:

> "If someone reading this said 'do it now,' could it complete within current session?"

Second answer = yes → doesn't belong in Future Directions. Belongs in current plan.

---

## Review Checks

Reviewers verify three things for every downscoping decision:

1. **Stronger approach attempted?** Or infeasibility documented with evidence (not just assertion)?
2. **Quantified impact credible?** Stated loss from downscoping matches what observed in results?
3. **Limitation documented in AN?** In method section, systematic table, and Future Directions?

Downscoping without evidence of attempting stronger method = Category A. Downscoping documented only in experiment log but absent from AN = Category B.
