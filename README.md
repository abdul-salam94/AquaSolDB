# AquaSolDB v1.2

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22870466.svg)](https://doi.org/10.5281/zenodo.22870466)
[![checks](https://github.com/abdul-salam94/AquaSolDB/actions/workflows/checks.yml/badge.svg)](https://github.com/abdul-salam94/AquaSolDB/actions)
![data CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-blue)
![code MIT](https://img.shields.io/badge/code-MIT-blue)
![rows 22,872](https://img.shields.io/badge/rows-22%2C872-teal)
![sources 497](https://img.shields.io/badge/sources-497-teal)
![version v1.2](https://img.shields.io/badge/version-v1.2-blue)

Published experimental measurements of how much gas dissolves in water and in
brine, read from the printed pages of the papers that reported them and put
into one set of tables with one set of units. 22,872 measurement rows from 497
sources. AquaSolDB is not AqSolDB (Sorkun, Khetan & Er, Scientific Data 6,
143, 2019, doi:10.1038/s41597-019-0151-1): that dataset lists aqueous
solubilities of organic compounds; this one holds gas solubilities in water
and brine. **Status: v1.2, released 2026-09-22** -- archived on Zenodo:
version DOI 10.5281/zenodo.22905509, concept DOI 10.5281/zenodo.22870466.

## How to cite

Cite this dataset for the compilation, and **cite the paper that printed a value
for the value itself**. Every row names its source in `source_id`, and
`csv/sources.csv` gives that source's full reference and, where one exists, its
DOI. `CITATION.cff` carries the same instruction in machine-readable form.

> Abd, A., & Abushaikha, A. (2026). AquaSolDB v1.2 [Data set]. Zenodo. https://doi.org/10.5281/zenodo.22870466

The concept DOI in that line always resolves to the newest version, so it is the
one to cite for the database as a whole. To cite exactly one version, use that
version's own DOI from the list below: a version DOI can never resolve to a
different set of rows. The files and the release notes are in the GitHub
repository https://github.com/abdul-salam94/AquaSolDB.

Version DOIs:

- v1.2 -- 10.5281/zenodo.22905509
- v1.1 -- 10.5281/zenodo.22872900
- v1.0 -- 10.5281/zenodo.22870467

## What is in it, and what is not

Nine gases -- CO2, CH4, H2, N2, H2S, ethane, propane, n-butane and i-butane --
plus a few audited rows of other gases, labelled as such. Two kinds of medium:
pure water and brine, where brine means **dissolved salts only**. Six kinds of
measurement: gas dissolved in water, gas dissolved in brine, gas-mixture
solubility, water content of a gas or vapour phase, water content of a liquid
non-aqueous phase (hydrocarbon- or CO2-rich), and phase-boundary points.

Measurements in anything else are out of scope and are in none of these files:
acids, bases, organic co-solvents such as methanol and the glycols, surfactants,
colloids, heavy water, exotic media such as uranyl sulfate. Nor are quantities
that are not an absolute measurement of dissolved gas -- solution enthalpies,
Henry-law constants, partial molal volumes, salting-out constants. Scope is
decided by the **medium the source names**, never by a reported concentration,
so an empty concentration cell must never be read as "pure water".

Whether a measurement was used by, held out of, or rejected from any model fit
is **not** recorded here: that is a property of the fit, and no column of this
database encodes it.

Values were read from rendered images of the printed pages, and the reading is
checked by sampling rather than row by row: the most recent audit re-read 60
published rows against their pages and found 56 as printed, 1 that disagreed
with the page, 1 page the rendered corpus does not hold, and 2 rows digitized
from a figure, which have no printed digit to check. Rows flagged
`digitized_from_figure` are outside that check by construction.

## The files

| file | rows | what it holds |
|---|---|---|
| `csv/solubility.csv` | 18,200 | gas dissolved in water or brine |
| `csv/watercontent.csv` | 2,010 | water in the gas or vapour phase |
| `csv/liquidwatercontent.csv` | 21 | water in a liquid non-aqueous phase (hydrocarbon- or CO2-rich) |
| `csv/mixtures.csv` | 1,661 | solubility from a gas mixture |
| `csv/phaseboundaries.csv` | 980 | hydrate, dew, bubble and three-phase points |
| `csv/sources.csv` | 497 | one row per source: full reference, year, DOI, row counts |
| `csv/column_dictionary.csv` | - | every column: unit, meaning, blank rule, how it was arrived at |
| `provenance/row_crosswalk.csv` | 22,872 | one row per published row, naming the internal record behind it |
| `provenance/screened_rows.csv` | 1,827 | every audited row NOT published, with the reason |
| `CONTRIBUTING.md` | - | how to report a wrong value, and how to contribute rows |

`SCHEMA.md` says the same as the column dictionary in document form, generated
from it. `provenance/CHECKSUMS.sha256` holds a digest for each data file and
`SHA256SUMS.txt` one for every file here. A measurement appears in exactly one
file; mixed-gas measurements are always in `csv/mixtures.csv`.

## The columns

Every measurement file starts with the same columns, so one reader works on all
five. `point_id` is a permanent row identifier; `gas`, `temperature_K` and
`pressure_MPa` are the state, with `pressure_basis` saying what the pressure was
measured against; `salt`, `salt_molality` and `salt_composition` describe the
medium; `m_Na`, `m_Cl`, `m_K`, `m_Ca`, `m_Mg` and `m_SO4` give that medium's
composition as per-ion molalities in mol per kg of water; `source_id`,
`reference` and `method` say where the number came from and how it was measured;
`flags` carries row-level warnings. After those come the measured quantity in
normalized units and the same quantity `value_as_printed` with its
`unit_as_printed`, exactly as the page gave it. **The ion rule:** the six ion
cells are filled together or blank together, never in part. Blank means the
composition is not known to us in numbers -- the source prints none we can
resolve, or the medium contains an ion outside these six, such as a carbonate or
a bicarbonate, and half a composition would state a brine that does not balance.
A blank is never a zero; pure water carries six zeros. Where the six are filled
they balance charge, m_Na + m_K + 2*m_Ca + 2*m_Mg equal to m_Cl + 2*m_SO4 within
5e-6 mol per kg. 17,961 published rows carry the six numbers and
4,911 carry six blanks.

## Flags

`flags` is empty on a clean row and otherwise holds one or more of five words,
separated by semicolons. `from_compilation` means the row reaches us through a
compilation, a data series or a secondary transcription rather than the primary
experimental paper. `digitized_from_figure` means the number was read off a
published figure, so there is no printed digit behind it. `printed_defect`
means the printed source itself carries a defect at this row -- a typo, a
mislabelled heading, an illegible cell, an impossible unit. `suspect_value`
means the value is physically or statistically implausible as printed.
`replicate` means the paper prints this measurement more than once -- an old
titration or volumetric sheet that tabulates each run instead of a mean, where two
runs round to the same digits -- and both rows are kept, so a reader who wants one
point per state can average or drop by hand rather than being handed our choice.
Flagged rows are published, never silently dropped: the flag is there so you can
decide.

## Methods

`method` says how the measurement was made, read from the source itself and
recorded per source rather than per row, so where a paper prints several
tables measured different ways the column gives the dominant one. Ten classes,
each defined in `SCHEMA.md`. `unstated` covers two cases and does not tell
them apart: the paper was read and does not state a method, or the paper was
not available to us, so nobody could read it -- 1,203 rows over 42 sources in
this release are the second case, and the per-source evidence is in the
project trackers. In this release, by rows:

analytical sampling 8,960, manometric volumetric 3,312, chromatography 2,049,
synthetic visual 2,328, electrochemical 409, gravimetric 1,271, pressure
decrease mass balance 32, calculated compilation 1,121, other 1,514, unstated
1,632.

## Known limitations

- **Some brine rows carry no ion composition.** 2,142 published rows
  labelled `mixed` have six blank ion cells, usually because the medium contains
  an ion outside the six, which the rule refuses to fill in part. A smaller
  group carries a printed zero that is a placeholder, not a measured zero (a
  "composition not separately reported" cell); those are blank too, rather than
  asserting a composition nobody printed.
- **Some rows reach us through a transcription, not the original page.** They
  carry `from_compilation`, and the source row names the compilation or series.
- **`salt_molality` is empty on some mixed brines.** It comes from the six ion
  molalities and is empty where those are blank. It is never the sum of two
  recorded salt slots, which double-counted on some sources.
- **`page_ref` is not published.** An internal audit found the page pointer
  wrong on about one row in eight, so it is held back until that pass is done.

## Licence

CC BY 4.0. The full legal code is in `LICENSE`, with a note on what the licence
covers: the compilation, not the measurements, which belong to the authors who
published them and must be cited.

## Versions

Semantic versions: 1.x for corrections and additions that do not change what the
database covers, 2.0 when the scope grows. `point_id`s are permanent; new rows
append. Each release gets its own DOI, and all of them sit under one concept DOI
that always resolves to the newest -- **cite the version DOI**, so that a number
computed from this database can be traced to the exact release it came from.
`CHANGELOG.md` has one section per release.

## What changed in v1.2

A corrections release under the versioning rule in the README: what the database covers is exactly what v1.1 covered. Measured against v1.1 across the seven shipped tables: 0 measurement values changed on the rows both releases publish under the same identifier (`temperature_K`, `pressure_MPa`, `solubility_mole_fraction`, `solubility_mol_per_kgw`, `value_as_printed`, `unit_as_printed`), 0 columns gained or lost, 78 rows added and 77 removed -- and every added and removed row is accounted for in `CHANGELOG.md`, by table. What moved is the identification of the papers behind the rows, the published definitions, and the release documents.

Every added, removed and changed cell is listed by identifier in `CHANGELOG.md`.

## Where to get it

- Repository (the files and the release notes):
  https://github.com/abdul-salam94/AquaSolDB
- Concept DOI, which always resolves to the newest archived version:
  https://doi.org/10.5281/zenodo.22870466
- v1.2's archived copy on Zenodo (the record its version DOI resolves to):
  https://zenodo.org/records/22905509
- v1.1's archived copy on Zenodo (the record its version DOI resolves to):
  https://zenodo.org/records/22872900
- v1.0's archived copy on Zenodo (the record its version DOI resolves to):
  https://zenodo.org/records/22870467

**Python package.** The repository ships a small reader, `aquasoldb`: it loads
these files into pandas with the units and blank rules above, narrows by gas,
medium, temperature and pressure, and derives ion strength, total ions and the
charge residual from the six ion columns, leaving a blank composition blank.
It needs pandas and nothing else, and it is installed from the repository:
`pip install .` in a clone, or `pip install git+https://github.com/abdul-salam94/AquaSolDB`.

```python
from aquasoldb import open_table, narrow
df = open_table("solubility")
hot = narrow(df, gas="H2", medium="brine", T_K=(298.15, 423.15))
```

`aquasoldb/README.md` is its ten-line manual. The data stays CC BY 4.0; the
reader's own code is MIT.
