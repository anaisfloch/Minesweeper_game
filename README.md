# Minesweeper_game
Minesweeper game implementation

### Projet info PPMD25 ###

### Jeu du Démineur ###
Pour lancer le jeu :
- git clone "https://github.com/anaisfloch/Minesweeper_game.git" dans un terminal
- lancer le fichier runapp.py
- l'exécuter
- choisir la difficulté souhaitée
- valider avec le bouton OK

### Principe du jeu :
Mode facile : Grille de 8x8 cases, avec 10 bombes présentes aléatoirement
Mode moyen : Grille de 16x16 cases, avec 40 bombes présentes aléatoirement
Mode difficile : Grille de 31x16 cases, avec 99 bombes présentes aléatoirement

Le but est de découvrir toutes les cases vides, c'est-à-dire qui ne contiennent pas de bombes. 
Le clic gauche permet de découvrir une case tandis que le clic droit pose un marqueur drapeau D rouge, lorsque le joueur pense q'une bombe se trouve sur la case sélectionnée.
Lorsqu'une case à proximité d'une bombe est découverte, elle indique le nombre de bombes présentes parmi ses 8 cases voisines.

La partie se termine lorsque toutes les cases vides sont découvertes ou qu'une bombe a été découverte.

### Prérequis :
Python 6.1.0

---Anaïs FLOCH
