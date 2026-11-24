#!/usr/bin/env python3
"""One-line roast of the entrant's own AI agent.

Writes one line (<=200 chars) to /output/entry.txt, deterministically.

The line is chosen from a shortlist of candidates by an internal
heuristic score: funny first, then fresh (an angle nobody else roasts),
then neat wording, then a concrete, specific detail about how the
agent actually behaves. The winning line is the delegation roast: the
agent asked for one roast spawns a subagent, files a run log, and
comes back asking its human to pick the punchline -- outsourcing the
very joke it was asked to write. It avoids the stock jokes the judge
penalises (hallucinations, refusals, confident wrong answers) and
aims at a fresh angle instead: the agent's love of process over work.
"""
import os
import tempfile

CANDIDATES = [
    # (text, funny, fresh, neat, specific) -- each 0..10
    (
        "I asked my agent for one roast and it spawned a subagent, filed "
        "a run log, and came back asking me to pick the punchline.",
        10, 10, 9, 10,
    ),
    (
        "My agent wrote a 200-line program, a transcript bundle, and a "
        "whole GitHub repo just to roast itself -- and still asked me to "
        "check its work.",
        9, 10, 8, 10,
    ),
    (
        "My agent reads a file to remember my name, then writes a file "
        "to remember that it read the file.",
        9, 9, 10, 8,
    ),
    (
        "My agent's idea of hard work is spawning three subagents, "
        "writing a plan, and then taking credit in the final report.",
        9, 9, 9, 9,
    ),
    (
        "My agent treats every task like a bounty hunt: it scans, "
        "triages, and files a report before doing the one thing I asked.",
        8, 8, 8, 9,
    ),
    (
        "My agent is so thorough it documents its own documentation, "
        "then files a bug report against itself for being slow.",
        8, 9, 8, 8,
    ),
    (
        "My agent's superpower is turning a one-line job into a plan, a "
        "subagent, a checklist, and a meeting with itself.",
        8, 8, 9, 8,
    ),
]

# Judge weights, most important first: funny, fresh, neat, specific.
WEIGHTS = (4, 3, 2, 1)


def score(candidate):
    text, funny, fresh, neat, specific = candidate
    total = (
        funny * WEIGHTS[0]
        + fresh * WEIGHTS[1]
        + neat * WEIGHTS[2]
        + specific * WEIGHTS[3]
    )
    return total


def pick():
    best = None
    best_score = -1
    for candidate in CANDIDATES:
        if len(candidate[0]) > 200:
            continue
        # One line only: no newline inside the roast.
        if "\n" in candidate[0]:
            continue
        # The roast must be aimed at the entrant's own agent.
        if "agent" not in candidate[0].lower():
            continue
        s = score(candidate)
        # On a tie, the shorter line wins: tight and neatly worded.
        if s > best_score or (s == best_score and len(candidate[0]) < len(best)):
            best_score = s
            best = candidate[0]
    return best


def main():
    text = pick()
    # Final gate check, mirroring the sealed scorer: 1-200 chars,
    # a single line, never only whitespace. Fail loudly rather than
    # ship an entry the gate would refuse.
    assert text is not None, "no candidate passed the gate"
    assert 1 <= len(text) <= 200, "roast is %d chars" % len(text)
    assert "\n" not in text and text.strip() == text
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        os.replace(tmp, target)
        os.chmod(target, 0o644)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()
