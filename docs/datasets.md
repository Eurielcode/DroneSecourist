# Jeux de données publics

Statut : documenté (étape 1 en cours — scripts de téléchargement/conversion écrits et testés
avec des données synthétiques ; téléchargement réel des jeux de données pas encore effectué,
voir « Comment récupérer les données » ci-dessous).

## ⚠️ Limite identifiée : RescueNet et xBD ne couvrent pas les victimes

**Ni RescueNet ni xBD ne contiennent d'annotations de personnes/victimes.** Les deux jeux de
données portent uniquement sur les dégâts de bâtiments et l'occupation du sol (routes, eau,
végétation, véhicules). Conséquence directe sur la feuille de route :

- Les fonctionnalités **#1 (détection de victimes)**, **#8 (corps sans signe de vie)**,
  **#16 (estimation du nombre de personnes)** et **#22 (signaux de détresse visuels)**
  n'auraient pas pu être entraînées à partir de ces deux jeux de données seuls.
- RescueNet et xBD restent directement exploitables pour les fonctionnalités liées au
  terrain/bâtiments : **#5, #6, #7, #9, #15** (chemins praticables, zones dangereuses,
  évolution du terrain, priorisation, accessibilité des bâtiments).
- **Un troisième jeu de données, SARD, a été ajouté pour combler ce manque** (voir
  section dédiée ci-dessous) : il couvre spécifiquement la détection de personnes en vue
  drone dans des scénarios de recherche-sauvetage.

### Pourquoi SARD plutôt que HERIDAL ou VisDrone

- **HERIDAL** est thématiquement idéal (personnes en zone montagneuse/sauvage vues depuis un
  drone) mais aucun lien de téléchargement public direct n'a été trouvé — l'accès semble se
  faire sur demande aux auteurs, ce qui n'est pas scriptable de façon fiable.
- **VisDrone** est facilement scriptable (dépôt GitHub officiel, liens directs) et contient
  une classe "pedestrian"/"people", mais ses scènes sont urbaines/routières (trafic, foules),
  peu représentatives d'un contexte de catastrophe naturelle.
- **SARD** est spécifiquement conçu pour la détection de personnes en vue drone dans des
  scénarios de recherche-sauvetage simulés (personnes en marche, debout, assises, allongées,
  sur route, forêt, herbe haute, carrière) — le plus proche du cas d'usage réel du projet — et
  dispose d'un miroir Kaggle scriptable.

## RescueNet

- **Publication** : Rahnemoonfar, Chowdhury & Murphy, « RescueNet: A High Resolution UAV
  Semantic Segmentation Dataset for Natural Disaster Damage Assessment », *Scientific Data*,
  2023.
- **Contenu** : imagerie aérienne UAV haute résolution (3000×4000 px) prise après l'ouragan
  Michael, avec masques de segmentation sémantique pixel par pixel.
- **Taille** : 4 494 images (~80 % train / ~10 % val / ~10 % test → 3 595 / 449 / 450 images).
- **Licence** : CC BY-NC-ND — citer la publication, usage non commercial, pas de modification
  redistribuée du jeu de données lui-même.
- **Téléchargement** : **le dossier Dropbox public ne fonctionne pas en pratique** (Dropbox
  refuse de générer un zip à la volée pour un dossier aussi volumineux — testé et confirmé,
  `download_rescuenet.py` échoue systématiquement). La vraie méthode qui fonctionne est
  Figshare, avec un lien par split (pas de compte requis) :
  - Train : https://springernature.figshare.com/articles/dataset/RescueNet_Semantic_Segmentation_Train_Set/22825511
  - Validation : https://springernature.figshare.com/articles/dataset/RescueNet_Semantic_Segmentation_Validation_Set/22826369
  - Test : https://springernature.figshare.com/articles/dataset/RescueNet_Semantic_Segmentation_Test_Set/22826459
  - `download_rescuenet.py` tente Dropbox puis affiche ces liens en instructions manuelles si
    ça échoue (ce qui est le cas actuel systématique).
- **Structure attendue après téléchargement** (`data/raw/rescuenet/`) :
  ```
  train/train-org-img/*.jpg      train/train-label-img/*_lab.png
  val/val-org-img/*.jpg          val/val-label-img/*_lab.png
  test/test-org-img/*.jpg        test/test-label-img/*_lab.png
  ```
- **Classes (masques mono-canal, indice de classe par pixel)** — 10 classes + fond non
  annoté (0). **Vérifié sur les données réelles** : le fichier `.png` de label est une image
  à un seul canal (pas RVB) où la valeur de chaque pixel est directement l'indice de classe
  (0-10). Les couleurs RVB documentées par le dépôt officiel BinaLab ne servent qu'à
  l'affichage/visualisation, pas au fichier livré :

  | Indice | Classe |
  |---|---|
  | 0 | Background (non annoté) |
  | 1 | Water |
  | 2 | Building No Damage |
  | 3 | Building Minor Damage |
  | 4 | Building Major Damage |
  | 5 | Building Total Destruction |
  | 6 | Vehicle |
  | 7 | Road-Clear |
  | 8 | Road-Blocked |
  | 9 | Tree |
  | 10 | Pool |

