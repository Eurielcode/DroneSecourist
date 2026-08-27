# data — Collecte et préparation des données

Statut : **en cours** (étape 1 de la feuille de route). Scripts écrits et testés avec des
données synthétiques ; téléchargement réel des jeux de données pas encore effectué (voir
`docs/datasets.md`).

## Contenu

- `raw/` : données brutes téléchargées (RescueNet, xBD). Gitignoré — jamais commité.
- `processed/` : annotations converties au format unifié (COCO). Gitignoré.
- `scripts/` :
  - `common.py` : utilitaires partagés (téléchargement en streaming, extraction sûre
    d'archives zip/tar.gz).
  - `download_rescuenet.py` : téléchargement automatique depuis Dropbox/Figshare.
  - `download_xbd.py` : détection + extraction des archives xBD téléchargées manuellement
    (inscription obligatoire sur xview2.org, voir `docs/datasets.md`).
  - `prepare_dataset.py` : conversion des annotations RescueNet (masques RVB) et xBD
    (polygones WKT) vers un format unifié de type COCO. Testé dans
    `tests/test_prepare_dataset.py`.

## Comment récupérer les données

```bash
pip install -r requirements.txt
python data/scripts/download_rescuenet.py
python data/scripts/download_xbd.py       # après téléchargement manuel des .tar.gz, voir docs/datasets.md
python data/scripts/prepare_dataset.py
```

## Limite connue

Ni RescueNet ni xBD ne contiennent d'annotations de personnes/victimes — voir
`docs/datasets.md` (section « Limite critique ») pour les conséquences sur la feuille de
route et les pistes de jeux de données complémentaires.

Voir aussi [`docs/datasets.md`](../docs/datasets.md) pour tous les détails (licences,
structure exacte, classes).
