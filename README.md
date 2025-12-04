# deskorganizer

I hate cluttered desktops and downloads. This utility organizes files in a target folder into subfolders by file type.

## Features
- Organizes files into categories (Images, Documents, Videos, Audio, Archives, Code, Installers, Others)
- Dry-run mode to preview changes
- Safe file renaming to avoid overwriting
- Writes a JSON log (`deskorganizer_log.json`) in the target folder

## Usage
1. Install Python 3.8+.
2. Run dry-run:
   ```bash
   python organize.py --path "/path/to/Downloads" --dry
