# Format d'annotations unifié pour RescueNet + xBD

Date : 2026-08-27

## Contexte

RescueNet fournit des masques de segmentation RVB (une couleur par classe, pixel par pixel).
xBD fournit des polygones de bâtiments au format WKT dans des fichiers JSON, avec un niveau de
dégât par bâtiment. Les deux formats sont incompatibles tels quels ; il faut un format commun
pour entraîner un seul modèle multi-classes (étape 2).

## Décision

Conversion des deux jeux de données vers un format unique de type **COCO** (`images`,
`annotations` avec `segmentation` polygonale + `bbox` + `category_id`, `categories`), avec une
taxonomie de catégories partagée :

`building_no_damage`, `building_minor_damage`, `building_major_damage`, `building_destroyed`,
`road_clear`, `road_blocked`, `water`, `vehicle`, `tree`, `pool`.

- RescueNet : chaque classe couleur du masque est convertie en polygones via extraction de
  contours (`cv2.findContours`) sur le masque binaire de cette couleur.
- xBD : les polygones WKT des bâtiments sont directement réutilisés ; le sous-type de dégât
  (`subtype`) est mappé vers la catégorie unifiée correspondante. Le sous-type
  `un-classified` est ignoré (pas d'équivalent fiable).
- Un seuil d'aire minimale (20 px²) filtre le bruit de segmentation.

Implémenté dans `data/scripts/prepare_dataset.py`, testé avec des données synthétiques dans
`tests/test_prepare_dataset.py` (voir ce fichier pour le détail).

## Conséquences

- Format directement compatible avec les frameworks d'entraînement usuels (Ultralytics YOLO
  après conversion COCO→YOLO, Detectron2, etc.) pour l'étape 2.
- **Limite identifiée** : RescueNet et xBD ne couvrent que les classes de dégâts/terrain,
  aucune annotation de personnes/victimes (voir `docs/datasets.md`). **Mise à jour du même
  jour** : un troisième jeu de données, **SARD** (Search And Rescue image Dataset), a été
  ajouté pour combler ce manque, avec une catégorie unifiée `person` supplémentaire — voir
  `convert_sard_split` dans `data/scripts/prepare_dataset.py` et la section SARD de
  `docs/datasets.md`.
- À revalider avec les données réelles une fois téléchargées : la logique n'a été testée que
  sur des exemples synthétiques minimalistes, pas sur la variabilité réelle des masques/labels
  (bâtiments qui se touchent, contours complexes, format exact des labels SARD, etc.).
