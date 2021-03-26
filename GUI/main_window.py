# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 17:52:00 2021

@author: scott
"""
import logging
log = logging.getLogger("main_window")
log.setLevel(logging.DEBUG)
log.debug("starting")

from pathlib import Path

from PyQt6.QtWidgets import (
    QLabel, 
    QMainWindow, 
    QToolBar, 
    # QAction,
    QStatusBar,
)

from PyQt6.QtGui import (
    QIcon,    
    QAction,
)
    
from PyQt6.QtCore import Qt, QSize

from constants import iconHome

buttonIconFile = str(iconHome / "auction-hammer--arrow.png")

log.debug("buttonIconFile is %s", buttonIconFile)

# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        log.debug("MainWindow.__init__")
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("USAGE - COUNTER usage statistics")

        
        self.toolbar = self.setupToolBar()  
        button_action = self.setupActionButton()
        
        self.toolbar.addAction(button_action)
        
        self.setStatusBar(QStatusBar(self))
        
        self.createMainWindowContent()
    
    def createMainWindowContent(self):
        label = QLabel("This is a PyQt6 window!")

        # The `Qt` namespace has a lot of attributes to customise
        # widgets. See: http://doc.qt.io/qt-5/qt.html
        label.setAlignment(Qt.Alignment.AlignCenter)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(label)

    def onMyToolBarButtonClick(self, s):
        print("click", s)
        
    def setupToolBar(self):
        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(32, 32))
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonFollowStyle)
        self.addToolBar(toolbar)
        
        return toolbar
    
    def setupActionButton(self):
        # we assume toolbar has already been set up
        icon = QIcon(str(buttonIconFile))

        button_action = QAction(icon, "Your button", self)
        
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        button_action.setCheckable(True)
        
        return button_action
        
    
def setupMainWindow():
    log.debug("setupMainWindow")
    return MainWindow()