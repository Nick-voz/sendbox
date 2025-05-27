from logging import Handler
from pathlib import Path
from typing import Any

from PIL import Image
from reportlab.pdfgen import canvas

IMG_EXTENSIONS = [
    ".png",
]
ROTATED_SUFFIX = "rotade_"
WIDTH = 400
HEIGHT = 100


def load_imgs_pats(dir_path: str) -> list[Any]:
    directory = Path(dir_path)
    if directory.exists() is False:
        raise FileNotFoundError(f"{directory} is not found")

    if directory.is_dir() is False:
        raise ValueError(f"{dir_path}is not directory")

    files_paths = [
        file_path
        for file_path in directory.iterdir()
        if file_path.is_file()
        and not file_path.name.startswith(".")
        and file_path.suffix.lower() in IMG_EXTENSIONS
    ]

    return files_paths


def rotate(path: Path, degrees: int = 90):
    if degrees % 90 != 0:
        raise ValueError("Rotation must be in increments of 90 degrees.")

    rotations = (degrees // 90) % 4

    image = Image.open(path)
    image = image.rotate(90 * rotations, expand=True)

    image.save(path.with_name(ROTATED_SUFFIX + path.name))


def glue_in_pdf(images_paths: list[Path], pdf_path: Path) -> None:
    c = canvas.Canvas(str(pdf_path))

    for image_file in images_paths:
        with Image.open(str(image_file)) as img:
            if img.mode != "RGB":
                img = img.convert("RGB")

            width, height = img.size

            c.setPageSize((width, height))
            c.drawImage(image_file, 0, 0, width=width, height=height)
            c.showPage()

    c.save()


def rename_all_to_numeric(paths: list[Path], prefix: str | None = None):
    for i, path in enumerate(paths, start=1):
        suffix = path.suffix
        prefix = prefix if prefix is not None else ""
        new_name = "".join((prefix, str(i), suffix))
        path.rename(path.with_name(new_name))


def main():
    TEST_DIR = "/Users/nikitavozisow/Desktop/dir1"

    images = load_imgs_pats(TEST_DIR)
    rename_all_to_numeric(images)

    # images = load_imgs_pats(TEST_DIR)
    # images = list(map(rotate, images))

    images = load_imgs_pats(TEST_DIR)
    glue_in_pdf(images, Path(TEST_DIR).joinpath(("bruh" + ".pdf")))


if __name__ == "__main__":
    main()
