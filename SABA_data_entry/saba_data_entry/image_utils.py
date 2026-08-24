from pathlib import Path
import tkinter as tk

IMAGE_DIR = Path(__file__).resolve().parent / "images"


def load_png(filename):

    image_path = IMAGE_DIR / filename

    if not image_path.exists():
        print(f"PNG image not found: {image_path}")
        return None

    try:
        return tk.PhotoImage(file=str(image_path))

    except tk.TclError as error:
        print(f"Could not load PNG image '{filename}': {error}")
        return None


def load_xbm(filename):
    image_path = IMAGE_DIR / filename

    if not image_path.exists():
        print(f"XBM image not found: {image_path}")
        return None

    try:
        return tk.BitmapImage(file=str(image_path))

    except tk.TclError as error:
        print(f"Could not load XBM image '{filename}': {error}")
        return None
