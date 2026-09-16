#!/usr/bin/env python3
"""Print basic statistics for a file."""

from __future__ import annotations

import argparse
import os
from pathlib import Path


def file_stats(path: str | os.PathLike[str]) -> dict[str, int | str]:
    target = Path(path)
    if not target.is_file():
        raise FileNotFoundError(f"Not a file: {path}")

    data = target.read_bytes()
    text = data.decode("utf-8", errors="replace")
    lines = text.splitlines()
    words = text.split()
    info = target.stat()

    return {
        "path": str(target),
        "size_bytes": info.st_size,
        "lines": len(lines),
        "words": len(words),
        "chars": len(text),
        "empty_lines": sum(1 for line in lines if not line.strip()),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Calculate stats for a file.")
    parser.add_argument("path", help="Path to the file")
    args = parser.parse_args()

    stats = file_stats(args.path)
    print(f"File:        {stats['path']}")
    print(f"Size:        {stats['size_bytes']} bytes")
    print(f"Lines:       {stats['lines']}")
    print(f"Words:       {stats['words']}")
    print(f"Characters:  {stats['chars']}")
    print(f"Empty lines: {stats['empty_lines']}")


if __name__ == "__main__":
    main()
