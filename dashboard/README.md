# dashboard — Interface de coordination

Statut : à faire (étape 5 de la feuille de route).

## Structure

- `backend/` (FastAPI prévu) :
  - API REST + WebSocket, modèles de données PostGIS (zones, victimes, chemins, scores).
  - `#21` Alerte automatique aux secours (déclenchée sur seuils de détection).
  - `#25` Journal d'intervention automatique (log structuré, export PDF/Markdown).
  - `#17` Suivi individuel jusqu'à l'évacuation (identifiants de détection persistés dans le
    temps).
- `frontend/` (React/Vite + Leaflet/MapLibre prévu) :
  - `#20` Tableau de bord centralisé : carte, liste des zones priorisées, alertes en direct.

Le guidage des secouristes au sol (#10) est traité dans le module séparé
[`field_guidance/`](../field_guidance/README.md), qui consomme les mêmes données que le
frontend.

## Dépendances

- Entrée : `prioritization/` (scores de zones), `ai_detection/` et `mapping/` (détections,
  cartes).
- Doit fonctionner en mode hors-ligne (voir [`offline_sync/`](../offline_sync/README.md)).

Aucun backend ni frontend n'est encore implémenté : ce module ne contient que sa structure à
ce stade.
