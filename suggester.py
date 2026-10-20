#!/usr/bin/env python3
"""BlogReach Guest Post Suggester.

Input a niche, get 10 guest-post topic ideas built from proven templates
combined with niche-specific angles, then near-duplicates are removed.

Usage:
    python suggester.py "personal finance"
    python suggester.py --niche "saas marketing" --count 10
"""
import argparse
import random
import re
from difflib import SequenceMatcher

# ---------------------------------------------------------------------------
# Template bank: each template is (pattern, angle_tag). Patterns contain
# {niche} and optionally {Niche} (title case), {year}, {num}.
# The angle_tag keeps selection diverse: one idea per angle wins first.
# ---------------------------------------------------------------------------
TEMPLATES = [
    ("The Beginner's Guide to {Niche} in {year}", "guide"),
    ("{num} {Niche} Mistakes Every Beginner Makes", "mistakes"),
    ("How to Choose the Right {Niche} Tools Without Wasting Money", "tools"),
    ("{Niche}: What Actually Works in {year} (Tested)", "tested"),
    ("The Hidden Costs of {Niche} Nobody Talks About", "costs"),
    ("How {Niche} Is Changing: {num} Trends to Watch", "trends"),
    ("{num} {Niche} Myths That Need to Die", "myths"),
    ("A Step-by-Step {Niche} Plan for Your First 90 Days", "plan"),
    ("{Niche} on a Budget: Maximum Results, Minimum Spend", "budget"),
    ("Case Study: What Happens When You Take {Niche} Seriously for 6 Months", "case-study"),
    ("The {Niche} Checklist: {num} Things to Do Before You Start", "checklist"),
    ("Why Most People Fail at {Niche} (And How to Be the Exception)", "failure"),
    ("{Niche} for Busy People: A Realistic Weekly Routine", "routine"),
    ("{num} Advanced {Niche} Tactics the Pros Don't Share", "advanced"),
    ("The Complete {Niche} FAQ: {num} Questions Answered", "faq"),
    ("{Niche} vs. the Alternatives: An Honest Comparison", "comparison"),
    ("How to Measure Success in {Niche} (Metrics That Matter)", "metrics"),
    ("{Niche} Ethics: Where to Draw the Line", "ethics"),
    ("From Zero to Confident: {article} {Niche} Roadmap", "roadmap"),
    ("{num} {Niche} Resources Worth Bookmarking in {year}", "resources"),
    ("The Psychology Behind Good {Niche} Decisions", "psychology"),
    ("What I Wish I Knew Before Starting {Niche}", "lessons"),
    ("{Niche} Automation: What to Automate and What to Keep Manual", "automation"),
    ("How to Recover When {Niche} Goes Wrong", "recovery"),
    ("The {Niche} Starter Kit: Everything You Need on Day One", "starter-kit"),
]

NUMBERS = [5, 7, 9, 10, 11, 12, 15]



SMALL_WORDS = {"and", "or", "of", "the", "in", "on", "for", "to", "a", "an"}
ACRONYMS = {"saas": "SaaS", "ai": "AI", "seo": "SEO", "b2b": "B2B", "diy": "DIY"}


def smart_title(text: str) -> str:
    words = text.split()
    out = []
    for i, w in enumerate(words):
        low = w.lower()
        if low in ACRONYMS:
            out.append(ACRONYMS[low])
        elif low in SMALL_WORDS and i > 0:
            out.append(low)
        else:
            out.append(w[:1].upper() + w[1:])
    return " ".join(out)


def article_for(phrase: str) -> str:
    return "An" if phrase[:1].lower() in "aeiou" else "A"

def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", text.lower())


def similarity(a: str, b: str) -> float:
    """Word-set Jaccard combined with sequence ratio."""
    wa, wb = set(normalize(a).split()), set(normalize(b).split())
    if not wa or not wb:
        return 0.0
    jaccard = len(wa & wb) / len(wa | wb)
    seq = SequenceMatcher(None, normalize(a), normalize(b)).ratio()
    return max(jaccard, seq)


def dedupe(ideas, threshold: float = 0.62):
    """Drop near-duplicates above the similarity threshold."""
    kept = []
    for idea in ideas:
        if all(similarity(idea, k) < threshold for k in kept):
            kept.append(idea)
    return kept


def fill(pattern, niche, year, rng):
    out = pattern.replace("{Niche}", smart_title(niche)).replace("{niche}", niche)
    out = out.replace("{article}", article_for(smart_title(niche)))
    out = out.replace("{year}", str(year))
    out = out.replace("{num}", str(rng.choice(NUMBERS)))
    return out


def suggest(niche: str, count: int = 10, year: int = 2026, seed: int = 42):
    """Generate `count` unique topic ideas for a niche."""
    rng = random.Random(f"{niche}-{seed}")
    pool = TEMPLATES[:]
    rng.shuffle(pool)

    # Round 1: one idea per distinct angle, in shuffled template order.
    chosen, angles = [], set()
    for pattern, angle in pool:
        if angle not in angles:
            chosen.append(fill(pattern, niche, year, rng))
            angles.add(angle)

    # Round 2: remaining templates if we still need more.
    for pattern, angle in pool:
        if len(chosen) >= count * 2:
            break
        idea = fill(pattern, niche, year, rng)
        if idea not in chosen:
            chosen.append(idea)

    unique = dedupe(chosen)
    return unique[:count]


def main():
    ap = argparse.ArgumentParser(description="BlogReach Guest Post Suggester")
    ap.add_argument("niche", nargs="?", help="The niche, e.g. 'personal finance'")
    ap.add_argument("--niche", dest="niche_kw", help="Same as positional")
    ap.add_argument("--count", type=int, default=10)
    ap.add_argument("--year", type=int, default=2026)
    args = ap.parse_args()
    niche = args.niche_kw or args.niche
    if not niche:
        ap.error("provide a niche, e.g. python suggester.py 'personal finance'")
    ideas = suggest(niche, args.count, args.year)
    print(f"Guest post ideas for: {niche}\n")
    for i, idea in enumerate(ideas, 1):
        print(f"{i:2}. {idea}")


if __name__ == "__main__":
    main()
