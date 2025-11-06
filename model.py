# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
from grille import Grille, CaseBombe, CaseVide


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1110, 878)
        
        # Zone Grille
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(180, 140, 731, 661))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.grid = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(2)
        self.grid.setObjectName("grid")
        
        # Zone titre
        self.title_text = QtWidgets.QPlainTextEdit(Dialog)
        self.title_text.setGeometry(QtCore.QRect(40, 20, 331, 51))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(21)
        font.setBold(True)
        font.setWeight(75)
        self.title_text.setFont(font)
        self.title_text.setAutoFillBackground(True)
        self.title_text.setObjectName("title_text")
        
        ### Boite de difficulté
        # Texte
        self.difficulty_text = QtWidgets.QPlainTextEdit(Dialog)
        self.difficulty_text.setGeometry(QtCore.QRect(40, 80, 100, 31)) #150 pour la largeur de la boite text
        font = QtGui.QFont("Yu Gothic UI", 11, QtGui.QFont.Bold)
        font.setFamily("Yu Gothic UI")
        self.difficulty_text.setFont(font)
        self.difficulty_text.setAutoFillBackground(True)
        self.difficulty_text.setObjectName("difficulty_text")
        
        # Choix difficulté
        self.difficulty_box_choice = QtWidgets.QComboBox(Dialog)
        self.difficulty_box_choice.setGeometry(QtCore.QRect(200, 90, 200, 22))
        self.difficulty_box_choice.setObjectName("difficulty_box_choice")
        self.difficulty_box_choice.addItems(["Facile","Moyen", "Difficile"])
        
        # Bouton valider
        self.button_validate_difficulty = QtWidgets.QPushButton(Dialog)
        self.button_validate_difficulty.setGeometry(QtCore.QRect(400, 90, 51, 23))
        self.button_validate_difficulty.setObjectName("button_validate_difficulty")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Démineur"))
        self.title_text.setPlainText(_translate("Dialog", "Minesweeper Game"))
        self.difficulty_text.setPlainText(_translate("Dialog", "Difficulté :"))
        self.button_validate_difficulty.setText(_translate("Dialog", "OK"))




class Window(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.grille_obj = None
        self.partie_terminee = False
        self.button_validate_difficulty.clicked.connect(self.start_game)
        
        
    def start_game(self):
        difficulte = self.difficulty_box_choice.currentIndex()
        self.grille_obj = Grille(difficulte)
        self.partie_terminee = False
        
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
                
                
        for i in range(self.grille_obj.taille[0]):
            for j in range(self.grille_obj.taille[1]):
                case = QtWidgets.QPushButton("")
                case.setFixedSize(35, 35)
                case.setStyleSheet("background-color: lightgray;")
                case.clicked.connect(lambda _, x = i, y = j: self.handle_left_click(x, y))
                case.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                case.customContextMenuRequested.connect(lambda _, x = i, y = j: self.handle_right_click(x, y))
                self.grid.addWidget(case, i, j)
                
        self.update_cases()
        
                
    def handle_left_click(self, x, y):
        if self.partie_terminee:
            return
        
        case = self.grille_obj.grille[x, y]
        if isinstance(case, CaseBombe):
            self.message("PERDUUUUUU ça a explosé ou quoi")
            self.reveal_all()
            self.partie_terminee = True
        else:
            case.decouvrir()
            self.update_cases()
            
            if self.check_victoire():
                self.message("GG Well played")
                self.reveal_all()
                self.partie_terminee = True
        
    def handle_right_click(self, x, y):
        if self.partie_terminee:
            return
        
        case = self.grille_obj.grille[x, y] 
        case.drapeau = 1 - case.drapeau
        self.update_cases()
        
    def update_cases(self):
        for i in range(self.grille_obj.taille[0]):
            for j in range(self.grille_obj.taille[1]):
                bouton = self.grid.itemAtPosition(i, j).widget()
                case = self.grille_obj.grille[i, j]
                
                if case.drapeau == 1:
                    bouton.setText("D")
                    bouton.setStyleSheet("background-color: #FF0000; font-weight: bold; ")
                elif not case.decouverte:
                    bouton.setText("")
                elif isinstance(case, CaseBombe):
                    bouton.setText("BOUM")
                    bouton.setStyleSheet("background-color: #FF0000; font-weight: bold; ")
                elif case.nbr_bombes_voisines > 0:
                    bouton.setText(str(case.nbr_bombes_voisines))
                    bouton.setStyleSheet("background-color: #Q8E6C9; font-weight: bold; ")
                else :
                    bouton.setText("")
                    bouton.setStyleSheet("background-color: #Q8E6C9; font-weight: bold; ")
                    
    def check_victoire(self):
        total_cases = self.grille_obj.taille[0] * self.grille_obj.taille[1]
        bombes = self.grille_obj.bombe
        if self.grille_obj.cases_decouvertes >= total_cases - bombes:
            return True
        
    def reveal_all(self):
        for i in range(self.grille_obj.taille[0]):
            for j in range(self.grille_obj.taille[1]):
                case = self.grille_obj.grille[i, j]
                case.decouverte = True
        self.update_cases()
        
        
    def message(self, titre, texte):
        message = QtWidgets.QMessageBox(self)
        message.setWindowTitle(titre)
        message.setText(texte)
        message.setIcon(QtWidgets.QMessageBox.Information)
        message.addButton("Rejouer", QtWidgets.QMessageBox.AcceptRole)
        message.addButton("Rejouer", QtWidgets.QMessageBox.RejectRole)
        choix = message.exec_()
        
        if choix == 0:
            self.start_game()
        else:
            self.close()
        
    
        