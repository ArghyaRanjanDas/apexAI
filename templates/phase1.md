# Phase 1: Strategy -- {{name}}

Type: {{analysis_type}}

---

## Objective

Commit to an analysis plan before writing any analysis code. The strategy
is binding -- departures after approval require re-review at the same tier.
Every decision is labeled [A] Assumption, [L] Limitation, or [D] Decision.

---

## Tasks

### 1a. Query the Corpus

1. **Read all applicable conventions** in `conventions/`. For each file,
   state "Will implement" or "Not applicable because [reason]."

2. **Search the techniques library** (`techniques/`) for relevant methods.
   Note which fitting, extraction, and statistical approaches apply.

### 1b. Enumerate Backgrounds

3. **List all expected backgrounds** for the signal process. For each:
   name, production mechanism, expected contribution relative to signal,
   estimation method (MC, data-driven, or hybrid), key discriminating
   variables.

### 1c. Define Selection Approaches

4. **Define at least two qualitatively different selection approaches.**
   Both are carried through Phase 3. "Cut-based vs MVA" qualifies;
   "tight vs loose" does not. For each approach: description, expected
   signal efficiency, expected background rejection, key variables.

### 1d. Systematic Catalog

5. **Enumerate every systematic source** with:

   | Source | Category | Method | Expected magnitude | Reference |
   |--------|----------|--------|-------------------|-----------|
   | ... | exp/theo/model | ... | ... | ... |

   Categories: experimental, theoretical, modeling. Sources to consider:
   luminosity, trigger efficiency, lepton ID/isolation, JES/JER, b-tag
   scale factors, pileup, PDF, QCD scale, parton shower, MC generator,
   signal/background modeling, MC statistics.

   Every variation must be motivated by a measurement or published
   uncertainty. Arbitrary conservative inflations are Category A.

### 1e. Reference Analyses

6. **Identify 3+ published analyses** of the same or similar process.
   For each: citation, technique, dataset, key result, systematic program.
   This table is a binding input to Phase 4 and Phase 5 reviews.

### 1f. Flagship Figures

7. **Define approximately 6 flagship figures:**

   | # | Title | Observable | Expected content | Phase | AN location |
   |---|-------|-----------|-----------------|-------|-------------|
   | 1 | ... | ... | ... | ... | ... |

### 1g. Binding Commitments

8. **Label every element** in the strategy:
   - **[A]** Assumption -- taken as given, not verified in this analysis
   - **[L]** Limitation -- known weakness, impact quantified
   - **[D]** Decision -- deliberate choice, binding in subsequent phases

---

## Deliverables

- `outputs/STRATEGY.md` containing items 1-8
- Systematic catalog with per-source details
- Reference analysis table
- Flagship figure list
- All elements labeled [A]/[L]/[D]

## Review Tier

**4-bot.** Physics + Critical + Constructive -> Arbiter. A-items block
advancement. The strategy is binding -- departures require re-review.

## References

- `conventions/` -- all convention files
- `techniques/fitting.md` -- model catalog
- `techniques/statistics.md` -- significance, limits, GoF
- `techniques/signal_extraction.md` -- sideband, OS-SS, ABCD, template
