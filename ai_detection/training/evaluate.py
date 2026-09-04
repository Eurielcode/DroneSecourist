"""Évaluation d'un modèle entraîné (mAP, précision/rappel par classe) sur un split donné.

Utilisation :
    python ai_detection/training/evaluate.py --weights ai_detection/models/dronesecourist/weights/best.pt
"""
from __future__ import annotations

import argparse
from pathlib import Path


def evaluate(
    weights: Path,
    data: Path = Path("ai_detection/configs/dataset.yaml"),
    split: str = "test",
):
    from ultralytics import YOLO  # import tardif : dépendance lourde, inutile hors évaluation

    if not weights.exists():
        raise FileNotFoundError(f"Poids introuvables : {weights}")
    if not data.exists():
        raise FileNotFoundError(
            f"{data} introuvable. Lancez d'abord : "
            "python ai_detection/training/prepare_yolo_dataset.py"
        )

    model = YOLO(str(weights))
    metrics = model.val(data=str(data), split=split)
    print(metrics)
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weights", type=Path, required=True)
    parser.add_argument("--data", type=Path, default=Path("ai_detection/configs/dataset.yaml"))
    parser.add_argument("--split", default="test", choices=["train", "val", "test"])
    args = parser.parse_args()
    evaluate(weights=args.weights, data=args.data, split=args.split)


if __name__ == "__main__":
    main()
