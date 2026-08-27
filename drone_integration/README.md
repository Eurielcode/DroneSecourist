# drone_integration — Intégration DJI SDK

Statut : bloqué, en attente de réception du drone (étapes 7-9 de la feuille de route).

## Rôle

Une fois le DJI Mini 3 Pro reçu :
- `dji_sdk/` : intégration du DJI Mobile SDK V5 (connexion à la télécommande RC N1, flux
  vidéo, télémétrie GPS/GLONASS/Galileo).
- Pont entre le flux réel du drone et le pipeline logiciel (`ai_detection/`,
  `mapping/photogrammetry/`), en remplacement des données simulées utilisées jusque-là.

Voir [`docs/hardware.md`](../docs/hardware.md) pour la checklist de vérification matérielle à
réception.

## Dépendances

Aucune tant que le drone n'est pas physiquement disponible. Le reste du pipeline logiciel est
développé et testé indépendamment (données publiques + simulation) pour ne pas être bloqué par
cette contrainte.
