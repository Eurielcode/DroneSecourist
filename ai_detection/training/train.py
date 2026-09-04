"""Entraînement du modèle de détection multi-classes (YOLOv8/v11, Ultralytics).

Prérequis : avoir généré le dataset YOLO au préalable :
    python ai_detection/training/prepare_yolo_dataset.py

Augmentation renforcée par défaut (occlusion + basse lumière) : nos datasets publics ne
contiennent ni images de nuit ni personnes fortement occluses en conditions réelles (voir
docs/datasets.md). En attendant de vraies données pour ces cas (drone réel, dataset dédié),
on pousse deux augmentations déjà intégrées à Ultralytics au-delà de leurs valeurs par
défaut :
  - `erasing` (effacement aléatoire de zones de l'image, simule une occlusion partielle) :
    0.4 -> 0.5 par défaut ici.
  - `hsv_v` (variation aléatoire de luminosité) : 0.4 -> 0.6 par défaut ici, pour mieux
    couvrir les conditions de faible luminosité.
Ce n'est qu'un pis-aller : ça ne remplace pas de vraies images de nuit ou de vraies victimes
occluses (voir C2A, ai_detection/README.md), mais c'est gratuit et améliore la robustesse
sans données supplémentaires.

Utilisation :
    python ai_detection/training/train.py [--model yolov8n.pt] [--epochs 50] [--imgsz 640]
        [--batch 16] [--data ai_detection/configs/dataset.yaml]
        [--erasing 0.5] [--hsv-v 0.6]
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
    erasing: float = 0.5,
    hsv_v: float = 0.6,
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
        erasing=erasing,
        hsv_v=hsv_v,
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
    parser.add_argument(
        "--erasing",
        type=float,
        default=0.5,
        help="Probabilité d'effacement aléatoire (simule une occlusion partielle). Défaut Ultralytics : 0.4.",
    )
    parser.add_argument(
        "--hsv-v",
        dest="hsv_v",
        type=float,
        default=0.6,
        help="Amplitude de variation de luminosité (simule des conditions de faible éclairage). Défaut Ultralytics : 0.4.",
    )
    args = parser.parse_args()
    train(
        data=args.data,
        model=args.model,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        project=args.project,
        name=args.name,
        erasing=args.erasing,
        hsv_v=args.hsv_v,
    )


if __name__ == "__main__":
    main()
