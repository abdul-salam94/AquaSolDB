# AquaSolDB v1.2 -- schema

Every column of every published file, with its unit, what it means, when it is blank, and whether the value was copied from the record behind it or computed when the file was built.

This file is GENERATED from `csv/column_dictionary.csv` by the build. The two cannot disagree: a test regenerates this text and fails if it differs from the file shipped here.

Conventions: UTF-8, comma separated, LF line endings, one header row. A missing value is an EMPTY CELL -- never `-999`, never `NA`. Units are kelvin, MPa, mole fraction, and mol per kg of water. Numbers keep the precision of the audited extraction and are not re-rounded.

## The columns every measurement file has

These 18 columns open each of `csv/solubility.csv`, `csv/watercontent.csv`, `csv/liquidwatercontent.csv`, `csv/mixtures.csv`, `csv/phaseboundaries.csv`, in this order.

| column | unit | meaning, and when it is blank | copied or computed |
|---|---|---|---|
| `point_id` | - | Stable permanent row ID: <gas>_<sourcekey>_<gasbank>_<nnn>. The gas-bank tag is always present, which makes the ID immune to database growth; nnn is the row number within (gas, source_id), zero-padded, assigned in source order at first publication; never reused, never renumbered; a gap in the numbering marks rows that moved to another source. Rows with unresolved gas use UNK as the gas part. | Generated at build time from the gas, the source key and the row position within its source; it is not the internal record own id, which is named in provenance/row_crosswalk.csv. |
| `gas` | - | Dissolved gas, chemical formula label: CO2, H2, CH4, N2, H2S, C2H6, C3H8, nC4H10, iC4H10 (a few audited off-program rows carry N2O, Ar, O2; empty = gas unresolved in the source). | Copied from the internal audited record without transformation. |
| `temperature_K` | K | Temperature; empty = not printed / not resolvable. | Copied from the internal audited record without transformation. |
| `pressure_MPa` | MPa | Pressure; the basis is given in pressure_basis; empty = not printed / not resolvable. | Copied from the internal audited record without transformation. |
| `pressure_basis` | - | What the pressure on this row is measured against: total system pressure, a partial pressure of the gas, or a basis the source does not settle. Values: total, partial_* (the variant names the route by which the partial pressure was established), unclear, unresolved; empty = the internal record carries no basis. | Copied from the internal audited record without transformation. |
| `salt` | - | Medium label: none, NaCl, KCl, CaCl2, MgCl2, seawater, or mixed. Every medium in this database is either pure water or a dissolved-salt solution: measurements in acids, bases, organic co-solvents, surfactants, colloids and other non-salt media are outside the database's scope and are not present in any file. 'mixed' covers every other audited SALT medium (multi-salt brines, other single electrolytes); exact composition in salt_composition. Empty = medium not recorded in the published source. | Mapped from the internal medium label: 'water'/'H2O'/blank give none; a label in the six-word vocabulary passes through; any other in-scope salt medium, and any medium with a second salt recorded, gives mixed. |
| `salt_molality` | mol/kg water | Total dissolved-salt molality; 0 for salt=none; NaCl-equivalent for seawater; empty = the total is not recoverable from the source as printed. | On a single-salt medium, the molality printed by the source. On a mixed medium it is computed from the per-ion molalities of the internal record as m_Na + m_K + m_Ca + m_Mg - m_SO4, which is exact for the salts those columns cover, and it is EMPTY where those columns are blank or where a sulfate sits beside calcium or magnesium (ion totals alone cannot then say which salt it was). It is never the sum of two recorded salt slots: on some sources the first slot already holds the total. |
| `salt_composition` | - | Text spelling out the medium when salt is mixed or seawater; empty otherwise. | Built text. For a mixed medium: the internal medium label, followed by the per-ion molalities of the internal record where they are known. For seawater: the NaCl-equivalent note, plus the salinity exactly as the source printed it where the source printed one. |
| `m_Na` | mol/kg water | Sodium ion molality of the aqueous medium, fully dissociated. Blank means the composition of this medium is not known to us in numbers: either the source prints no composition we can resolve, or the medium contains an ion outside these six (a carbonate, a bicarbonate, a hydroxide) and a partial fill would state a brine that does not balance. All six cells of a row are filled together or blank together; a blank is never a zero, and a zero is never a stand-in for 'not recorded'. Rows in pure water carry six zeros. Where the six are filled they balance charge: m_Na + m_K + 2*m_Ca + 2*m_Mg equals m_Cl + 2*m_SO4 to within 5e-6 mol/kg water, the storage precision of the internal record. | Copied from the internal audited record without transformation. |
| `m_Cl` | mol/kg water | Chloride ion molality of the aqueous medium, fully dissociated. Blank means the composition of this medium is not known to us in numbers: either the source prints no composition we can resolve, or the medium contains an ion outside these six (a carbonate, a bicarbonate, a hydroxide) and a partial fill would state a brine that does not balance. All six cells of a row are filled together or blank together; a blank is never a zero, and a zero is never a stand-in for 'not recorded'. Rows in pure water carry six zeros. Where the six are filled they balance charge: m_Na + m_K + 2*m_Ca + 2*m_Mg equals m_Cl + 2*m_SO4 to within 5e-6 mol/kg water, the storage precision of the internal record. | Copied from the internal audited record without transformation. |
| `m_K` | mol/kg water | Potassium ion molality of the aqueous medium, fully dissociated. Blank means the composition of this medium is not known to us in numbers: either the source prints no composition we can resolve, or the medium contains an ion outside these six (a carbonate, a bicarbonate, a hydroxide) and a partial fill would state a brine that does not balance. All six cells of a row are filled together or blank together; a blank is never a zero, and a zero is never a stand-in for 'not recorded'. Rows in pure water carry six zeros. Where the six are filled they balance charge: m_Na + m_K + 2*m_Ca + 2*m_Mg equals m_Cl + 2*m_SO4 to within 5e-6 mol/kg water, the storage precision of the internal record. | Copied from the internal audited record without transformation. |
| `m_Ca` | mol/kg water | Calcium ion molality of the aqueous medium, fully dissociated. Blank means the composition of this medium is not known to us in numbers: either the source prints no composition we can resolve, or the medium contains an ion outside these six (a carbonate, a bicarbonate, a hydroxide) and a partial fill would state a brine that does not balance. All six cells of a row are filled together or blank together; a blank is never a zero, and a zero is never a stand-in for 'not recorded'. Rows in pure water carry six zeros. Where the six are filled they balance charge: m_Na + m_K + 2*m_Ca + 2*m_Mg equals m_Cl + 2*m_SO4 to within 5e-6 mol/kg water, the storage precision of the internal record. | Copied from the internal audited record without transformation. |
| `m_Mg` | mol/kg water | Magnesium ion molality of the aqueous medium, fully dissociated. Blank means the composition of this medium is not known to us in numbers: either the source prints no composition we can resolve, or the medium contains an ion outside these six (a carbonate, a bicarbonate, a hydroxide) and a partial fill would state a brine that does not balance. All six cells of a row are filled together or blank together; a blank is never a zero, and a zero is never a stand-in for 'not recorded'. Rows in pure water carry six zeros. Where the six are filled they balance charge: m_Na + m_K + 2*m_Ca + 2*m_Mg equals m_Cl + 2*m_SO4 to within 5e-6 mol/kg water, the storage precision of the internal record. | Copied from the internal audited record without transformation. |
| `m_SO4` | mol/kg water | Sulfate ion molality of the aqueous medium, fully dissociated. Blank means the composition of this medium is not known to us in numbers: either the source prints no composition we can resolve, or the medium contains an ion outside these six (a carbonate, a bicarbonate, a hydroxide) and a partial fill would state a brine that does not balance. All six cells of a row are filled together or blank together; a blank is never a zero, and a zero is never a stand-in for 'not recorded'. Rows in pure water carry six zeros. Where the six are filled they balance charge: m_Na + m_K + 2*m_Ca + 2*m_Mg equals m_Cl + 2*m_SO4 to within 5e-6 mol/kg water, the storage precision of the internal record. | Copied from the internal audited record without transformation. |
| `source_id` | - | Paper-level source key (leading author + year where parseable) plus a gas-domain suffix, always: e.g. culbersonmcketta1950_ch4. Cross-gas identity of same-name-same-year papers is not assumed. One row per source_id in aquasoldb_sources.csv. | Derived from the internal source id (or, where that carries no year, the internal campaign label) plus the gas-bank tag. |
| `reference` | - | Short human-readable reference (e.g. 'Drummond 1981'); full citation in aquasoldb_sources.csv. | Read from this project per-gas source trackers, with repository bookkeeping removed; no citation is typed by hand where a DOI resolves. |
| `method` | - | Measurement-method class, controlled vocabulary of ten values (definitions in README): analytical_sampling, manometric_volumetric, chromatography, synthetic_visual, electrochemical, gravimetric, pressure_decrease_mass_balance, calculated_compilation, other, unstated. One value per source, read from the paper itself with source-page verification; where a source prints several tables measured differently, the dominant class is given. 'unstated' covers two cases the column does not tell apart: the source was read and does not say, or the paper was not available to us, so nobody could read it; the README gives how many rows are the second case. 'pending' means the method has not yet been classified. | Resolved per SOURCE, not per row: the class recorded for that source in this project method campaign, then carried onto every row of the source. |
| `flags` | - | Semicolon-separated row-status flags: from_compilation, digitized_from_figure, printed_defect, suspect_value, replicate. Empty = clean. 'replicate' means the paper prints this measurement more than once; both rows are kept. Definitions in README. | Mapped from the internal conversion flags through a fixed, closed table (printed in the build log): several internal tokens can raise one public flag, and every internal token outside the table raises none. Flags that record a row role in a model fit are not published. 'replicate' is the one flag no internal token raises: it is derived at build time on every member of a group of rows that are identical, cell for cell, on every column of one internal file except that file's own row id. |

