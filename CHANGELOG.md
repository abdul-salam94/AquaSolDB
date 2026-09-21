# AquaSolDB -- CHANGELOG

## v1.1 -- source identifiers settled

A corrections release under the versioning rule in the README: no measurement value, no row and no column changed, so what the database covers is exactly what v1.0 covered. What moved is the identification of the papers behind the rows, and the release documents.

### The data files

Byte-comparable and unchanged against v1.0, row for row and cell for cell: `csv/solubility.csv`, `csv/watercontent.csv`, `csv/liquidwatercontent.csv`, `csv/mixtures.csv`, `csv/phaseboundaries.csv`, `csv/column_dictionary.csv`.

`csv/sources.csv`: 496 rows (v1.0 held 496); 0 rows added, 0 removed, 4 cells changed.

Every changed cell, by source_id:

- `hou2015_co2` `reference`: `Hou, D.; Luo, P.; et al. (2015). J. Jilin Univ. (Earth Sci.) 45(2), 564-572.` -> `Hou, D.; Luo, P.; et al. (2015). J. Jilin Univ. (Earth Sci.) 45(2), 564-572. DOI: 10.13278/j.cnki.jjuese.201502205.`
- `hou2015_co2` `doi`: (blank) -> `10.13278/j.cnki.jjuese.201502205`
- `sultanovskripkanamiot1972_ch4` `reference`: `Sultanov, R.G., Skripka, V.G., Namiot, A.Y., 1972 (citation as printed in SDS-27/28 §1.2 ref-list).` -> `Sultanov, R.G., Skripka, V.G., Namiot, A.Y., 1972. Zh. Fiz. Khim. 1972, 46, 2160; VINITI, 4387-72; Gazov. Prom. 1972, 17, 6-7.`
- `yuanyang1993_co2` `url`: (blank) -> `http://www.cjcu.jlu.edu.cn/CN/Y1993/V14/I1/80`

### The release documents

- `README.md` and `CITATION.cff` now cite the CONCEPT DOI 10.5281/zenodo.22870466, which always resolves to the newest archived version, and list each version's own DOI beside it, including this release's own, 10.5281/zenodo.22872900, which Zenodo minted when this release was published (R-DB3-24).
- The version DOIs known when this file was written: v1.0 10.5281/zenodo.22870467; v1.1 10.5281/zenodo.22872900.
- The author line is `Abd, A., & Abushaikha, A.` (R-DB3-25). Each author carries their own affiliation and ORCID in `CITATION.cff` and `.zenodo.json`.
- `CHANGELOG.md` now keeps one section per release, newest first. The v1.0 section below is the text that release shipped, with one tense correction: it was written before anything was deposited and said so in the present tense.

## v1.0 -- first public version

This is the first version of AquaSolDB released to anyone. Nothing had been deposited before it: at the time of this release no DOI had been minted and no archive record existed, and no `point_id` in this file has ever been published elsewhere. Two earlier folders in the project's own repository are labelled v1.0 and v1.0.1; those were packaged internally and never left it. They are kept unchanged as the project's own history, and the sections below say what moved between the later of them and this release, so that a reader who has seen an internal copy can reconcile it.

Measured over the five measurement tables: the internally packaged state held 23075 rows, this release holds 22872. 21815 row ids are in both, 1057 are new, and 1260 are not carried forward. Of the ids in both, 4286 sit in a source whose row count moved, so the id means a different measurement on the two sides and the comparisons below leave them out; 17529 are compared.

### 1. Label corrections

1269 of those 17529 rows carry a different medium label or a different composition text. The bulk of this is the new composition text: where the project's internal records now hold the per-ion make-up of a brine, the composition column spells it out instead of naming a second salt and its molality.

### 2. Recomputed molalities

768 of those 17529 rows carry a different total salt molality. The rule changed: on a brine of several salts the total is now computed from the per-ion molalities of the internal record, and it is no longer the sum of two recorded salt slots. The sum was wrong wherever the first slot already held the total -- on those rows it counted the second salt twice.

415 of those 17529 rows carry a different solubility value. Those changes come from corrections made in the project's internal records between the two packagings, each recorded in that record's own change candidate; no value is edited in this file.

### 3. Restructured rows (retired and re-added, never a silent count change)

489 row ids are not carried forward from a source that still contributes rows and whose row count changed. A source that gains or loses rows can renumber the ids of the rows after them, because the number counts position within the source. Those ids are RETIRED and the source's rows are re-added under new ids; nothing is silently overwritten. 1057 row ids are new in this release.

### 4. Rows deleted from the internal records

758 row ids are not carried forward and belong to a paper the 2026-08-30 duplicate-deletion manifest names; a further 9 belong to a paper that manifest names AND that also has rows the medium screen removes, so those two causes cannot be told apart at paper level and are reported together rather than assigned to one. The deletion covered 1,380 internal rows and post-dates the earlier packaging. The match is by leading author and year, which is a proxy: the manifest keys its rows by the internal source id, not by the published one.

### 5. Rows that left the public view because a scope rule changed

4 row ids are not carried forward and belong to a paper that has rows this build screens out for its medium -- acids, bases, organic co-solvents, surfactants and the like; 2 sources lie behind those rows. Screened rows are REMOVED FROM THE PUBLIC VIEW, NOT DELETED: every one is retained in the project's internal records, counted in the build's own reconciliation, and listed row by row in the build's screened-row table.

### Not attributed

0 row ids are not carried forward and fall in none of the classes above. They are stated rather than folded into a neighbouring class.

### Columns

- `pressure_basis` is new: what the pressure on a row is measured against.
- The six per-ion molality columns `m_Na`, `m_Cl`, `m_K`, `m_Ca`, `m_Mg` and `m_SO4` are new, in every measurement file. They give the medium's composition as numbers instead of only as text. They are filled together or blank together, never in part, and where they are filled they balance charge; the blank rule is in the column dictionary and in `SCHEMA.md`.
- `SCHEMA.md` is new: every column of every file, generated from the column dictionary so the two cannot drift apart.
- `CITATION.cff` is new: the citation metadata in machine-readable form, including the instruction to cite the original paper for any value used.
- `LICENSE` is new: the CC BY 4.0 legal code, with a note saying that what is licensed is the compilation and not anyone's measurements.
- `provenance/screened_rows.csv` is new: every audited row that is NOT published, with the reason it is not.
- `SHA256SUMS.txt` is new: a digest for every file in this package.
- The build log is no longer packaged. It is a record of how this repository built the release, not part of the distribution, and it stays in the repository.
- `column_dictionary.csv` gains a `derivation` column: for every published column it now says whether the value was copied from the internal record or computed at build time, and by what rule.
- `provenance/row_crosswalk.csv` is new: one row per published row, naming the internal record it came from.
- Two flags are withdrawn, `critical_locus` and `validation_only`. They marked a row's role in one of this project's own model fits, which is not a property of the measurement, and they were emitted on 2 rows out of the 1,818 the internal records mark. The rows themselves all ship.
- `method` gains one class, `pressure_decrease_mass_balance`.
