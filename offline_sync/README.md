# offline_sync — Mode hors-ligne / réseau local

Statut : à faire (étape 6 de la feuille de route pour la validation complète).

## Rôle

Garantir que l'ensemble de la stack (base de données, backend, frontend, tuiles
cartographiques) puisse fonctionner sur un réseau local, sans accès internet — condition
réaliste sur un site de catastrophe (#24).

Prévu : déploiement via `infra/docker-compose.yml`, tuiles cartographiques pré-téléchargées,
synchronisation différée si une connexion redevient disponible.

## Dépendances

- Concerne l'ensemble de la stack `dashboard/` et `field_guidance/`.
- Configuration d'infrastructure dans [`infra/`](../infra/README.md).

Aucune configuration n'est encore implémentée : ce module ne contient que sa structure à ce
stade.
