# cirwel.github.io

Single-page research index for Kenny Wang / CIRWEL: systems, papers, datasets, and
experiments around runtime infrastructure for persistent AI agents.

Served as a GitHub Pages user site at **https://cirwel.github.io/**.

## House style

The page is set in **Engraved Instrument**, the same house style as
[cirwel.org](https://cirwel.org) (`cirwel/cirwel-site`): cream `#F5F1E8`, oxblood
`#7A1F1F`, Bodoni Moda for display, EB Garamond for reading, JetBrains Mono for
data. Hairline rules, no border-radius, no cards.

**The rule: ornament must be load-bearing.** If a mark carries no information it
does not ship. Here that means every entry is keyed to its own identifier — a
DOI, a package name, a licence, a dataset path — the way a register keys a shelf
mark, and the running head takes its text from the section's own `§NN` label so
it cannot drift out of step with the section it names.

The tokens in `index.html` are copied from `cirwel-site`'s
`tailwind.config.mjs` and `src/styles/global.css`. It is hand-written CSS rather
than Tailwind because this repo is served straight from Pages with no build
step; if the two surfaces disagree, cirwel-site is the source of truth.

## Checked

`scripts/check-index.py` verifies that the page still lists everything CIRWEL has
published, against the **live** page and the **live** Zenodo API:

- **completeness** — every public deposit under the ORCID has its concept DOI on
  the page. This is the leg that catches a paper nobody linked;
- **count** — the stated number of papers equals the number of deposits Zenodo
  classes as publications (software and data are deliberately not counted);
- **no strays** — every Zenodo DOI on the page is a concept DOI, so a reader is
  never pinned to a stale revision;
- **assets** — every vendored font and mark resolves.

Ground truth is neither half of the page. A hand-maintained count beside a
hand-maintained list cannot catch its own omission, because both halves are
edited by whoever forgot. Zenodo's record is written by the act of depositing.

    ./scripts/check-index.py              # the live site
    ./scripts/check-index.py --local      # ./index.html instead
    ./scripts/check-index.py --self-test  # offline negative control

Exit codes are the contract, matching `check-claims.py` in cirwel-site: `0` ok,
`1` drift, `2` unverifiable — **never `0` because a fetch failed**.
⛔Do not edit the checker without re-running `--self-test`, which replays the
2026-09-07 page (two deposits missing, count understated) and asserts it fails.

## Layout

- `index.html` — the whole page. No build step, no dependencies.
- `fonts/` — self-hosted woff2 subsets (latin + latin-ext). No font CDN: the
  page must render identically with no third-party request.
- `assets/` — brand marks, copied from `cirwel-site/public`.
- `scripts/check-index.py` — the deposit check above. Standard library + curl,
  no dependencies.

The public entrance is intentionally plain; deeper research vocabulary belongs in
the linked papers and project repositories rather than in a rotating homepage
taxonomy.
