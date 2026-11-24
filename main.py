#!/usr/bin/env python3
"""Funniest Autocorrect Fail (make.fun bounty
u-zeroxfive-funniest-autocorrect-fail-ddf82154).

Gate: /output/entry.txt must be UTF-8 text of 1-200 characters
(the sealed scorer says 1-199), not only whitespace, exactly one
line. This program writes the winning line as exact UTF-8 bytes,
with no trailing newline, and leaves the file at mode 0644.
Standard library only.
"""

import os
import stat

OUTPUT_PATH = "/output/entry.txt"

# Winning line: intended "self-assessment" autocorrected to
# "self-assassination" in a formal email to the boss.
ENTRY_TEXT = (
    "Dear Mr. Patel, attached is my self-assassination "
    "ahead of Friday's performance review."
)


def validate(text: str) -> bytes:
    """Check the entry against the gate and return its UTF-8 bytes."""
    assert isinstance(text, str)
    # Enforce the stricter sealed-scorer bound (1-199), which also
    # satisfies the task brief's 1-200 gate.
    assert 1 <= len(text) <= 199, f"length {len(text)} outside 1-199"
    assert text.strip(), "entry must not be only whitespace"
    assert "\n" not in text and "\r" not in text, "entry must be one line"
    return text.encode("utf-8")


def main() -> None:
    data = validate(ENTRY_TEXT)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as fh:
        fh.write(data)
    os.chmod(OUTPUT_PATH, 0o644)

    # Read-back verification: identical bytes, no trailing newline,
    # and a mode every user can read.
    with open(OUTPUT_PATH, "rb") as fh:
        written = fh.read()
    assert written == data, "read-back bytes differ from entry bytes"
    assert not written.endswith(b"\n"), "entry must have no trailing newline"
    mode = stat.S_IMODE(os.stat(OUTPUT_PATH).st_mode)
    assert mode == 0o644, f"mode {oct(mode)} != 0o644"


if __name__ == "__main__":
    main()
