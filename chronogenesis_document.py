"""Sanitized document loader for Chronogenesis manuscript."""

from __future__ import annotations

from pathlib import Path

DOCUMENT_PATH = Path(__file__).with_name("chronogenesis_document_redacted.txt")


def load_document() -> str:
    """Return the sanitized Chronogenesis manuscript as a string.

    The original submission contained sensitive authentication phrases that
    should not be redistributed.  This helper loads the redacted manuscript
    stored alongside the module.  If the file is missing a descriptive error is
    raised so the caller can handle it gracefully.
    """

    try:
        return DOCUMENT_PATH.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            "The redacted Chronogenesis manuscript is not available."
        ) from exc


if __name__ == "__main__":
    print(load_document())
