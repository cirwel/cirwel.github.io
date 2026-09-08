#!/usr/bin/env python3
"""
check-index.py — does the research index still list everything CIRWEL published?

The failure this exists to prevent, observed 2026-09-08: "Accountability Without
a Trusted Center" had a public CC-BY Zenodo deposit for 25 days and appeared on
neither cirwel.github.io nor cirwel.org. Nothing noticed, because nothing was
looking. The page also stated "3 papers / preprints" beside two DOIs while four
deposits existed.

A count maintained by hand next to a list maintained by hand cannot catch its
own omission: both halves are edited by whoever forgot. So the ground truth is
neither half of the page. It is Zenodo's own record of what this ORCID has
published, which is written by the act of depositing rather than by the act of
remembering.

Four legs, checked against the LIVE page and the LIVE Zenodo API:

  A. completeness — every public deposit's CONCEPT DOI is on the page.
                    This is the leg that catches a paper nobody linked.
  B. count        — the stated number of papers equals the number of deposits
                    whose Zenodo resource type is a publication. Software and
                    data deposits are deliberately not counted as papers.
  C. no strays    — every Zenodo DOI on the page is a known concept DOI. Catches
                    a typo, and catches a VERSION doi pasted where the concept
                    doi belongs (a version doi freezes the reader on an old PDF).
  D. assets       — every vendored font and mark the page references resolves.

Exit codes are the contract, and match scripts/check-claims.py in cirwel-site:

  0  everything checks out
  1  DRIFT — the page and the record disagree
  2  UNVERIFIABLE — could not reach a source

Never 0 because a fetch failed. An instrument that fails toward "healthy" is
worse than no instrument.

Fetching goes through curl, not urllib: the python.org build on the operator's
machine ships no CA bundle, so every https URL raises CERTIFICATE_VERIFY_FAILED
and the whole run degrades to UNKNOWN. curl also keeps this independent of
whichever python3 a scheduler happens to resolve.

Usage:
    ./scripts/check-index.py                 # check the live site
    ./scripts/check-index.py --local         # check ./index.html instead
    ./scripts/check-index.py --self-test     # offline negative control
"""

import json
import re
import subprocess
import sys
from pathlib import Path

PAGE_URL = "https://cirwel.github.io/"
ORCID = "0009-0006-7544-2374"
# Unauthenticated Zenodo caps page size at 25 and 400s above it, so this
# paginates rather than assuming one page will always hold every deposit.
ZENODO_QUERY = (
    "https://zenodo.org/api/records"
    "?q=metadata.creators.person_or_org.identifiers.identifier:%22" + ORCID + "%22"
    "&size=25&all_versions=false"
)

DRIFT, UNVERIFIABLE = 1, 2

NUMBER_WORDS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12,
}


def fetch(url, what):
    """Return the body, or None. None means UNVERIFIABLE, never a pass."""
    try:
        out = subprocess.run(
            ["curl", "-sSL", "--max-time", "30", "--fail", url],
            capture_output=True, text=True, timeout=45,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"  ! could not fetch {what}: {exc}")
        return None
    if out.returncode != 0:
        print(f"  ! could not fetch {what}: curl exit {out.returncode} {out.stderr.strip()[:120]}")
        return None
    return out.stdout


def flatten(html):
    """Strip tags and collapse whitespace, so a phrase that wraps across a line
    or a tag boundary still matches as one string."""
    text = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("&amp;", "&").replace("&nbsp;", " ")
    return re.sub(r"\s+", " ", text).strip()


def fetch_deposits():
    """Every public record for this ORCID, following pagination.

    Returns (deposits, error). A None deposits list means UNVERIFIABLE.
    """
    deposits, url, pages = [], ZENODO_QUERY, 0
    while url:
        pages += 1
        if pages > 20:                       # a runaway pager is a broken API
            return None, "Zenodo pagination did not terminate"
        body = fetch(url, f"the Zenodo record for this ORCID (page {pages})")
        if body is None:
            return None, "could not reach Zenodo"
        try:
            payload = json.loads(body)
        except json.JSONDecodeError as exc:
            return None, f"Zenodo returned unparseable JSON: {exc}"
        page_deposits, err = parse_page(payload)
        if err:
            return None, err
        deposits.extend(page_deposits)
        url = (payload.get("links") or {}).get("next")
    return deposits, None


def parse_page(payload):
    """[(concept_doi, title, is_publication)] for one page of records."""
    deposits = []
    for hit in payload.get("hits", {}).get("hits", []):
        meta = hit.get("metadata", {})
        concept = hit.get("conceptdoi") or (hit.get("parent") or {}).get("id")
        if not concept:
            # A record with no concept DOI cannot be cited stably. Surfacing the
            # version DOI instead would pin readers to one revision, so treat a
            # missing concept DOI as unverifiable rather than silently skipping.
            return None, f"record {hit.get('id')} has no concept DOI"
        rtype = (meta.get("resource_type") or {}).get("type")
        deposits.append((concept.strip(), meta.get("title", "").strip(), rtype == "publication"))
    return deposits, None


