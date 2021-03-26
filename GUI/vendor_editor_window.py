# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 18:33:58 2021

@author: scott
"""

import logging
logging.basicConfig()

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.debug("begin main")

# import sys
# from pathlib import Path

from PyQt6.QtWidgets import (
    # QApplication,
    # QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    # QLabel, 
    # QMainWindow,
    # QMessageBox,
    QPushButton,
    QTableView,
    # QVBoxLayout,
    QWidget
)

from PyQt6.QtCore import Qt

from PyQt6.QtSql import (
    # QSqlDatabase,
    QSqlTableModel,
    # QSqlRecord
)

# from peewee import CharField

# import constants

from db import (
    registerModel, 
    DatabaseConnection
)

# from db.models import ModelBase


class TableEditor(QWidget):
    def __init__(self, model, parent):
        super(QWidget, self).__init__(parent)
        
        log.debug("TableEditor.__init__")
        
        self.model = model
        log.debug("model is %s", model)
        self.qtModel = None
        self.view = None
        
        self.setupModel()
        self.setupView()
        self.setupButtons()
        self.setupLayout()
        
        self.qtModel.select()
        
        log.debug("qtModel is %r", self.qtModel)
        
    def setupModel(self):
        self.qtModel = QSqlTableModel()
        self.qtModel.setTable(self.model._meta.table_name)

        print(self.qtModel.editStrategy())
        
        self.qtModel.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        
        for i, idx in enumerate(self.model.headerNames):
            self.qtModel.setHeaderData(idx + 1, Qt.Orientations.Horizontal, i)
    
    def setupView(self):
        self.view = QTableView()
        self.view.setModel(self.qtModel)
        self.view.resizeColumnsToContents()
        self.view.hideColumn(0)
    
    def setupButtons(self):
        self.submitButton = QPushButton("Submit")
        self.submitButton.setDefault(True)
        self.revertButton = QPushButton("&Revert")
        self.quitButton = QPushButton("Quit")
        self.addRowButton = QPushButton("Add new")
        self.deleteRowButton = QPushButton("Delete selected")
    
        self.buttonBox = QDialogButtonBox(Qt.Orientations.Vertical);
        self.buttonBox.addButton(self.submitButton, QDialogButtonBox.ButtonRole.ActionRole)
        self.buttonBox.addButton(self.revertButton, QDialogButtonBox.ButtonRole.ActionRole)
        self.buttonBox.addButton(self.quitButton, QDialogButtonBox.ButtonRole.RejectRole)
        self.buttonBox.addButton(self.addRowButton, QDialogButtonBox.ButtonRole.ActionRole)
        self.buttonBox.addButton(self.deleteRowButton, QDialogButtonBox.ButtonRole.ActionRole)
        
        self.submitButton.clicked.connect(self.submit)
        # self.revertButton.clicked.connect(self.session.rollback)
        self.quitButton.clicked.connect(self.close)
        self.addRowButton.clicked.connect(self.addBlankRow)
        self.deleteRowButton.clicked.connect(self.deleteRow)
        
    def setupLayout(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.view)
        self.mainLayout.addWidget(self.buttonBox)
        self.setLayout(self.mainLayout)
    
    def submit(self):
        log.debug("submit clicked.")
        
        self.qtModel.submitAll()
        with dbConnection.contextManager():
            query = FourWords.select()
    
    def addBlankRow(self):
        # blankRecord = QSqlRecord()
        
        worked = self.qtModel.insertRow(self.qtModel.rowCount())
        
        # self.qtModel.insertRecord(-1, blankRecord)
        self.qtModel.submitAll()
        with dbConnection.contextManager():
            query = FourWords.select()
    
    def deleteRow(self):
        # determine the currently selected row
        currentRow = self.view.currentIndex()
        log.debug("currentRow is %s", currentRow)
        
        yesno = SafeDeleteDlg.get_safe_confirmation_dialog("Delete row %d?" % currentRow.row())
        log.debug("yesno is %s", yesno)
        
        self.qtModel.removeRow(currentRow.row())
        self.qtModel.submitAll()
        with dbConnection.contextManager():
            query = FourWords.select()
