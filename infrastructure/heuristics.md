# Heuristics -- agent-maintained tool idiom library

Living document of non-obvious patterns for Python HEP stack. Agents add entries when they discover pattern that cost time to figure out. Goal = prevent re-discovering same API quirks every session.

## mplhep

**Set experiment style once at top**:
```python
import mplhep as hep
hep.style.use("CMS")  # or "ATLAS", "LHCb", "ALICE"
```

**Experiment label on every plot**:
```python
hep.cms.label(data=True, lumi=59.7, year=2018, ax=ax)
# data=False for MC-only, loc=0 for upper-left
```

**Histogram plotting with ratio panel**:
```python
fig, (ax, rax) = plt.subplots(2, 1, gridspec_kw={"height_ratios": [3, 1]},
                               sharex=True)
hep.histplot(h_data, ax=ax, histtype="errorbar", color="k", label="Data")
hep.histplot([h_bkg1, h_bkg2], ax=ax, stack=True, label=["QCD", "TTbar"])
```

**2D histogram**:
```python
hep.hist2dplot(h2d, ax=ax, cbar=True, cbarlabel="Events")
```

## uproot

**Lazy array loading** -- load branches on demand, not full tree:
```python
tree = uproot.open("file.root:Events")
arrays = tree.arrays(["pt", "eta", "phi"], library="ak")
```

**Cut strings** -- apply selection at read time:
```python
arrays = tree.arrays(["pt", "eta"], cut="pt > 20 && abs(eta) < 2.4")
```

**Concatenating multiple files**:
```python
arrays = uproot.concatenate(["f1.root:Events", "f2.root:Events"],
                            ["pt", "eta"], library="ak")
```

## hist

**Create and fill histogram**:
```python
import hist
h = hist.Hist(hist.axis.Regular(50, 0, 200, name="mass", label="m [GeV]"))
h.fill(mass=mass_array)
```

**Project 2D histogram to 1D**:
```python
h_proj = h2d[:, sum]   # project out the second axis
h_slice = h2d[:, 2j:5j]  # slice then project: h_slice[:, sum]
```

**Rebin**:
```python
h_rebinned = h[::2j]  # merge every 2 bins
# or use hist.rebin(factor)
h_rebinned = h[hist.rebin(4)]
```

## iminuit

**Basic Minuit setup**:
```python
from iminuit import Minuit
m = Minuit(cost_function, param1=1.0, param2=0.5)
m.limits["param1"] = (0, None)  # lower bound only
m.fixed["param2"] = True        # fix during first fit
m.migrad()
```

**HESSE vs MINOS**: HESSE gives symmetric parabolic errors (fast). MINOS gives asymmetric profile likelihood intervals (slow, more accurate near boundaries). Always run HESSE first. Run MINOS for parameters of interest or when HESSE errors = suspect.
```python
m.hesse()  # symmetric errors
m.minos("param1")  # asymmetric errors for param1
```

**Parameter limits near boundaries**: if parameter sits at its limit after fit → covariance matrix unreliable. Either widen limit or reparametrize.

## awkward

**Nested array masking**:
```python
import awkward as ak
# select jets with pt > 30 within each event
good_jets = jets[jets.pt > 30]
# require at least 2 good jets per event
events = events[ak.num(good_jets) >= 2]
```

**Combinations** -- all pairs of objects in event:
```python
pairs = ak.combinations(jets, 2, fields=["j1", "j2"])
dijet_mass = (pairs.j1 + pairs.j2).mass
```

**Flattening for histogramming**:
```python
flat_pt = ak.flatten(jets.pt)  # remove event structure
h.fill(mass=ak.to_numpy(flat_pt))
```

**Padding to fixed-length arrays**:
```python
padded = ak.pad_none(jets.pt, 4, clip=True)  # exactly 4 entries
filled = ak.fill_none(padded, 0.0)  # replace None with 0
```

---

*Maintenance*: agents add entries below when they discover non-obvious pattern. Include tool name as section header and minimal working example.
