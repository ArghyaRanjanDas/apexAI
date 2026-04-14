# Open Data Portals and Data Acquisition

## Portal Overview

| Experiment | Portal URL | Format | Units | Notes |
|---|---|---|---|---|
| ATLAS | opendata.atlas.cern | ROOT mini TTrees | MeV | Easiest to start with; well-documented tutorials |
| CMS | opendata.cern.ch | NanoAOD (Events TTree) | GeV | Largest dataset collection; multiple data tiers |
| DELPHI | opendata.cern.ch | Fortran DST (.sdst/.xsdst) | GeV | Requires container environment |
| ALEPH | opendata.cern.ch | Migrating to EDM4hep | GeV | Format transition in progress |
| L3 | opendata.cern.ch | Limited ROOT ntuples | GeV | Small selection of datasets |
| OPAL | opendata.cern.ch | Legacy formats, ported | GeV | Partial ROOT availability |

## Search Strategy

When looking for data for an analysis, follow these steps:

1. **Web search** for the experiment's open data portal and documentation
2. **Fetch the portal page** and read available dataset descriptions
3. **Find getting-started guides** -- these show the expected workflow and data format
4. **Identify specific datasets** relevant to the physics process of interest
5. **Check for simplified ntuples** -- many experiments provide reduced formats that are much easier to work with than raw data

## Key Documentation URLs

- ATLAS Open Data: https://opendata.atlas.cern/docs
- ATLAS Getting Started: https://opendata.atlas.cern/docs/category/getting-started
- CMS Open Data: https://opendata.cern.ch/search?experiment=CMS
- CMS Getting Started: https://opendata.cern.ch/docs/cms-getting-started-2015
- CMS Data Release: https://opendata.cern.ch/docs/cms-releases-information
- DELPHI Getting Started: https://opendata.cern.ch/docs/delphi-getting-started
- ALEPH Migration: https://opendata.cern.ch/docs/aleph-getting-started

## Download Methods

### cernopendata-client (by record ID)

```bash
pip install cernopendata-client
cernopendata-client download-files --recid 15005
```

### wget (direct URL)

```bash
wget http://opendata.cern.ch/record/15005/files/GamGam.root
```

### xrootd (large CMS datasets)

```bash
# Requires xrootd client
xrdcp root://eospublic.cern.ch//eos/opendata/cms/Run2015D/DoubleMuon/NANOAOD/file.root .
```

## Verification

After downloading, always verify the file is readable and contains the expected structure:

```python
import uproot

f = uproot.open("downloaded_file.root")
print(f.keys())            # list all objects in the file
print(f.classnames())       # show object types (TTree, TH1F, etc.)

# For a TTree:
tree = f["Events"]          # or whatever the tree name is
print(tree.keys())          # list all branches
print(tree.num_entries)     # number of events
print(tree.typenames())     # branch data types

# Quick sanity check: read one branch
pt = tree["Muon_pt"].array()
print(f"Entries: {len(pt)}, min: {pt.min()}, max: {pt.max()}")
```

## Format Quick-Reference

### ATLAS Mini TTree

- Tree name: `mini`
- Units: MeV (divide by 1000 for GeV)
- Common branches: `lep_n`, `lep_pt`, `lep_eta`, `lep_phi`, `lep_E`, `lep_type`, `lep_charge`
- Trigger branches: `trigM`, `trigE`, `trigP`
- Weight branches: `mcWeight`, `scaleFactor_*`

### CMS NanoAOD

- Tree name: `Events`
- Units: GeV
- Muon branches: `nMuon`, `Muon_pt`, `Muon_eta`, `Muon_phi`, `Muon_mass`, `Muon_charge`
- Electron branches: `nElectron`, `Electron_pt`, `Electron_eta`, `Electron_phi`
- Trigger branches: `HLT_*` (boolean flags)
- Event info: `run`, `luminosityBlock`, `event`

### DELPHI DST

- File extensions: `.sdst`, `.xsdst`
- Format: Fortran-based, not directly readable with ROOT or uproot
- Container required: use the DELPHI software environment
- Simplified ntuples may be available for some analyses

## Data Manifest Template

Before starting analysis, fill out this manifest for each dataset:

```
Source:           [experiment name and portal URL]
Record ID:        [cernopendata record number]
Experiment:       [ATLAS / CMS / DELPHI / ...]
Format:           [mini TTree / NanoAOD / DST / ...]
Documentation:    [URL of getting-started guide you read]
Files downloaded: [list of filenames]
Uproot readable:  [yes / no / needs container]
Units:            [MeV / GeV]
Tree name:        [mini / Events / ...]
Key branches:     [list the ones you will use]
Notes:            [anything unusual about the data]
```

## Always Start with ONE File

When beginning a new analysis:

- Download a single file first
- Verify it opens and contains the expected branches
- Run your analysis code on that one file to confirm everything works
- Only then scale up to the full dataset

This avoids wasting time downloading gigabytes of data only to discover a format mismatch or missing branches.
