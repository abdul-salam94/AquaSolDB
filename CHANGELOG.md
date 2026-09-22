# AquaSolDB -- CHANGELOG

## v1.2 -- definitions, source identification and the replicate flag corrected

A corrections release under the versioning rule in the README: what the database covers is exactly what v1.1 covered. Measured against v1.1 across the seven shipped tables: 0 measurement values changed on the rows both releases publish under the same identifier (`temperature_K`, `pressure_MPa`, `solubility_mole_fraction`, `solubility_mol_per_kgw`, `value_as_printed`, `unit_as_printed`), 0 columns gained or lost, 78 rows added and 77 removed -- and every added and removed row is accounted for in `CHANGELOG.md`, by table. What moved is the identification of the papers behind the rows, the published definitions, and the release documents.

### The data files

`csv/solubility.csv`: 18200 rows (v1.1 held 18200); 42 rows added, 42 removed, 311 cells changed.

Rows added, by point_id: `CO2_hou2013jsf73water_co2_001`, `CO2_hou2013jsf73water_co2_002`, `CO2_hou2013jsf73water_co2_003`, `CO2_hou2013jsf73water_co2_004`, `CO2_hou2013jsf73water_co2_005`, `CO2_hou2013jsf73water_co2_006`, `CO2_hou2013jsf73water_co2_007`, `CO2_hou2013jsf73water_co2_008`, `CO2_hou2013jsf73water_co2_009`, `CO2_hou2013jsf73water_co2_010`, `CO2_hou2013jsf73water_co2_011`, `CO2_hou2013jsf73water_co2_012`, `CO2_hou2013jsf73water_co2_013`, `CO2_hou2013jsf73water_co2_014`, `CO2_hou2013jsf73water_co2_015`, `CO2_hou2013jsf73water_co2_016`, `CO2_hou2013jsf73water_co2_017`, `CO2_hou2013jsf73water_co2_018`, `CO2_hou2013jsf73water_co2_019`, `CO2_hou2013jsf73water_co2_020`, `CO2_hou2013jsf73water_co2_021`, `CO2_hou2013jsf73water_co2_022`, `CO2_hou2013jsf73water_co2_023`, `CO2_hou2013jsf73water_co2_024`, `CO2_hou2013jsf73water_co2_025`, `CO2_hou2013jsf73water_co2_026`, `CO2_hou2013jsf73water_co2_027`, `CO2_hou2013jsf73water_co2_028`, `CO2_hou2013jsf73water_co2_029`, `CO2_hou2013jsf73water_co2_030`, `CO2_hou2013jsf73water_co2_031`, `CO2_hou2013jsf73water_co2_032`, `CO2_hou2013jsf73water_co2_033`, `CO2_hou2013jsf73water_co2_034`, `CO2_hou2013jsf73water_co2_035`, `CO2_hou2013jsf73water_co2_036`, `CO2_hou2013jsf73water_co2_037`, `CO2_hou2013jsf73water_co2_038`, `CO2_hou2013jsf73water_co2_039`, `CO2_hou2013jsf73water_co2_040`, `CO2_hou2013jsf73water_co2_041`, `CO2_hou2013jsf73water_co2_042`.

Rows removed, by point_id: `CO2_hou2013_co2_001`, `CO2_hou2013_co2_002`, `CO2_hou2013_co2_003`, `CO2_hou2013_co2_004`, `CO2_hou2013_co2_005`, `CO2_hou2013_co2_006`, `CO2_hou2013_co2_007`, `CO2_hou2013_co2_008`, `CO2_hou2013_co2_009`, `CO2_hou2013_co2_010`, `CO2_hou2013_co2_011`, `CO2_hou2013_co2_012`, `CO2_hou2013_co2_013`, `CO2_hou2013_co2_014`, `CO2_hou2013_co2_015`, `CO2_hou2013_co2_016`, `CO2_hou2013_co2_017`, `CO2_hou2013_co2_018`, `CO2_hou2013_co2_019`, `CO2_hou2013_co2_020`, `CO2_hou2013_co2_021`, `CO2_hou2013_co2_022`, `CO2_hou2013_co2_023`, `CO2_hou2013_co2_024`, `CO2_hou2013_co2_025`, `CO2_hou2013_co2_026`, `CO2_hou2013_co2_027`, `CO2_hou2013_co2_028`, `CO2_hou2013_co2_029`, `CO2_hou2013_co2_030`, `CO2_hou2013_co2_031`, `CO2_hou2013_co2_032`, `CO2_hou2013_co2_033`, `CO2_hou2013_co2_034`, `CO2_hou2013_co2_035`, `CO2_hou2013_co2_036`, `CO2_hou2013_co2_037`, `CO2_hou2013_co2_038`, `CO2_hou2013_co2_039`, `CO2_hou2013_co2_040`, `CO2_hou2013_co2_041`, `CO2_hou2013_co2_042`.

