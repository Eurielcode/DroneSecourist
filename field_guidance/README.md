# field_guidance — Guidage temps réel des secouristes au sol

Statut : à faire (étape 5 de la feuille de route).

## Rôle

Fournir aux secouristes sur le terrain une vue simplifiée et actionnable (#10) :
itinéraire recommandé (à partir de `mapping/pathfinding/`), position des victimes détectées,
zones dangereuses à éviter (`mapping/risk_zones/`).

Pensé pour fonctionner sur un appareil mobile léger, connecté au réseau local du dashboard
(voir [`offline_sync/`](../offline_sync/README.md)) — pas de dépendance à une connexion
internet sur le terrain.

## Dépendances

- Entrée : `mapping/`, `prioritization/`, `dashboard/backend/` (API).

Aucune interface n'est encore implémentée : ce module ne contient que sa structure à ce stade.
