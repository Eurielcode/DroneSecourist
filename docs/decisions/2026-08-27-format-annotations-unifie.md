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

## Mise à jour — 2026-08-28 : validation sur données réelles

Les trois jeux de données ont été réellement téléchargés (RescueNet via Figshare, SARD et xBD
via des miroirs Kaggle faute d'accès fiable aux sources officielles) et passés dans
`prepare_dataset.py`. Ça a révélé un bug bloquant qui n'existait pas dans les tests
synthétiques :

- **RescueNet n'est pas encodé en RVB.** L'hypothèse initiale (masque couleur, une couleur par
  classe) était fausse : les fichiers `*_lab.png` réels sont **mono-canal**, la valeur de
  chaque pixel étant directement l'indice de classe (0-10). Les couleurs RVB documentées par
  le dépôt officiel BinaLab ne servent qu'à la visualisation. Avec l'ancien code, la conversion
  tournait sans erreur mais produisait **zéro annotation** pour RescueNet (aucune couleur ne
  matchait jamais). Corrigé : `RESCUENET_INDEX_TO_CATEGORY` (indice → catégorie) remplace
  `RESCUENET_COLOR_TO_CATEGORY`, lecture en `cv2.IMREAD_UNCHANGED` au lieu de `IMREAD_COLOR`.
- Résultat après correction sur les données réelles : train 7636 images / (annotations à
  revérifier après le prochain run complet), val 1593 images, test 1020 images — cohérent avec
  RescueNet (3595/449/450) + SARD augmenté (~4041/1144/570).
- Les miroirs Kaggle de SARD et xBD extraient chacun dans un sous-dossier intermédiaire
  (`search-and-rescue/` et `xbd/` respectivement) plutôt que directement à la racine attendue —
  la résolution de chemin dans `prepare_dataset.py` a été rendue plus tolérante (recherche
  récursive) pour SARD ; pour xBD, un déplacement manuel du sous-dossier suffit.

Leçon retenue : les tests unitaires sur données synthétiques valident la *logique* de
conversion (structure COCO, calculs de bbox/aire) mais ne peuvent pas détecter une hypothèse
erronée sur le *format réel* des fichiers sources — seul un test sur un échantillon réel
aurait permis de le détecter plus tôt.