Changed cells by column: `flags` 167, `method` 72, `reference` 72.

Every changed cell, by point_id:

- `CH4_abdi2017_ch4_111` `flags`: (blank) -> `replicate`
- `CH4_abdi2017_ch4_119` `flags`: (blank) -> `replicate`
- `CH4_aljeban2026_ch4_001` `flags`: `digitized_from_figure;printed_defect` -> `digitized_from_figure;printed_defect;replicate`
- `CH4_aljeban2026_ch4_006` `flags`: `digitized_from_figure` -> `digitized_from_figure;replicate`
- `CH4_aljeban2026_ch4_008` `flags`: `digitized_from_figure;printed_defect` -> `digitized_from_figure;printed_defect;replicate`
- `CH4_aljeban2026_ch4_013` `flags`: `digitized_from_figure` -> `digitized_from_figure;replicate`
- `CH4_aljeban2026_ch4_015` `flags`: `digitized_from_figure;printed_defect` -> `digitized_from_figure;printed_defect;replicate`
- `CH4_aljeban2026_ch4_022` `flags`: `digitized_from_figure;printed_defect` -> `digitized_from_figure;printed_defect;replicate`
- `CH4_aljeban2026_ch4_024` `flags`: `digitized_from_figure` -> `digitized_from_figure;replicate`
- `CH4_aljeban2026_ch4_031` `flags`: `digitized_from_figure` -> `digitized_from_figure;replicate`
- `CH4_aljeban2026_ch4_032` `flags`: `digitized_from_figure;printed_defect` -> `digitized_from_figure;printed_defect;replicate`
- `CH4_aljeban2026_ch4_034` `flags`: `digitized_from_figure` -> `digitized_from_figure;replicate`
- `CH4_aljeban2026_ch4_040` `flags`: `digitized_from_figure` -> `digitized_from_figure;replicate`
- `CH4_aljeban2026_ch4_043` `flags`: `digitized_from_figure;printed_defect` -> `digitized_from_figure;printed_defect;replicate`
- `CH4_aljeban2026_ch4_045` `flags`: `digitized_from_figure` -> `digitized_from_figure;replicate`
- `CH4_aljeban2026_ch4_051` `flags`: `digitized_from_figure` -> `digitized_from_figure;replicate`
- `CH4_aljeban2026_ch4_052` `flags`: `digitized_from_figure` -> `digitized_from_figure;replicate`
- `CH4_blountprice1982_ch4_036` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_037` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_064` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_066` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_118` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_119` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_122` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_123` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_128` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_129` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_185` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_187` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_192` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_193` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_276` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_277` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_281` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_282` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_304` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_305` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_334` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_335` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_418` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_419` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_463` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_464` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_690` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_691` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_692` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_693` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_712` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_713` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_714` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_715` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_716` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_717` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_726` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_727` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_735` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_737` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_741` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_742` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_756` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_758` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_760` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_761` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_762` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_763` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_764` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_771` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_772` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_782` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_783` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_787` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_788` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_794` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_796` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_797` `flags`: (blank) -> `replicate`
- `CH4_blountprice1982_ch4_798` `flags`: (blank) -> `replicate`
- `CH4_morrisonbillett1948_ch4_002` `flags`: (blank) -> `replicate`
- `CH4_morrisonbillett1948_ch4_003` `flags`: (blank) -> `replicate`
- `CH4_morrisonbillett1948_ch4_004` `flags`: (blank) -> `replicate`
- `CH4_morrisonbillett1948_ch4_005` `flags`: (blank) -> `replicate`
- `CO2_alimohammadi2025_co2_002` `flags`: (blank) -> `replicate`
- `CO2_alimohammadi2025_co2_004` `flags`: (blank) -> `replicate`
- `CO2_harneddavis1943_co2_080` `flags`: (blank) -> `replicate`
- `CO2_harneddavis1943_co2_081` `flags`: (blank) -> `replicate`
- `CO2_harneddavis1943_co2_105` `flags`: (blank) -> `replicate`
- `CO2_harneddavis1943_co2_107` `flags`: (blank) -> `replicate`
- `CO2_hou2013_co2_043` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_043` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_044` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_044` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_045` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_045` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_046` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_046` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_047` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_047` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_048` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_048` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_049` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_049` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_050` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_050` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_051` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_051` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_052` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_052` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_053` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_053` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_054` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_054` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_055` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_055` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_056` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_056` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_057` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_057` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_058` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_058` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_059` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_059` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_060` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_060` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_061` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_061` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_062` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_062` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_063` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_063` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_064` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_064` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_065` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_065` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_066` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_066` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_067` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_067` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_068` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_068` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_069` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_069` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_070` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_070` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_071` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_071` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_072` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_072` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_073` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_073` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_074` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_074` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_075` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_075` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_076` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_076` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_077` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_077` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_078` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_078` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_079` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_079` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_080` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_080` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_081` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_081` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_082` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_082` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_083` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_083` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_084` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_084` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_085` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_085` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_086` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_086` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_087` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_087` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_088` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_088` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_089` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_089` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_090` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_090` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_091` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_091` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_092` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_092` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_093` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_093` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_094` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_094` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_095` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_095` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_096` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_096` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_097` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_097` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_098` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_098` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_099` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_099` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_100` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_100` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_101` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_101` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_102` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_102` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_103` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_103` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_104` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_104` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_105` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_105` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_106` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_106` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_107` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_107` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_108` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_108` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_109` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_109` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_110` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_110` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_111` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_111` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_112` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_112` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_113` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_113` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_114` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_114` `method`: `unstated` -> `chromatography`
- `CO2_jacobsaylor2016_co2_013` `flags`: (blank) -> `replicate`
- `CO2_jacobsaylor2016_co2_016` `flags`: (blank) -> `replicate`
- `CO2_jacobsaylor2016_co2_022` `flags`: (blank) -> `replicate`
- `CO2_jacobsaylor2016_co2_025` `flags`: (blank) -> `replicate`
- `CO2_jacobsaylor2016_co2_195` `flags`: (blank) -> `replicate`
- `CO2_jacobsaylor2016_co2_196` `flags`: (blank) -> `replicate`
- `CO2_mousavi2024_co2_077` `flags`: (blank) -> `replicate`
- `CO2_mousavi2024_co2_078` `flags`: (blank) -> `replicate`
- `H2_aljeban2026_h2_001` `flags`: `digitized_from_figure;printed_defect` -> `digitized_from_figure;printed_defect;replicate`
- `H2_aljeban2026_h2_010` `flags`: `digitized_from_figure;printed_defect` -> `digitized_from_figure;printed_defect;replicate`
- `H2_aljeban2026_h2_019` `flags`: `digitized_from_figure;printed_defect` -> `digitized_from_figure;printed_defect;replicate`
- `H2_aljeban2026_h2_028` `flags`: `digitized_from_figure;printed_defect` -> `digitized_from_figure;printed_defect;replicate`
- `H2_aljeban2026_h2_038` `flags`: `digitized_from_figure;printed_defect` -> `digitized_from_figure;printed_defect;replicate`
- `H2_aljeban2026_h2_049` `flags`: `digitized_from_figure;printed_defect` -> `digitized_from_figure;printed_defect;replicate`
- `H2_crozieryamamoto1974_h2_032` `flags`: `from_compilation` -> `from_compilation;replicate`
- `H2_crozieryamamoto1974_h2_033` `flags`: `from_compilation` -> `from_compilation;replicate`
- `H2_crozieryamamoto1974_h2_135` `flags`: `from_compilation` -> `from_compilation;replicate`
- `H2_crozieryamamoto1974_h2_136` `flags`: `from_compilation` -> `from_compilation;replicate`
- `H2_crozieryamamoto1974_h2_138` `flags`: `from_compilation` -> `from_compilation;replicate`
- `H2_crozieryamamoto1974_h2_145` `flags`: `from_compilation` -> `from_compilation;replicate`
- `H2_crozieryamamoto1974_h2_159` `flags`: `from_compilation` -> `from_compilation;replicate`
- `H2_crozieryamamoto1974_h2_160` `flags`: `from_compilation` -> `from_compilation;replicate`
- `H2_crozieryamamoto1974_h2_178` `flags`: `from_compilation` -> `from_compilation;replicate`
- `H2_crozieryamamoto1974_h2_179` `flags`: `from_compilation` -> `from_compilation;replicate`
- `H2_crozieryamamoto1974_h2_198` `flags`: `from_compilation` -> `from_compilation;replicate`
- `H2_crozieryamamoto1974_h2_209` `flags`: `from_compilation` -> `from_compilation;replicate`
- `H2_crozieryamamoto1974_h2_210` `flags`: `from_compilation` -> `from_compilation;replicate`
- `H2_crozieryamamoto1974_h2_213` `flags`: `from_compilation` -> `from_compilation;replicate`
- `H2_crozieryamamoto1974_h2_216` `flags`: `from_compilation` -> `from_compilation;replicate`
- `H2_crozieryamamoto1974_h2_223` `flags`: `from_compilation` -> `from_compilation;replicate`
- `H2_crozieryamamoto1974_h2_225` `flags`: `from_compilation` -> `from_compilation;replicate`
- `H2_crozieryamamoto1974_h2_239` `flags`: `from_compilation` -> `from_compilation;replicate`
- `H2_crozieryamamoto1974_h2_240` `flags`: `from_compilation` -> `from_compilation;replicate`
- `H2_kishima1989_h2_025` `flags`: (blank) -> `replicate`
- `H2_kishima1989_h2_027` `flags`: (blank) -> `replicate`
- `H2_kishima1989_h2_039` `flags`: (blank) -> `replicate`
- `H2_kishima1989_h2_041` `flags`: (blank) -> `replicate`
- `H2_wiebegaddy1935_h2_001` `flags`: `from_compilation` -> `from_compilation;replicate`
- `H2_wiebegaddy1935_h2_002` `flags`: `from_compilation` -> `from_compilation;replicate`
- `H2_wiebegaddy1935_h2_004` `flags`: `from_compilation` -> `from_compilation;replicate`
- `H2_wiebegaddy1935_h2_005` `flags`: `from_compilation` -> `from_compilation;replicate`
- `H2S_barrett1988_h2s_047` `flags`: (blank) -> `replicate`
- `H2S_barrett1988_h2s_055` `flags`: (blank) -> `replicate`
- `H2S_barrett1988_h2s_107` `flags`: (blank) -> `replicate`
- `H2S_barrett1988_h2s_119` `flags`: (blank) -> `replicate`
- `H2S_barrett1988_h2s_131` `flags`: (blank) -> `replicate`
- `H2S_barrett1988_h2s_145` `flags`: (blank) -> `replicate`
- `H2S_barrett1988_h2s_152` `flags`: (blank) -> `replicate`
- `H2S_barrett1988_h2s_153` `flags`: (blank) -> `replicate`
- `H2S_barrett1988_h2s_166` `flags`: (blank) -> `replicate`
- `H2S_barrett1988_h2s_168` `flags`: (blank) -> `replicate`
- `H2S_barrett1988_h2s_174` `flags`: (blank) -> `replicate`
- `H2S_barrett1988_h2s_178` `flags`: (blank) -> `replicate`
- `H2S_barrett1988_h2s_189` `flags`: (blank) -> `replicate`
- `H2S_barrett1988_h2s_195` `flags`: (blank) -> `replicate`
- `H2S_barrett1988_h2s_242` `flags`: (blank) -> `replicate`
- `H2S_barrett1988_h2s_244` `flags`: (blank) -> `replicate`
- `H2S_barrett1988_h2s_249` `flags`: (blank) -> `replicate`
- `H2S_barrett1988_h2s_250` `flags`: (blank) -> `replicate`
- `H2S_drummond1981_h2s_185` `flags`: (blank) -> `replicate`
- `H2S_drummond1981_h2s_186` `flags`: (blank) -> `replicate`
- `H2S_gamsjagerrainerschindler1967_h2s_002` `flags`: (blank) -> `replicate`
- `H2S_gamsjagerrainerschindler1967_h2s_003` `flags`: (blank) -> `replicate`
- `H2S_gamsjagerrainerschindler1967_h2s_009` `flags`: (blank) -> `replicate`
- `H2S_gamsjagerrainerschindler1967_h2s_010` `flags`: (blank) -> `replicate`
- `H2S_kishima1989_h2s_009` `flags`: (blank) -> `replicate`
- `H2S_kishima1989_h2s_021` `flags`: (blank) -> `replicate`
- `N2_douglas1964_n2_012` `flags`: `from_compilation` -> `from_compilation;replicate`
- `N2_douglas1964_n2_014` `flags`: `from_compilation` -> `from_compilation;replicate`
- `N2_douglas1964_n2_016` `flags`: `from_compilation` -> `from_compilation;replicate`
- `N2_douglas1964_n2_017` `flags`: `from_compilation` -> `from_compilation;replicate`
- `N2_douglas1964_n2_022` `flags`: `from_compilation` -> `from_compilation;replicate`
- `N2_douglas1964_n2_023` `flags`: `from_compilation` -> `from_compilation;replicate`
- `N2_douglas1964_n2_048` `flags`: `from_compilation` -> `from_compilation;replicate`
- `N2_douglas1964_n2_050` `flags`: `from_compilation` -> `from_compilation;replicate`
- `N2_douglas1964_n2_054` `flags`: `from_compilation` -> `from_compilation;replicate`
- `N2_douglas1964_n2_056` `flags`: `from_compilation` -> `from_compilation;replicate`
- `N2_vanslyke1934_n2_003` `flags`: `from_compilation` -> `from_compilation;replicate`
- `N2_vanslyke1934_n2_004` `flags`: `from_compilation` -> `from_compilation;replicate`
- `N2_vanslyke1934_n2_006` `flags`: `from_compilation` -> `from_compilation;replicate`
- `N2_vanslyke1934_n2_008` `flags`: `from_compilation` -> `from_compilation;replicate`

