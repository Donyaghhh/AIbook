#!/usr/bin/env python3
"""Collect basic statistics for a file."""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FileStats:
    path: str
    size_bytes: int
    lines: int
    words: int
    chars: int
    empty_lines: int


def collect_stats(path: str | os.PathLike[str]) -> FileStats:
    target = Path(path)
    if not target.is_file():
        raise FileNotFoundError(f"Not a file: {path}")

    text = target.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    return FileStats(
        path=str(target),
        size_bytes=target.stat().st_size,
        lines=len(lines),
        words=len(text.split()),
        chars=len(text),
        empty_lines=sum(1 for line in lines if not line.strip()),
    )


def format_stats(stats: FileStats) -> str:
    return "\n".join(
        [
            f"File:        {stats.path}",
            f"Size:        {stats.size_bytes} bytes",
            f"Lines:       {stats.lines}",
            f"Words:       {stats.words}",
            f"Characters:  {stats.chars}",
            f"Empty lines: {stats.empty_lines}",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect stats for a file.")
    parser.add_argument("path", help="Path to the file")
    args = parser.parse_args()
    stats = collect_stats(args.path)
    print(format_stats(stats))


if __name__ == "__main__":
    main()
