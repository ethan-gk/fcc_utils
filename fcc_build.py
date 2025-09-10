import os
import re
import requests
import shutil
import sys
import mimetypes
from pathlib import Path

HELP_TEXT = """
📘 FreeCodeCamp Solution Builder

A simple tool to build project folders for downloaded solutions to labs completed
on freeCodeCamp.org

Usage:
  python fcc_build.py [source_folder] [destination_folder] [--no-move] [--offline]

Arguments:
  source_folder         Folder containing .txt files exported from FreeCodeCamp.
  destination_folder    Folder in which to create output folders. If omitted, uses
                        source_folder.
  --no-move             Prevents moving original *.txt files to 'Originals' folder
                        (implied unless source and destination are the same)
  --offline             Skips downloading external resources and leaves URLs unchanged.
  --help                Shows this message.
"""

def extract_sections(text):
    pattern = r"\*\* start of (.*?) \*\*(.*?)\*\* end of \1 \*\*"
    matches = re.findall(pattern, text, re.DOTALL)
    return {name.strip(): content.strip() for name, content in matches}

def get_extension_from_url_or_response(url, response):
    ext = os.path.splitext(url.split("?")[0])[1]
    if ext:
        return ext
    content_type = response.headers.get("Content-Type", "")
    guessed_ext = mimetypes.guess_extension(content_type.split(";")[0].strip())
    return guessed_ext or ".bin"

def download_resource(url, dest_folder, index):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        ext = get_extension_from_url_or_response(url, response)
        filename = f"resource-{index}{ext}"
        filepath = os.path.join(dest_folder, filename)
        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"📥 Saved resource: [{filename}] from {url}")
        return filename
    except Exception as e:
        print(f"⚠️ Failed to download {url}: {e}")
        return None

def replace_external_urls(code, folder, offline=False):
    if offline:
        return code

    patterns = {
        "css_url": r'@import\s+url\((["\']?)(https?://[^"\')]+)\1\)',
        "style_url": r'url\((["\']?)(https?://[^"\')]+)\1\)',
        "img_tag": r'<img[^>]+src=["\'](https?://[^"\']+)["\']',
        "link_tag": r'<link[^>]+href=["\'](https?://[^"\']+)["\']',
        "script_tag": r'<script[^>]+src=["\'](https?://[^"\']+)["\']',
    }

    all_urls = set()
    for pattern in patterns.values():
        matches = re.findall(pattern, code)
        urls = [url if isinstance(url, str) else url[1] for url in matches]
        all_urls.update(urls)

    for i, url in enumerate(sorted(all_urls), start=1):
        filename = download_resource(url, folder, i)
        if not filename:
            raise RuntimeError(f"Resource download failed: {url}")
        code = code.replace(url, filename)
    return code

def process_txt_file(txt_path, dest_root, offline=False):
    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read()

    sections = extract_sections(content)
    if not sections:
        print(f"⏭️ {txt_path.name} does not appear to be a freeCodeCamp solution -- skipping...")
        return "skipped"

    base_name = Path(txt_path).stem
    output_dir = Path(dest_root) / base_name
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        for name, code in sections.items():
            code = replace_external_urls(code, output_dir, offline=offline)
            with open(output_dir / name, "w", encoding="utf-8") as f:
                f.write(code)
        rel_path = os.path.relpath(output_dir, Path.cwd())
        print(f"✅ Processed: {txt_path.name} → {rel_path}")
        return "processed"
    except Exception as e:
        print(f"❌ {txt_path.name} failed due to error: {e}")
        shutil.rmtree(output_dir, ignore_errors=True)
        return "failed"

def batch_process(source_folder=None, destination_folder=None, move_originals=True, offline=False):
    script_dir = Path(__file__).parent.resolve()
    source = Path(source_folder) if source_folder else script_dir
    dest = Path(destination_folder) if destination_folder else source

    all_files = list(source.glob("*"))
    txt_files = [f for f in all_files if f.suffix.lower() == ".txt"]
    other_files = [f for f in all_files if f.suffix.lower() != ".txt"]
    
    processed = 0
    skipped = 0
    failed = 0
    originals_dir = source / "Originals"

    for other in other_files:
        print(f"🚫 Skipping unsupported file: {other.name}")
        skipped += 1

    if not txt_files:
        print(f"🚫 No *.txt files found in {source}")
        return

    for txt_file in txt_files:
        result = process_txt_file(txt_file, dest, offline=offline)
        if result == "processed":
            processed += 1
            if move_originals and source == dest:
                originals_dir.mkdir(exist_ok=True)
                shutil.move(str(txt_file), originals_dir / txt_file.name)
        elif result == "skipped":
            skipped += 1
        elif result == "failed":
            failed += 1

    print(f"\n🏁 FINISHED - {processed} Processed, {skipped} Skipped, {failed} Failed")

# Optional: command-line usage
if __name__ == "__main__":
    args = sys.argv[1:]
    if "--help" in args:
        print(HELP_TEXT)
        sys.exit(0)

    src = args[0] if len(args) >= 1 and not args[0].startswith("--") else None
    dst = args[1] if len(args) >= 2 and not args[1].startswith("--") else src
    move_flag = "--no-move" not in args
    offline_flag = "--offline" in args

    batch_process(src, dst, move_originals=move_flag, offline=offline_flag)

