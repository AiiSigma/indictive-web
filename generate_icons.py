from PIL import Image
import os
import sys

# Simple icon generator for Android mipmap folders.
# Usage:
#  - Ensure source image is available (default: icon.png at repo root)
#  - Optionally set ICON_SOURCE and OUT_DIR environment variables in workflow
# Example in workflow step:
# ICON_SOURCE=assets/my_icon.png OUT_DIR=android/app/src/main/res python3 generate_icons.py

SOURCE = os.environ.get("ICON_SOURCE", "icon.png")
OUT_DIR = os.environ.get("OUT_DIR", "android/app/src/main/res")

SIZES = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}

ICONS = ["ic_launcher.png", "ic_launcher_round.png"]


def fail(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)


def main():
    if not os.path.exists(SOURCE):
        fail(f"Source file not found: {SOURCE}")
    try:
        img = Image.open(SOURCE).convert("RGBA")
    except Exception as e:
        fail(f"Failed to open source image: {e}")

    for folder, size in SIZES.items():
        d = os.path.join(OUT_DIR, folder)
        os.makedirs(d, exist_ok=True)
        for icon_name in ICONS:
            out_path = os.path.join(d, icon_name)
            resized = img.resize((size, size), Image.LANCZOS)
            # Save as PNG
            try:
                resized.save(out_path, optimize=True)
                print(f"Wrote {out_path}")
            except Exception as e:
                fail(f"Failed to write {out_path}: {e}")

    print("Icons generated successfully.")


if __name__ == "__main__":
    main()
