# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 09:57:30 2021

@author: scott
"""
import logging
logging.basicConfig()

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.debug("begin main")

import sys
# from pathlib import Path

from PyQt6.QtCore import (
    Qt,
    # QAbstractTableModel,
    # QModelIndex,
)

from PyQt6.QtWidgets import (
    QApplication,
    # QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    # QLabel, 
    QMainWindow,
    # QMessageBox,
    QPushButton,
    # QStandardItemModel,
    # QStandardItem,
    QStyleFactory,
    QTableView,
    # QVBoxLayout,
    QWidget
)

# from peewee import CharField

import constants

from db import (
    # registerModel,
    DatabaseConnection
)

from GUI.lib.usefulbuttons import addItemButton, deleteItemButton
from GUI.lib.usefuldialogs import SafeDeleteDlg
from GUI.lib.peeweetable import PeeWeeTableModel
# from sqlstuff import createDatabaseConnection, createSqlModel

# from db.models import ModelBase
from db.models.vendor import VendorModel

# @registerModel
# class FourWords(ModelBase):
#     word1 = CharField()
#     word2 = CharField()
#     word3 = CharField()
#     word4 = CharField()
#
#     headerNames = ModelBase.headerNames + [ "Word1", "wOrd2", "woRd3", "worD4"]
#
# log.debug("class FourWords defined, is %s", FourWords)

class TableEditor(QWidget):
    def __init__(self, model, parent=None):
        super(QWidget, self).__init__(parent=parent)
        
        log.debug("TableEditor.__init__")

        self.model = model
        log.debug("model is %s", model)
        self.qtModel = None
        self.view = None
        
        self.setupModel()
        self.setupView()
        self.setupButtons()
        self.setupLayout()

        log.debug("qtModel is %r", self.qtModel)
        
    def setupModel(self):
        self.qtModel = PeeWeeTableModel(self.model)
        log.debug("qtModel is %r", self.qtModel)
    
    def setupView(self):

        self.view = QTableView()
        self.view.setModel(self.qtModel)
        self.view.resizeColumnsToContents()
        self.view.hideColumn(0)
        self.view.setSelectionBehavior(self.view.SelectionBehavior.SelectRows)
        self.view.setEnabled(True)
        
        self.view.horizontalHeader().setVisible(True)
        self.view.verticalHeader().setVisible(True)

    def setupButtons(self):
        self.buttonBox = QDialogButtonBox(Qt.Orientations.Vertical)
        
        self.submitButton = QPushButton("Submit")
        self.submitButton.setDefault(True)
        
        self.editButton = QPushButton("&Edit row")
        self.quitButton = QPushButton("Quit")
        self.addRowButton = addItemButton(self.addBlankRow, parent=self.buttonBox)
        self.deleteRowButton = deleteItemButton(self.deleteRow, parent=self.buttonBox)
    
        self.buttonBox.addButton(self.submitButton, QDialogButtonBox.ButtonRole.ActionRole)
        self.buttonBox.addButton(self.editButton, QDialogButtonBox.ButtonRole.ActionRole)
        self.buttonBox.addButton(self.quitButton, QDialogButtonBox.ButtonRole.RejectRole)
        self.buttonBox.addButton(self.addRowButton, QDialogButtonBox.ButtonRole.ActionRole)
        self.buttonBox.addButton(self.deleteRowButton, QDialogButtonBox.ButtonRole.ActionRole)
        
        self.submitButton.clicked.connect(self.submit)
        self.editButton.clicked.connect(self.edit)
        # self.revertButton.clicked.connect(self.session.rollback)
        self.quitButton.clicked.connect(self.close)
        # self.addRowButton.clicked.connect(self.addBlankRow)
        # self.deleteRowButton.clicked.connect(self.deleteRow)
        
        # self.selfLayout.addWidget(self.buttonBox)
        
    def setupLayout(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.view)
        self.mainLayout.addWidget(self.buttonBox)
        self.setLayout(self.mainLayout)
    
    def submit(self):
        log.debug("submit clicked.")
        
        self.qtModel.submitAll()
        self.model.freshen()

    def edit(self):
        log.debug("edit clicked")

        index = self.view.currentIndex()
        row = index.row()
        log.debug("  row %d", row)

    def getRowData(self, rowNum):
        cols = self.qtModel.rowCount()

        retData = []
        for i in range(cols):
            idx = self.qtModel.index(rowNum, cols)
            rowData.append(self.qtModel.data(idx))

        return retData

    
    def addBlankRow(self):
        log.debug("addBlankRow")
        
        worked = self.qtModel.insertRow(self.qtModel.rowCount())
        log.debug("insertRow returned %s", worked)
        
        # self.qtModel.submitAll()
        # self.model.freshen()
    
    def deleteRow(self):
        # determine the currently selected row
        currentRow = self.view.currentIndex()
        log.debug("currentRow is %s", currentRow)
        
        yesno = SafeDeleteDlg.get_safe_confirmation_dialog("Delete row %d?" % currentRow.row())
        log.debug("yesno is %s", yesno)
        
        self.qtModel.removeRow(currentRow.row())
        self.qtModel.submitAll()
        self.model.freshen()
        
class TestDataTable:
    def __init__(self):
        self.defineDatabase()
        self.checkDatabase()

    def defineDatabase(self):      
        # testData = FourWords.create(word1="how",
        #                      word2="now",
        #                      word3="brown",
        #                      word4="cow")
        #
        # t2 = FourWords.create(word1="my",
        #                       word2="cat",
        #                       word3="is",
        #                       word4="hat")
        #
        # t3 = FourWords.create(word1="pig",
        #                       word2="likes",
        #                       word3="to",
        #                       word4="eat")

        t1 = VendorModel(name="Friendly",
                      identifier="FRIENDLY",
                      description="Bob's yer log",
                      contact="541-888-9999",
                      status="Active",
                      url_template="https://one.two.three/",
                      requester_id="sgs",
                      customer_id="13759",
                      requester_name="tink tank",
                      customer_name="Bob's fishing",
                      user_name="orville",
                      password="encinada",
                      requester_email="trouble@example.com",
                      api_key="",
                      platform="Quisling Productions")

        t2 = VendorModel(name="Second Vendor",
                      identifier="UNFRIENDLY",
                      description="go away",
                      contact="hah! as if",
                      status="None of your business",
                      url_template="https://find.your.karma/elsewhere",
                      requester_id="slinker",
                      customer_id="stinker",
                      requester_name="sly",
                      customer_name="Stinker, I told you!",
                      user_name="blinky",
                      password="",
                      requester_email="",
                      api_key="",
                      platform="")

        t3 = VendorModel(name="Thames & Hudson",
                      identifier="T&H",
                      description="another vendor",
                      contact="",
                      status="",
                      url_template="",
                      requester_id="circ1234",
                      customer_id="177502",
                      requester_name="",
                      customer_name="",
                      user_name="",
                      password="",
                      requester_email="njlemon@newjersey.com",
                      api_key="",
                      platform="")

        with dbConnection.contextManager():
            t1.save()
            t2.save()
            t3.save()
        
    def checkDatabase(self):
        log.debug("TestDataTable.checkDatabase:")
        
        with dbConnection.contextManager():
            query = VendorModel.select()
        
        results = list(query)
        log.debug("results is %s", results)
        
# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.db = TestDataTable()

        self.setWindowTitle("My Awesome App")
        
        self.createTableView()
        self.setCentralWidget(self.tableView)
        
    def createTableView(self):    
        log.debug("MainWindow.createTableView")
        self.tableView = TableEditor(VendorModel, parent=self)
        log.debug("self.tableView is %s", self.tableView)
        
        self.tableView.show()
        
if __name__ == "__main__":
    dbConnection = DatabaseConnection(constants.dbFileName)
    
    dbConnection.prepareConnection()
    dbConnection.createTables(drop_first=True)
    
    app = QApplication(sys.argv)
    
    ff = QStyleFactory.create("fusion")
    app.setStyle(ff)
    
    window = MainWindow()
    window.show()
    
    status = app.exec()
    
    dbConnection.closeConnection()

    sys.exit(status)