## `csv/solubility.csv`  (18200 rows)

The shared columns above, then:

| column | unit | meaning, and when it is blank | copied or computed |
|---|---|---|---|
| `solubility_mole_fraction` | mol/mol | Dissolved-gas mole fraction in the aqueous phase (basis as resolved during normalization); empty = the internal record carries no mole fraction on this basis. | Copied from the internal audited record without transformation. |
| `solubility_mol_per_kgw` | mol/kg water | Dissolved-gas molality; empty = the internal record carries no molality for this row. | Copied from the internal audited record without transformation. |
| `value_as_printed` | - | The solubility, water-content or boundary quantity exactly as the source printed it. This column is deliberately not numeric. Five closed forms, and the build refuses anything else: a number; a number with a printed uncertainty such as 0.0014(1); a decimal comma such as 0,0149; ILLEGIBLE (the printed cell could not be read and is never guessed); NOT PRINTED (the source gives the quantity in some other form). Anything else is the prose class -- wording the source printed instead of a digit, carried through as printed and counted in the build log. Empty = the source printed no value in any form for this row. It never holds an internal marker of this project own. | Copied from the internal audited record without transformation. |
| `unit_as_printed` | - | The printed unit/basis wording for value_as_printed; empty = the source printed no unit wording with the value. | Copied from the internal audited record without transformation. |

