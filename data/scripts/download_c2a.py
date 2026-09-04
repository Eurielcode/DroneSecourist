"""Téléchargement du jeu de données C2A (Combination to Application).

Ajouté pour combler une limite identifiée après l'étape 1 : SARD montre des personnes bien
visibles sur terrain dégagé, pas des victimes partiellement cachées sous des débris — le cas
le plus critique en contexte réel de catastrophe. C2A comble ce manque.

Source : Nihal et al., « UAV-Enhanced Combination to Application: Comprehensive Analysis and
Benchmarking of a Human Detection Dataset for Disaster Scenarios ».
https://github.com/Ragib-Amin-Nihal/C2A
Dataset synthétique : poses humaines (LSP/MPII-MPHB) incrustées sur des fonds de catastrophe
réels (AIDER : incendie/fumée, inondation, bâtiment effondré/décombres, accident de la route).
10 215 images, plus de 360 000 personnes annotées, poses variées (debout, assise, allongée,
à genoux, penchée). Classe unique : "person". Licence : non précisée par les auteurs.

Méthode de téléchargement retenue : miroir Kaggle (même méthode que SARD), slug
"rgbnihal/c2a-dataset".

Utilisation :
    pip install kaggle
    python data/scripts/download_c2a.py [--dest data/raw/c2a]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

KAGGLE_DATASET_SLUG = "rgbnihal/c2a-dataset"

MANUAL_INSTRUCTIONS = """
Téléchargement automatique impossible. Deux sources possibles :

  - Kaggle (recommandé) :
      1. Créer un compte sur https://www.kaggle.com et un jeton API
         (https://www.kaggle.com/docs/api : Account -> Create New Token -> kaggle.json)
      2. pip install kaggle
      3. Placer kaggle.json dans ~/.kaggle/kaggle.json (chmod 600)
      4. Relancer ce script
      Ou manuellement : https://www.kaggle.com/datasets/rgbnihal/c2a-dataset
  - GitHub (source du papier, peut nécessiter une demande d'accès aux données) :
      https://github.com/Ragib-Amin-Nihal/C2A

Quelle que soit la source, placez les fichiers extraits dans data/raw/c2a/ en respectant la
structure attendue par prepare_dataset.py (voir docs/datasets.md) :

  data/raw/c2a/train/images/*.jpg   data/raw/c2a/train/labels/*.txt
  data/raw/c2a/val/images/*.jpg     data/raw/c2a/val/labels/*.txt
  data/raw/c2a/test/images/*.jpg    data/raw/c2a/test/labels/*.txt

(labels au format YOLO : "<classe> <x_centre> <y_centre> <largeur> <hauteur>" normalisés)
"""


def download_c2a(dest: Path = Path("data/raw/c2a")) -> None:
    if dest.exists() and any(dest.iterdir()):
        print(f"{dest} existe déjà et n'est pas vide — rien à faire.")
        return

    try:
        import kaggle  # import tardif : dépendance optionnelle, échoue si pas de jeton API
    except ImportError as exc:
        print("Le package 'kaggle' n'est pas installé (pip install kaggle).", file=sys.stderr)
        print(MANUAL_INSTRUCTIONS, file=sys.stderr)
        raise SystemExit(1) from exc

    try:
        kaggle.api.authenticate()
        print(f"Téléchargement de {KAGGLE_DATASET_SLUG} depuis Kaggle...")
        dest.mkdir(parents=True, exist_ok=True)
        kaggle.api.dataset_download_files(KAGGLE_DATASET_SLUG, path=str(dest), unzip=True)
        print("Terminé.")
    except Exception as exc:
        print(f"\nÉchec du téléchargement automatique : {exc}", file=sys.stderr)
        print(MANUAL_INSTRUCTIONS, file=sys.stderr)
        raise SystemExit(1) from exc


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", type=Path, default=Path("data/raw/c2a"))
    args = parser.parse_args()
    download_c2a(dest=args.dest)


if __name__ == "__main__":
    main()
