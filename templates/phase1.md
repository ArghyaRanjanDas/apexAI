# Phase 1: Strategy -- {{name}}

Type: {{analysis_type}}

---

## Objective

Commit to analysis plan before writing any analysis code. Strategy =
binding -- departures after approval require re-review at same tier.
Every decision labeled [A] Assumption, [L] Limitation, or [D] Decision.

---

## Tasks

### 1a. Query Corpus

1. **Read all applicable conventions** in `conventions/`. Per file,
   state "Will implement" or "Not applicable because [reason]."

2. **Search techniques library** (`techniques/`) for relevant methods.
   Note which fitting, extraction, statistical approaches apply.

### 1b. Enumerate Backgrounds

3. **List all expected backgrounds** for signal process. Per background:
   name, production mechanism, expected contribution relative to signal,
   estimation method (MC, data-driven, or hybrid), key discriminating
   variables.

### 1c. Define Selection Approaches

4. **Define 2+ qualitatively different selection approaches.**
   Both carried through Phase 3. "Cut-based vs MVA" qualifies;
   "tight vs loose" does not. Per approach: description, expected
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

   Every variation must be motivated by measurement or published
   uncertainty. Arbitrary conservative inflations = Category A.

### 1e. Reference Analyses

6. **Identify 3+ published analyses** of same or similar process.
   Per analysis: citation, technique, dataset, key result, systematic
   program. Table = binding input to Phase 4 and Phase 5 reviews.

### 1f. Flagship Figures

7. **Define ~6 flagship figures:**

   | # | Title | Observable | Expected content | Phase | AN location |
   |---|-------|-----------|-----------------|-------|-------------|
   | 1 | ... | ... | ... | ... | ... |

### 1g. Binding Commitments

8. **Label every element** in strategy:
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

**4-bot.** Physics + Critical + Constructive → Arbiter. A-items block
advancement. Strategy = binding -- departures require re-review.

## References

- `conventions/` -- all convention files
- `techniques/fitting.md` -- model catalog
- `techniques/statistics.md` -- significance, limits, GoF
- `techniques/signal_extraction.md` -- sideband, OS-SS, ABCD, template
