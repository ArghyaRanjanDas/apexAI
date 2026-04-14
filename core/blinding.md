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

- Fixed random seed. Reproducible subset.
- MC normalized to 10% luminosity.
- Comparisons = data vs. scaled-MC in 10% subset.
- No methodology iteration from 4b observations.

## Pre-Gate Verification Flow

Post-4b → three-stage verification before humans see anything.
Humans judge **complete, VC-endorsed package** only. No partial results.

```
Phase 4b (10% results)
  → Phase 5 (draft AN — complete methodology + 10% numbers)
    → 5-bot internal review (physics + critical + constructive + plot + rendering + bibtex → arbiter)
      → VC1 full review (5 specialist reviewers attest the draft)
        → VC2 full review (5 independent reviewers — adversarial, cross-analyst, blind audit)
          → HUMAN GATE (multiple humans judge the AI-verified package)
```

## Human Gate

VC1 + VC2 both PASS → orchestrator presents package to human arbiter(s).

**Materials:**
- Draft AN (VC1+VC2 endorsed, methodology final)
- VC1 reports + responses
- VC2 reports (adversarial, cross-analyst, blind audit)
- Unblinding checklist (below)

**Responses:**

| Response | Meaning |
|----------|---------|
| **APPROVE** | Proceed to Phase 6 (full data). Methodology frozen. |
| **ITERATE** | Fixable in draft scope → fix, re-review, re-present |
| **REGRESS(N)** | Problem traces to Phase N → return, re-traverse to gate |
| **PAUSE** | External input needed (POG, convener) |

## Unblinding Checklist

All must pass before humans rule.

- [ ] Background model validated (closure passes)
- [ ] Systematics stable (no nuisance >30% post-fit swing 4a↔4b)
- [ ] Expected results sensible (Asimov limits within physics priors)
- [ ] Signal injection passes (recovered within 1 sigma)
- [ ] 10% data healthy (data/MC agreement, no pathological pulls)
- [ ] Perturbation tests pass (scale, removal, injection)
- [ ] Draft AN complete (methodology, figures, systematics)
- [ ] 5-bot: PASS
- [ ] VC1: ALL 5 PASS
- [ ] VC2: ALL 5 PASS

## Post-Approval Rules

1. **Methodology freeze.** All methodology frozen. Phase 6 = results only.
2. **No re-optimization.** Cuts, BDT working points, binning locked.
3. **Anomaly escalation.** Phase 6 result >2 sigma from 4a expected → 4-bot review before updating.
4. **Append-only log.** Every Phase 6-7 action in experiment log.
5. **Post-gate VC passes.** After Phase 7 → VC1 + VC2 light passes (results integration + reproducibility only).
