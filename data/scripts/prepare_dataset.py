"""Conversion de RescueNet, xBD et SARD vers un format d'annotations unifié (style COCO).

Décision de format documentée dans docs/decisions/2026-08-27-format-annotations-unifie.md.

RescueNet fournit des masques de segmentation RVB multi-classes (une couleur par classe,
voir RESCUENET_COLOR_TO_CATEGORY) ; xBD fournit des polygones de bâtiments au format WKT dans
des fichiers JSON, avec un niveau de dégât par bâtiment (voir XBD_SUBTYPE_TO_CATEGORY) ; SARD
fournit des boîtes englobantes de personnes au format YOLO (voir convert_sard_split).

RescueNet et xBD ne contiennent aucune annotation de personnes/victimes (voir
docs/datasets.md, section « Limite critique ») : c'est SARD qui couvre cette classe.

Les fonctions de conversion sont testées avec des données synthétiques dans
tests/test_prepare_dataset.py (le jeu de données réel n'est pas présent dans cet
environnement). À revalider avec les données réelles une fois téléchargées.

Utilisation :
    python data/scripts/prepare_dataset.py [--raw-dir data/raw] [--output-dir data/processed]
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable, Optional

import cv2
import numpy as np

UNIFIED_CATEGORIES = [
    "building_no_damage",
    "building_minor_damage",
    "building_major_damage",
    "building_destroyed",
    "road_clear",
    "road_blocked",
    "water",
    "vehicle",
    "tree",
    "pool",
    "person",
]
CATEGORY_IDS = {name: idx + 1 for idx, name in enumerate(UNIFIED_CATEGORIES)}

# Couleurs RVB des masques RescueNet -> catégorie unifiée.
# Source : Segmentation-Experiments/data/rescuenet.py du dépôt officiel BinaLab/RescueNet.
RESCUENET_COLOR_TO_CATEGORY = {
    (61, 230, 250): "water",
    (180, 120, 120): "building_no_damage",
    (235, 255, 7): "building_minor_damage",
    (255, 184, 6): "building_major_damage",
    (255, 0, 0): "building_destroyed",
    (255, 0, 245): "vehicle",
    (140, 140, 140): "road_clear",
    (160, 150, 20): "road_blocked",
    (4, 250, 7): "tree",
    (255, 235, 0): "pool",
}

# Sous-types de dégât xBD -> catégorie unifiée. "un-classified" est ignoré : pas
# d'équivalent fiable dans la taxonomie unifiée.
XBD_SUBTYPE_TO_CATEGORY = {
    "no-damage": "building_no_damage",
    "minor-damage": "building_minor_damage",
    "major-damage": "building_major_damage",
    "destroyed": "building_destroyed",
}

MIN_POLYGON_AREA = 20.0  # px^2 — élimine le bruit de segmentation (artefacts sub-pixel)

_WKT_POLYGON_RE = re.compile(r"POLYGON\s*\(\(([^)]+)\)\)", re.IGNORECASE)


def _new_coco_dict() -> dict:
    return {
        "images": [],
        "annotations": [],
        "categories": [{"id": cat_id, "name": name} for name, cat_id in CATEGORY_IDS.items()],
    }


def _add_image(coco: dict, file_name: str, width: int, height: int) -> int:
    image_id = len(coco["images"]) + 1
    coco["images"].append({"id": image_id, "file_name": file_name, "width": width, "height": height})
    return image_id


def _add_polygon_annotation(coco: dict, image_id: int, category_name: str, polygon: np.ndarray) -> None:
    polygon = polygon.reshape(-1, 2).astype(np.float64)
    if len(polygon) < 3:
        return
    area = float(cv2.contourArea(polygon.astype(np.float32)))
    if area < MIN_POLYGON_AREA:
        return
    # Bbox calculée directement à partir des sommets (min/max), pas via cv2.boundingRect qui
    # arrondit sur des coordonnées entières de pixels et introduit un décalage de +1 en
    # largeur/hauteur pour des polygones vectoriels (WKT xBD notamment).
    x_min, y_min = polygon.min(axis=0)
    x_max, y_max = polygon.max(axis=0)
    coco["annotations"].append(
        {
            "id": len(coco["annotations"]) + 1,
            "image_id": image_id,
            "category_id": CATEGORY_IDS[category_name],
            "segmentation": [polygon.flatten().tolist()],
            "bbox": [float(x_min), float(y_min), float(x_max - x_min), float(y_max - y_min)],
            "area": area,
            "iscrowd": 0,
        }
    )


def _find_matching_label(image_path: Path, label_dir: Path) -> Optional[Path]:
    stem = image_path.stem
    for candidate in (label_dir / f"{stem}_lab.png", label_dir / f"{stem}.png"):
        if candidate.exists():
            return candidate
    matches = list(label_dir.glob(f"{stem}*.png"))
    return matches[0] if matches else None


def convert_rescuenet_split(split_dir: Path) -> dict:
    """Convertit un split RescueNet (train/val/test) en dict COCO.

    Structure attendue : split_dir/<nom>-org-img/*.jpg et split_dir/<nom>-label-img/*.png
    (masques RVB multi-classes). Voir docs/datasets.md.
    """
    coco = _new_coco_dict()
    img_dirs = sorted(split_dir.glob("*-org-img"))
    label_dirs = sorted(split_dir.glob("*-label-img"))
    if not img_dirs or not label_dirs:
        raise FileNotFoundError(
            f"Structure RescueNet inattendue dans {split_dir} "
            "(dossiers *-org-img / *-label-img introuvables)."
        )
    img_dir, label_dir = img_dirs[0], label_dirs[0]

    image_paths = sorted(img_dir.glob("*.jpg"))
    total = len(image_paths)
    for index, image_path in enumerate(image_paths, start=1):
        if index == 1 or index % 100 == 0 or index == total:
            print(f"\r  RescueNet {split_dir.name} : image {index}/{total}", end="", flush=True)
        label_path = _find_matching_label(image_path, label_dir)
        if label_path is None:
            continue
        mask = cv2.imread(str(label_path), cv2.IMREAD_COLOR)
        if mask is None:
            continue
        height, width = mask.shape[:2]
        image_id = _add_image(coco, image_path.name, width, height)
        mask_rgb = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)

        for color, category_name in RESCUENET_COLOR_TO_CATEGORY.items():
            binary = np.all(mask_rgb == np.array(color, dtype=mask_rgb.dtype), axis=-1).astype(np.uint8)
            if not binary.any():
                continue
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                _add_polygon_annotation(coco, image_id, category_name, contour)

    if total:
        print()
    return coco


def _parse_wkt_polygon(wkt: str) -> Optional[np.ndarray]:
    match = _WKT_POLYGON_RE.search(wkt)
    if not match:
        return None
    points = []
    for pair in match.group(1).split(","):
        parts = pair.strip().split()
        if len(parts) < 2:
            continue
        points.append((float(parts[0]), float(parts[1])))
    return np.array(points, dtype=np.float64) if len(points) >= 3 else None


def convert_xbd_split(split_dir: Path) -> dict:
    """Convertit un split xBD en dict COCO à partir des labels post-catastrophe.

    Structure attendue : split_dir/images/*_post_disaster.png et
    split_dir/labels/*_post_disaster.json (format xView2). Voir docs/datasets.md.
    """
    coco = _new_coco_dict()
    images_dir = split_dir / "images"
    labels_dir = split_dir / "labels"
    if not labels_dir.exists():
        raise FileNotFoundError(f"Dossier de labels xBD introuvable : {labels_dir}")

    for label_path in sorted(labels_dir.glob("*_post_disaster.json")):
        with open(label_path, encoding="utf-8") as f:
            label = json.load(f)

        metadata = label.get("metadata", {})
        width, height = metadata.get("width"), metadata.get("height")
        image_name = label_path.stem + ".png"
        if width is None or height is None:
            image_path = images_dir / image_name
            image = cv2.imread(str(image_path)) if image_path.exists() else None
            if image is None:
                continue
            height, width = image.shape[:2]

        image_id = _add_image(coco, image_name, width, height)

        for feature in label.get("features", {}).get("xy", []):
            subtype = feature.get("properties", {}).get("subtype")
            category_name = XBD_SUBTYPE_TO_CATEGORY.get(subtype)
            if category_name is None:
                continue
            polygon = _parse_wkt_polygon(feature.get("wkt", ""))
            if polygon is None:
                continue
            _add_polygon_annotation(coco, image_id, category_name, polygon)

    return coco


_IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png")


def convert_sard_split(split_dir: Path) -> dict:
    """Convertit un split SARD (format YOLO) en dict COCO.

    Hypothèse de structure (format YOLO le plus courant pour ce jeu de données, notamment via
    son miroir Roboflow) : split_dir/images/*.{jpg,png} et split_dir/labels/*.txt, une ligne
    par personne au format YOLO normalisé : "<classe> <x_centre> <y_centre> <largeur>
    <hauteur>". SARD est mono-classe (person). À valider/ajuster une fois le jeu de données
    réel téléchargé et inspecté (voir docs/datasets.md) — le mirroir Kaggle brut pourrait
    utiliser un format d'annotation différent.
    """
    coco = _new_coco_dict()
    images_dir = split_dir / "images"
    labels_dir = split_dir / "labels"
    if not images_dir.exists() or not labels_dir.exists():
        raise FileNotFoundError(
            f"Structure SARD inattendue dans {split_dir} (images/ ou labels/ introuvable)."
        )

    for label_path in sorted(labels_dir.glob("*.txt")):
        image_path = next(
            (
                candidate
                for ext in _IMAGE_EXTENSIONS
                if (candidate := images_dir / f"{label_path.stem}{ext}").exists()
            ),
            None,
        )
        if image_path is None:
            continue
        image = cv2.imread(str(image_path))
        if image is None:
            continue
        height, width = image.shape[:2]
        image_id = _add_image(coco, image_path.name, width, height)

        for line in label_path.read_text().splitlines():
            parts = line.split()
            if len(parts) != 5:
                continue
            _, x_center, y_center, box_w, box_h = (float(p) for p in parts)
            x_min = (x_center - box_w / 2) * width
            y_min = (y_center - box_h / 2) * height
            abs_w, abs_h = box_w * width, box_h * height
            polygon = np.array(
                [
                    [x_min, y_min],
                    [x_min + abs_w, y_min],
                    [x_min + abs_w, y_min + abs_h],
                    [x_min, y_min + abs_h],
                ]
            )
            _add_polygon_annotation(coco, image_id, "person", polygon)

    return coco


def _merge_coco(dicts: Iterable[dict]) -> dict:
    merged = _new_coco_dict()
    image_id_offset = 0
    for coco in dicts:
        id_map = {}
        for image in coco["images"]:
            new_id = image["id"] + image_id_offset
            id_map[image["id"]] = new_id
            merged["images"].append({**image, "id": new_id})
        for ann in coco["annotations"]:
            merged["annotations"].append(
                {**ann, "id": len(merged["annotations"]) + 1, "image_id": id_map[ann["image_id"]]}
            )
        image_id_offset = max((img["id"] for img in merged["images"]), default=image_id_offset)
    return merged


def prepare_dataset(raw_dir: Path = Path("data/raw"), output_dir: Path = Path("data/processed")) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    for split in ("train", "val", "test"):
        cocos = []

        rescuenet_split = raw_dir / "rescuenet" / split
        if rescuenet_split.exists():
            cocos.append(convert_rescuenet_split(rescuenet_split))

        # xBD n'a pas de split "val" officiel : on utilise son split "hold" comme validation.
        xbd_split = raw_dir / "xbd" / ("hold" if split == "val" else split)
        if xbd_split.exists():
            cocos.append(convert_xbd_split(xbd_split))

        # SARD (miroir Roboflow) nomme son split de validation "valid", pas "val", et certains
        # miroirs (ex. Kaggle) extraient les données dans un sous-dossier intermédiaire
        # (ex. sard/search-and-rescue/train/) : on cherche récursivement le bon dossier.
        for sard_split_name in ({"val": "valid"}.get(split, split), split):
            sard_split = next(
                (
                    candidate
                    for candidate in raw_dir.glob(f"sard/**/{sard_split_name}")
                    if (candidate / "images").exists() and (candidate / "labels").exists()
                ),
                None,
            )
            if sard_split is not None:
                cocos.append(convert_sard_split(sard_split))
                break

        if not cocos:
            continue

        merged = _merge_coco(cocos)
        output_path = output_dir / f"{split}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(merged, f)
        print(
            f"{split}: {len(merged['images'])} images, "
            f"{len(merged['annotations'])} annotations -> {output_path}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/processed"))
    args = parser.parse_args()
    prepare_dataset(raw_dir=args.raw_dir, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
