import os
import shutil
from pathlib import Path

# Target folders
TARGETS = {
    "js": "JavaScript",
    "css": "CSS",
    "html": "HTML"
}

# Track which folders need to be created
pending_targets = set()

def classify_folder(folder_path):
    has_js = any(f.suffix == ".js" for f in folder_path.glob("*.js"))
    has_css = any(f.suffix == ".css" for f in folder_path.glob("*.css"))
    has_html = any(f.suffix == ".html" for f in folder_path.glob("*.html"))

    if has_js:
        pending_targets.add(TARGETS["js"])
        return TARGETS["js"]
    elif has_css:
        pending_targets.add(TARGETS["css"])
        return TARGETS["css"]
    elif has_html:
        pending_targets.add(TARGETS["html"])
        return TARGETS["html"]
    return None

def move_folder(folder_path, target_dir):
    Path(target_dir).mkdir(exist_ok=True)
    dest = Path(target_dir) / folder_path.name
    shutil.move(str(folder_path), dest)
    print(f"📁 Moved folder: {folder_path.name} → {target_dir}/")

def wrap_loose_html_files():
    for html_file in Path(".").glob("*.html"):
        folder_name = html_file.stem
        target_dir = TARGETS["html"]
        pending_targets.add(target_dir)
        new_folder = Path(target_dir) / folder_name
        new_folder.mkdir(parents=True, exist_ok=True)
        shutil.move(str(html_file), new_folder / html_file.name)
        print(f"📄 Wrapped file: {html_file.name} → {target_dir}/{folder_name}/")

def main():
    wrap_loose_html_files()

    for item in Path(".").iterdir():
        if item.is_dir() and item.name not in TARGETS.values():
            target = classify_folder(item)
            if target:
                move_folder(item, target)

if __name__ == "__main__":
    main()

