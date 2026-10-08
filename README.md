<!-- DRAFT for the author's approval. Not approved, not deposited, not published. -->
# AquaSolDB v2.0

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22870466.svg)](https://doi.org/10.5281/zenodo.22870466)
[![checks](https://github.com/abdul-salam94/AquaSolDB/actions/workflows/checks.yml/badge.svg)](https://github.com/abdul-salam94/AquaSolDB/actions)
![data CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-blue)
![code MIT](https://img.shields.io/badge/code-MIT-blue)
![rows 23,263](https://img.shields.io/badge/rows-23%2C263-teal)
![sources 499](https://img.shields.io/badge/sources-499-teal)
![version v2.0](https://img.shields.io/badge/version-v2.0-blue)

Published experimental measurements of how much gas dissolves in water and in
brine, read from the printed pages of the papers that reported them and put
into one set of tables with one set of units. 23,263 measurement rows from 499
sources. AquaSolDB is not AqSolDB (Sorkun, Khetan & Er, Scientific Data 6,
143, 2019, doi:10.1038/s41597-019-0151-1): that dataset lists aqueous
solubilities of organic compounds; this one holds gas solubilities in water
and brine. **Status: v2.0 (public candidate, NOT deposited)** -- archived on
Zenodo under concept DOI 10.5281/zenodo.22870466; this version's own DOI is
minted at the release and written here after.

## How to cite

Cite this dataset for the compilation, and **cite the paper that printed a value
for the value itself**. Every row names its source in `source_id`, and
`csv/sources.csv` gives that source's full reference and, where one exists, its
DOI. Row and source ids are fixed labels, not citations; the reference
column gives the correct year and spelling. `CITATION.cff` carries the same
instruction in machine-readable form.

> Abd, A., & Abushaikha, A. (2026). AquaSolDB v2.0 [Data set]. Zenodo. https://doi.org/10.5281/zenodo.22870466

The concept DOI 10.5281/zenodo.22870466 in that line always resolves to the newest
version, so it is the one to cite for the database as a whole. To cite exactly
this version, use its own DOI (minted by Zenodo at this release; added here after). A version DOI never
resolves to a different set of rows. The files and the release notes are in
the GitHub repository https://github.com/abdul-salam94/AquaSolDB.

## What is in it, and what is not

Nine gases -- CO2, CH4, H2, N2, H2S, C2H6, C3H8, n-C4H10 and i-C4H10.
One other gas appears: `water_content` holds
38 rows of H2O in compressed N2O vapour (Coan & King, 1971).
Two kinds of medium: pure
water and brine, where brine means **dissolved salts only**. Four kinds of
measurement, one file each: gas dissolved in water or brine, the water content
of a gas, vapour or liquid non-aqueous phase, gas-mixture solubility, and
phase-boundary points. A fifth file holds the rows a source prints as some
other quantity, or prints with no number in the units of the other four.

Measurements in anything else are out of scope: acids, bases, organic
co-solvents such as methanol and the glycols, surfactants, colloids, heavy
water, exotic media such as uranyl sulfate. Quantities that are not an absolute
measurement of dissolved gas -- solution enthalpies, Henry-law constants,
partial molal volumes, salting-out constants -- are not collected; where a
source prints one beside its measurements, that row is in
`csv/other_quantities.csv` exactly as printed. Scope is decided by the
**medium the source names**, never by a reported concentration; where the
source names no medium, `salt` says `not_stated` (927 rows).

Values were read from rendered images of the printed pages, and the reading is
checked by sampling rather than row by row. Rows flagged
`digitized_from_figure` were read off a figure, so no printed digit stands
behind them.

## The files

| file | rows | what it holds |
|---|---|---|
| `csv/solubility.csv` | 17,423 | gas dissolved in water or brine, in mol per kg of water |
| `csv/water_content.csv` | 1,954 | water in a gas or vapour phase, or in a liquid non-aqueous phase (hydrocarbon- or CO2-rich), as a mole fraction; column `phase` says which |
| `csv/mixtures.csv` | 1,122 | the solubility of each gas of a gas mixture, in mol per kg of water |
| `csv/phase_boundaries.csv` | 842 | phase-boundary points: hydrate, dew, bubble, three-phase and critical points, transitions of a sample of fixed composition, and points on a coexistence line |
| `csv/other_quantities.csv` | 1,922 | rows printed as another quantity, or with no usable number, kept as printed |
| `csv/sources.csv` | 499 | one row per source: full reference, kind of publication, DOI, method |
| `csv/column_dictionary.csv` | 115 | every column of every file: unit, meaning, what an empty cell means |
| `detail/printed_values.csv` | 23,263 | each measurement row's value, unit wording and page exactly as printed |
| `detail/excluded_sources.csv` | 84 | rows left out of the database (1,810), counted by source and reason |
| `detail/id_changes.csv` | 567 | each row id of the previous release that no longer ships under the same id, with what happened and why |
| `SCHEMA.md` | - | the column dictionary as a document |
| `CHANGELOG.md` | - | what changed in each release |
| `CITATION.cff` | - | how to cite, in machine-readable form |
| `LICENSE` | - | CC BY 4.0, with a note on what the licence covers |
| `CONTRIBUTING.md` | - | how to report a wrong value, and how to contribute rows |
| `AquaSolDB.xlsx` | - | the tables above in one spreadsheet |

A measurement appears in exactly one file, and `point_id` is unique across the
five measurement files. `AquaSolDB.xlsx` holds the same tables as the CSV files,
one sheet each, and the CSV files are the reference copy. `SHA256SUMS.txt` holds
a digest for every file of the release.

## Status and reason

Every row of the five measurement files says what kind of number it holds, in
`status`, and why, in `status_reason`. `status` is one of three words.
`measured` (21,938 rows) is an experimental result as the source reports
it. `calculated` (1,132 rows) is a number the source or a compiler
worked out from measured data, such as a smoothed table or a value computed
from the author's own constant. `no_value` (193 rows) is a point the
source shows without a number we could read: a point on a plot only, an
illegible cell, or a cell the source left empty. `status_reason` is one plain
sentence; on most rows it reads "Experimental result as reported in the
source." The reason never repeats a flag or another column of the same row.

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

## Units

Temperature is in kelvin (`temperature_K`) and pressure in MPa
(`pressure_MPa`). In `water_content`, `mixtures` and `phase_boundaries` the
pressure is the total pressure; in `solubility` and `other_quantities` the
column `pressure_basis` says what it is. Dissolved gas is given in one unit
only, mol per kg of water (`solubility_mol_per_kgw`); where a source printed
a mole fraction, it was converted with 55.508 mol of water per kg, and the
dictionary states the formula. Water content is the mole fraction of water in
the phase the row names (`water_mole_fraction`). `salt_molality` and the ion
columns are in mol per kg of water. The value, its unit wording and its page
exactly as printed are in `detail/printed_values.csv`, one row per measurement
row.

## The medium and the ion columns

`salt` names the medium: `none` for pure water, one salt (`NaCl`, `KCl`,
`CaCl2`, `MgCl2`), `seawater`, `mixed` for a brine of several salts, or
`not_stated`. For `seawater` the salinity is given as the source prints it,
in `salt_composition`, and `salt_molality` is empty. `salt_molality` and
`salt_composition` describe it, and the ion columns (`m_Na`, `m_Cl`, `m_K`,
`m_Ca`, `m_Mg`, `m_SO4`) give its composition as per-ion molalities. Each file
keeps only the ion columns it uses; the column dictionary names the ones a
file leaves out because they are zero on all of its rows. **The ion rule:** a
row's ion cells are filled together or blank together, never in part. Blank
means the composition is not known to us in numbers -- the source prints none
we can resolve, or the medium contains an ion outside these six, such as a
carbonate or a bicarbonate. A blank is never a zero; pure water carries zeros.
Where the ion cells are filled they balance charge, m_Na + m_K + 2*m_Ca +
2*m_Mg equal to m_Cl + 2*m_SO4 within 5e-6 mol per kg. Over the five
measurement files, the ion composition is known in numbers on 18,196
rows and not known on 5,067.

## Methods

`method` says how the measurement was made, read from the source itself and
recorded per source rather than per row, so where a paper prints several
tables measured different ways the column gives the dominant one. Ten classes,
each defined in `SCHEMA.md`. `unstated` covers two cases and does not tell
them apart: the paper was read and does not state a method, or the paper was
not available to us, so nobody could read it -- 1,225 rows over 44 sources in
this release are the second case, and the per-source evidence is in the
project trackers. In this release, by rows:

analytical sampling 9,384, manometric volumetric 3,411, chromatography 2,056,
synthetic visual 2,315, electrochemical 409, gravimetric 1,359, pressure
decrease mass balance 32, calculated compilation 1,127, other 1,516, unstated
1,654.

## Known limitations

- **Some brine rows carry no ion composition.** 2,133 rows labelled
  `mixed` have blank ion cells, usually because the medium contains an ion
  outside the six, which the rule refuses to fill in part. A smaller group
  carries a printed zero that is a placeholder, not a measured zero (a
  "composition not separately reported" cell); those are blank too, rather than
  asserting a composition nobody printed.
- **Some rows reach us through a transcription, not the original page.** They
  carry `from_compilation`, and the source row names the compilation or series.
- **`salt_molality` is empty on some mixed brines.** It comes from the ion
  molalities and is empty where those are blank. It is never the sum of two
  recorded salt slots, which double-counted on some sources.
- **`page_ref` means different things in different sources.** It is the page
  pointer of our record, copied without change, and what the number counts
  depends on the source: for most it is the page index inside the PDF, for the
  IUPAC SDS 62 volume it is the page number printed on the page, and for NIST
  ThermoML sources it is a dataset pointer, not a page. `page_ref_convention`
  says which of those it is on every row, `page_offset` gives the measured gap
  between the two page numberings where one has been measured, and
  `unverified` marks the sources nobody has yet read to settle the question.

## Licence

CC BY 4.0. The full legal code is in `LICENSE`, with a note on what the licence
covers: the compilation, not the measurements, which belong to the authors who
published them and must be cited.

## Versions

Version numbers: a release that corrects or adds rows and keeps the layout of
the files and what the database covers changes the second number; a new first
number, such as 2.0, means the layout or the scope changed, so code that reads
the files must change too. From this release on a `point_id` is permanent: it
is never renamed and never reused, and new rows append. Each release gets its
own DOI, and all of them sit under one concept DOI that always resolves to the
newest -- **cite the version DOI**, so that a number computed from this
database can be traced to the exact release it came from.
`CHANGELOG.md` has one section per release.

## What changed in v2.0

Version 2.0 is the corrected database in a simpler layout. Every measurement row now says whether its number was measured or calculated, or that the source prints none (`status`), and why (`status_reason`). Dissolved gas is given in one unit, mol per kg of water. Rows that are not a solubility, a water content, a gas-mixture solubility or a phase-boundary point, or that have no number in those units, are in the new file `csv/other_quantities.csv` (1,922 rows). Compared with the previous release, 431 rows gained a value converted from the printed page; 252 row ids were renamed so that the gas part names the row's gas; 20 ids were retired; and 295 rows were removed when the records behind them were corrected, 283 of them as duplicates. Each of these ids is listed with its reason in `detail/id_changes.csv`.

`CHANGELOG.md` gives the details, file by file and column by column, and keeps the notes of every earlier release.

## Where to get it

- Repository (the files and the release notes):
  https://github.com/abdul-salam94/AquaSolDB
- Concept DOI, which always resolves to the newest archived version:
  https://doi.org/10.5281/zenodo.22870466
- This version's own DOI: minted by Zenodo at this release; added here after.
- Web viewer, to browse, plot and download the data in a browser, with no
  installation: (its address is added here at publication).

**Python package.** The repository ships a small reader, `aquasoldb`: it loads
these files into pandas with the units and blank rules above, narrows by gas,
medium, temperature and pressure, and derives ion strength, total ions and the
charge residual from the ion columns, leaving a blank composition blank. It
needs pandas and nothing else, and it is installed from the repository:
`pip install .` in a clone, or `pip install git+https://github.com/abdul-salam94/AquaSolDB`.

```python
from aquasoldb import open_table, narrow
df = open_table("solubility")
hot = narrow(df, gas="H2", medium="brine", T_K=(298.15, 423.15))
```

`aquasoldb/README.md` is its short manual. The data stays CC BY 4.0; the
reader's own code is MIT.
