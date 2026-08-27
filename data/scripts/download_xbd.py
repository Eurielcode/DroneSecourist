"""Téléchargement du jeu de données xBD (xView2 Building Damage).

xBD ne peut PAS être téléchargé automatiquement : il faut créer un compte sur xview2.org et
accepter la licence CC BY-NC-SA 4.0 avant de pouvoir télécharger les archives.

Étapes manuelles :
  1. Créer un compte sur https://xview2.org (inscription requise).
  2. Aller sur https://xview2.org/dataset et télécharger au minimum :
       - train_images_labels_targets.tar.gz (obligatoire)
       - test_images_labels_targets.tar.gz (obligatoire)
     et optionnellement :
       - hold_images_labels_targets.tar.gz (utilisé ici comme split de validation)
       - tier3.tar.gz (données d'entraînement supplémentaires)
  3. Placer ces fichiers .tar.gz (sans les décompresser) dans data/raw/xbd_archives/.
  4. Relancer ce script : il détecte les archives présentes et les extrait dans data/raw/xbd/.

Ce script ne fait donc que détecter et extraire les archives déjà téléchargées manuellement.

Utilisation :
    python data/scripts/download_xbd.py [--archives-dir data/raw/xbd_archives] [--dest data/raw/xbd]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import extract_archive  # noqa: E402

EXPECTED_ARCHIVES = {
    "train": "train_images_labels_targets.tar.gz",
    "test": "test_images_labels_targets.tar.gz",
    "hold": "hold_images_labels_targets.tar.gz",
    "tier3": "tier3.tar.gz",
}
REQUIRED_SPLITS = ("train", "test")

MANUAL_INSTRUCTIONS = """
Aucune archive xBD trouvée dans {archives_dir}.

xBD nécessite une inscription manuelle (licence CC BY-NC-SA 4.0) :
  1. Créer un compte sur https://xview2.org
  2. Télécharger depuis https://xview2.org/dataset :
       - train_images_labels_targets.tar.gz (obligatoire)
       - test_images_labels_targets.tar.gz (obligatoire)
       - hold_images_labels_targets.tar.gz (optionnel, utilisé comme split de validation)
       - tier3.tar.gz (optionnel, données supplémentaires)
  3. Placer ces fichiers .tar.gz dans {archives_dir}/ puis relancer ce script.
"""


def download_xbd(
    archives_dir: Path = Path("data/raw/xbd_archives"),
    dest: Path = Path("data/raw/xbd"),
) -> None:
    archives_dir.mkdir(parents=True, exist_ok=True)
    found = {
        split: archives_dir / filename
        for split, filename in EXPECTED_ARCHIVES.items()
        if (archives_dir / filename).exists()
    }

    missing_required = [s for s in REQUIRED_SPLITS if s not in found]
    if missing_required:
        print(MANUAL_INSTRUCTIONS.format(archives_dir=archives_dir), file=sys.stderr)
        if not found:
            raise SystemExit(1)
        print(f"Archives trouvées : {sorted(found)} — extraction de celles-ci uniquement.")

    for split, archive_path in found.items():
        split_dest = dest / split
        if split_dest.exists() and any(split_dest.iterdir()):
            print(f"{split_dest} existe déjà et n'est pas vide — ignoré.")
            continue
        print(f"Extraction de {archive_path.name} vers {split_dest}...")
        extract_archive(archive_path, split_dest)

    print("Terminé." if found else "Rien à extraire.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archives-dir", type=Path, default=Path("data/raw/xbd_archives"))
    parser.add_argument("--dest", type=Path, default=Path("data/raw/xbd"))
    args = parser.parse_args()
    download_xbd(archives_dir=args.archives_dir, dest=args.dest)


if __name__ == "__main__":
    main()
