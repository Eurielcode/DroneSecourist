"""Téléchargement du jeu de données SARD (Search And Rescue image Dataset).

Ajouté pour combler un manque identifié à l'étape 1 : ni RescueNet ni xBD ne contiennent
d'annotations de personnes/victimes (voir docs/datasets.md). SARD comble ce manque pour les
fonctionnalités #1, #8, #16, #22.

Source : Ivašić-Kos et al., publié sur IEEE DataPort —
https://ieee-dataport.org/documents/search-and-rescue-image-dataset-person-detection-sard
1 981 images annotées de personnes vues depuis un drone en situation simulée de recherche et
sauvetage (personnes en marche, debout, assises, allongées ; terrain varié : route, forêt,
herbe haute, carrière). Classe unique : "person".
Licence : à vérifier précisément sur la page IEEE DataPort (site non accessible depuis cet
environnement de développement) — citer la publication en cas d'utilisation.

Méthode de téléchargement retenue : miroir Kaggle (le plus simple à scripter), slug
"nikolasgegenava/sard-search-and-rescue". Nécessite un compte Kaggle et un jeton API
(~/.kaggle/kaggle.json) — voir https://www.kaggle.com/docs/api (bouton "Create New Token"
dans les paramètres du compte Kaggle).

Si le téléchargement automatique échoue (package absent, pas de jeton, accès réseau bloqué),
les instructions de téléchargement manuel sont affichées.

Utilisation :
    pip install kaggle
    python data/scripts/download_sard.py [--dest data/raw/sard]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

KAGGLE_DATASET_SLUG = "nikolasgegenava/sard-search-and-rescue"

MANUAL_INSTRUCTIONS = """
Téléchargement automatique impossible. Trois sources possibles :

  - Kaggle (recommandé) :
      1. Créer un compte sur https://www.kaggle.com et un jeton API
         (https://www.kaggle.com/docs/api : Account -> Create New Token -> kaggle.json)
      2. pip install kaggle
      3. Placer kaggle.json dans ~/.kaggle/kaggle.json (chmod 600)
      4. Relancer ce script
      Ou manuellement : https://www.kaggle.com/datasets/nikolasgegenava/sard-search-and-rescue
  - IEEE DataPort (source originale, citer la publication) :
      https://ieee-dataport.org/documents/search-and-rescue-image-dataset-person-detection-sard
  - Roboflow Universe (miroir déjà au format YOLO, nécessite une clé API Roboflow gratuite) :
      https://universe.roboflow.com/dataset-ay6sw/sard-peykp

Quelle que soit la source, placez les images/labels extraits dans data/raw/sard/ en
respectant la structure attendue par prepare_dataset.py (voir docs/datasets.md) :

  data/raw/sard/train/images/*.jpg   data/raw/sard/train/labels/*.txt
  data/raw/sard/valid/images/*.jpg   data/raw/sard/valid/labels/*.txt
  data/raw/sard/test/images/*.jpg    data/raw/sard/test/labels/*.txt

(labels au format YOLO : "<classe> <x_centre> <y_centre> <largeur> <hauteur>" normalisés)
"""


def download_sard(dest: Path = Path("data/raw/sard")) -> None:
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
    parser.add_argument("--dest", type=Path, default=Path("data/raw/sard"))
    args = parser.parse_args()
    download_sard(dest=args.dest)


if __name__ == "__main__":
    main()