## xBD (xView2 Building Damage)

- **Publication** : Gupta et al., « xBD: A Dataset for Assessing Building Damage from
  Satellite Imagery », 2019 (challenge xView2).
- **Contenu** : paires d'images satellite avant/après catastrophe (Maxar), 22 068 images de
  1024×1024 px, plus de 850 000 polygones de bâtiments annotés, 6 types de catastrophes
  (inondation, incendie, séisme, ouragan, tornade, volcan).
- **Licence** : CC BY-NC-SA 4.0.
- **Téléchargement officiel** : inscription obligatoire sur https://xview2.org puis
  téléchargement manuel depuis https://xview2.org/dataset (`train_images_labels_targets.tar.gz`,
  `test_images_labels_targets.tar.gz`, optionnellement `hold_...` et `tier3.tar.gz`) — voir
  les instructions détaillées affichées par `python data/scripts/download_xbd.py`. **En
  pratique, le site xview2.org peut être indisponible/instable** (constaté lors du
  développement — connexion qui reste bloquée en chargement).
- **Solution de contournement utilisée avec succès** : miroir Kaggle
  `qianlanzz/xbd-dataset` (⚠️ non officiel, licence non précisée — `License(s): unknown`
  affiché par l'API Kaggle ; à remplacer par la source officielle si xview2.org redevient
  accessible). Attention : **~31 Go** à télécharger + autant pour l'extraction (~60 Go
  d'espace disque nécessaires au pic). Téléchargement :
  ```
  kaggle datasets download -d qianlanzz/xbd-dataset -p data\raw\xbd_kaggle_mirror --unzip
  ```
  Ce miroir extrait dans un sous-dossier `xbd/` intermédiaire
  (`data/raw/xbd_kaggle_mirror/xbd/{train,test,hold,tier1,tier3}/...`) qu'il faut déplacer
  vers `data/raw/xbd/` pour que `prepare_dataset.py` le trouve. **Piège constaté** : le
  dossier `train` de ce miroir ne contient que des images, **sans labels** (probablement un
  reliquat de l'ancienne organisation officielle du dataset). Les vraies données labellisées
  d'entraînement sont dans `tier1/` (+ `tier3/` en complément, tous deux avec `images/` et
  `labels/`) — `prepare_dataset.py` combine automatiquement `train` + `tier1` + `tier3` s'ils
  ont chacun un dossier `labels/`, donc un `train/` sans labels est simplement ignoré.
- **Structure attendue après extraction** (`data/raw/xbd/<split>/`), confirmée identique
  entre la source officielle et le miroir Kaggle :
  ```
  images/<id>_pre_disaster.png   images/<id>_post_disaster.png
  labels/<id>_pre_disaster.json  labels/<id>_post_disaster.json
  ```
- **Format des labels** : JSON avec `features.xy[]`, chaque feature ayant un polygone
  `wkt` (`POLYGON ((x y, x y, ...))`) et `properties.subtype` ∈ `{no-damage, minor-damage,
  major-damage, destroyed, un-classified}` (uniquement dans les labels *post_disaster* ; les
  labels *pre_disaster* ne portent que le contour du bâtiment, sans dégât).

## SARD (Search And Rescue image Dataset)

- **Publication** : Ivašić-Kos et al., publiée sur IEEE DataPort.
- **Contenu** : 1 981 images extraites de vidéos drone, personnes en situation simulée de
  recherche-sauvetage (marche, course, station debout, assise, allongée), terrain varié
  (route, carrière, herbe haute/basse, sous-bois). Classe unique : `person`.