## `csv/watercontent.csv`  (2010 rows)

The shared columns above, then:

| column | unit | meaning, and when it is blank | copied or computed |
|---|---|---|---|
| `water_mole_fraction_vapor` | mol/mol | Water mole fraction in the gas/vapour phase; empty where the source provides only a non-mole-fraction printed form. | Copied from the internal audited record without transformation. |
| `value_as_printed` | - | The solubility, water-content or boundary quantity exactly as the source printed it. This column is deliberately not numeric. Five closed forms, and the build refuses anything else: a number; a number with a printed uncertainty such as 0.0014(1); a decimal comma such as 0,0149; ILLEGIBLE (the printed cell could not be read and is never guessed); NOT PRINTED (the source gives the quantity in some other form). Anything else is the prose class -- wording the source printed instead of a digit, carried through as printed and counted in the build log. Empty = the source printed no value in any form for this row. It never holds an internal marker of this project own. | Copied from the internal audited record without transformation. |
| `unit_as_printed` | - | The printed unit/basis wording for value_as_printed; empty = the source printed no unit wording with the value. | Copied from the internal audited record without transformation. |

## `csv/liquidwatercontent.csv`  (21 rows)

The shared columns above, then:

| column | unit | meaning, and when it is blank | copied or computed |
|---|---|---|---|
| `water_mole_fraction_liquid_hydrocarbon` | mol/mol | Water mole fraction in a liquid non-aqueous phase (hydrocarbon- or CO2-rich); this is neither gas dissolved in aqueous water nor water in a gas/vapour phase. | Copied from the internal audited record without transformation. |
| `value_as_printed` | - | The solubility, water-content or boundary quantity exactly as the source printed it. This column is deliberately not numeric. Five closed forms, and the build refuses anything else: a number; a number with a printed uncertainty such as 0.0014(1); a decimal comma such as 0,0149; ILLEGIBLE (the printed cell could not be read and is never guessed); NOT PRINTED (the source gives the quantity in some other form). Anything else is the prose class -- wording the source printed instead of a digit, carried through as printed and counted in the build log. Empty = the source printed no value in any form for this row. It never holds an internal marker of this project own. | Copied from the internal audited record without transformation. |
| `unit_as_printed` | - | The printed unit/basis wording for value_as_printed; empty = the source printed no unit wording with the value. | Copied from the internal audited record without transformation. |

