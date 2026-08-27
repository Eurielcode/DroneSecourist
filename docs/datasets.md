# Jeux de données publics

Statut : à faire (document créé à l'étape 0 ; à compléter à l'étape 1 de la feuille de route).

## RescueNet

- Jeu de données d'imagerie aérienne post-catastrophe (ouragan), annoté pour la segmentation
  sémantique de dégâts (bâtiments, routes, végétation, etc.) et la détection d'éléments
  pertinents pour les secours.
- À documenter ici une fois téléchargé : source exacte, licence, nombre d'images, résolution,
  liste des classes, répartition train/val/test.

## xBD (xView2 Building Damage)

- Jeu de données de paires d'images avant/après catastrophe, annoté pour la classification du
  niveau de dégât des bâtiments (non endommagé → détruit).
- À documenter ici une fois téléchargé : source exacte, licence, nombre d'images, classes de
  dégâts, répartition train/val/test.

## Format cible unifié

Les annotations des deux jeux de données seront converties vers un format unique (COCO ou
YOLO, à trancher à l'étape 1 selon la structure réelle des annotations) afin de pouvoir
entraîner un seul modèle multi-classes (voir `ai_detection/`).

## Statistiques et biais

À renseigner à l'étape 1 : déséquilibre entre classes, résolution/qualité des images,
répartition géographique, biais potentiels (types de catastrophes sur-représentés, conditions
d'éclairage, etc.) — utile pour interpréter les performances du modèle et documenter ses
limites dans la restitution finale (étape 11).
