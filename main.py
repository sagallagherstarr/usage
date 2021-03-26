# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 11:27:55 2021

@author: scott

main.py

Set up the application (a Qt5 application)
Also set up to test
"""

import logging
logging.basicConfig()

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.debug("begin main")

import sys

from PyQt6.QtWidgets import (
    QApplication,
    QStyleFactory,
)

from GUI.main_window import setupMainWindow

masterApp = None

class MasterApp:
    def __init__(self, *args, **kwargs):
        log.debug("MasterApp.__init__")
        self.app = QApplication(*args)
        ff = QStyleFactory.create("fusion")
        app.setStyle(ff)

        self.mainWindow = setupMainWindow()
    
    def getMainWindow(self):
        log.debug("MasterApp.getMainWindow")
        return self.mainWindow
    
    def showMainWindow(self):
        log.debug("MasterApp.showMainWindow")
        if self.mainWindow is not None:
            self.mainWindow.show()
    
    def startApp(self):
        log.debug("MasterApp.startApp")
        if self.app is not None:
            log.debug("self.app is not None")
            self.showMainWindow()
            self.app.exec()
        else:
            log.debug("self.app is None")

def setupMasterApp(*args, **kwargs):
    log.debug("setupMasterApp")
    return MasterApp(*args, **kwargs)
    

if __name__ == "__main__":
    log.debug("main startup")
    masterApp = setupMasterApp(sys.argv)
    masterApp.startApp()

    