## `csv/mixtures.csv`  (1661 rows)

The shared columns above, then:

| column | unit | meaning, and when it is blank | copied or computed |
|---|---|---|---|
| `gas2` | - | Second gas of the mixture pair, where identifiable from the audited record; empty otherwise. | INFERRED, not transcribed: a bounded search for a gas name in the internal source id and the opening of the internal notes, which fills the cell only when exactly one non-primary gas name is found and leaves it empty otherwise. The hydrogen mixture rows are the exception: their partner gas is taken from the pairing the source states. |
| `gas2_mole_fraction_feed` | mol/mol | Feed (charged) mole fraction of gas2, filled only where the source prints the feed ratio; empty otherwise. | Read from the printed feed ratio (a panel caption, table heading or row note) through a fixed set of patterns; never estimated. |
| `solubility_mole_fraction` | mol/mol | Dissolved-gas mole fraction in the aqueous phase (basis as resolved during normalization); empty = the internal record carries no mole fraction on this basis. | Copied from the internal audited record without transformation. |
| `solubility_mol_per_kgw` | mol/kg water | Dissolved-gas molality; empty = the internal record carries no molality for this row. | Copied from the internal audited record without transformation. |
| `value_as_printed` | - | The solubility, water-content or boundary quantity exactly as the source printed it. This column is deliberately not numeric. Five closed forms, and the build refuses anything else: a number; a number with a printed uncertainty such as 0.0014(1); a decimal comma such as 0,0149; ILLEGIBLE (the printed cell could not be read and is never guessed); NOT PRINTED (the source gives the quantity in some other form). Anything else is the prose class -- wording the source printed instead of a digit, carried through as printed and counted in the build log. Empty = the source printed no value in any form for this row. It never holds an internal marker of this project own. | Copied from the internal audited record without transformation. |
| `unit_as_printed` | - | The printed unit/basis wording for value_as_printed; empty = the source printed no unit wording with the value. | Copied from the internal audited record without transformation. |

## `csv/phaseboundaries.csv`  (980 rows)

The shared columns above, then:

| column | unit | meaning, and when it is blank | copied or computed |
|---|---|---|---|
| `boundary_type` | - | Phase-boundary class: dew_point, bubble_point, hydrate, three_phase; empty where the available source record does not resolve the branch (e.g. isopleth crossings). | INFERRED from the wording of the internal notes, unit string, flags and identifiers -- hydrate wording gives hydrate, unambiguous dew or bubble wording gives that branch, three-phase wording gives three_phase -- and left empty when the wording settles nothing. |
| `value_as_printed` | - | The solubility, water-content or boundary quantity exactly as the source printed it. This column is deliberately not numeric. Five closed forms, and the build refuses anything else: a number; a number with a printed uncertainty such as 0.0014(1); a decimal comma such as 0,0149; ILLEGIBLE (the printed cell could not be read and is never guessed); NOT PRINTED (the source gives the quantity in some other form). Anything else is the prose class -- wording the source printed instead of a digit, carried through as printed and counted in the build log. Empty = the source printed no value in any form for this row. It never holds an internal marker of this project own. | Copied from the internal audited record without transformation. |
| `unit_as_printed` | - | The printed unit/basis wording for value_as_printed; empty = the source printed no unit wording with the value. | Copied from the internal audited record without transformation. |

