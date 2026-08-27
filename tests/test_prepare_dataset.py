"""Tests des convertisseurs RescueNet/xBD/SARD -> format unifié, avec des données synthétiques.

Le jeu de données réel n'est pas disponible dans l'environnement de développement (taille,
inscription requise pour xBD/SARD) : ces tests construisent de fausses images/labels
minimalistes pour valider que la logique de conversion produit une structure COCO cohérente.
À revalider manuellement avec un échantillon réel une fois les données téléchargées (étape 1).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "data" / "scripts"))
from prepare_dataset import (  # noqa: E402
    CATEGORY_IDS,
    convert_rescuenet_split,
    convert_sard_split,
    convert_xbd_split,
)


def _make_rescuenet_split(tmp_path: Path) -> Path:
    split_dir = tmp_path / "train"
    img_dir = split_dir / "train-org-img"
    label_dir = split_dir / "train-label-img"
    img_dir.mkdir(parents=True)
    label_dir.mkdir(parents=True)

    height, width = 40, 40
    image = np.zeros((height, width, 3), dtype=np.uint8)
    cv2.imwrite(str(img_dir / "0001.jpg"), image)

    # Masque label : fond noir + un carré "building_no_damage" (180,120,120 en RVB -> BGR pour cv2)
    mask_rgb = np.zeros((height, width, 3), dtype=np.uint8)
    mask_rgb[5:20, 5:20] = (180, 120, 120)  # building_no_damage
    mask_rgb[25:35, 25:35] = (4, 250, 7)  # tree
    mask_bgr = cv2.cvtColor(mask_rgb, cv2.COLOR_RGB2BGR)
    cv2.imwrite(str(label_dir / "0001_lab.png"), mask_bgr)

    return split_dir


def test_convert_rescuenet_split(tmp_path: Path) -> None:
    split_dir = _make_rescuenet_split(tmp_path)
    coco = convert_rescuenet_split(split_dir)

    assert len(coco["images"]) == 1
    assert coco["images"][0]["file_name"] == "0001.jpg"
    assert len(coco["categories"]) == len(CATEGORY_IDS)

    category_ids_found = {ann["category_id"] for ann in coco["annotations"]}
    assert CATEGORY_IDS["building_no_damage"] in category_ids_found
    assert CATEGORY_IDS["tree"] in category_ids_found
    for ann in coco["annotations"]:
        assert ann["area"] > 0
        assert len(ann["bbox"]) == 4


def _make_xbd_split(tmp_path: Path) -> Path:
    split_dir = tmp_path / "test"
    images_dir = split_dir / "images"
    labels_dir = split_dir / "labels"
    images_dir.mkdir(parents=True)
    labels_dir.mkdir(parents=True)

    label = {
        "metadata": {"width": 100, "height": 100},
        "features": {
            "xy": [
                {
                    "properties": {"feature_type": "building", "subtype": "major-damage"},
                    "wkt": "POLYGON ((10 10, 30 10, 30 30, 10 30, 10 10))",
                },
                {
                    "properties": {"feature_type": "building", "subtype": "un-classified"},
                    "wkt": "POLYGON ((50 50, 60 50, 60 60, 50 60, 50 50))",
                },
            ]
        },
    }
    label_path = labels_dir / "disaster_00000001_post_disaster.json"
    with open(label_path, "w", encoding="utf-8") as f:
        json.dump(label, f)

    return split_dir


def test_convert_xbd_split(tmp_path: Path) -> None:
    split_dir = _make_xbd_split(tmp_path)
    coco = convert_xbd_split(split_dir)

    assert len(coco["images"]) == 1
    assert coco["images"][0]["width"] == 100
    assert coco["images"][0]["height"] == 100

    # Un seul bâtiment doit être conservé : le "un-classified" est ignoré (pas de catégorie).
    assert len(coco["annotations"]) == 1
    assert coco["annotations"][0]["category_id"] == CATEGORY_IDS["building_major_damage"]
    assert coco["annotations"][0]["bbox"] == [10.0, 10.0, 20.0, 20.0]


def _make_sard_split(tmp_path: Path) -> Path:
    split_dir = tmp_path / "train"
    images_dir = split_dir / "images"
    labels_dir = split_dir / "labels"
    images_dir.mkdir(parents=True)
    labels_dir.mkdir(parents=True)

    height, width = 200, 100
    image = np.zeros((height, width, 3), dtype=np.uint8)
    cv2.imwrite(str(images_dir / "frame_001.jpg"), image)

    # Une personne centrée en (0.5, 0.25) de taille (0.2 x 0.1) en coordonnées normalisées.
    (labels_dir / "frame_001.txt").write_text("0 0.5 0.25 0.2 0.1\n")

    return split_dir


def test_convert_sard_split(tmp_path: Path) -> None:
    split_dir = _make_sard_split(tmp_path)
    coco = convert_sard_split(split_dir)

    assert len(coco["images"]) == 1
    assert coco["images"][0]["file_name"] == "frame_001.jpg"

    assert len(coco["annotations"]) == 1
    ann = coco["annotations"][0]
    assert ann["category_id"] == CATEGORY_IDS["person"]
    # width=100 -> x_center=50, box_w=20 -> x_min=40 ; height=200 -> y_center=50, box_h=20 -> y_min=40
    assert ann["bbox"] == [40.0, 40.0, 20.0, 20.0]
