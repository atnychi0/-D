"""Utility for deduplicating image files and optionally performing OCR.

This script replicates the exploratory Python session captured in the
conversation history while providing better error handling and optional OCR
support.  If the ``pytesseract`` package is not available the script will
gracefully skip the OCR step and explain how to enable it.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.util
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


def _load_optional_pytesseract():
    """Return the ``pytesseract`` module if it is installed, otherwise ``None``."""

    spec = importlib.util.find_spec("pytesseract")
    if spec is None:
        return None
    return importlib.import_module("pytesseract")


PYTESSERACT = _load_optional_pytesseract()


def _load_optional_image_module():
    """Return the ``PIL.Image`` module if pillow is installed."""

    spec = importlib.util.find_spec("PIL")
    if spec is None:
        return None
    return importlib.import_module("PIL.Image")


PIL_IMAGE = _load_optional_image_module()


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Deduplicate image files by hash and optionally perform OCR on the "
            "unique files.  If no paths are supplied the script looks for "
            "files matching 'input_file_*.jpeg' in the current working "
            "directory."
        )
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help=(
            "File or directory paths to inspect.  Directories are searched "
            "recursively for JPEG files."
        ),
    )
    parser.add_argument(
        "--pattern",
        default="input_file_*.jpeg",
        help=(
            "Glob pattern used when scanning directories or when no paths "
            "are provided."
        ),
    )
    parser.add_argument(
        "--no-ocr",
        action="store_true",
        help="Skip OCR even if pytesseract is installed.",
    )
    return parser.parse_args(argv)


def gather_files(paths: Iterable[Path], pattern: str) -> List[Path]:
    """Return a sorted list of file paths based on the provided inputs."""

    collected: List[Path] = []

    def add_path(path: Path) -> None:
        if path.is_file():
            collected.append(path)
        elif path.is_dir():
            for nested in sorted(path.rglob(pattern)):
                if nested.is_file():
                    collected.append(nested)
        else:
            raise FileNotFoundError(f"Path does not exist: {path}")

    raw_paths = list(paths)
    if not raw_paths:
        raw_paths = sorted(Path.cwd().glob(pattern))

    for raw_path in raw_paths:
        add_path(raw_path)

    return collected


def deduplicate(files: Iterable[Path]) -> List[Path]:
    """Return a list of files with duplicate content removed."""

    seen_hashes: Dict[str, Path] = {}
    unique_files: List[Path] = []

    for file_path in files:
        with file_path.open("rb") as fh:
            digest = hashlib.md5(fh.read()).hexdigest()

        if digest not in seen_hashes:
            seen_hashes[digest] = file_path
            unique_files.append(file_path)

    return unique_files


def perform_ocr(files: Iterable[Path]) -> Dict[Path, str]:
    """Extract text from images using pytesseract when available."""

    if PYTESSERACT is None or PIL_IMAGE is None:
        raise RuntimeError(
            "OCR requires both pillow and pytesseract to be installed."
        )

    extracted: Dict[Path, str] = {}
    for file_path in files:
        text = PYTESSERACT.image_to_string(PIL_IMAGE.open(file_path))
        extracted[file_path] = text
    return extracted


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)

    try:
        all_files = gather_files(args.paths, args.pattern)
    except FileNotFoundError as exc:
        print(exc)
        return 1

    if not all_files:
        print("No files matched the provided arguments.")
        return 1

    unique_files = deduplicate(all_files)

    print("Unique files identified:")
    for index, file_path in enumerate(unique_files, start=1):
        print(f"{index}. {file_path}")

    if args.no_ocr:
        return 0

    if PYTESSERACT is None or PIL_IMAGE is None:
        print(
            "\nOCR skipped because pillow and/or pytesseract are not installed. "
            "Install pillow, pytesseract, and the Tesseract binary to enable "
            "text extraction."
        )
        return 0

    print("\nPerforming OCR on unique files...")
    extracted_text = perform_ocr(unique_files)

    for file_path, text in extracted_text.items():
        separator = "-" * 10
        print(f"\n{separator} Extracted text from {file_path} {separator}\n{text}\n{separator} End of text from {file_path} {separator}")

    print("\nCombined extracted text:\n")
    print("\n\n".join(extracted_text.values()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