`csv/watercontent.csv`: 2010 rows (v1.1 held 2013); 32 rows added, 35 removed, 169 cells changed.

Rows added, by point_id: `CO2_hou2013jsf73water_co2_043`, `CO2_hou2013jsf73water_co2_044`, `CO2_hou2013jsf73water_co2_045`, `CO2_hou2013jsf73water_co2_046`, `CO2_hou2013jsf73water_co2_047`, `CO2_hou2013jsf73water_co2_048`, `CO2_hou2013jsf73water_co2_049`, `CO2_hou2013jsf73water_co2_050`, `CO2_hou2013jsf73water_co2_051`, `CO2_hou2013jsf73water_co2_052`, `CO2_hou2013jsf73water_co2_053`, `CO2_hou2013jsf73water_co2_054`, `CO2_hou2013jsf73water_co2_055`, `CO2_hou2013jsf73water_co2_056`, `CO2_hou2013jsf73water_co2_057`, `CO2_hou2013jsf73water_co2_058`, `CO2_hou2013jsf73water_co2_059`, `CO2_hou2013jsf73water_co2_060`, `CO2_hou2013jsf73water_co2_061`, `CO2_hou2013jsf73water_co2_062`, `CO2_hou2013jsf73water_co2_063`, `CO2_hou2013jsf73water_co2_064`, `CO2_hou2013jsf73water_co2_065`, `CO2_hou2013jsf73water_co2_066`, `CO2_hou2013jsf73water_co2_067`, `CO2_hou2013jsf73water_co2_068`, `CO2_hou2013jsf73water_co2_069`, `CO2_hou2013jsf73water_co2_070`, `CO2_hou2013jsf73water_co2_071`, `CO2_hou2013jsf73water_co2_072`, `CO2_hou2013jsf73water_co2_073`, `CO2_hou2013jsf73water_co2_074`.

