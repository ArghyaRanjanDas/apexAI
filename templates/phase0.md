# Phase 0: Data Acquisition -- {{name}}

Type: {{analysis_type}}

---

## Objective

Obtain collision data, verify it opens and contains the expected structure,
and record full provenance. Install dependencies. Orient: identify the
experiment, units, and physics variables.

---

## Tasks

### 0a. Search and Download

1. **Search open-data portals** for the relevant experiment and process.
   See `techniques/data_sources.md` for portal URLs and download commands.

   | Portal | URL | Experiments |
   |--------|-----|-------------|
   | CERN Open Data | opendata.cern.ch | CMS, ATLAS, ALICE, LHCb, LEP |
   | HEPData | hepdata.net | Published measurements (any) |
   | DPHEP | dphep.org | Preserved datasets |

2. **Read documentation BEFORE downloading.** Understand the file format,
   tree names, branch naming conventions, and any known issues.

3. **Download ONE file first.** Validate before bulk fetch:
   ```python
   import uproot
   f = uproot.open("downloaded_file.root")
   tree = f[tree_name]
   print(tree.keys(), tree.num_entries)
   df = tree.arrays(library="pd", entry_stop=100)
   print(df.describe())
   ```

4. **Verify the file** opens cleanly, contains the expected tree, and has
   a reasonable number of entries. Check for NaN/inf in numeric branches.

5. **Download remaining files** (if multiple). Verify each opens with
   the same tree structure.

### 0b. Record Provenance

6. **Write `data_manifest.md`** in `outputs/` with:
   - Portal name and URL
   - DOI or record identifier
   - Retrieval date
   - SHA-256 checksum of each file
   - Event count per file
   - File size
   - Tree name and branch count
   - Any known caveats from the documentation

### 0c. Install Dependencies

7. **Run `pixi install`** in the analysis root. Verify core packages
   import without error:
   ```python
   import uproot, awkward, hist, numpy, scipy
   import matplotlib, mplhep, vector, particle
   ```

### 0d. Orient

8. **List all branches** in the tree. Print types and sample values.

9. **Determine experiment format:**

   | Pattern | Experiment | Format |
   |---------|------------|--------|
   | `nMuon`, `Muon_pt`, `Jet_btagDeepFlavB` | CMS | NanoAOD |
   | `el_pt`, `jet_jvt`, `mcChannelNumber` | ATLAS | PHYSLITE |
   | `nTracks`, `thrust`, `R2` | LEP | Custom |
   | `foxWolframR2`, `nCDCHits` | Belle/II | basf2 |

10. **Detect units.** Sample 1000 events; if median leading-object pT
    exceeds 1000, the file is in MeV. Record and convert consistently.

11. **Map branches to physics variables.** Create a mapping table:
    branch name, physics quantity, units, typical range.

12. **Log orientation** in the experiment log: experiment, format, units,
    collision type, energy, luminosity, tree name, branch count, events.

---

## Deliverables

- `data/` directory with downloaded files
- `outputs/data_manifest.md` with full provenance
- Branch mapping table
- Experiment log entry with orientation results

## Review Tier

Self-check. Escalate to Investigator if files fail to open.

## References

- `techniques/data_sources.md` -- portal URLs and download commands
