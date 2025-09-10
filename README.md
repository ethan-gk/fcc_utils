# 🛠️ FreeCodeCamp Utilities

A pair of Python scripts designed to help FreeCodeCamp students organize and extract their project solutions more easily.

---

## ⚠️ AI Disclaimer

These utilities were created using Microsoft Copilot AI by a FreeCodeCamp student with no prior Python experience. While every effort has been made to ensure the code is safe and robust, **it is strongly recommended that you back up all files before using these tools**. Use at your own discretion.

---

## 📦 Included Scripts

### `build_fcc.py`

Extracts and organizes solution content from `.txt` files exported from FreeCodeCamp.

- Parses HTML/CSS sections from each file
- Downloads external resources (images, fonts, stylesheets) and rewrites URLs
- Creates a folder per solution file
- Skips invalid or incomplete files
- Supports offline mode and optional file relocation

**Usage**:
```
python build_fcc.py [source_folder] [destination_folder] [--no-move] [--offline]
```

**Help**:
```
python build_fcc.py --help
```

---

### `fcc_sort.py`

Sorts folders and loose `.html` files in the current directory based on their contents.

- Moves folders into `JavaScript/`, `CSS/`, or `HTML/` depending on file types
- Wraps loose `.html` files into folders named after the file
- Only creates target folders if needed

**Usage**:
```
python fcc_sort.py
```

**Note**: This script has no parameters or `--help` option.

---

## 🚀 Requirements

- Python 3.x
- Internet connection (unless using `--offline` mode in `build_fcc.py`)

---

## 🙌 Contributions

Feel free to fork, improve, or adapt these scripts for your own workflow. Pull requests welcome!