Rows removed, by point_id: `CO2_hou2013_co2_115`, `CO2_hou2013_co2_116`, `CO2_hou2013_co2_117`, `CO2_hou2013_co2_118`, `CO2_hou2013_co2_119`, `CO2_hou2013_co2_120`, `CO2_hou2013_co2_121`, `CO2_hou2013_co2_122`, `CO2_hou2013_co2_123`, `CO2_hou2013_co2_124`, `CO2_hou2013_co2_125`, `CO2_hou2013_co2_126`, `CO2_hou2013_co2_127`, `CO2_hou2013_co2_128`, `CO2_hou2013_co2_129`, `CO2_hou2013_co2_130`, `CO2_hou2013_co2_131`, `CO2_hou2013_co2_132`, `CO2_hou2013_co2_133`, `CO2_hou2013_co2_134`, `CO2_hou2013_co2_135`, `CO2_hou2013_co2_136`, `CO2_hou2013_co2_137`, `CO2_hou2013_co2_138`, `CO2_hou2013_co2_139`, `CO2_hou2013_co2_140`, `CO2_hou2013_co2_141`, `CO2_hou2013_co2_142`, `CO2_hou2013_co2_143`, `CO2_hou2013_co2_144`, `CO2_hou2013_co2_145`, `CO2_hou2013_co2_146`, `CO2_king1992_co2_028`, `CO2_king1992_co2_029`, `CO2_king1992_co2_030`.

