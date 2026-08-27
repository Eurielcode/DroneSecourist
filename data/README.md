# data — Collecte et préparation des données

Statut : à faire (étape 1 de la feuille de route).

## Contenu

- `raw/` : données brutes téléchargées (RescueNet, xBD). Gitignoré — jamais commité.
- `processed/` : données prétraitées / converties au format unifié. Gitignoré.
- `scripts/` : scripts de téléchargement et de préparation.
  - `download_rescuenet.py` : téléchargement du jeu de données RescueNet.
  - `download_xbd.py` : téléchargement du jeu de données xBD.
  - `prepare_dataset.py` : conversion des annotations vers un format unifié (COCO/YOLO) et
    génération des splits train/val/test.

## Comment régénérer les données

À documenter précisément à l'étape 1 (sources exactes, identifiants nécessaires, licences).
Voir aussi [`docs/datasets.md`](../docs/datasets.md).

Aucun script n'est encore fonctionnel : ce sont des squelettes créés à l'étape 0, à implémenter
lors du démarrage de l'étape 1.
