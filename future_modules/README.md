# future_modules — Fonctionnalités en attente de matériel

Statut : mis de côté (étape 12 de la feuille de route — extensions éventuelles).

## Contenu

- `phone_signal_detection/` : détection de signaux de téléphone (#4). Nécessite un capteur
  radio non compatible avec le DJI Mini 3 Pro (pas de baie de charge utile modulaire). Module
  à part, non prioritaire.
- `acoustic_listening/` : écoute acoustique (#3). Mis de côté pour la même raison matérielle.
- `loudspeaker_comm/` : communication directe par haut-parleur (#13). Mis de côté pour la même
  raison matérielle.

Ces modules ne seront réactivés que si le matériel évolue (nouveau drone avec charge utile
modulaire, partenariat matériel, etc.). Voir [`docs/hardware.md`](../docs/hardware.md).