Changed cells by column: `flags` 25, `method` 72, `reference` 72.

Every changed cell, by point_id:

- `C2H6_alassi2023_c2c4_001` `flags`: (blank) -> `replicate`
- `C2H6_alassi2023_c2c4_002` `flags`: (blank) -> `replicate`
- `C2H6_alassi2023_c2c4_004` `flags`: (blank) -> `replicate`
- `C2H6_alassi2023_c2c4_005` `flags`: (blank) -> `replicate`
- `C2H6_alassi2023_c2c4_007` `flags`: (blank) -> `replicate`
- `C2H6_alassi2023_c2c4_008` `flags`: (blank) -> `replicate`
- `C2H6_alassi2023_c2c4_009` `flags`: (blank) -> `replicate`
- `C2H6_alassi2023_c2c4_010` `flags`: (blank) -> `replicate`
- `C2H6_alassi2023_c2c4_011` `flags`: (blank) -> `replicate`
- `C2H6_alassi2023_c2c4_012` `flags`: (blank) -> `replicate`
- `C2H6_alassi2023_c2c4_014` `flags`: (blank) -> `replicate`
- `C2H6_alassi2023_c2c4_015` `flags`: (blank) -> `replicate`
- `C2H6_alassi2023_c2c4_020` `flags`: (blank) -> `replicate`
- `C2H6_alassi2023_c2c4_021` `flags`: (blank) -> `replicate`
- `C2H6_alassi2023_c2c4_022` `flags`: (blank) -> `replicate`
- `C2H6_alassi2023_c2c4_023` `flags`: (blank) -> `replicate`
- `C2H6_alassi2023_c2c4_031` `flags`: (blank) -> `replicate`
- `C2H6_alassi2023_c2c4_032` `flags`: (blank) -> `replicate`
- `C2H6_alassi2023_c2c4_034` `flags`: (blank) -> `replicate`
- `C2H6_alassi2023_c2c4_035` `flags`: (blank) -> `replicate`
- `C2H6_alassi2023_c2c4_040` `flags`: (blank) -> `replicate`
- `C2H6_alassi2023_c2c4_049` `flags`: (blank) -> `replicate`
- `C2H6_alassi2023_c2c4_050` `flags`: (blank) -> `replicate`
- `C2H6_coanking1971_c2c4_006` `flags`: (blank) -> `replicate`
- `C2H6_coanking1971_c2c4_007` `flags`: (blank) -> `replicate`
- `CO2_hou2013_co2_147` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_147` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_148` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_148` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_149` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_149` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_150` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_150` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_151` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_151` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_152` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_152` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_153` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_153` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_154` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_154` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_155` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_155` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_156` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_156` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_157` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_157` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_158` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_158` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_159` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_159` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_160` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_160` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_161` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_161` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_162` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_162` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_163` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_163` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_164` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_164` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_165` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_165` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_166` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_166` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_167` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_167` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_168` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_168` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_169` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_169` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_170` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_170` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_171` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_171` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_172` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_172` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_173` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_173` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_174` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_174` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_175` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_175` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_176` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_176` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_177` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_177` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_178` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_178` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_179` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_179` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_180` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_180` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_181` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_181` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_182` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_182` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_183` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_183` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_184` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_184` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_185` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_185` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_186` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_186` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_187` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_187` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_188` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_188` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_189` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_189` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_190` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_190` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_191` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_191` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_192` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_192` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_193` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_193` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_194` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_194` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_195` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_195` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_196` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_196` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_197` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_197` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_198` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_198` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_199` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_199` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_200` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_200` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_201` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_201` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_202` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_202` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_203` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_203` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_204` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_204` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_205` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_205` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_206` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_206` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_207` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_207` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_208` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_208` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_209` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_209` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_210` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_210` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_211` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_211` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_212` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_212` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_213` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_213` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_214` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_214` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_215` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_215` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_216` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_216` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_217` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_217` `method`: `unstated` -> `chromatography`
- `CO2_hou2013_co2_218` `reference`: `Hou et al. (2013, JSF 73)` -> `Hou et al. (2013, JSF 78)`
- `CO2_hou2013_co2_218` `method`: `unstated` -> `chromatography`

`csv/liquidwatercontent.csv`: 21 rows (v1.1 held 18); 3 rows added, 0 removed, 0 cells changed.

Rows added, by point_id: `CO2_king1992_co2_028`, `CO2_king1992_co2_029`, `CO2_king1992_co2_030`.

`csv/mixtures.csv`: 1661 rows (v1.1 held 1661); 0 rows added, 0 removed, 23 cells changed.

Changed cells by column: `flags` 23.

Every changed cell, by point_id:

- `C2H6_amirijafari1972_c2c4_017` `flags`: (blank) -> `replicate`
- `C2H6_amirijafari1972_c2c4_033` `flags`: (blank) -> `replicate`
- `H2_aljeban2026_h2_060` `flags`: `digitized_from_figure;printed_defect` -> `digitized_from_figure;printed_defect;replicate`
- `H2_aljeban2026_h2_064` `flags`: `digitized_from_figure` -> `digitized_from_figure;replicate`
- `H2_aljeban2026_h2_066` `flags`: `digitized_from_figure` -> `digitized_from_figure;replicate`
- `H2_aljeban2026_h2_067` `flags`: `digitized_from_figure;printed_defect` -> `digitized_from_figure;printed_defect;replicate`
- `H2_aljeban2026_h2_071` `flags`: `digitized_from_figure` -> `digitized_from_figure;replicate`
- `H2_aljeban2026_h2_073` `flags`: `digitized_from_figure` -> `digitized_from_figure;replicate`
- `H2_aljeban2026_h2_074` `flags`: `digitized_from_figure;printed_defect` -> `digitized_from_figure;printed_defect;replicate`
- `H2_aljeban2026_h2_081` `flags`: `digitized_from_figure;printed_defect` -> `digitized_from_figure;printed_defect;replicate`
- `H2_aljeban2026_h2_087` `flags`: `digitized_from_figure` -> `digitized_from_figure;replicate`
- `H2_aljeban2026_h2_088` `flags`: `digitized_from_figure;printed_defect` -> `digitized_from_figure;printed_defect;replicate`
- `H2_aljeban2026_h2_094` `flags`: `digitized_from_figure` -> `digitized_from_figure;replicate`
- `H2_aljeban2026_h2_095` `flags`: `digitized_from_figure;printed_defect` -> `digitized_from_figure;printed_defect;replicate`
- `H2_aljeban2026_h2_102` `flags`: `digitized_from_figure;printed_defect` -> `digitized_from_figure;printed_defect;replicate`
- `H2_aljeban2026_h2_105` `flags`: `digitized_from_figure` -> `digitized_from_figure;replicate`
- `H2_aljeban2026_h2_106` `flags`: `digitized_from_figure` -> `digitized_from_figure;replicate`
- `H2_aljeban2026_h2_108` `flags`: `digitized_from_figure` -> `digitized_from_figure;replicate`
- `H2_aljeban2026_h2_109` `flags`: `digitized_from_figure;printed_defect` -> `digitized_from_figure;printed_defect;replicate`
- `H2_aljeban2026_h2_112` `flags`: `digitized_from_figure` -> `digitized_from_figure;replicate`
- `H2_aljeban2026_h2_113` `flags`: `digitized_from_figure` -> `digitized_from_figure;replicate`
- `H2_aljeban2026_h2_115` `flags`: `digitized_from_figure` -> `digitized_from_figure;replicate`
- `H2_aljeban2026_h2_116` `flags`: `digitized_from_figure;printed_defect` -> `digitized_from_figure;printed_defect;replicate`

`csv/phaseboundaries.csv`: 980 rows (v1.1 held 980); 0 rows added, 0 removed, 2 cells changed.

Changed cells by column: `flags` 2.

Every changed cell, by point_id:

- `C2H6_maekawa2001_c2c4_038` `flags`: (blank) -> `replicate`
- `C2H6_maekawa2001_c2c4_039` `flags`: (blank) -> `replicate`

`csv/sources.csv`: 497 rows (v1.1 held 496); 1 rows added, 0 removed, 4 cells changed.

Rows added, by source_id: `hou2013jsf73water_co2`.

Changed cells by column: `n_liquidwatercontent` 1, `n_solubility` 1, `n_watercontent` 2.

Every changed cell, by source_id:

- `hou2013_co2` `n_solubility`: `114` -> `72`
- `hou2013_co2` `n_watercontent`: `104` -> `72`
- `king1992_co2` `n_watercontent`: `41` -> `38`
- `king1992_co2` `n_liquidwatercontent`: `0` -> `3`

`csv/column_dictionary.csv`: 36 rows (v1.1 held 36); 0 rows added, 0 removed, 8 cells changed.

Changed cells by column: `definition` 8.

Every changed cell, by column:

- `point_id` `definition`: `Stable permanent row ID: <gas>_<sourcekey>_<gasbank>_<nnn>. The gas-bank tag is always present, which makes the ID immune to database growth; nnn is the row number within (gas, source_id), zero-padded, assigned in source order and never renumbered across versions. Rows with unresolved gas use UNK as the gas part.` -> `Stable permanent row ID: <gas>_<sourcekey>_<gasbank>_<nnn>. The gas-bank tag is always present, which makes the ID immune to database growth; nnn is the row number within (gas, source_id), zero-padded, assigned in source order at first publication; never reused, never renumbered; a gap in the numbering marks rows that moved to another source. Rows with unresolved gas use UNK as the gas part.`
- `temperature_K` `definition`: `Temperature.` -> `Temperature; empty = not printed / not resolvable.`
- `method` `definition`: `Measurement-method class, controlled vocabulary of ten values (definitions in README): analytical_sampling, manometric_volumetric, chromatography, synthetic_visual, electrochemical, gravimetric, pressure_decrease_mass_balance, calculated_compilation, other, unstated. One value per source, read from the paper itself with source-page verification; where a source prints several tables measured differently, the dominant class is given. 'unstated' means the source was read and does not say. 'pending' means the method has not yet been classified.` -> `Measurement-method class, controlled vocabulary of ten values (definitions in README): analytical_sampling, manometric_volumetric, chromatography, synthetic_visual, electrochemical, gravimetric, pressure_decrease_mass_balance, calculated_compilation, other, unstated. One value per source, read from the paper itself with source-page verification; where a source prints several tables measured differently, the dominant class is given. 'unstated' covers two cases the column does not tell apart: the source was read and does not say, or the paper was not available to us, so nobody could read it; the README gives how many rows are the second case. 'pending' means the method has not yet been classified.`
- `solubility_mole_fraction` `definition`: `Dissolved-gas mole fraction in the aqueous phase (basis as resolved during normalization).` -> `Dissolved-gas mole fraction in the aqueous phase (basis as resolved during normalization); empty = the internal record carries no mole fraction on this basis.`
- `solubility_mol_per_kgw` `definition`: `Dissolved-gas molality.` -> `Dissolved-gas molality; empty = the internal record carries no molality for this row.`
- `water_mole_fraction_liquid_hydrocarbon` `definition`: `Water mole fraction in a hydrocarbon-rich liquid phase; this is neither gas dissolved in aqueous water nor water in a gas/vapour phase.` -> `Water mole fraction in a liquid non-aqueous phase (hydrocarbon- or CO2-rich); this is neither gas dissolved in aqueous water nor water in a gas/vapour phase.`
- `value_as_printed` `definition`: `The solubility, water-content or boundary quantity exactly as the source printed it. This column is deliberately not numeric: it holds numbers, numbers with a printed uncertainty such as 0.0014(1), decimal commas such as 0,0149, prose the source printed instead of a digit, and two labels -- ILLEGIBLE (the printed cell could not be read and is never guessed) and NOT PRINTED (the source gives the quantity in some other form). It never holds an internal marker of this project own.` -> `The solubility, water-content or boundary quantity exactly as the source printed it. This column is deliberately not numeric. Five closed forms, and the build refuses anything else: a number; a number with a printed uncertainty such as 0.0014(1); a decimal comma such as 0,0149; ILLEGIBLE (the printed cell could not be read and is never guessed); NOT PRINTED (the source gives the quantity in some other form). Anything else is the prose class -- wording the source printed instead of a digit, carried through as printed and counted in the build log. Empty = the source printed no value in any form for this row. It never holds an internal marker of this project own.`
- `unit_as_printed` `definition`: `The printed unit/basis wording for value_as_printed.` -> `The printed unit/basis wording for value_as_printed; empty = the source printed no unit wording with the value.`

### The release documents

- `README.md` and `CITATION.cff` now cite the CONCEPT DOI 10.5281/zenodo.22870466, which always resolves to the newest archived version, and list each version's own DOI beside it. A version DOI is minted by Zenodo when that version's release is published, so this release's own DOI is written in by the documentation commit that follows it (R-DB3-24).
- The version DOIs known when this file was written: v1.0 10.5281/zenodo.22870467; v1.1 10.5281/zenodo.22872900; v1.2 minted by Zenodo at this release; added here after.
- The author line is `Abd, A., & Abushaikha, A.` (R-DB3-25). Each author carries their own affiliation and ORCID in `CITATION.cff` and `.zenodo.json`.
- `CHANGELOG.md` keeps one section per release, newest first. The v1.1 section below and every section under it are quoted from the release that wrote them, unchanged.

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
