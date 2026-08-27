# Jeux de données publics

Statut : documenté (étape 1 en cours — scripts de téléchargement/conversion écrits et testés
avec des données synthétiques ; téléchargement réel des jeux de données pas encore effectué,
voir « Comment récupérer les données » ci-dessous).

## ⚠️ Limite critique : aucune annotation de victimes

**Ni RescueNet ni xBD ne contiennent d'annotations de personnes/victimes.** Les deux jeux de
données portent uniquement sur les dégâts de bâtiments et l'occupation du sol (routes, eau,
végétation, véhicules). Conséquence directe sur la feuille de route :

- Les fonctionnalités **#1 (détection de victimes)**, **#8 (corps sans signe de vie)**,
  **#16 (estimation du nombre de personnes)** et **#22 (signaux de détresse visuels)** ne
  peuvent **pas** être entraînées à partir de ces deux jeux de données seuls.
- Il faudra ajouter un troisième jeu de données orienté détection de personnes en vue aérienne
  pour ces fonctionnalités, par exemple : **SARD** (Search And Rescue image Dataset),
  **HERIDAL** (détection de personnes en montagne depuis un drone), ou la classe "person" de
  **VisDrone**. À évaluer et ajouter dans une itération ultérieure de l'étape 1.
- RescueNet et xBD restent en revanche directement exploitables pour les fonctionnalités liées
  au terrain/bâtiments : **#5, #6, #7, #9, #15** (chemins praticables, zones dangereuses,
  évolution du terrain, priorisation, accessibilité des bâtiments).

## RescueNet

- **Publication** : Rahnemoonfar, Chowdhury & Murphy, « RescueNet: A High Resolution UAV
  Semantic Segmentation Dataset for Natural Disaster Damage Assessment », *Scientific Data*,
  2023.
- **Contenu** : imagerie aérienne UAV haute résolution (3000×4000 px) prise après l'ouragan
  Michael, avec masques de segmentation sémantique pixel par pixel.
- **Taille** : 4 494 images (~80 % train / ~10 % val / ~10 % test → 3 595 / 449 / 450 images).
- **Licence** : CC BY-NC-ND — citer la publication, usage non commercial, pas de modification
  redistribuée du jeu de données lui-même.
- **Téléchargement** :
  - Dropbox (dossier public) : https://www.dropbox.com/scl/fo/ntgeyhxe2mzd2wuh7he7x/AHJ-cNzQL-Eu04HS6bvBgcw
  - Figshare (miroir) : https://springernature.figshare.com/collections/RescueNet_A_High_Resolution_UAV_Semantic_Segmentation_Benchmark_Dataset_for_Natural_Disaster_Damage_Assessment/6647354
  - Script : `python data/scripts/download_rescuenet.py`
- **Structure attendue après téléchargement** (`data/raw/rescuenet/`) :
  ```
  train/train-org-img/*.jpg      train/train-label-img/*_lab.png
  val/val-org-img/*.jpg          val/val-label-img/*_lab.png
  test/test-org-img/*.jpg        test/test-label-img/*_lab.png
  ```
- **Classes (masques RVB)** — 10 classes + fond non annoté :

  | Classe | Couleur RVB |
  |---|---|
  | Water | (61, 230, 250) |
  | Building No Damage | (180, 120, 120) |
  | Building Minor Damage | (235, 255, 7) |
  | Building Major Damage | (255, 184, 6) |
  | Building Total Destruction | (255, 0, 0) |
  | Vehicle | (255, 0, 245) |
  | Road-Clear | (140, 140, 140) |
  | Road-Blocked | (160, 150, 20) |
  | Tree | (4, 250, 7) |
  | Pool | (255, 235, 0) |

## xBD (xView2 Building Damage)

- **Publication** : Gupta et al., « xBD: A Dataset for Assessing Building Damage from
  Satellite Imagery », 2019 (challenge xView2).
- **Contenu** : paires d'images satellite avant/après catastrophe (Maxar), 22 068 images de
  1024×1024 px, plus de 850 000 polygones de bâtiments annotés, 6 types de catastrophes
  (inondation, incendie, séisme, ouragan, tornade, volcan).
- **Licence** : CC BY-NC-SA 4.0.
- **Téléchargement** : **inscription obligatoire** sur https://xview2.org puis téléchargement
  manuel depuis https://xview2.org/dataset (`train_images_labels_targets.tar.gz`,
  `test_images_labels_targets.tar.gz`, optionnellement `hold_...` et `tier3.tar.gz`) — voir
  les instructions détaillées affichées par `python data/scripts/download_xbd.py`.
- **Structure attendue après extraction** (`data/raw/xbd/<split>/`) :
  ```
  images/<id>_pre_disaster.png   images/<id>_post_disaster.png
  labels/<id>_pre_disaster.json  labels/<id>_post_disaster.json
  ```
- **Format des labels** : JSON avec `features.xy[]`, chaque feature ayant un polygone
  `wkt` (`POLYGON ((x y, x y, ...))`) et `properties.subtype` ∈ `{no-damage, minor-damage,
  major-damage, destroyed, un-classified}` (uniquement dans les labels *post_disaster* ; les
  labels *pre_disaster* ne portent que le contour du bâtiment, sans dégât).

## Format unifié

Les deux jeux de données sont convertis vers un format commun de type COCO par
`data/scripts/prepare_dataset.py`. Détail de la décision et de la taxonomie de catégories
partagée : [`docs/decisions/2026-08-27-format-annotations-unifie.md`](decisions/2026-08-27-format-annotations-unifie.md).

## Comment récupérer les données

```bash
pip install -r requirements.txt
python data/scripts/download_rescuenet.py     # automatique
python data/scripts/download_xbd.py           # nécessite d'avoir téléchargé les .tar.gz manuellement au préalable (voir ci-dessus)
python data/scripts/prepare_dataset.py        # génère data/processed/{train,val,test}.json
```

Ces trois scripts sont écrits et testés (voir `tests/test_prepare_dataset.py`), mais le
téléchargement réel des jeux de données complets n'a pas encore été exécuté (volumes trop
importants pour l'environnement de développement actuel) — à faire sur une machine avec
suffisamment d'espace disque et un accès réseau complet.

## Statistiques et biais

À renseigner une fois les données réellement téléchargées : déséquilibre entre classes,
résolution/qualité des images, répartition géographique, biais potentiels — utile pour
interpréter les performances du modèle et documenter ses limites (étape 11).
