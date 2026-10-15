# AstroSim

AstroSim est une simulation gravitationnelle en 2D écrite en Python avec
Pygame. Elle affiche un système planétaire et permet d'ajouter des corps
célestes pendant l'exécution.

## Fonctionnalités

- Initialisation d'une étoile et des planètes du système solaire.
- Calcul des interactions gravitationnelles entre les corps.
- Création d'une planète à la position du curseur avec un clic gauche.
- Création d'un trou noir à la position du curseur avec la touche `B`.
- Transfert de masse lorsque deux corps entrent en contact.
- Affichage plein écran et traces des trajectoires.

## Prérequis

- Python 3
- Pygame

## Installation et lancement

Depuis la racine du projet, crée un environnement virtuel et installe Pygame :

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pygame
```

Lance ensuite la simulation :

```bash
python engine.py
```

Sous Windows, active l'environnement avec `.venv\Scripts\activate` puis
lance `python engine.py`.

## Commandes

| Action | Commande |
| --- | --- |
| Ajouter une planète à la position du curseur | Clic gauche |
| Ajouter un trou noir à la position du curseur | `B` |
| Quitter la simulation | `Échap` ou fermeture de la fenêtre |

La simulation s'ouvre en plein écran.

## Structure du projet

```text
.
├── constantes.py       # Paramètres de simulation et corps initiaux
├── engine.py            # Boucle principale, événements et affichage
└── models/
    ├── planete.py       # Physique et rendu des planètes
    └── vaisseau.py      # Modèle de vaisseau et de ses destinations
```

Le modèle de vaisseau est défini dans `models/vaisseau.py`, mais n'est pas
encore utilisé par la boucle principale.

## Configuration

Les paramètres modifiables se trouvent dans `constantes.py`, notamment la
fréquence d'affichage, la vitesse de simulation, la gravitation, les couleurs,
les caractéristiques des corps créés et les données du système initial.