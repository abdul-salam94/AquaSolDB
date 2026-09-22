# Contributing to AquaSolDB

This dataset is a compilation of published measurements, read from the printed
pages of the papers that reported them. Contributions work the same way: a
number enters only when someone can point at the page it is printed on.

## Reporting a wrong value or a missing paper

Open an issue on the public repository. For a wrong value, give the
`point_id` of the row, the paper's full reference
and DOI, the table or figure it comes from, the page, and the value exactly as
that page prints it. For a missing paper, give the reference and DOI, the gas
and the medium it covers, and roughly how many rows it holds.

Attach nothing copyrighted: no publisher PDF, no scan, no page photograph.
Quote the few numbers at issue and say where they are printed; we read the page
ourselves.

## Contributing rows

A pull request adds an as-printed input table plus a page reference for every
table it adds -- never an edited CSV. The published CSVs are generated files,
and a hand-edited one is rejected even when its numbers are right.

The input table is our 12-column as-printed schema: `source_id`, `pdf_page`,
`T_as_printed`, `T_unit`, `P_as_printed`, `P_unit`, `salt_type`,
`salt_conc_as_printed`, `salt_conc_unit`, `solubility_as_printed`,
`solubility_unit_or_basis`, `notes`. Units go in as the page gives them; the
converter does every conversion.

- Every value must be readable on the printed page you cite. A value you
  computed, converted, fitted, interpolated or read out of a model does not
  belong here, and neither does anything a language model produced.
- Cite the original paper. A row taken from another compilation, a data series
  or a review, without the original in hand, is not accepted: those are the
  rows that carry one transcription error from decade to decade.
- Say what you deliberately left out of a table, and why.

The converter and the builder then regenerate the public files, `SCHEMA.md` and
the checksums from your input table. You never edit those yourself.

## What a maintainer checks

- Every value is re-read against a rendered image of the printed page.
- On a mixed brine, the charge balance of the six ion molalities holds.
- The flags and the method vocabulary are the ones `SCHEMA.md` defines.
- The checksums regenerate and the freshness check is green.
- The reference resolves, and the DOI, where one exists, is the right paper.

Anything a maintainer cannot read on the page comes back to you as a question,
never as a guess.

## How corrections are versioned

Versions are semantic: 1.x for corrections and additions that do not change
what the database covers, 2.0 when the scope grows. `point_id`s are permanent
-- a corrected row keeps its id, and a row that can no longer be supported is
retired rather than renumbered. Every correction gets its own line in
`CHANGELOG.md` saying what changed and on whose evidence, and each release
keeps its own DOI, so a number taken from here stays traceable to its release.

## Licence for contributions

By opening a pull request you agree that your contribution is released under
CC BY 4.0, the licence of the compilation. The measurements themselves stay
with the authors who published them and are cited, not licensed, by us.

You are credited: the sources you contribute carry your name in the sources
table, in a `contributed_by` column added with the first accepted contribution,
and in the changelog line of the release that carries them.

## Contact

Issues and pull requests on the public repository are the route for anything
about the data. For anything that does not belong in public, write to
abdul.salam.abd@hotmail.com.
