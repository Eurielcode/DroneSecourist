"""Tests de l'export COCO -> YOLO, avec un mini jeu de données COCO synthétique."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ai_detection" / "training"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "data" / "scripts"))
from prepare_dataset import CATEGORY_IDS  # noqa: E402
from prepare_yolo_dataset import export_split, write_dataset_yaml  # noqa: E402


def _make_processed_split(tmp_path: Path):
    raw_dir = tmp_path / "raw"
    source_image_dir = raw_dir / "rescuenet" / "train" / "train-org-img"
    source_image_dir.mkdir(parents=True)
    image = np.zeros((100, 200, 3), dtype=np.uint8)
    cv2.imwrite(str(source_image_dir / "0001.jpg"), image)

    coco = {
        "images": [
            {
                "id": 1,
                "file_name": "0001.jpg",
                "width": 200,
                "height": 100,
                "source_path": "rescuenet/train/train-org-img/0001.jpg",
            }
        ],
        "annotations": [
            {
                "id": 1,
                "image_id": 1,
                "category_id": CATEGORY_IDS["building_no_damage"],
                "bbox": [20.0, 10.0, 40.0, 20.0],
                "area": 800.0,
                "iscrowd": 0,
                "segmentation": [[20, 10, 60, 10, 60, 30, 20, 30]],
            }
        ],
        "categories": [],
    }
    processed_dir = tmp_path / "processed"
    processed_dir.mkdir()
    processed_json = processed_dir / "train.json"
    with open(processed_json, "w", encoding="utf-8") as f:
        json.dump(coco, f)

    return processed_json, raw_dir


def test_export_split(tmp_path: Path) -> None:
    processed_json, raw_dir = _make_processed_split(tmp_path)
    output_dir = tmp_path / "dataset"

    count = export_split(processed_json, raw_dir, output_dir, "train")

    assert count == 1
    image_files = list((output_dir / "train" / "images").glob("*"))
    assert len(image_files) == 1
    assert image_files[0].name == "0000001.jpg"

    label_path = output_dir / "train" / "labels" / "0000001.txt"
    assert label_path.exists()
    line = label_path.read_text().strip()
    parts = line.split()
    assert len(parts) == 5

    expected_class = CATEGORY_IDS["building_no_damage"] - 1
    assert int(parts[0]) == expected_class
    # bbox [20,10,40,20] sur image 200x100 -> centre (40/200, 20/100), taille (40/200, 20/100)
    x_center, y_center, w, h = (float(p) for p in parts[1:])
    assert abs(x_center - 0.20) < 1e-6
    assert abs(y_center - 0.20) < 1e-6
    assert abs(w - 0.20) < 1e-6
    assert abs(h - 0.20) < 1e-6


def test_write_dataset_yaml(tmp_path: Path) -> None:
    output_dir = tmp_path / "dataset"
    config_path = tmp_path / "configs" / "dataset.yaml"
    write_dataset_yaml(output_dir, config_path)

    content = config_path.read_text()
    assert "train: train/images" in content
    assert "val: val/images" in content
    assert "test: test/images" in content
    assert "person" in content
    assert "building_no_damage" in content
