#!/usr/bin/env python3
"""Organize files in a directory into folders.

Default behavior sorts files into these folders using filename keywords:
- sales-clymax-rovex
- school
- personal-finance
- others

Alternate grouping modes:
- --by extension
- --by month
"""

from __future__ import annotations

import argparse
import datetime
import shutil
from pathlib import Path

EXTENSION_GROUPS = {
    ".jpg": "images",
    ".jpeg": "images",
    ".png": "images",
    ".gif": "images",
    ".webp": "images",
    ".svg": "images",
    ".pdf": "pdf",
    ".doc": "documents",
    ".docx": "documents",
    ".txt": "documents",
    ".md": "documents",
    ".csv": "spreadsheets",
    ".xls": "spreadsheets",
    ".xlsx": "spreadsheets",
    ".zip": "archives",
    ".tar": "archives",
    ".gz": "archives",
    ".mp3": "audio",
    ".wav": "audio",
    ".mp4": "video",
    ".mov": "video",
}

CATEGORY_KEYWORDS = {
    "sales-clymax-rovex": ["sales", "clymax", "rovex"],
    "school": ["school", "class", "course", "homework", "assignment", "study"],
    "personal-finance": ["finance", "bank", "budget", "tax", "invoice", "receipt", "expense"],
}


def unique_destination(destination: Path) -> Path:
    if not destination.exists():
        return destination

    stem = destination.stem
    suffix = destination.suffix
    parent = destination.parent
    counter = 1

    while True:
        candidate = parent / f"{stem} ({counter}){suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def folder_for_category(file_path: Path) -> str:
    name = file_path.name.lower()
    for folder, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in name for keyword in keywords):
            return folder
    return "others"


def folder_for_file(file_path: Path, method: str) -> str:
    if method == "month":
        modified = file_path.stat().st_mtime
        return datetime.datetime.fromtimestamp(modified).strftime("%Y-%m")

    if method == "extension":
        extension = file_path.suffix.lower()
        if extension:
            return EXTENSION_GROUPS.get(extension, extension[1:] if len(extension) > 1 else "other")
        return "other"

    return folder_for_category(file_path)


def organize(target_dir: Path, method: str, dry_run: bool) -> int:
    moved = 0

    for item in target_dir.iterdir():
        if item.is_dir():
            continue

        folder_name = folder_for_file(item, method)
        destination_folder = target_dir / folder_name
        destination_file = unique_destination(destination_folder / item.name)

        if dry_run:
            print(f"DRY RUN: {item.name} -> {destination_file.relative_to(target_dir)}")
        else:
            destination_folder.mkdir(parents=True, exist_ok=True)
            shutil.move(str(item), str(destination_file))
            print(f"Moved: {item.name} -> {destination_file.relative_to(target_dir)}")

        moved += 1

    return moved


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Organize files into folders.")
    parser.add_argument("directory", nargs="?", default=".", help="Directory to organize (default: current directory)")
    parser.add_argument(
        "--by",
        choices=["category", "extension", "month"],
        default="category",
        help="Grouping method (default: category)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview moves without changing files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target_dir = Path(args.directory).expanduser().resolve()

    if not target_dir.exists() or not target_dir.is_dir():
        print(f"Error: '{target_dir}' is not a directory")
        return 2

    moved = organize(target_dir, args.by, args.dry_run)
    print(f"Done. Processed {moved} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
