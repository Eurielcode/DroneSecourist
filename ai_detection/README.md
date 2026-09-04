# ai_detection — Modèle IA multi-classes

Statut : **en cours** (étape 2). Pipeline d'entraînement écrit et validé de bout en bout
(export YOLO + entraînement + évaluation testés avec un vrai mini-entraînement sur données
synthétiques). Entraînement réel sur les données de l'étape 1 pas encore lancé.

## Rôle

Entraîner et exécuter un modèle de détection multi-classes sur les images aériennes, à partir
des données unifiées de l'étape 1 (RescueNet + xBD + SARD, `data/processed/*.json`), pour
alimenter les modules de cartographie et de priorisation.

## Structure

- `configs/` : `dataset.yaml` généré par `training/prepare_yolo_dataset.py` (config
  Ultralytics, gitignoré car il contient un chemin absolu propre à chaque machine).
- `training/` :
  - `prepare_yolo_dataset.py` : convertit `data/processed/{train,val,test}.json` (format
    unifié COCO de l'étape 1) vers un dataset au format YOLO. Les images ne sont pas copiées
    mais liées en dur (hard link) vers `data/raw/` pour ne pas doubler l'espace disque déjà
    occupé par les données brutes (plusieurs dizaines de Go).
  - `train.py` : entraînement via Ultralytics YOLO (YOLOv8/v11 selon les poids de départ
    choisis).
  - `evaluate.py` : évaluation d'un modèle entraîné (mAP, précision/rappel par classe) sur un
    split donné.
- `dataset/` : sortie de `prepare_yolo_dataset.py` (gitignoré).
- `models/` : checkpoints entraînés (gitignoré, trop volumineux pour git).
- `inference/` : un module par fonctionnalité livrée, chacun consommant le(s) modèle(s)
  entraîné(s) — **pas encore implémentés**, dépendent d'un premier modèle entraîné :
  - `detect_victims.py` — détection de victimes (#1), version dégradée RGB+IA (pas de caméra
    thermique sur le DJI Mini 3 Pro).
  - `night_mode.py` — mode nuit (#19), dégradé RGB+IA (amélioration basse lumière).
  - `microdisplacement.py` — micro-mouvements/respiration (#2), **axe expérimental**, non
    garanti fiable (voir `docs/architecture.md`, section limites).
  - `crowd_estimation.py` — estimation du nombre de personnes dans une zone (#16).
  - `terrain_damage.py` — dégâts de bâtiments / zones dangereuses, alimente `mapping/risk_zones/`
    et `mapping/building_3d/` (#6, #15).
  - `distress_signals.py` — reconnaissance de signaux de détresse visuels (#22).
  - Détection de corps sans signe de vie (#8) : intégrée à `detect_victims.py`, toujours
    formulée comme un indice de priorisation (posture/immobilité), jamais un diagnostic.

## Utilisation

```bash
pip install -r requirements.txt   # installe ultralytics (+ torch)
python ai_detection/training/prepare_yolo_dataset.py
python ai_detection/training/train.py --model yolov8n.pt --epochs 50 --imgsz 640
python ai_detection/training/evaluate.py --weights ai_detection/models/dronesecourist/weights/best.pt
```

Validé avec un mini-entraînement réel (1 epoch, données synthétiques) : le pipeline
construit bien un modèle à 11 classes, entraîne, sauvegarde des checkpoints et évalue avec
les vrais noms de catégories. L'entraînement réel sur les données de l'étape 1
(16 804 images en train) n'a pas encore été lancé — nécessite une machine avec de préférence
un GPU (l'entraînement CPU serait très long sur ce volume).

## Dépendances

- Données préparées par `data/` (étape 1, terminée).
- Résultats consommés par `mapping/` et `prioritization/` (étape 4).
