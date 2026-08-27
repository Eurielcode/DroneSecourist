# Architecture technique

Statut : à faire (document créé à l'étape 0, à compléter progressivement).

## Vue d'ensemble

Le pipeline logiciel est prévu en 5 grandes étapes de traitement :

```
Images drone (ou dataset public)
        │
        ▼
  ai_detection/      → détections multi-classes par image (victimes, dégâts, obstacles...)
        │
        ▼
  mapping/photogrammetry/  → orthomosaïque + modèle d'élévation (DEM/DSM) à partir des images géoréférencées
        │
        ▼
  mapping/ (pathfinding, risk_zones, terrain_history, building_3d)
        │
        ▼
  prioritization/    → score composite par zone
        │
        ▼
  dashboard/backend/ → API, alertes, journal, suivi
        │
        ▼
  dashboard/frontend/ + field_guidance/ → visualisation et guidage terrain
```

`pipeline/orchestrator.py` (étape 6 de la feuille de route) enchaînera ces étapes de bout en
bout, d'abord sur données simulées, puis sur le flux réel du drone (étape 8).

## Choix techniques

- **Langage principal** : Python (PyTorch/Ultralytics pour l'IA, scripts d'orchestration
  OpenDroneMap, FastAPI pour le backend).
- **Détection IA** : YOLOv8/v11 pour la détection multi-classes ; segmentation sémantique
  (U-Net/DeepLabV3) pour les masques de dégâts issus de xBD. Export ONNX prévu pour un futur
  déploiement embarqué.
- **Photogrammétrie** : OpenDroneMap (CLI), avec possibilité d'évoluer vers WebODM (interface
  web) une fois le pipeline validé sur données d'exemple.
- **Géodonnées** : PostgreSQL + PostGIS pour stocker zones, chemins, victimes détectées et
  scores de priorité ; export GeoJSON/MBTiles pour les cartes hors-ligne.
- **Dashboard** : backend FastAPI (API REST + WebSocket pour les alertes temps réel),
  frontend React/Vite avec carte Leaflet/MapLibre (compatible tuiles hors-ligne).
- **Mode hors-ligne (#24)** : l'ensemble de la stack (base de données, backend, frontend) doit
  pouvoir tourner en local via Docker Compose, sans dépendance à un réseau internet, avec des
  tuiles cartographiques pré-téléchargées.
- **Intégration drone** : DJI Mobile SDK V5, développée uniquement à réception du matériel
  (étape 7 de la feuille de route), dans un module isolé (`drone_integration/`) pour ne pas
  bloquer le développement logiciel en attendant.

## Limites techniques assumées

- **Détection thermique (#1) et mode nuit (#19)** : le DJI Mini 3 Pro n'a pas de caméra
  thermique ni de baie modulaire pour en ajouter une. Ces fonctionnalités sont donc
  implémentées en version dégradée (caméra RGB + modèles d'amélioration d'image en basse
  lumière / détection de silhouettes), avec une qualité de détection nécessairement inférieure
  à un vrai capteur thermique. À réévaluer si le matériel change (étape 12).
- **Micro-mouvements / respiration (#2)** : détecter un mouvement de quelques millimètres
  (respiration) depuis une caméra RGB aéroportée à distance est un problème de recherche non
  résolu de façon fiable en conditions réelles (vent, vibrations du drone, distance). Ce module
  est traité comme un axe expérimental (ex. amplification vidéo eulérienne), pas comme une
  fonctionnalité livrable garantie.
- **Détection de corps sans signe de vie (#8)** : un modèle de vision ne peut donner qu'un
  indice de posture/immobilité prolongée, jamais un diagnostic médical. Cette sortie est
  toujours présentée comme une aide à la priorisation des secours, jamais comme un verdict.
- **Signal téléphone (#4)** : nécessite un capteur radio non compatible avec le DJI Mini 3 Pro
  (pas de charge utile modulaire). Traité comme module séparé (`future_modules/`), non
  prioritaire tant que le matériel n'évolue pas.
