# aquasoldb -- the reference reader for AquaSolDB

Reads the CSVs that ship with AquaSolDB into pandas, narrows them, and derives the brine
quantities the six ion columns support. It contains no measurement of its own.

```python
from aquasoldb import open_table, narrow, ion_strength, save_csv

df = open_table("solubility")                 # or watercontent, liquidwatercontent,
                                              # mixtures, phaseboundaries, sources
hot = narrow(df, gas="H2", medium="brine", T_K=(298.15, 423.15), P_MPa=(1.0, 40.0),
             flags_exclude="digitized_from_figure")
hot["ion_strength"] = ion_strength(hot)       # NaN where the six ion cells are blank
save_csv(hot, "h2_brine.csv")
```

Install from the repository (`pip install .` in this folder, or `pip install
aquasoldb[parquet]` to add Parquet output); it needs pandas and nothing else.
`open_table(family, root=...)` or the `AQUASOLDB_ROOT` environment variable points it at a
copy anywhere on disk; `open_table(family, verify=True)` re-hashes the file against
`provenance/CHECKSUMS.sha256` first. `python -m aquasoldb` prints the row counts.

A blank ion cell means the composition is not known to us in numbers, so it reads as NaN
and stays NaN through every derived quantity: a blank is never a zero and is never
guessed. `narrow` refuses a gas, salt, source or flag the column does not hold, so a typo
is an error rather than an empty answer.

Code MIT (`aquasoldb/LICENSE-CODE`); data CC BY 4.0. Cite the paper that printed a value
for the value itself -- every row names it in `source_id`.
