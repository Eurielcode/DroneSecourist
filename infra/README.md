# infra — Environnement local / déploiement hors-ligne

Statut : à faire (étape 6 de la feuille de route).

Ce dossier contiendra la configuration nécessaire pour faire tourner l'ensemble de la stack en
local, sans dépendance internet (voir [`offline_sync/`](../offline_sync/README.md)) :

- `docker-compose.yml` : orchestration des services (base de données PostGIS, backend,
  frontend, serveur de tuiles cartographiques locales).
- `.env.example` : variables d'environnement nécessaires (jamais de vraies valeurs commitées).

Rien n'est encore implémenté à ce stade.
