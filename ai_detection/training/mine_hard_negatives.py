"""Hard negative mining : convertit les faux positifs d'un modèle déjà entraîné en exemples
négatifs pour le prochain entraînement.

Contexte : nos datasets publics (RescueNet, xBD, SARD, C2A) ne contiennent pas d'exemples de
"pièges" propres à notre contexte (rochers/sacs/débris qui ressemblent à une personne). Ce
script comble ce manque sans nouveau jeu de données : on fait tourner un premier modèle
entraîné sur des images dont on sait avec certitude qu'elles ne contiennent aucun objet
d'intérêt, et chaque détection (donc chaque erreur) est réinjectée dans le dataset
d'entraînement comme exemple négatif (image + fichier label vide), pour que le modèle
apprenne à ne plus s'y tromper au prochain entraînement.

Prérequis :
  - Un modèle déjà entraîné (voir train.py).
  - Un dossier d'images dont on est CERTAIN qu'elles ne contiennent aucun objet des classes
    du modèle (ex. photos aériennes de terrain vide, zones sans dégât ni personne). Ce script
    ne construit pas ce dossier — il faut le constituer soi-même (extraits de zones "vides"
    des datasets déjà téléchargés, ou nouvelles photos).

Utilisation :
    python ai_detection/training/mine_hard_negatives.py
        --weights ai_detection/models/dronesecourist/weights/best.pt
        --images-dir <dossier d'images sans objet d'intérêt>
        [--output-dir ai_detection/dataset/train] [--conf 0.25]

Après exécution, relancer l'entraînement (train.py) pour que les nouveaux exemples négatifs
soient pris en compte.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

_IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png")


def mine_hard_negatives(
    weights: Path,
    images_dir: Path,
    output_dir: Path,
    conf: float = 0.25,
) -> int:
    from ultralytics import YOLO  # import tardif : dépendance lourde, inutile sans exécution

    if not weights.exists():
        raise FileNotFoundError(f"Poids introuvables : {weights}")
    if not images_dir.exists():
        raise FileNotFoundError(f"Dossier d'images introuvable : {images_dir}")

    images_out = output_dir / "images"
    labels_out = output_dir / "labels"
    images_out.mkdir(parents=True, exist_ok=True)
    labels_out.mkdir(parents=True, exist_ok=True)

    model = YOLO(str(weights))
    image_paths = sorted(p for p in images_dir.iterdir() if p.suffix.lower() in _IMAGE_EXTENSIONS)

    found = 0
    for image_path in image_paths:
        results = model.predict(source=str(image_path), conf=conf, verbose=False)
        if not results or len(results[0].boxes) == 0:
            continue  # pas de fausse détection sur cette image : rien à faire

        dest_image = images_out / f"hardneg_{image_path.name}"
        shutil.copy2(image_path, dest_image)
        # Fichier de label vide : indique explicitement au modèle qu'il n'y a aucun objet ici,
        # malgré ce qu'il a cru détecter.
        (labels_out / f"hardneg_{image_path.stem}.txt").write_text("")
        found += 1
        print(f"Faux positif sur {image_path.name} ({len(results[0].boxes)} détection(s))")

    print(f"{found} exemple(s) négatif(s) ajouté(s) dans {output_dir}")
    return found


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weights", type=Path, required=True)
    parser.add_argument("--images-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("ai_detection/dataset/train"))
    parser.add_argument(
        "--conf",
        type=float,
        default=0.25,
        help="Seuil de confiance minimal pour compter une détection comme faux positif.",
    )
    args = parser.parse_args()
    mine_hard_negatives(
        weights=args.weights, images_dir=args.images_dir, output_dir=args.output_dir, conf=args.conf
    )


if __name__ == "__main__":
    main()