## `csv/sources.csv`  (497 rows)

One row per source. Join it to any measurement file on `source_id`.

| column | unit | meaning, and when it is blank | copied or computed |
|---|---|---|---|
| `source_id` | - | Paper-level source key (leading author + year where parseable) plus a gas-domain suffix, always: e.g. culbersonmcketta1950_ch4. Cross-gas identity of same-name-same-year papers is not assumed. One row per source_id in aquasoldb_sources.csv. | Derived from the internal source id (or, where that carries no year, the internal campaign label) plus the gas-bank tag. |
| `reference` | - | Short human-readable reference (e.g. 'Drummond 1981'); full citation in aquasoldb_sources.csv. | Read from this project per-gas source trackers, with repository bookkeeping removed; no citation is typed by hand where a DOI resolves. |
| `year` | - | Publication year. | Taken from the short reference where that carries a year, otherwise from the tracker citation, otherwise from the source key. |
| `source_type` | - | What kind of publication the source is, one word of six: journal, thesis, report, compilation, conference, book-chapter. Every source carries exactly one; the cell is never empty. `compilation` means the values were read out of a compiled or evaluated secondary source -- an IUPAC Solubility Data Series volume, say, or a later paper's literature table -- rather than out of the paper that first printed them; the reference text names both. At v1.0 no source is `book-chapter`; the word is in the vocabulary and the count is zero. | Decided by the build, in this order. (1) Where a tracker row this build reads states a no-DOI reason in the written form `no DOI (<class>)`, that written class decides. (2) Otherwise the published citation's own shape decides. Both routes use ONE keyword table, tried in the order thesis, report, conference, compilation, book-chapter, and the first family that matches wins. (3) `journal` is the last resort: authors, a year and a venue, with nothing saying otherwise. On the citation route `compilation` is narrow on purpose -- 'data reproduced from', 'compiled in', or a Solubility Data Series volume cited as the venue -- so a journal paper merely annotated with a compilation's volume number stays a journal. |
| `doi` | - | DOI, empty where none exists (theses, pre-DOI journals). | Extracted from the tracker full citation text. The identifier is taken WHOLE: a DOI suffix may legally contain ';' and ',' and the reader no longer stops at either (KI-158), because a truncated identifier resolves to nothing while still looking like a DOI. |
| `url` | - | A resolvable record for a source that has no DOI -- a thesis repository or report archive entry -- empty otherwise. A source that carries a DOI never carries a url as well: the DOI is the resolvable record there. At v1.0 this column is empty on every source; it is the place such a record goes as they are found. | READ, never constructed: the first `https://` locator printed on the tracker row this build reads for the source, with trailing sentence punctuation removed. The build never composes a URL from an institution name, and never publishes an insecure `http://` one. |
| `n_solubility` | rows | Computed row count contributed to aquasoldb_solubility.csv. | Counted over the built file. |
| `n_watercontent` | rows | Computed row count contributed to aquasoldb_watercontent.csv. | Counted over the built file. |
| `n_liquidwatercontent` | rows | Computed row count contributed to aquasoldb_liquidwatercontent.csv. | Counted over the built file. |
| `n_mixtures` | rows | Computed row count contributed to aquasoldb_mixtures.csv. | Counted over the built file. |
| `n_phaseboundaries` | rows | Computed row count contributed to aquasoldb_phaseboundaries.csv. | Counted over the built file. |

## `csv/column_dictionary.csv`

The same information as a table you can read with a program, one row per column name.

| column | meaning |
|---|---|
| `column` | the column name, as it appears in the header of a data file |
| `unit` | its unit, or `-` where the value is a label rather than a quantity |
| `definition` | what the value means, and when the cell is blank |
| `applies_to` | the files that carry this column |
| `derivation` | copied from the record behind it, or computed at build time, and by what rule |

