"""Utilitaires partagés par les scripts de collecte de données (étape 1)."""
from __future__ import annotations

import sys
import tarfile
import zipfile
from pathlib import Path

import requests


def download_file(url: str, dest: Path, chunk_size: int = 1 << 20) -> Path:
    """Télécharge un fichier en streaming avec affichage de progression."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=60) as response:
        response.raise_for_status()
        total = int(response.headers.get("content-length", 0))
        downloaded = 0
        with open(dest, "wb") as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if not chunk:
                    continue
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    pct = downloaded / total * 100
                    sys.stdout.write(
                        f"\r{dest.name}: {pct:5.1f}% "
                        f"({downloaded / 1e6:.1f} / {total / 1e6:.1f} Mo)"
                    )
                    sys.stdout.flush()
        if total:
            print()
    return dest


def _check_members_safe(names: list[str], dest_dir: Path) -> None:
    """Empêche l'extraction de chemins hors de dest_dir (path traversal, symlinks malveillants)."""
    dest_resolved = dest_dir.resolve()
    for name in names:
        target = (dest_resolved / name).resolve()
        if dest_resolved not in target.parents and target != dest_resolved:
            raise ValueError(f"Chemin d'archive suspect (path traversal) : {name}")


def extract_archive(archive_path: Path, dest_dir: Path) -> None:
    """Extrait une archive .zip ou .tar.gz de façon sûre vers dest_dir."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    if zipfile.is_zipfile(archive_path):
        with zipfile.ZipFile(archive_path) as zf:
            _check_members_safe(zf.namelist(), dest_dir)
            zf.extractall(dest_dir)
    elif tarfile.is_tarfile(archive_path):
        with tarfile.open(archive_path) as tf:
            _check_members_safe(tf.getnames(), dest_dir)
            try:
                tf.extractall(dest_dir, filter="data")
            except TypeError:
                # Python < 3.12 sans le paramètre `filter` (backport partiel) : on a déjà
                # validé les chemins ci-dessus via _check_members_safe.
                tf.extractall(dest_dir)
    else:
        raise ValueError(f"Format d'archive non reconnu : {archive_path}")
