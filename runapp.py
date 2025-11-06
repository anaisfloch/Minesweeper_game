# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 15:16:24 2025

@author: Formation
"""

import sys
from PyQt5 import QtWidgets
from model import Window


if __name__=="__main__":
    app = QtWidgets.QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
        