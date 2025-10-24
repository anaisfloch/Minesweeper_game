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
    
    def __init__(self, taille, bombe):
        """Initialise la grille de jeu du démineur avec une certaine 
        taille et un nombre de bombes en fonction de la difficulté choisie.
        
        Paramètres
        ---------
        taille : int
            Nombre de cases présentes dans la grille.
        bombe : int
            Nombre de bombes présentes dans la grille.
        """
        pass

class Case():
    
    def __init__(self, position, drapeau = False):
        """Initialise une case de la grille de jeu du démineur dans un 
        certain état et une position particulière.
        
        Paramètres
        ---------
        position : tuple
            Coordonnées de la case dans la grille de jeu.
        drapeau : bool
            Indique la présence ou non d'un drapeau sur la case. Par défaut 
            égal à False'
        """
        self.drapeau = drapeau
    
    @abstractmethod
    def decouvrir(case):
        pass


class CaseBombe(Case):
    
    def __init__(self, position, drapeau = False):
        super().__init__(position, drapeau = False)
        
    def decouvrir(self, position):
        #terminer la partie sauf s'il y a déjà un drapeau = True 
        pass
    
    def drapeau(self, position):
        #ajouter un drapeau sur la case, set drapeau = True
        self.drapeau = True
        pass
    
class CaseVide(Case):
    
    def __init__(self, position, drapeau = False):
        super().__init__(position, drapeau = False)
        
    def decouvrir(self, position):
        #decouvrir la case et afficher le nombre de bombes proches trouvé par get_nbr_bomb()
        pass
    
    def drapeau(self, position, drapeau = False):
        #ajouter un drapeau sur la case, set drapeau = True
        self.drapeau = True
        pass
    
    def get_nbr_bomb(self, position):
        #return le nombre de bombes environnantes
        pass