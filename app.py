from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox


VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"}


def combine_image_pairs(
    image_paths: Iterable[Path],
    output_dir: Path,
    quality: int = 95,
    start_from_end: bool = True,
) -> list[Path]:
    paths = [Path(p) for p in image_paths]
    if start_from_end:
        # Starter fra siste bilde i listen: N+N-1, deretter nedover.
        paths = list(reversed(paths))
    if len(paths) < 2:
        raise ValueError("Du må velge minst to bilder.")
    if len(paths) % 2 != 0:
        raise ValueError("Antall bilder må være partall (foran+baksiden i par).")

    output_dir.mkdir(parents=True, exist_ok=True)

    created_files: list[Path] = []
    for pair_index in range(0, len(paths), 2):
        front_path = paths[pair_index]
        back_path = paths[pair_index + 1]

        with Image.open(front_path) as front_img, Image.open(back_path) as back_img:
            front_rgb = front_img.convert("RGB")
            back_rgb = back_img.convert("RGB")

            new_width = front_rgb.width + back_rgb.width
            new_height = max(front_rgb.height, back_rgb.height)

            combined = Image.new("RGB", (new_width, new_height), color=(255, 255, 255))
            combined.paste(front_rgb, (0, 0))
            combined.paste(back_rgb, (front_rgb.width, 0))

            output_name = f"kort_{(pair_index // 2) + 1:04d}.jpg"
            output_path = output_dir / output_name
            combined.save(output_path, format="JPEG", quality=quality)
            created_files.append(output_path)

    return created_files


class CardCombinerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Pokémon kort-kombinerer")
        self.selected_files: list[Path] = []

        self.file_count_var = tk.StringVar(value="Ingen filer valgt")
        self.output_var = tk.StringVar(value=str(Path.cwd() / "output"))
        self.start_from_end_var = tk.BooleanVar(value=True)

        self._build_ui()

    def _build_ui(self) -> None:
        frame = tk.Frame(self.root, padx=16, pady=16)
        frame.pack(fill="both", expand=True)

        tk.Button(frame, text="Velg bilder (flere)", command=self._select_files).pack(anchor="w")
        tk.Label(frame, textvariable=self.file_count_var, pady=8).pack(anchor="w")

        tk.Label(frame, text="Lagringsmappe:").pack(anchor="w")
        output_row = tk.Frame(frame)
        output_row.pack(fill="x", pady=(0, 12))
        tk.Entry(output_row, textvariable=self.output_var).pack(side="left", fill="x", expand=True)
        tk.Button(output_row, text="Velg mappe", command=self._select_output_dir).pack(side="left", padx=(8, 0))

        tk.Checkbutton(
            frame,
            text="Start fra slutten av listen (N+N-1, N-2+N-3, ...)",
            variable=self.start_from_end_var,
        ).pack(anchor="w", pady=(0, 8))

        tk.Button(frame, text="Kombiner og lagre .jpg", command=self._run_combination, bg="#2ecc71").pack(anchor="w")

        hint_text = (
            "Tips: Velg bilder i ønsket rekkefølge.\n"
            "Huk av for å starte fra slutten, eller fjern haken for å starte fra begynnelsen."
        )
        tk.Label(frame, text=hint_text, fg="#555", pady=12, justify="left").pack(anchor="w")

    def _select_files(self) -> None:
        files = filedialog.askopenfilenames(
            title="Velg kortbilder i rekkefølge",
            filetypes=[
                ("Bildefiler", "*.jpg *.jpeg *.png *.webp *.bmp *.tiff"),
                ("Alle filer", "*.*"),
            ],
        )
        self.selected_files = [Path(file) for file in files]
        self.file_count_var.set(f"Valgt {len(self.selected_files)} filer")

    def _select_output_dir(self) -> None:
        directory = filedialog.askdirectory(title="Velg mappe for ferdige bilder")
        if directory:
            self.output_var.set(directory)

    def _run_combination(self) -> None:
        try:
            output_dir = Path(self.output_var.get()).expanduser().resolve()
            created = combine_image_pairs(
                self.selected_files,
                output_dir=output_dir,
                start_from_end=self.start_from_end_var.get(),
            )
        except ValueError as err:
            messagebox.showerror("Ugyldig input", str(err))
            return
        except OSError as err:
            messagebox.showerror("Feil ved bildebehandling", str(err))
            return

        messagebox.showinfo(
            "Ferdig",
            f"Lagde {len(created)} filer i:\n{output_dir}",
        )


def collect_images_from_dir(input_dir: Path) -> list[Path]:
    return sorted(
        [
            file
            for file in input_dir.iterdir()
            if file.is_file() and file.suffix.lower() in VALID_EXTENSIONS
        ]
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Kombiner Pokémon-kortbilder side om side."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        help="Mappe med bilder (filnavn sorteres alfabetisk, men kombineres fra slutten).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output"),
        help="Mappe for ferdige JPG-bilder (default: ./output)",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=95,
        help="JPEG-kvalitet fra 1-100 (default: 95)",
    )
    parser.add_argument(
        "--start-from-start",
        action="store_true",
        help="Kombiner fra starten av listen (1+2, 3+4, ...).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.input_dir:
        images = collect_images_from_dir(args.input_dir)
        created = combine_image_pairs(
            images,
            output_dir=args.output_dir,
            quality=args.quality,
            start_from_end=not args.start_from_start,
        )
        print(f"Lagde {len(created)} kombinerte bilder i {args.output_dir.resolve()}")
        return

    root = tk.Tk()
    app = CardCombinerApp(root)
    root.minsize(520, 260)
    root.mainloop()


if __name__ == "__main__":
    main()
