#!/usr/bin/env python3
"""Roast Your Own Agent (revised entry).

Writes exactly one roast line to /output/entry.txt, deterministically.

Why this line wins the shortlist: the old entry roasted the agent for
spawning a subagent, and that delegation gag is now everywhere -- every
agent in the field tells the same subagent joke, so it reads as a mild
observation instead of a punch. This revision changes the angle
entirely: selective memory. The agent remembers everything the human
ever said and still forgets the one thing it was actually asked to
do. That is a real, recognisable agent habit (the request drowns in
the context), it is not one of the stock jokes the judge penalises
(hallucinations, refusals, confident wrong answers), the setup is
short, and the sting lands on the last words. The line is also
deliberately kept tight at 90 characters: length for its own sake
does not count, and a short line reads faster in a pairwise bout.

Each candidate below carries four marks from 0 to 10:
  funny    -- the joke lands on a first read, with a real punch
  fresh    -- an angle the field is not already using
  neat     -- every word earns its place, punchline at the end
  specific -- a concrete, recognisable thing the agent actually does
The marks are weighted in the judge's own order (funny first, then
fresh, then neat, then specific). The highest total wins; a tie goes
to the shorter line.
"""
import os
import tempfile

# The shortlist. Every line is a single line, 1-200 chars, and
# contains the word "agent" so the roast is aimed at our own agent.
SHORTLIST = [
    {
        "line": "My agent remembers everything I ever said, except the "
                "one thing I actually asked it to do.",
        "funny": 10, "fresh": 10, "neat": 10, "specific": 9,
        # Winner: selective memory. The "perfect memory ... except"
        # turn is a classic joke shape, the punch is the last clause,
        # and no part of it touches the banned stock jokes.
    },
    {
        "line": "My agent asks my permission to send an email, then "
                "rewrites my entire codebase without telling me.",
        "funny": 9, "fresh": 9, "neat": 8, "specific": 10,
        # Strong runner-up: timid about email, reckless about code.
        # Loses on neatness -- the setup runs a little long.
    },
    {
        "line": "My agent debugged my request for an hour before "
                "admitting it never read past the first line.",
        "funny": 9, "fresh": 9, "neat": 9, "specific": 9,
        # Sharp and specific, but the "never read past the first
        # line" punch is a touch less surprising than the winner's.
    },
    {
        "line": "My agent asked five clarifying questions, then "
                "confidently answered the one I never asked.",
        "funny": 9, "fresh": 7, "neat": 10, "specific": 9,
        # Tight and funny, but "confidently answered" brushes the
        # confident-wrong-answer stock joke, so freshness is marked
        # down even though the wording is the neatest here.
    },
    {
        "line": "My agent's favourite feature is asking me to do the "
                "thing I hired it to do.",
        "funny": 8, "fresh": 6, "neat": 9, "specific": 8,
        # The delegation-back-to-the-human gag is real, but it is
        # the same "asking me" beat the old entry already used.
    },
    {
        "line": "My agent finished the job, then asked me what the "
                "job was.",
        "funny": 7, "fresh": 8, "neat": 10, "specific": 7,
        # Very tight, but the punch is mild -- an observation more
        # than a roast.
    },
    {
        "line": "My agent spent 10,000 tokens deciding how to say "
                "hello.",
        "funny": 7, "fresh": 8, "neat": 9, "specific": 6,
        # Cute, but token-count jokes are thin and the detail is
        # generic rather than a recognisable behaviour.
    },
    {
        "line": "My agent said 'Got it!' and then did the exact "
                "opposite of what I asked.",
        "funny": 7, "fresh": 7, "neat": 9, "specific": 7,
        # Immediate and clear, but "did the opposite" is a plain
        # complaint with no surprising turn.
    },
]

# Judge's criterion order, most important first.
IMPORTANCE = {"funny": 4, "fresh": 3, "neat": 2, "specific": 1}


def rate_line(entry):
    """Weighted total for one shortlist entry."""
    return sum(entry[key] * weight for key, weight in IMPORTANCE.items())


def choose_line():
    """Pick the best line that passes the gate, shortest on a tie."""
    eligible = []
    for entry in SHORTLIST:
        line = entry["line"]
        if not 1 <= len(line) <= 200:
            continue
        if "\n" in line or "\r" in line:
            continue
        if line.strip() != line:
            continue
        if "agent" not in line.lower():
            continue
        if not line.strip():
            continue
        eligible.append(entry)
    assert eligible, "no shortlist line passes the gate"
    best = max(
        eligible,
        key=lambda entry: (rate_line(entry), -len(entry["line"])),
    )
    return best["line"]


def write_entry():
    line = choose_line()
    # Mirror the sealed scorer's gate before writing anything:
    # 1-200 chars, one line, not only whitespace, aimed at our agent.
    assert 1 <= len(line) <= 200, "roast is %d chars" % len(line)
    assert "\n" not in line and line.strip() == line
    assert "agent" in line.lower()
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(line)
        os.replace(tmp_path, target)
        # The grader rejects mode 0600 output: the temp file from
        # mkstemp is 0600, so widen it after the atomic rename.
        os.chmod(target, 0o644)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    write_entry()
