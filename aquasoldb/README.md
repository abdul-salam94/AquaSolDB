# aquasoldb -- the reference reader for AquaSolDB

Reads the CSVs that ship with AquaSolDB into pandas, narrows them, and derives the brine
quantities and mole fractions the published columns support. It contains no measurement
of its own.

```python
from aquasoldb import open_table, narrow, ion_strength, to_mole_fraction, with_citation, save_csv

df = open_table("solubility")                 # or water_content, mixtures,
                                              # phase_boundaries, other_quantities, sources
hot = narrow(df, gas="H2", medium="brine", status="measured",
             T_K=(298.15, 423.15), P_MPa=(1.0, 40.0),
             flags_exclude="digitized_from_figure")
hot["ion_strength"] = ion_strength(hot)       # NaN where the ion cells are blank
hot["x_gas"] = to_mole_fraction(hot, include_salt=True)
save_csv(with_citation(hot), "h2_brine.csv")  # adds each row's reference and DOI
```

Install from the repository (`pip install .` in this folder, or `pip install
aquasoldb[parquet]` to add Parquet output); it needs pandas and nothing else.
`open_table(name, root=...)` or the `AQUASOLDB_ROOT` environment variable points it at a
copy anywhere on disk; without either it reads the copy beside the package (a clone of the
repository), then a copy saved by `download()`, which fetches the archived release from
Zenodo once, on request, checks every file against the archive's hash list and keeps it in
a cache on disk. `open_detail("printed_values")` reads the values as printed, with their
page; `open_table(name, verify=True)` re-hashes the file against the release's checksum
list first. `python -m aquasoldb` prints the row counts.

`narrow` filters by gas, medium, salt, status, phase, temperature, pressure, source and
flags. `medium="water"` is salt `none`; `medium="brine"` is any dissolved salt; rows whose
medium the source did not record (`not_stated`) are in neither, and `salt="not_stated"`
selects them. `narrow` refuses a value the column does not hold, so a typo is an error
rather than an empty answer.

A blank ion cell means the composition is not known to us in numbers, so it reads as NaN
and stays NaN through every derived quantity: a blank is never a zero and is never
guessed. Pure water counts as zero ions, and so does an ion column a file leaves out
because the column dictionary declares it dropped as always zero. `to_mole_fraction` gives
x = m / (m + 55.508373) with 1000 / 18.0153 mol of water per kg, or, with the salt,
x = m / (m + 55.508373 + the sum of the ion molalities).

Code MIT (`aquasoldb/LICENSE-CODE`); data CC BY 4.0. Cite the paper that printed a value
for the value itself -- every row names it in `source_id`.
