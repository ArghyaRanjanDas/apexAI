# Staged Unblinding Protocol

## Data Exposure by Phase

| Phase | Data Used | Purpose |
|-------|-----------|---------|
| 1-3 | MC only | Selection development, background modeling, systematics |
| 4a | Asimov data + MC pseudo-data | Validate fit machinery, expected limits, signal injection |
| 4b | 10% real data (fixed seed) | Controlled validation against real detector conditions |
| 5 | 10% data (same as 4b) | Draft AN uses 10% results; methodology complete |
| 6 | Full data | Final observed results (methodology frozen) |
| 7 | Full data | Final AN updated with full results |

## Phase 4b: 10% Data Rules

- Fixed random seed for event selection (reproducible subset).
- MC normalized to 10% of total luminosity.
- All comparisons are data vs. scaled-MC in the 10% subset.
- No iteration on selection or methodology based on 4b observations.

## Pre-Gate Verification Flow

After Phase 4b, the analysis enters a three-stage verification sequence
before any human sees it. This ensures humans judge a **complete, AI-attested,
endorsed package** — not raw partial results.

```
Phase 4b (10% results)
  → Phase 5 (draft AN — complete methodology + 10% numbers)
    → 5-bot internal review (physics + critical + constructive + plot + rendering + bibtex → arbiter)
      → VC1 full review (5 specialist reviewers attest the draft)
        → VC2 full review (5 independent reviewers — adversarial, cross-analyst, blind audit)
          → HUMAN GATE (multiple humans judge the AI-verified package)
```

## Human Gate

After VC1 and VC2 have both passed, the orchestrator presents the following
to the human arbiter(s):

**Materials presented:**
- Complete draft AN (VC1+VC2 endorsed, all methodology sections final)
- VC1 review reports + response documents
- VC2 review reports (adversarial results, cross-analyst comparison, blind audit)
- Unblinding checklist (below)

**Response options:**

| Response | Meaning |
|----------|---------|
| **APPROVE** | Proceed to Phase 6 (full data). Methodology frozen. |
| **ITERATE** | Issue fixable within draft scope; fix, re-review, re-present |
| **REGRESS(N)** | Problem traces to Phase N; return there, re-traverse to gate |
| **PAUSE** | External input needed (POG recommendation, convener guidance) |

## Unblinding Checklist

All items must be satisfied before humans are asked to rule.

- [ ] Background model validated (closure test passes)
- [ ] Systematics stable (no single nuisance >30% post-fit swing between 4a and 4b)
- [ ] Expected results sensible (Asimov limits within physics priors)
- [ ] Signal injection test passes (recovered within 1σ)
- [ ] 10% data healthy (data/MC agreement, no pathological pulls)
- [ ] Perturbation tests pass (scale, removal, injection)
- [ ] Draft AN complete (all methodology sections, all figures, all systematics)
- [ ] 5-bot review: PASS
- [ ] VC1 review: ALL 5 members PASS
- [ ] VC2 review: ALL 5 members PASS

## Post-Approval Rules

1. **Methodology freeze.** All methodology sections frozen after human approval.
   Phase 6 touches results sections only.
2. **No re-optimization.** Selection cuts, BDT working points, and binning locked.
3. **Anomaly escalation.** If any Phase 6 result deviates >2σ from Phase 4a
   expected, escalate to 4-bot review before updating results.
4. **Append-only log.** Every Phase 6-7 action recorded in experiment log.
5. **Post-gate VC passes.** After Phase 7, VC1 and VC2 run light passes
   (results integration and reproducibility only — methodology already endorsed).
