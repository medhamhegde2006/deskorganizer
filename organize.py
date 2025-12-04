#!/usr/bin/env python3
"""
deskorganizer - move files in a folder into subfolders by type.

Usage examples:
  python organize.py --path "/home/medha/Downloads" --dry
  python organize.py --path "C:\\Users\\Medha\\Desktop" --run
"""

import os
import shutil
import argparse
from pathlib import Path
import json
from datetime import datetime

# Mapping of folder name -> list of extensions (lowercase, without dot)
CATEGORIES = {
    "Images": ["jpg","jpeg","png","gif","bmp","webp","svg","heic"],
    "Documents": ["pdf","doc","docx","xls","xlsx","ppt","pptx","txt","odt","ods"],
    "Videos": ["mp4","mkv","mov","avi","flv","webm"],
    "Audio": ["mp3","wav","aac","flac","m4a"],
    "Archives": ["zip","rar","tar","gz","7z","bz2"],
    "Code": ["py","js","java","c","cpp","cs","html","css","json","yaml","yml","kt","rs"],
    "Installers": ["exe","msi","deb","rpm","pkg"],
}

LOG_FILE = "deskorganizer_log.json"

def detect_category(ext: str) -> str:
    ext = ext.lower().lstrip(".")
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Others"

def safe_move(src_path: Path, dest_dir: Path) -> str:
    """
    Move src_path into dest_dir. If a file with same name exists,
    append a counter: name (1).ext, name (2).ext, ...
    Returns the final filename under dest_dir.
    """
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src_path.name
    if not dest.exists():
        shutil.move(str(src_path), str(dest))
        return dest.name

    stem = src_path.stem
    suffix = src_path.suffix
    counter = 1
    while True:
        new_name = f"{stem} ({counter}){suffix}"
        new_dest = dest_dir / new_name
        if not new_dest.exists():
            shutil.move(str(src_path), str(new_dest))
            return new_dest.name
        counter += 1

def organize(folder: Path, dry_run: bool = False):
    folder = folder.resolve()
    if not folder.is_dir():
        raise ValueError(f"{folder} is not a directory")
    log = {"timestamp": datetime.utcnow().isoformat()+"Z", "source": str(folder), "moves": []}
    for item in folder.iterdir():
        # skip directories (we don't move folders)
        if item.is_dir():
            continue
        ext = item.suffix.lstrip(".")
        category = detect_category(ext)
        dest_dir = folder / category
        if dry_run:
            # show preview only
            log["moves"].append({"from": str(item), "to": str(dest_dir / item.name), "action": "dry"})
            print(f"[DRY] {item.name} -> {category}/")
        else:
            new_name = safe_move(item, dest_dir)
            log["moves"].append({"from": str(item), "to": str(dest_dir / new_name), "action": "moved"})
            print(f"MOVED: {item.name} -> {category}/{new_name}")
    # write log
    with open(folder / LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)
    print("Log written to", folder / LOG_FILE)

def main():
    parser = argparse.ArgumentParser(description="Organize a folder by file types.")
    parser.add_argument("--path", required=True, help="Target folder path")
    parser.add_argument("--dry", action="store_true", help="Dry run (no files moved)")
    parser.add_argument("--run", action="store_true", help="Actually move files")
    args = parser.parse_args()
    if not args.dry and not args.run:
        print("You must pass --dry or --run. Use --dry to preview, --run to move files.")
        return
    # If both provided, prefer --run
    dry_run = args.dry and not args.run
    target = Path(args.path)
    organize(target, dry_run=dry_run)

if __name__ == "__main__":
    main()