## The `method` vocabulary

One value per source, read from the source itself. Where a paper prints several tables measured different ways, the column gives the dominant one.

- `analytical_sampling` -- A sample of a phase is withdrawn from the equilibrium vessel and quantified somewhere else: by titration, by the gas evolved from the withdrawn aliquot, by mass spectrometry, or by weighing.
- `manometric_volumetric` -- Gas uptake or the fall in pressure is read off the apparatus itself -- a manometer, a gas buret, an absorptiometer, a closed-cell PVT balance -- with no liquid ever withdrawn. The classic Bunsen and Ostwald absorptiometers, and the Ben-Naim & Baer and Scholander families, are here.
- `chromatography` -- Gas chromatography is the named quantification step.
- `synthetic_visual` -- A charge of known composition is made up and a phase change is watched for: a bubble or dew point in a windowed cell.
- `electrochemical` -- An electrochemical or inline sensor reads the composition -- a Karl Fischer cell, a hygrometer probe.
- `gravimetric` -- Quantities are established by weighing, as with a weighing bomb.
- `pressure_decrease_mass_balance` -- A known charge of gas is admitted to a closed cell and the amount dissolved is obtained from the measured fall in pressure, closed against the mass balance of the charge.
- `calculated_compilation` -- The number is derived or recomputed by a compiler rather than measured in the work cited.
- `other` -- A technique outside the families above: spectroscopy, a calorimetric derivation, an isotopic tracer, densitometry.
- `unstated` -- No method is recorded for this source, and the column does not tell two cases apart: the source was read and does not say how the measurement was made, or the paper was not available to us, so nobody could read it. The README gives how many rows are the second case; the per-source evidence is in the project trackers. This is not the same as `pending`, which means nobody has classified it yet.
- `pending` -- no classification has reached this source yet. The reason is recorded per source rather than guessed at.

## Machine-readable rule constants

The release's own test file `tests/test_data.py` READS the block below rather than restating any of it, so a vocabulary, a tolerance or a plausibility band cannot be changed in one place and left standing in the other. `range <column>: low, high` is a plausibility band, not a measurement of the data: it is wide enough that no shipped row sits near an edge, and narrow enough that a unit slip lands outside it. `published_rows` plus `screened_rows` is `audited_rows`, the total the compilation's own records expect for these campaigns; the rows not published are listed one by one, with the reason, in `provenance/screened_rows.csv`.

```
flags: digitized_from_figure, from_compilation, printed_defect, replicate, suspect_value
method: analytical_sampling, manometric_volumetric, chromatography, synthetic_visual, electrochemical, gravimetric, pressure_decrease_mass_balance, calculated_compilation, other, unstated
method_extra: pending
source_type: book-chapter, compilation, conference, journal, report, thesis
ion_columns: m_Na, m_Cl, m_K, m_Ca, m_Mg, m_SO4
ion_charge_balance_tolerance: 5e-06
value_labels: ILLEGIBLE, NOT PRINTED
forbidden_cell_values: -999, -999.0, -9999, 999999, NA, N/A, #N/A, NULL, NONE, NAN, NaN, TBD, TO-RESOLVE, TODO, XXX, FIXME, ?, ??, ???, UNKNOWN, PLACEHOLDER, placeholder
forbidden_columns: critical_locus, fit_eligible, fit_pool, fit_role, fit_weight, held_out, holdout, in_fit, regression_ready, test_only, tier, train_test, validation_only, weight
published_rows: 22872
screened_rows: 1827
audited_rows: 24699
range temperature_K: 150, 900
range pressure_MPa: 0, 2000
range solubility_mole_fraction: 0, 1
range water_mole_fraction_vapor: 0, 1
range water_mole_fraction_liquid_hydrocarbon: 0, 1
range gas2_mole_fraction_feed: 0, 1
range solubility_mol_per_kgw: 0, 100
range salt_molality: 0, 100
range m_Na: 0, 100
range m_Cl: 0, 100
range m_K: 0, 100
range m_Ca: 0, 100
range m_Mg: 0, 100
range m_SO4: 0, 100
```

