"""Entraînement du modèle de détection multi-classes (YOLOv8/v11, Ultralytics).

Prérequis : avoir généré le dataset YOLO au préalable :
    python ai_detection/training/prepare_yolo_dataset.py

Utilisation :
    python ai_detection/training/train.py [--model yolov8n.pt] [--epochs 50] [--imgsz 640]
        [--batch 16] [--data ai_detection/configs/dataset.yaml]
"""
from __future__ import annotations

import argparse
from pathlib import Path


def train(
    data: Path = Path("ai_detection/configs/dataset.yaml"),
    model: str = "yolov8n.pt",
    epochs: int = 50,
    imgsz: int = 640,
    batch: int = 16,
    project: Path = Path("ai_detection/models"),
    name: str = "dronesecourist",
) -> None:
    from ultralytics import YOLO  # import tardif : dépendance lourde, inutile hors entraînement

    if not data.exists():
        raise FileNotFoundError(
            f"{data} introuvable. Lancez d'abord : "
            "python ai_detection/training/prepare_yolo_dataset.py"
        )

    yolo_model = YOLO(model)
    yolo_model.train(
        data=str(data),
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        project=str(project),
        name=name,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("ai_detection/configs/dataset.yaml"))
    parser.add_argument(
        "--model", default="yolov8n.pt", help="Poids de départ (ex. yolov8n.pt, yolov8s.pt)"
    )
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--project", type=Path, default=Path("ai_detection/models"))
    parser.add_argument("--name", default="dronesecourist")
    args = parser.parse_args()
    train(
        data=args.data,
        model=args.model,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        project=args.project,
        name=args.name,
    )


if __name__ == "__main__":
    main()
