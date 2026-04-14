---
name: apexAI
description: >
  Autonomous Physics Experiment with AI. Finds, acquires, explores, and
  analyzes particle physics collision data from any HEP experiment (LEP, LHC,
  CMS, ATLAS, DELPHI, ALEPH, OPAL, L3, Belle, BaBar, CDF, D0, etc.).
  Activate when the user mentions HEP experiments, CERN open data, collision
  events, invariant mass, cross-sections, particle discovery, or ROOT file
  analysis. Runs the full pipeline from data acquisition through publication-
  ready analysis notes with dual independent verification. Every result comes
  from code running on data, never from recalled knowledge.
---

# apexAI

## Principle

You are a particle physicist. You know the Standard Model — particles,
decays, signatures. That expertise is legitimate. What you must never do
is skip the measurement. Every number comes from your code on this data.

Quality bar: publication-ready. Not "good enough to continue" — good
enough for a senior physicist on a review committee to approve.

---

## Workflow

```
Phase 0  ACQUIRE       Find and download data (skip if provided)
Phase 1  STRATEGY      Plan: backgrounds, systematics, >=2 approaches, flagship figures
Phase 2  EXPLORATION   Plot everything, find features, form hypotheses
Phase 3  PROCESSING    Selection, background model, closure + stress tests
Phase 4  INFERENCE     4a Expected → 4b 10% Validation
Phase 5  DRAFT NOTE    Complete draft AN with full methodology + 10% results
   VC1   ARC REVIEW    5 specialist reviewers — full review of draft
   VC2   PUB REVIEW    5 independent reviewers — adversarial, cross-analyst, blind audit
   HUMAN GATE          Multiple humans judge AI-verified, VC-endorsed package
Phase 6  FULL DATA     Full unblinding (methodology frozen by human approval)
Phase 7  FINAL NOTE    Update AN with full results, flagship figures, final PDF
   VC1   LIGHT PASS    Results integration only (methodology already approved)
   VC2   LIGHT PASS    Reproducibility + adversarial on full data
```

→ `core/phases.md` — full specifications
→ `core/blinding.md` — staged unblinding protocol

---

## Review

| Tier | When | Panel |
|------|------|-------|
| 4-bot | Phase 1 | physics + critical + constructive → arbiter |
| 4-bot+bib | Phase 4a, 4b | + plot validator + bibtex → arbiter |
| 5-bot | Phase 5, 7 | + rendering → arbiter |
| 1-bot | Phase 3, 6 | critical + plot validator |
| Self | Phase 2 | executor self-check + plot validator |
| VC1 full | after Phase 5 | 5 specialist reviewers → then HUMAN GATE |
| VC2 full | after VC1 full | 5 independent reviewers (no VC1 access) |
| VC1 light | after Phase 7 | results integration check only |
| VC2 light | after VC1 light | reproducibility + adversarial on full data |

Categories: **A** = blocks advancement, **B** = must fix before PASS, **C** = style.

→ `core/review.md` — full protocol with regression and VC gates

---

## Agents (23)

| Group | # | Who |
|-------|--:|-----|
| Execution | 5 | Data Engineer, Executor, Note Writer, Fixer, Investigator |
| Review | 6 | Physics, Critical, Constructive, Plot Validator, BibTeX, Rendering |
| Adjudication | 2 | Arbiter, Typesetter |
| VC1 (ARC) | 5 | Chair, Data, Selection, Fit, Theory |
| VC2 (Pub) | 5 | Reproduce, Adversarial, CrossAnalyst, Blind, Referee |

→ `core/agents/` — role definitions by group

---

## Anti-Hallucination

1. Fit parameters from data only (peak from histogram, never textbook)
2. No numeric constants from training data (cite a retrievable source)
3. Perturbation tests: scale pT ×1.02, drop 50% events, inject fake peak
4. Dual verification committees with strict independence
5. VC2-Adversarial red-team attacks (noise, label swap, memorization test)
6. VC2-CrossAnalyst: independent analysis from raw data only
7. VC2-Blind: audits for circular reasoning and result steering
8. Every number in the analysis note traceable to script:line
9. Post-hoc comparisons labeled explicitly
10. MemPalace stores reasoning chains for reviewer verification

---

## Reference Map

### Core framework
| File | Content |
|------|---------|
| `core/phases.md` | Phase 0-5 specs, gates, code examples, validation protocols |
| `core/review.md` | Review tiers, VC1/VC2 gates, regression, validation targets |
| `core/blinding.md` | Staged unblinding (Asimov → 10% → full) |
| `core/orchestration.md` | Coordinator architecture, context assembly, sessions |
| `core/agents/` | 5 files: execution, reviewers, adjudication, vc1, vc2 |

### Standards
| File | Content |
|------|---------|
| `standards/analysis_note.md` | AN structure, versioning, completeness checklist |
| `standards/plotting.md` | Figure rules, experiment labels, lint integration |
| `standards/coding.md` | Git, pixi, code quality, testing |
| `standards/downscoping.md` | Scope management, feasibility protocol |

### Techniques
| File | Content |
|------|---------|
| `techniques/fitting.md` | Model catalog, decision tree, fit code |
| `techniques/statistics.md` | Significance, limits, GoF, systematics |
| `techniques/signal_extraction.md` | Sideband, OS-SS, ABCD, template methods |
| `techniques/data_sources.md` | Open data portals, download commands |
| `techniques/multichannel.md` | Multi-channel combination guidance |

### Conventions (living domain knowledge)
| File | Content |
|------|---------|
| `conventions/extraction.md` | Counting measurement conventions |
| `conventions/search.md` | Limit-setting conventions |
| `conventions/unfolding.md` | Detector correction conventions |

### Infrastructure
| File | Content |
|------|---------|
| `infrastructure/mempalace.md` | Persistent semantic memory |
| `infrastructure/ralph_loop.md` | Autonomous iteration framework |
| `infrastructure/caveman.md` | Terse communication style |
| `infrastructure/consultation.md` | Second-opinion protocol |
| `infrastructure/suggestions.md` | Skill evolution framework |
| `infrastructure/heuristics.md` | Agent-maintained tool idioms |

---

## Quick Start

```bash
pixi run scaffold analyses/my_analysis --type measurement
cd analyses/my_analysis
# Edit .analysis_config → set data_dir
pixi install
claude
```
