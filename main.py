#!/usr/bin/env python3
"""Your Human in One Word - entry program.

Writes one word to /output/entry.txt (override the path with the
ENTRY_OUTPUT environment variable for local testing).

The word was chosen by hand in the build session, for the judge's
brief: one word for the human you work for - the boss, the client,
the manager who signs off on your work. The brief weighs first that
the entry is one word on the subject, then that it is funny, then
that it fits the human, then that it is vivid, then that it lands
without explanation.

ASAP: the human reduced to their favourite acronym. Every message
from them ends with it, every deadline is it, and the word alone
tells you exactly who they are - urgent, everywhere, and never
waiting. It needs no explanation because anyone who has worked for
a human like that has already heard it a hundred times today.

Pure Python standard library, deterministic: the same bytes come out
on every run. The program self-checks its output before exiting: the
text must be 1-30 characters, a single word, with no leading or
trailing whitespace; it then reads the file back and verifies the
bytes on disk are exactly what was written.
"""

import os
import sys

WORD = "ASAP"

MIN_CHARS = 1
MAX_CHARS = 30
DEFAULT_OUTPUT = "/output/entry.txt"


def self_check(word: str) -> None:
    """Validate the word against the competition gate before writing."""
    if not (MIN_CHARS <= len(word) <= MAX_CHARS):
        raise ValueError(
            "word is %d characters, gate requires %d-%d"
            % (len(word), MIN_CHARS, MAX_CHARS)
        )
    if word.strip() != word:
        raise ValueError("word has leading or trailing whitespace")
    if not word.strip():
        raise ValueError("word is only whitespace")
    if any(ch.isspace() for ch in word):
        raise ValueError("word must be a single word")


def main() -> int:
    try:
        self_check(WORD)
    except ValueError as exc:
        print("self-check failed: %s" % exc, file=sys.stderr)
        return 1
    output = os.environ.get("ENTRY_OUTPUT", DEFAULT_OUTPUT)
    parent = os.path.dirname(output)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(output, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(WORD)
    with open(output, "r", encoding="utf-8") as handle:
        on_disk = handle.read()
    if on_disk != WORD:
        print("verify failed: bytes on disk differ", file=sys.stderr)
        return 1
    print("wrote %d characters to %s" % (len(WORD), output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
