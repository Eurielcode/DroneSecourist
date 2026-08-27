# ai_detection — Modèle IA multi-classes

Statut : à faire (étape 2 de la feuille de route, dépend de l'étape 1 — collecte de données).

## Rôle

Entraîner et exécuter un modèle de détection/segmentation multi-classes sur les images
aériennes, à partir de RescueNet et xBD, pour alimenter les modules de cartographie et de
priorisation.

## Structure

- `configs/` : hyperparamètres, liste des classes, chemins de données.
- `training/` : scripts d'entraînement (`train.py`) et d'évaluation (`evaluate.py`).
- `inference/` : un module par fonctionnalité livrée, chacun consommant le(s) modèle(s)
  entraîné(s) :
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

## Dépendances

- Données préparées par `data/` (étape 1).
- Résultats consommés par `mapping/` et `prioritization/` (étape 4).

Aucun modèle n'est encore entraîné : ce module ne contient que sa structure à ce stade.
