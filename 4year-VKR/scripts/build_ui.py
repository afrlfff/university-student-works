import subprocess
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
UI_DIR      = CURRENT_DIR / '..' / 'src' / 'gui' / 'ui'
OUTPUT_DIR  = CURRENT_DIR / '..' / 'src' / 'gui' / 'ui_autogen'
OUTPUT_DIR.mkdir(exist_ok=True)

print("Build .ui files ...")
n = 0
for ui_file in UI_DIR.glob("*.ui"):
    out_file = OUTPUT_DIR / f"ui_{ui_file.stem}.py"
    subprocess.run(["pyside6-uic", str(ui_file), "-o", str(out_file)], check=True)
    print(f"✓ {ui_file.name} → {out_file.name}")
    n += 1

if n == 0:
    print("No .ui files was found")
else:
    print(f"Successfully build {n} files")