def zenodo_dois_on(text):
    return set(re.findall(r"10\.5281/zenodo\.\d+", text))


def check(page_html, deposits):
    """Legs A, B, C. Returns a list of failure strings."""
    failures = []
    flat = flatten(page_html)

    # --- A. completeness ---------------------------------------------------
    on_page = zenodo_dois_on(page_html)
    for concept, title, _ in deposits:
        if concept not in on_page:
            failures.append(f"[A] deposit not on the page: {concept} — {title[:70]}")

    # --- B. count ----------------------------------------------------------
    expected = sum(1 for _, _, is_pub in deposits if is_pub)
    match = re.search(r"([A-Za-z]+|\d+)\s+papers?\s+and\s+preprints?", flat, re.I)
    if not match:
        failures.append("[B] no 'N papers and preprints' line found on the page")
    else:
        raw = match.group(1)
        stated = int(raw) if raw.isdigit() else NUMBER_WORDS.get(raw.lower())
        if stated is None:
            failures.append(f"[B] could not read the stated count: {raw!r}")
        elif stated != expected:
            failures.append(
                f"[B] page says {raw} papers and preprints; Zenodo has {expected} "
                f"publication deposits under ORCID {ORCID}"
            )

    # --- C. no strays ------------------------------------------------------
    known = {concept for concept, _, _ in deposits}
    for doi in sorted(on_page - known):
        failures.append(
            f"[C] page cites {doi}, which is not a concept DOI of any public "
            f"deposit (a version DOI pins readers to one revision)"
        )

    return failures


def check_assets(page_html, local):
    """Leg D. Every vendored reference resolves."""
    failures = []
    refs = sorted(set(re.findall(r'(?:src|href)="((?:fonts|assets)/[^"]+)"', page_html)))
    if not refs:
        return ["[D] page references no vendored fonts or marks — the self-hosting is gone"]
    for ref in refs:
        if local:
            if not (Path(__file__).resolve().parent.parent / ref).exists():
                failures.append(f"[D] missing local file: {ref}")
        elif fetch(PAGE_URL.rstrip("/") + "/" + ref, ref) is None:
            failures.append(f"[D] unreachable: {ref}")
    return failures


SELF_TEST_PAGE = """<html><body>
  <div class="n">3</div><div class="k">papers and preprints</div>
  <a href="https://doi.org/10.5281/zenodo.19647159">Zenodo</a>
  <a href="https://doi.org/10.5281/zenodo.20098168">Zenodo</a>
  <img src="assets/mark-c-illuminated.svg">
</body></html>"""

SELF_TEST_DEPOSITS = [
    ("10.5281/zenodo.19647159", "UNITARES", True),
    ("10.5281/zenodo.20098168", "Trajectory Identity", True),
    ("10.5281/zenodo.21930092", "Digital Proprioception", True),
    ("10.5281/zenodo.21930161", "Accountability Without a Trusted Center", True),
    ("10.5281/zenodo.20320440", "UNITARES software", False),
]


def self_test():
    """Offline negative control: replay the 2026-09-07 page, which was missing
    two deposits and understated the count, and assert this script fails it.
    A checker nobody has watched fail is not evidence of anything."""
    print("self-test: replaying the 2026-09-07 page (2 deposits missing, count understated)")
    failures = check(SELF_TEST_PAGE, SELF_TEST_DEPOSITS)
    legs = {f[1] for f in failures}
    for f in failures:
        print("   ", f)
    if "A" not in legs:
        print("FAIL: leg A did not fire on a page missing two deposits")
        return DRIFT
    if "B" not in legs:
        print("FAIL: leg B did not fire on a page understating its count")
        return DRIFT
    print(f"self-test PASSED — {len(failures)} failures raised, legs A and B both fired")
    return 0


def main():
    args = sys.argv[1:]
    if "--self-test" in args:
        return self_test()
    local = "--local" in args

    if local:
        path = Path(__file__).resolve().parent.parent / "index.html"
        if not path.exists():
            print(f"UNVERIFIABLE: {path} not found")
            return UNVERIFIABLE
        page = path.read_text(encoding="utf-8")
        print(f"checking {path}")
    else:
        page = fetch(PAGE_URL, "the live page")
        if page is None:
            return UNVERIFIABLE
        print(f"checking {PAGE_URL}")

    deposits, err = fetch_deposits()
    if err:
        print(f"  ! {err}")
        return UNVERIFIABLE
    if not deposits:
        # Zero deposits for a published ORCID is far more likely to be a changed
        # query shape than an emptied account. Do not let it read as a pass.
        print("  ! Zenodo returned no deposits for this ORCID — treating as unverifiable")
        return UNVERIFIABLE

    print(f"  {len(deposits)} public deposits on record")
    failures = check(page, deposits) + check_assets(page, local)

    if failures:
        print(f"\nDRIFT — {len(failures)} problem(s):")
        for f in failures:
            print("   ", f)
        return DRIFT

    print("  all deposits listed, count agrees, no stray DOIs, assets resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
