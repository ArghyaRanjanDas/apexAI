# Mempalace -- persistent semantic memory

Persistent knowledge store backed by ChromaDB (vector search) and SQLite (structured queries). Gives agents durable memory across sessions without relying on conversation context.

## Setup

```bash
pip install mempalace
claude mcp add mempalace -- mempalace serve
```

Server exposes MCP tools: `store`, `recall`, `list_wings`, `search`.

## Wing convention

One wing per analysis, named `<experiment>_<channel>`:

```
cms_hh_bbtautau
atlas_h_gamgam
cms_top_ljets
```

Wings = isolated. Agent in one wing cannot accidentally read or overwrite another analysis.

## Per-phase storage

Each phase deposits specific entity types into wing:

| Phase | Stored entities |
|-------|-----------------|
| 0 Acquire | Datasets, file paths, luminosity, run ranges |
| 1 Strategy | Variables, Cuts (planned), Fit Models (proposed), Systematics (enumerated) |
| 2 Exploration | Variables (observed distributions), Failed Approaches |
| 3 Processing | Cuts (final), selection efficiencies, background estimates |
| 4 Inference | Fit Models (fitted), Systematics (evaluated), expected results |
| 5 Draft note | Document structure, figure registry, reference list |
| 6 Full data | Observed results, nuisance parameter pulls |
| 7 Final note | Final figures, tables, conclusions |

## Knowledge graph entities

- **Datasets**: name, path, luminosity, cross-section, generator, number of events.
- **Variables**: branch name, definition, unit, distribution shape notes.
- **Cuts**: expression, efficiency on signal, efficiency on each background, motivation.
- **Fit Models**: functional form, parameters, fit range, chi2/ndf.
- **Systematics**: source, type (shape/norm), size, correlation across channels.
- **Failed Approaches**: what was tried, why it failed, what replaced it.

## Search patterns

```
recall("what cuts were applied to the ditau mass")
recall("which systematics affect the b-tagging efficiency")
recall("why was the ABCD method abandoned")
```

Vector search returns top-k most relevant entries. Structured queries filter by entity type, phase, or metadata fields.

## Anti-hallucination role

Mempalace stores **reasoning chains** and **measured values** -- numbers from code running on data in this analysis.

NEVER stores textbook values as measurements. If agent recalls cross-section → must be tagged with source: either "measured in this analysis" or "theory prediction from [reference]". Untagged numbers = suspect.

Cross-analysis learning accumulates in mempalace (e.g. "ABCD method fails when two axes are correlated") but NEVER shortcuts scientific process. Lesson from prior analysis = hypothesis to test, not fact to assert.
