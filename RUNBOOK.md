# Runbook: BlogReach Guest Post Suggester

## Run it

```bash
python suggester.py "your niche"
python suggester.py --niche "your niche" --count 10 --year 2026
```

Requirements: Python 3.9+. No dependencies, no API keys, no secrets.

## How generation works

- `TEMPLATES` in `suggester.py` holds 25 headline patterns, each tagged with an
  angle. Generation picks one idea per angle first (diversity), then fills any
  remaining slots from the leftover templates.
- Output is deterministic per niche (seeded), so the same niche always returns
  the same list. Change the `--seed` behavior in code if you need variety.

## How near-duplicate removal works

- `similarity()` combines word-set Jaccard overlap with a difflib sequence
  ratio and takes the max.
- `dedupe()` keeps an idea only if it is below 0.62 similarity against every
  idea already kept.
- To make dedupe stricter, lower the threshold in `dedupe()`; to allow closer
  variations, raise it. Below ~0.5 it starts dropping legitimately different
  ideas that share the niche phrase.

## Extending it

- **Add templates**: append a `(pattern, angle)` pair to `TEMPLATES`. Patterns
  support `{Niche}`, `{niche}`, `{year}`, `{num}`, and `{article}` (A/An).
- **Add acronyms**: extend the `ACRONYMS` map so new niches render correctly.
- **AI mode (optional)**: the template engine needs no keys. If richer,
  niche-specific ideas are wanted later, an LLM call can replace `suggest()`
  while keeping `dedupe()` unchanged. Any API key must come from an environment
  variable, never committed to the repo.

## Troubleshooting

- Output looks repetitive across niches: expected for a template engine; the
  angles repeat, the niches change. See REVIEW.md for the honest assessment.
- A niche name renders with wrong casing: add it to `ACRONYMS` or adjust
  `SMALL_WORDS`.
