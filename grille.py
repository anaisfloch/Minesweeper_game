# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 09:05:11 2025

@author: afloch
"""

### Imports ###
import numpy as np
from abc import abstractmethod

### Définition d'une grille de jeu ###

class Grille():
    
    def __init__(self, grille, taille, bombe, difficulte):
        """Initialise la grille de jeu du démineur avec une certaine 
        taille et un nombre de bombes en fonction de la difficulté choisie.
        
        Paramètres
        ---------
        grille : array
            Matrice vide représentant la grille de jeu.
        taille : tuple
            Longeur et largeur de la grille.
        bombe : int
            Nombre de bombes présentes dans la grille.
        difficulte : int
            Codes de difficulté :
                0 - facile, 8x8, 10 bombes
                1 - moyen, 16x16, 40 bombes
                2 - difficile, 30x16, 99 bombes
        """
        self.difficulte = difficulte
        
        # Choix de config en fonction de la difficulté
        if difficulte == 0:
            self.taille = (8,8)
            self.bombe = 10
        elif difficulte == 1:
            self.taille = (16,16)
            self.bombe = 40
        elif difficulte == 2:
            self.taille = (16,30)
            self.bombe = 99
        else:
            raise ValueError("Le code de difficulté doit être de 0 (facile), 1 (moyen) ou 2 (difficile).")
            
        self.grille = np.empty(self.taille)
        nb_case = taille[0] * taille [1]
        #position_bombe = np.random.choice(nb_case, self.bombe, replace = False)
        

        
        for i in range(taille[0]):
            for j in range(taille[1]):
                pass
            
        pass 
        
    

### Définition d'une case de jeu ###

class Case():
    
    def __init__(self, position, drapeau = 0):
        """Initialise une case de la grille de jeu du démineur dans un 
        certain état et une position particulière.
        
        Paramètres
        ---------
        position : tuple
            Coordonnées de la case dans la grille de jeu.
        drapeau : int
            Indique la présence ou non d'un drapeau sur la case. Par défaut 
            égal à 0'
        """
        self.drapeau = drapeau
    
    @abstractmethod
    def decouvrir(case):
        pass
    
    @abstractmethod
    def drapeau(self, position):
        pass


class CaseBombe(Case):
    
    def __init__(self, position, drapeau = 0):
        super().__init__(position, drapeau = 0)
        
    def decouvrir(self, position):
        #terminer la partie sauf s'il y a déjà un drapeau = True 
        pass
    
    def drapeau(self, position):
        #ajouter un drapeau sur la case, set drapeau = True
        self.drapeau = True
        pass
    
class CaseVide(Case):
    
    def __init__(self, position, drapeau = 0):
        super().__init__(position, drapeau = 0)
        
    def decouvrir(self, position):
        #decouvrir la case et afficher le nombre de bombes proches trouvé par get_nbr_bomb()
        pass
    
    def drapeau(self, position, drapeau = 0):
        #ajouter un drapeau sur la case, set drapeau = True
        self.drapeau = True
        pass
    
    def get_nbr_bomb(self, position):
        #return le nombre de bombes environnantes
        voisins = []
        
        pass