# Matériel — DJI Mini 3 Pro

Statut : drone non encore reçu (commandé par l'école). Ce document sera complété avec les
résultats de vérification réelle à l'étape 7 de la feuille de route.

## Caractéristiques retenues

- Caméra 48MP, stabilisation 3 axes (gimbal).
- Positionnement : GPS + GLONASS + Galileo.
- Autonomie : ~34 à 47 minutes selon la version de batterie.
- Détection d'obstacles tri-directionnelle.
- Compatible SDK officiel DJI : Mobile SDK V5, télécommande DJI RC N1.

## Contrainte structurante pour le projet

**Pas de baie de charge utile modulaire** : impossible d'ajouter une caméra thermique ou tout
autre capteur additionnel sur ce modèle précis. Conséquences directes sur la conception
logicielle :

- Détection thermique de victimes (#1) et mode nuit (#19) → implémentées en version dégradée
  (caméra RGB + IA), voir `docs/architecture.md` et `ai_detection/README.md`.
- Détection de signaux de téléphone (#4) → nécessite un capteur radio non disponible sur ce
  drone ; traitée comme module séparé et non prioritaire (`future_modules/`).
- Écoute acoustique (#3) et communication haut-parleur (#13) → mises de côté pour la même
  raison, réactivables si le matériel évolue (étape 12 de la feuille de route).

## Checklist de vérification à réception (étape 7)

- [ ] Confirmer la précision GPS/GLONASS/Galileo en conditions réelles.
- [ ] Vérifier la qualité d'image et le comportement du gimbal en vol.
- [ ] Tester la connexion au DJI Mobile SDK V5 depuis la télécommande RC N1 (flux vidéo,
      télémétrie).
- [ ] Vérifier le format et le géoréférencement des photos exportées (compatibilité avec le
      pipeline de photogrammétrie `mapping/photogrammetry/`).
- [ ] Tester l'autonomie réelle en conditions de terrain.
