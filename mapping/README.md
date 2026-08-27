# mapping — Photogrammétrie et cartographie

Statut : à faire (étapes 3-4 de la feuille de route, dépend de `ai_detection/`).

## Structure

- `photogrammetry/odm_pipeline/` : orchestration OpenDroneMap pour générer orthomosaïques et
  modèles d'élévation (DEM/DSM) à partir des images géoréférencées du drone (étape 3).
- `pathfinding/` : cartographie des chemins praticables (#5) — algorithme de coût de
  déplacement (ex. A* sur grille pondérée) à partir des masques de dégâts et du DEM.
- `risk_zones/` : détection de zones dangereuses (#6) — inondation, effondrement, pente,
  combinant sorties du modèle IA (`ai_detection/`) et données d'élévation.
- `terrain_history/` : suivi de l'évolution du terrain dans le temps (#7) — comparaison
  d'orthomosaïques entre plusieurs passages du drone.
- `building_3d/` : carte 3D d'accessibilité des bâtiments (#15) — à partir du nuage de points
  photogrammétrique.

## Dépendances

- Entrée : détections IA (`ai_detection/`), images géoréférencées (drone réel ou données
  d'exemple en attendant).
- Sortie : consommée par `prioritization/` et `dashboard/`.

Aucun pipeline n'est encore implémenté : ce module ne contient que sa structure à ce stade.
