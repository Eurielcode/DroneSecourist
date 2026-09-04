"""Export du format unifié COCO vers un dataset YOLO pour l'entraînement Ultralytics.

Lit data/processed/{train,val,test}.json (voir data/scripts/prepare_dataset.py) et construit
un dataset au format attendu par Ultralytics YOLO :

    ai_detection/dataset/<split>/images/<id>.<ext>
    ai_detection/dataset/<split>/labels/<id>.txt

Les images ne sont pas copiées mais liées en dur (hard link) vers les fichiers sources dans
data/raw/ quand c'est possible (même volume) — ça évite de doubler l'espace disque déjà
occupé par les données brutes (RescueNet + xBD + SARD font plusieurs dizaines de Go). Si le
hard link échoue (systèmes de fichiers différents, réseau, etc.), le fichier est copié.

Génère aussi ai_detection/configs/dataset.yaml, le fichier de configuration Ultralytics
pointant vers ce dataset.

Utilisation :
    python ai_detection/training/prepare_yolo_dataset.py
        [--processed-dir data/processed] [--raw-dir data/raw]
        [--output-dir ai_detection/dataset] [--config-path ai_detection/configs/dataset.yaml]
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "data" / "scripts"))
from prepare_dataset import UNIFIED_CATEGORIES  # noqa: E402


def _link_or_copy(source: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        return
    try:
        os.link(source, dest)
    except OSError:
        shutil.copy2(source, dest)


def _yolo_line(category_id: int, bbox: list, width: int, height: int) -> str:
    x, y, w, h = bbox
    x_center = (x + w / 2) / width
    y_center = (y + h / 2) / height
    return f"{category_id - 1} {x_center:.6f} {y_center:.6f} {w / width:.6f} {h / height:.6f}"


def export_split(processed_json: Path, raw_dir: Path, output_dir: Path, split: str) -> int:
    with open(processed_json, encoding="utf-8") as f:
        coco = json.load(f)

    annotations_by_image: dict = {}
    for ann in coco["annotations"]:
        annotations_by_image.setdefault(ann["image_id"], []).append(ann)

    images_out = output_dir / split / "images"
    labels_out = output_dir / split / "labels"
    images_out.mkdir(parents=True, exist_ok=True)
    labels_out.mkdir(parents=True, exist_ok=True)

    exported = 0
    total = len(coco["images"])
    for index, image in enumerate(coco["images"], start=1):
        if index == 1 or index % 1000 == 0 or index == total:
            print(f"\r  {split} : image {index}/{total}", end="", flush=True)
        source_path = raw_dir / image["source_path"]
        if not source_path.exists():
            continue

        unique_name = f"{image['id']:07d}{source_path.suffix.lower()}"
        _link_or_copy(source_path, images_out / unique_name)

        lines = [
            _yolo_line(ann["category_id"], ann["bbox"], image["width"], image["height"])
            for ann in annotations_by_image.get(image["id"], [])
        ]
        label_content = "\n".join(lines) + ("\n" if lines else "")
        (labels_out / f"{image['id']:07d}.txt").write_text(label_content)
        exported += 1

    if total:
        print()
    return exported


def write_dataset_yaml(output_dir: Path, config_path: Path) -> None:
    names_block = "\n".join(f"  {i}: {name}" for i, name in enumerate(UNIFIED_CATEGORIES))
    content = (
        f"path: {output_dir.resolve().as_posix()}\n"
        "train: train/images\n"
        "val: val/images\n"
        "test: test/images\n"
        "names:\n"
        f"{names_block}\n"
    )
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(content)


def prepare_yolo_dataset(
    processed_dir: Path = Path("data/processed"),
    raw_dir: Path = Path("data/raw"),
    output_dir: Path = Path("ai_detection/dataset"),
    config_path: Path = Path("ai_detection/configs/dataset.yaml"),
) -> None:
    for split in ("train", "val", "test"):
        processed_json = processed_dir / f"{split}.json"
        if not processed_json.exists():
            print(f"{processed_json} introuvable, {split} ignoré.")
            continue
        count = export_split(processed_json, raw_dir, output_dir, split)
        print(f"{split}: {count} images exportées -> {output_dir / split}")

    write_dataset_yaml(output_dir, config_path)
    print(f"Configuration Ultralytics écrite dans {config_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--processed-dir", type=Path, default=Path("data/processed"))
    parser.add_argument("--raw-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--output-dir", type=Path, default=Path("ai_detection/dataset"))
    parser.add_argument("--config-path", type=Path, default=Path("ai_detection/configs/dataset.yaml"))
    args = parser.parse_args()
    prepare_yolo_dataset(
        processed_dir=args.processed_dir,
        raw_dir=args.raw_dir,
        output_dir=args.output_dir,
        config_path=args.config_path,
    )


if __name__ == "__main__":
    main()
