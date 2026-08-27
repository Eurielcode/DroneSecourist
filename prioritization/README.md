# prioritization — Priorisation automatique des zones d'intervention

Statut : à faire (étape 4 de la feuille de route).

## Rôle

Calculer un score composite par zone (#9) à partir de :
- la densité de victimes estimée (`ai_detection/inference/crowd_estimation.py`,
  `detect_victims.py`),
- la gravité des dégâts (`mapping/risk_zones/`),
- l'accessibilité (`mapping/pathfinding/`, `mapping/building_3d/`).

Le score alimente le tableau de bord (`dashboard/`) pour orienter les secours vers les zones
les plus critiques en premier.

## Dépendances

- Entrée : sorties de `ai_detection/` et `mapping/`.
- Sortie : consommée par `dashboard/backend/`.

Aucun algorithme de scoring n'est encore implémenté : ce module ne contient que sa structure à
ce stade.
