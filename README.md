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

## Layout

- `index.html` — the whole page. No build step, no dependencies.
- `fonts/` — self-hosted woff2 subsets (latin + latin-ext). No font CDN: the
  page must render identically with no third-party request.
- `assets/` — brand marks, copied from `cirwel-site/public`.

The public entrance is intentionally plain; deeper research vocabulary belongs in
the linked papers and project repositories rather than in a rotating homepage
taxonomy.