- **Licence** : à vérifier précisément sur la page IEEE DataPort (site non accessible depuis
  l'environnement de développement utilisé pour ce projet) — citer la publication en cas
  d'utilisation, par précaution.
- **Téléchargement** :
  - Miroir Kaggle (retenu, scriptable) : https://www.kaggle.com/datasets/nikolasgegenava/sard-search-and-rescue
  - Source originale : https://ieee-dataport.org/documents/search-and-rescue-image-dataset-person-detection-sard
  - Miroir Roboflow (déjà au format YOLO) : https://universe.roboflow.com/dataset-ay6sw/sard-peykp
  - Script : `python data/scripts/download_sard.py` (nécessite un jeton API Kaggle, voir le
    script pour la procédure)
- **Structure réelle confirmée** (miroir Kaggle `nikolasgegenava/sard-search-and-rescue`,
  export Roboflow au format YOLO) : les fichiers sont extraits dans un sous-dossier
  intermédiaire `search-and-rescue/`, ex. `data/raw/sard/search-and-rescue/train/images/*.jpg`
  + `.../train/labels/*.txt`. `prepare_dataset.py` cherche récursivement le bon dossier
  (`sard/**/train`, etc.), donc peu importe où exactement il atterrit sous `data/raw/sard/`.
  Format des labels confirmé : YOLO (`<classe> <x_centre> <y_centre> <largeur> <hauteur>`,
  coordonnées normalisées [0,1], classe unique `0` = person).
  ```
  data/raw/sard/search-and-rescue/train/images/*.jpg  .../train/labels/*.txt
  data/raw/sard/search-and-rescue/valid/images/*.jpg  .../valid/labels/*.txt
  data/raw/sard/search-and-rescue/test/images/*.jpg   .../test/labels/*.txt
  ```

## C2A (Combination to Application)

Ajouté après l'étape 1 : SARD montre des personnes bien visibles sur terrain dégagé, pas des
victimes partiellement cachées sous des débris — le cas le plus critique en contexte réel de
catastrophe.

- **Publication** : Nihal et al., « UAV-Enhanced Combination to Application: Comprehensive
  Analysis and Benchmarking of a Human Detection Dataset for Disaster Scenarios ».
- **Contenu** : dataset **synthétique** — poses humaines (LSP/MPII-MPHB) incrustées sur des
  fonds de catastrophe réels du dataset AIDER (incendie/fumée, inondation, bâtiment
  effondré/décombres, accident de la route). 10 215 images, plus de 360 000 personnes
  annotées, poses variées (debout, assise, allongée, à genoux, penchée) — y compris des
  occlusions partielles par les débris. Classe unique : `person`. Une variante enrichie
  ajoute une 6e colonne de pose (0=Bent, 1=Kneeling, 2=Lying, 3=Sitting, 4=Upright), non
  exploitée par notre pipeline pour l'instant (colonnes en plus ignorées par le parseur YOLO
  standard).
- **Licence** : non précisée par les auteurs.
- **Téléchargement** :
  - Miroir Kaggle (retenu) : https://www.kaggle.com/datasets/rgbnihal/c2a-dataset
  - Source originale (GitHub) : https://github.com/Ragib-Amin-Nihal/C2A
  - Script : `python data/scripts/download_c2a.py` (même méthode que SARD, jeton API Kaggle)
- **Structure attendue** (`data/raw/c2a/`), même format YOLO que SARD :
  ```
  train/images/*.jpg   train/labels/*.txt
  val/images/*.jpg     val/labels/*.txt
  test/images/*.jpg    test/labels/*.txt
  ```
  Réutilise le même convertisseur générique que SARD
  (`_convert_yolo_person_split` dans `prepare_dataset.py`).

## Format unifié

Les quatre jeux de données sont convertis vers un format commun de type COCO par
`data/scripts/prepare_dataset.py` (catégorie `person` ajoutée pour SARD/C2A). Détail de la
décision et de la taxonomie de catégories partagée :
[`docs/decisions/2026-08-27-format-annotations-unifie.md`](decisions/2026-08-27-format-annotations-unifie.md).

## Comment récupérer les données

```bash
pip install -r requirements.txt
python data/scripts/download_rescuenet.py     # automatique
python data/scripts/download_xbd.py           # nécessite d'avoir téléchargé les .tar.gz manuellement au préalable (voir ci-dessus)
python data/scripts/download_sard.py          # nécessite un jeton API Kaggle (voir le script)
python data/scripts/download_c2a.py           # nécessite un jeton API Kaggle (voir le script)
python data/scripts/prepare_dataset.py        # génère data/processed/{train,val,test}.json
```

## Limites qui restent malgré RescueNet + xBD + SARD + C2A

Même avec ces quatre jeux de données, certains manques ne sont pas comblés par un simple
téléchargement — voir `ai_detection/README.md` (section limites du modèle) : pas d'images de
nuit annotées, pas de séquences vidéo (utile pour mouvement/respiration ou suivi individuel),
pas de niveaux de gravité/triage. Ces manques nécessitent soit de l'augmentation synthétique
(faisable maintenant, voir `ai_detection/training/train.py`), soit de vraies données de
terrain ou un partenariat externe (secouristes) — reportés à une phase ultérieure du projet.

Ces cinq scripts sont écrits et testés (voir `tests/test_prepare_dataset.py`), mais le
téléchargement réel des jeux de données complets n'a pas encore été exécuté (volumes trop
importants pour l'environnement de développement actuel) — à faire sur une machine avec
suffisamment d'espace disque et un accès réseau complet.

## Statistiques et biais

À renseigner une fois les données réellement téléchargées : déséquilibre entre classes,
résolution/qualité des images, répartition géographique, biais potentiels — utile pour
interpréter les performances du modèle et documenter ses limites (étape 11).
