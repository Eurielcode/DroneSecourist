"""Préparation du jeu de données unifié à partir de RescueNet et xBD.

Squelette créé à l'étape 0 de la feuille de route. À implémenter à l'étape 1 :
- conversion des annotations RescueNet et xBD vers un format unifié (COCO ou YOLO) ;
- génération des splits train/val/test ;
- calcul de statistiques de classes (déséquilibre, tailles d'image) pour docs/datasets.md.
"""


def prepare_dataset(
    raw_dir: str = "data/raw", output_dir: str = "data/processed"
) -> None:
    raise NotImplementedError("À implémenter à l'étape 1 de la feuille de route.")


if __name__ == "__main__":
    prepare_dataset()
