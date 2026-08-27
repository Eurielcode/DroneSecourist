# pipeline — Orchestration bout-en-bout

Statut : à faire (étape 6 de la feuille de route).

## Rôle

`orchestrator.py` enchaînera l'ensemble du pipeline logiciel : collecte d'images (simulées
d'abord, puis flux réel du drone à l'étape 8) → détection IA (`ai_detection/`) →
photogrammétrie et cartographie (`mapping/`) → priorisation (`prioritization/`) →
alimentation du tableau de bord (`dashboard/`).

Ce module sera d'abord testé avec un jeu de données simulées représentant un scénario fictif
de catastrophe, avec des tests d'intégration dans [`tests/`](../tests/README.md).

## Dépendances

Dépend de tous les autres modules logiciels (`data/`, `ai_detection/`, `mapping/`,
`prioritization/`, `dashboard/`). Ne peut être implémenté qu'une fois ces modules
fonctionnels individuellement.

Aucun orchestrateur n'est encore implémenté : ce module ne contient que sa structure à ce
stade.
