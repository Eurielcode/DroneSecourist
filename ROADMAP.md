# Feuille de route — DroneSecourist

Statut : `à faire` / `en cours` / `fait`. Mise à jour à chaque avancée (voir README.md).

| # | Étape | Statut | Module(s) principal(aux) |
|---|---|---|---|
| 0 | Mise en place initiale du dépôt | fait | (structure complète) |
| 1 | Collecte des données publiques (RescueNet, xBD) | en cours | `data/` |
| 2 | Entraînement du modèle de détection IA (multi-classes) | à faire | `ai_detection/` |
| 3 | Photogrammétrie (OpenDroneMap/WebODM) sur données d'exemple | à faire | `mapping/photogrammetry/` |
| 4 | Module de cartographie et priorisation | à faire | `mapping/`, `prioritization/` |
| 5 | Interface de coordination (tableau de bord, alertes, journal) | à faire | `dashboard/`, `field_guidance/` |
| 6 | Intégration du pipeline logiciel complet, testé avec données simulées | à faire | `pipeline/`, `offline_sync/`, `tests/` |
| 7 | Réception du drone réel et vérification (GPS, caméra, SDK) | à faire (bloqué : matériel non reçu) | `drone_integration/`, `docs/hardware.md` |
| 8 | Connexion du logiciel au drone réel | à faire (bloqué : matériel non reçu) | `drone_integration/` |
| 9 | Test sur site simulé | à faire (bloqué : matériel non reçu) | — |
| 10 | Ajustement et amélioration du modèle | à faire | `ai_detection/` |
| 11 | Documentation et préparation de la restitution finale | à faire | `docs/restitution/` |
| 12 | Extensions éventuelles selon matériel et partenariats disponibles | à faire | `future_modules/` |

## Détail par étape

### Étape 1 — Collecte des données publiques
- [x] Scripts de téléchargement RescueNet/xBD/**SARD** (`data/scripts/`), écrits et testés.
- [x] Conversion vers un format unifié (COCO), testée sur données synthétiques
  (`tests/test_prepare_dataset.py`, 3 tests).
- [x] Point découvert et résolu : ni RescueNet ni xBD ne contiennent d'annotations de
  personnes/victimes → **SARD** (Search And Rescue image Dataset) ajouté pour couvrir les
  fonctionnalités #1, #8, #16, #22 (catégorie unifiée `person`). Voir `docs/datasets.md`.
- [ ] Téléchargement réel des trois jeux de données complets (pas encore effectué — volumes
  importants et/ou inscriptions requises, à faire sur une machine dédiée).
- [ ] Statistiques de classes réelles consignées dans `docs/datasets.md` (après
  téléchargement).

### Étape 2 — Entraînement du modèle de détection IA
- Entraînement multi-classes (YOLOv8/v11) sur RescueNet/xBD.
- Modules d'inférence séparés par fonctionnalité : détection de victimes (#1, dégradé
  RGB+IA), mode nuit (#19, dégradé), micro-mouvements (#2, expérimental), estimation du
  nombre de personnes (#16), dégâts/zones dangereuses (#6, #15), signaux de détresse
  visuels (#22), corps sans signe de vie (#8, formulé comme indice de priorisation et non
  un diagnostic).
- Évaluation (mAP, biais dataset) et export ONNX.

### Étape 3 — Photogrammétrie
- Orchestration OpenDroneMap sur images d'exemple.
- Génération d'orthomosaïques et de modèles d'élévation (DEM/DSM).
- Documentation du pipeline (ressources, temps de calcul).

### Étape 4 — Cartographie et priorisation
- Chemins praticables (#5), zones dangereuses (#6), suivi de l'évolution du terrain (#7),
  carte 3D d'accessibilité des bâtiments (#15).
- Priorisation automatique des zones d'intervention (#9).

### Étape 5 — Interface de coordination
- Backend : alertes automatiques (#21), journal d'intervention (#25), suivi individuel
  jusqu'à l'évacuation (#17).
- Frontend : tableau de bord centralisé (#20), guidage des secouristes au sol (#10).

### Étape 6 — Intégration du pipeline complet
- Orchestrateur bout-en-bout testé sur données simulées.
- Mode hors-ligne / réseau local validé (#24).
- Tests d'intégration + CI de base.

### Étape 7-9 — Drone réel (bloquées tant que le matériel n'est pas reçu)
- Vérification matérielle (GPS, caméra, SDK), connexion du logiciel au drone, test sur site
  simulé.

### Étape 10 — Amélioration du modèle
- Fine-tuning avec les données réelles collectées lors des tests terrain.

### Étape 11 — Documentation et restitution finale
- Supports de soutenance, bilan par fonctionnalité vs feuille de route.

### Étape 12 — Extensions éventuelles
- Modules matériel-dépendants (`future_modules/`) : signal téléphone (#4), écoute
  acoustique (#3), communication haut-parleur (#13), à réévaluer selon le matériel
  disponible.
