# BlogReach Guest Post Suggester

Input a niche, get 10 guest-post topic ideas. Built for BlogReach (guest-posting
marketplace) so outreach writers never start from a blank page.

## How it works

1. **Template engine** (`suggester.py`): 25 proven headline templates, each tagged
   with an angle (guide, mistakes, tools, trends, myths, case-study, and so on).
   The niche is slotted into the template, so every run covers diverse angles
   instead of 10 variations of the same headline.
2. **Near-duplicate removal**: after generation, every idea is compared against
   the ones already kept using word-set Jaccard similarity plus a sequence
   ratio. Anything at or above 0.62 similarity is dropped.
3. **Smart casing**: small words stay lowercase, common acronyms render correctly
   (SaaS, AI, SEO), and "A/An" is chosen by the niche's first letter.

## Usage

```bash
python suggester.py "personal finance"
python suggester.py --niche "saas marketing" --count 10
```

No API keys, no secrets, no network calls. Python 3 standard library only.

## Files

- `suggester.py` - the tool
- `REVIEW.md` - quality review of the output for 10 niches, with weak results noted
- `RUNBOOK.md` - how to run, extend, and troubleshoot

## Example output

```
Guest post ideas for: personal finance

 1. Personal Finance Automation: What to Automate and What to Keep Manual
 2. 7 Personal Finance Resources Worth Bookmarking in 2026
 3. Personal Finance Ethics: Where to Draw the Line
 4. How to Recover When Personal Finance Goes Wrong
 5. A Step-by-Step Personal Finance Plan for Your First 90 Days
 6. The Personal Finance Checklist: 7 Things to Do Before You Start
 7. Personal Finance vs. the Alternatives: An Honest Comparison
 8. Case Study: What Happens When You Take Personal Finance Seriously for 6 Months
 9. The Psychology Behind Good Personal Finance Decisions
10. The Hidden Costs of Personal Finance Nobody Talks About
```
