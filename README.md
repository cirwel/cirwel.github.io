# cirwel.github.io

Single-page research index for Kenny Wang / CIRWEL: systems, papers, datasets, and
experiments around infrastructure for long-lived AI agents.

Served as a GitHub Pages user site at **https://cirwel.github.io/**.

## House style

The page is set in **Engraved Instrument**, the same house style as
[cirwel.org](https://cirwel.org) (`cirwel/cirwel-site`): cream `#F5F1E8`, oxblood
`#7A1F1F`, Bodoni Moda for display, EB Garamond for reading, JetBrains Mono for
data. Hairline rules, no border-radius, no cards.

The layout is a compact personal research index, distinct from the UNITARES
presentation at cirwel.org. Kenny Wang's profile and contact links sit beside
papers and preprints, followed by software and datasets. On mobile, the profile
and section navigation stack above the entries. Publication and release links
use concept DOIs so readers can reach current revisions.

Shared typography and colors provide family resemblance; the index does not
reuse the main site's product hero, decorative seals, or deployment statistics.
The theme control supports automatic, day, and night modes, and the full index
remains readable without JavaScript.

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
- **assets** — every vendored font and mark resolves;
- **register** — the palette and typefaces still match cirwel-site's. This page
  is a hand-written mirror of those tokens, so nothing but a check stops the two
  surfaces drifting apart again. They already did once: the 2026-09-07 rebuild
  put this page in a near-black ground with a bright accent, re-opening the
  two-face split that consolidating cirwelsystems.com into cirwel.org had closed.

Ground truth is neither half of the page. A hand-maintained count beside a
hand-maintained list cannot catch its own omission, because both halves are
edited by whoever forgot. Zenodo's record is written by the act of depositing.

    ./scripts/check-index.py              # the live site
    ./scripts/check-index.py --local      # ./index.html instead
    ./scripts/check-index.py --self-test  # offline negative control

Exit codes are the contract, matching `check-claims.py` in cirwel-site: `0` ok,
`1` drift, `2` unverifiable — **never `0` because a fetch failed**.
⛔Do not edit the checker without re-running `--self-test`. It is a no-network
negative control: it replays the 2026-09-07 page (two deposits missing, count
understated) and asserts the completeness and count legs fire, then re-themes a
page to a dark ground and swaps its serifs for a sans and asserts the register
leg fires on both. A checker nobody has watched fail is not evidence.

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
