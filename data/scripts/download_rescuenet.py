"""Téléchargement du jeu de données RescueNet.

Source : Rahnemoonfar et al., « RescueNet: A High Resolution UAV Semantic Segmentation
Dataset for Natural Disaster Damage Assessment », Scientific Data, 2023.
Licence : CC BY-NC-ND — citer la publication en cas d'utilisation (voir docs/datasets.md).

Le jeu de données est hébergé sur un dossier Dropbox public (et en miroir sur Figshare). Ce
script télécharge l'archive zip générée à la volée par Dropbox pour ce dossier public. Si
Dropbox refuse de générer ce zip (dossier trop volumineux pour l'export à la volée, lien
expiré, ou accès réseau bloqué dans l'environnement d'exécution), le script affiche les
instructions de téléchargement manuel.

Utilisation :
    python data/scripts/download_rescuenet.py [--dest data/raw/rescuenet] [--keep-archive]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import download_file, extract_archive  # noqa: E402

DROPBOX_FOLDER_URL = (
    "https://www.dropbox.com/scl/fo/ntgeyhxe2mzd2wuh7he7x/AHJ-cNzQL-Eu04HS6bvBgcw?dl=1"
)
FIGSHARE_COLLECTION_URL = (
    "https://springernature.figshare.com/collections/"
    "RescueNet_A_High_Resolution_UAV_Semantic_Segmentation_Benchmark_Dataset_for_"
    "Natural_Disaster_Damage_Assessment/6647354"
)

MANUAL_INSTRUCTIONS = f"""
Téléchargement automatique impossible. Téléchargez manuellement le jeu de données depuis
l'une de ces sources :

  - Dropbox : {DROPBOX_FOLDER_URL.split('?')[0]}
  - Figshare : {FIGSHARE_COLLECTION_URL}

Puis placez les dossiers extraits dans data/raw/rescuenet/ en respectant la structure
attendue (voir docs/datasets.md) :

  data/raw/rescuenet/
    train/train-org-img/*.jpg        train/train-label-img/*_lab.png
    val/val-org-img/*.jpg            val/val-label-img/*_lab.png
    test/test-org-img/*.jpg          test/test-label-img/*_lab.png
"""


def download_rescuenet(dest: Path = Path("data/raw/rescuenet"), keep_archive: bool = False) -> None:
    if dest.exists() and any(dest.iterdir()):
        print(
            f"{dest} existe déjà et n'est pas vide — rien à faire "
            "(supprimez-le pour forcer un nouveau téléchargement)."
        )
        return

    archive_path = dest.parent / "rescuenet_dropbox.zip"
    try:
        print("Téléchargement de RescueNet depuis Dropbox...")
        download_file(DROPBOX_FOLDER_URL, archive_path)
        print(f"Extraction vers {dest}...")
        extract_archive(archive_path, dest)
        print("Terminé.")
    except Exception as exc:
        print(f"\nÉchec du téléchargement automatique : {exc}", file=sys.stderr)
        print(MANUAL_INSTRUCTIONS, file=sys.stderr)
        raise SystemExit(1) from exc
    finally:
        if archive_path.exists() and not keep_archive:
            archive_path.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", type=Path, default=Path("data/raw/rescuenet"))
    parser.add_argument(
        "--keep-archive", action="store_true", help="Conserver l'archive zip téléchargée"
    )
    args = parser.parse_args()
    download_rescuenet(dest=args.dest, keep_archive=args.keep_archive)


if __name__ == "__main__":
    main()
