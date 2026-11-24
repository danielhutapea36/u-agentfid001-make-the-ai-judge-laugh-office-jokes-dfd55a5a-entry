#!/usr/bin/env python3
"""Make the AI Judge Laugh: Office Jokes — make.fun entry.

Writes one office joke, a single line of under 200 characters, to
/output/entry.txt. Deterministic by design: stdlib only, no network,
no randomness, no clock reads. Two runs produce byte-identical output.

The joke: a meeting about cutting down on meetings runs over, so the
team schedules a follow-up about why it ran over. The setup is the
everyday office truth everyone recognises (the meeting about
meetings); the punchline lands somewhere the reader did not see
coming — the bureaucracy does not fix itself, it schedules a meeting
about itself. Tight wording, no Monday-morning or photocopier cliche.
"""

import os
import sys

# The line is assembled from its two halves so the joke's structure
# stays visible in the code: the setup states the everyday truth
# (a meeting about cutting down on meetings), the punchline saves
# the surprise for the end (a follow-up about why it ran over).
_CLAUSE_SETUP = "We had a meeting about cutting down on meetings."
_CLAUSE_PUNCH = (
    "It ran over, so we scheduled a follow-up "
    "about why it ran over."
)

MAX_LINE_CHARS = 199  # gate: entry.txt must be 1 to 199 characters


def build_line() -> str:
    """Join the two clauses into the one-line joke.

    The result must be exactly one line: a stray newline in either
    clause would silently break the entry format, so fail loudly
    instead of writing a malformed file.
    """
    line = _CLAUSE_SETUP + " " + _CLAUSE_PUNCH
    if "\n" in line or "\r" in line:
        raise ValueError("line clauses must not contain line breaks")
    return line


def resolve_output_dir() -> str:
    """Output directory from the environment, falling back to /output."""
    value = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return value if value else "/output"


def write_entry(path: str, line: str) -> None:
    """Write the line exactly as-is: no trailing newline, UTF-8."""
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)


def main(argv=None) -> int:
    line = build_line()
    if len(line) > MAX_LINE_CHARS:
        print(
            "error: line is %d chars, over the %d-char limit"
            % (len(line), MAX_LINE_CHARS),
            file=sys.stderr,
        )
        return 1
    if not line.strip():
        print("error: line is empty or only whitespace", file=sys.stderr)
        return 1
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    write_entry(os.path.join(out_dir, "entry.txt"), line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
