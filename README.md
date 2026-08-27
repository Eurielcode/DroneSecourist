# DroneSecourist

Système logiciel de cartographie post-catastrophe assisté par drone, destiné à aider les
secours à localiser des victimes et identifier des chemins d'accès après une catastrophe
naturelle (inondation, séisme, glissement de terrain). Projet étudiant sur un an.

Ce README est le document de référence sur l'état du projet : il doit toujours permettre à
quiconque (l'auteur, une IA, un relecteur) de comprendre où en est le projet sans relire
l'historique des conversations. Il est mis à jour **à chaque avancée significative**, pas
seulement en fin d'étape.

## Contexte

- Le drone physique (DJI Mini 3 Pro) n'est pas encore disponible — il sera fourni par l'école
  et récupéré plus tard. Tout le travail actuel est logiciel, basé sur des données publiques
  (RescueNet, xBD).
- Contrainte matérielle importante : le DJI Mini 3 Pro n'a **pas de baie de charge utile
  modulaire** → pas de caméra thermique ni de capteur additionnel possible sur ce modèle. Les
  fonctionnalités de détection thermique et de signal téléphone sont donc traitées en version
  dégradée (caméra RGB + IA) ou mises en attente d'un futur matériel.
- Détail complet des choix techniques et de la feuille de route : voir [`ROADMAP.md`](ROADMAP.md)
  et [`docs/architecture.md`](docs/architecture.md).

## État actuel

**Phase : Étape 1 — Collecte des données publiques (RescueNet, xBD, SARD), en cours.**

- Arborescence complète du projet en place (un module par grande fonctionnalité/étape de la
  feuille de route), chaque module documenté par son propre `README.md`.
- **Étape 1 (`data/`)** : scripts de téléchargement (`download_rescuenet.py`,
  `download_xbd.py`, `download_sard.py`) et de conversion vers un format unifié de type COCO
  (`prepare_dataset.py`) écrits et **testés** (données synthétiques, voir
  `tests/test_prepare_dataset.py` — 3 tests passent ; un bug réel de calcul de bbox a été
  détecté et corrigé en cours de route). Le téléchargement réel des jeux de données complets
  n'a pas encore été effectué (volumes importants et/ou inscriptions requises) — à lancer sur
  une machine avec assez d'espace disque et un accès réseau complet.
- **Point découvert et résolu pendant la recherche** : ni RescueNet ni xBD ne contiennent
  d'annotations de personnes/victimes — seulement des dégâts de bâtiments et du terrain. Un
  troisième jeu de données, **SARD** (Search And Rescue image Dataset — personnes vues depuis
  un drone en scénario de recherche-sauvetage), a été ajouté pour couvrir les fonctionnalités
  #1, #8, #16, #22. Détails et justification du choix dans
  [`docs/datasets.md`](docs/datasets.md).
- Tous les autres modules (`ai_detection/`, `mapping/`, `dashboard/`, etc.) restent au statut
  `à faire`.

## Structure du dépôt

```
DroneSecourist/
├── docs/                  # Architecture, datasets, matériel, décisions, supports de restitution
├── data/                  # Données brutes/prétraitées (gitignorées) + scripts de collecte
├── ai_detection/          # Modèle IA multi-classes (détection victimes, dégâts, nuit, etc.)
├── mapping/               # Photogrammétrie, chemins praticables, zones à risque, 3D bâtiments
├── prioritization/        # Priorisation automatique des zones d'intervention
├── dashboard/             # Backend (API/alertes/journal) + frontend (carte, tableau de bord)
├── field_guidance/        # Guidage temps réel des secouristes au sol
├── offline_sync/          # Mode hors-ligne / réseau local
├── pipeline/              # Orchestration bout-en-bout du pipeline logiciel
├── drone_integration/     # Intégration DJI SDK (activée à réception du drone)
├── future_modules/        # Modules en attente de matériel (signal téléphone, acoustique, haut-parleur)
├── tests/                 # Tests transverses / intégration
├── notebooks/             # Prototypage rapide (Jupyter)
└── infra/                 # Docker Compose, configuration d'environnement local
```

Chaque dossier de module a son propre `README.md` avec son rôle et son statut d'avancement.

## Fonctionnalités visées (mapping module ↔ fonctionnalité)

| # | Fonctionnalité | Module | Statut |
|---|---|---|---|
| 1 | Détection thermique de victimes (dégradée RGB+IA) | `ai_detection/` | à faire |
| 2 | Détection de micro-mouvements/respiration (expérimental) | `ai_detection/` | à faire (recherche) |
| 4 | Détection de signaux de téléphone | `future_modules/phone_signal_detection/` | en attente de matériel |
| 5 | Cartographie des chemins praticables | `mapping/pathfinding/` | à faire |
| 6 | Détection de zones dangereuses | `mapping/risk_zones/` | à faire |
| 7 | Suivi de l'évolution du terrain dans le temps | `mapping/terrain_history/` | à faire |
| 8 | Détection de corps sans signe de vie | `ai_detection/` | à faire |
| 9 | Priorisation automatique des zones d'intervention | `prioritization/` | à faire |
| 10 | Guidage en temps réel des secouristes au sol | `field_guidance/` | à faire |
| 15 | Carte 3D d'accessibilité des bâtiments | `mapping/building_3d/` | à faire |
| 16 | Estimation du nombre de personnes dans une zone | `ai_detection/` | à faire |
| 17 | Suivi individuel jusqu'à l'évacuation | `dashboard/backend/` | à faire |
| 19 | Mode nuit (dégradé RGB+IA) | `ai_detection/` | à faire |
| 20 | Interface centralisée / tableau de bord | `dashboard/frontend/` | à faire |
| 21 | Alerte automatique aux secours | `dashboard/backend/` | à faire |
| 22 | Reconnaissance de signaux de détresse visuels | `ai_detection/` | à faire |
| 24 | Mode hors-ligne / réseau local | `offline_sync/` | à faire |
| 25 | Journal d'intervention automatique | `dashboard/backend/` | à faire |
| 3, 13 | Écoute acoustique, communication haut-parleur | `future_modules/` | mis de côté |

## Prochaines étapes

Alignées sur la feuille de route complète (voir [`ROADMAP.md`](ROADMAP.md)) :

1. **Collecte des données publiques** (RescueNet, xBD, SARD) — scripts prêts et testés, reste
   à lancer le téléchargement réel des trois jeux de données sur une machine adaptée.
2. Entraînement du modèle de détection IA (multi-classes).
3. Mise en place de la photogrammétrie (OpenDroneMap/WebODM) sur données d'exemple.
4. Module de cartographie et priorisation.
5. Interface de coordination (tableau de bord, alertes, journal).
6. Intégration du pipeline logiciel complet, testé avec données simulées.
7. Réception du drone réel et vérification (GPS, caméra, SDK).
8. Connexion du logiciel au drone réel.
9. Test sur site simulé.
10. Ajustement et amélioration du modèle.
11. Documentation et préparation de la restitution finale.
12. Extensions éventuelles selon matériel et partenariats disponibles.

## Journal des changements

- **2026-08-27** — Étape 1 (collecte de données), suite : ajout du jeu de données **SARD**
  (Search And Rescue image Dataset) pour combler l'absence d'annotations de personnes/victimes
  dans RescueNet/xBD — `download_sard.py`, catégorie unifiée `person` dans
  `prepare_dataset.py`, test dédié (`tests/test_prepare_dataset.py`, 3 tests passent).
  Justification du choix (vs HERIDAL/VisDrone) documentée dans `docs/datasets.md`.
- **2026-08-27** — Étape 1 (collecte de données) : recherche des sources officielles
  RescueNet/xBD (structure, classes, licences), implémentation et test des scripts de
  téléchargement (`download_rescuenet.py`, `download_xbd.py`) et de conversion vers un format
  unifié COCO (`prepare_dataset.py`), avec tests sur données synthétiques
  (`tests/test_prepare_dataset.py`). Documentation détaillée dans `docs/datasets.md` et
  décision de format dans `docs/decisions/2026-08-27-format-annotations-unifie.md`.
  **Point important** : ni RescueNet ni xBD ne couvrent la détection de personnes/victimes —
  un jeu de données complémentaire sera nécessaire.
- **2026-08-27** — Mise en place initiale du dépôt : arborescence complète des modules,
  README par module, `ROADMAP.md`, `.gitignore`, squelettes des scripts de collecte de
  données (RescueNet/xBD).
