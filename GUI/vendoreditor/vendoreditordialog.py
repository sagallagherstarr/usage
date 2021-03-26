# # -*- coding: utf-8 -*-
# """
# Created on Wed Mar 17 19:11:06 2021

# @author: scott
# """
import logging
logging.basicConfig()

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.debug("begin main")

from collections import namedtuple

import datetime

from PyQt6.QtWidgets import (
    # QApplication,
    QButtonGroup,
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    # QMainWindow,
    # QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget
)

from PyQt6.QtCore import (
    Qt,
    pyqtSignal as Signal,
    pyqtSlot as Slot
)

from GUI import ActiveRecordEditorDialog

""" name = CharField()
    identifier = CharField(unique=True)
    description = CharField(null=True)
    contact = CharField(null=True)
    status = CharField()
    url_template = CharField(null=False)
    requester_id = CharField()
    customer_id = CharField()
    requester_name = CharField()
    customer_name = CharField()
    user_name = CharField()
    password = CharField()
    requester_email = CharField()
    api_key = CharField()
    platform = CharField()

"""

class EditorWidget:
    def __init__(self, fieldName, editWidgetType, row, column, labelText=None, orientation=Qt.Orientations.Horizontal):
        # if labelText is None, no label widget will be created and the edit widget will be
        # placed at row, column.
        # if labelText is not None, the label widget will be placed at row, column and the edit
        # widget will be at the next row or column, as determined by orientation
        self.labelText = labelText
        self.editWidgetType = editWidgetType
        self.row = row
        self.column = column
        self.orientation = orientation
        self.labelWidget = None
        self.editWidget = None

    def createWidgets(self, gridLayout):
        row = self.row
        column = self.column

        if self.labelText is not None:
            self.labelWidget = QLabel()
            self.setLabelText(self.labelText)

            gridLayout.addWidget(self.lableWidget, row, column)

            if self.orientation == Qt.Orientations.Horizontal:
                column = column + 1
            elif self.orientation == Qt.Orientations.Vertical:
                row = row + 1

        self.editWidget = self.editWidgetType()
        self.gridLayout.addWidget(self.editWidget, row, column)

    def setEditWidgetContents(self, newContents):
        self.editWidget.setText(newContents)

    def setLabelText(self, newLabelText):
        self.labelWidget.setText(newLabelText)

    def getEditWidgetContents(self):
        return self.editWidget.text()

class VendorEditorDialog(ActiveRecordEditorDialog):
    def __init__(self, pwModel, selectionRow : int, *args, **kwargs):
        super(VendorEditorDialog, self).__init__(*args, **kwargs)

        self.editorBox = QGroupBox("Vendor Info", parent=self) 
        
        # formLayout = QFormLayout(parent=self.editorBox)
        # self.editorBox.setLayout(formLayout)

        self.editorWidgets = []

        for i in zip(pwModel.sorted_field_names, pwModel.headerNames)[3:]:
            self.editorWidgets.append(EditorWidget(i[0], QLineEdit, 0, 0, i[1]))

    def createContentWidget(self):
        # child classes must implement this function
        # to see their content
        super().createContentWidget()
        masterLayout = QHBoxLayout()
        editorBox = QGroupBox("Vendor Info")

        self.editorContentWidget.setLayout(masterLayout)
        masterLayout.addWidget(editorBox)

        innerLayout = QGridLayout()
        editorBox.setLayout(innerLayout)

    def okAction(self):
        log.debug("VendorEditorDialog: clicked ok")

    def revertAction(self):
        log.debug("VendorEditorDialog: clicked revert")

    def cancelAction(self):
        log.debug("VendorEditorDialog: clicked cancel")


# from db import (
#     DatabaseConnection
# )

# from db.models import VendorModel

# from GUI.lib.usefulbuttons import addItemButton, deleteItemButton

# class TableEditor(QWidget):
#     def __init__(self, modelClass, parent):
#         super(QWidget, self).__init__(parent)
        
#         log.debug("TableEditor.__init__")
        
        
#         self.modelClass = modelClass
#         self.qtModel = None
#         self.view = None
        
#         self.setupModel()
#         self.setupView()
#         self.setupButtons()
#         self.setupLayout()
        
#         self.qtModel.select()
        
#         log.debug("qtModel is %r", self.qtModel)
        
#     def setupModel(self):
#         self.qtModel = PeeWeeTableModel(self.modelClass)
#         self.qtModel.setTable(self.modelClass._meta.table_name)
        
#         self.qtModel.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        
#         for idx, i in enumerate(self.modelKlass.headerNames):
#             self.qtModel.setHeaderData(idx, Qt.Orientations.Horizontal, i)
    
#     def setupView(self):
#         self.view = QTableView()
#         # self.view = AlchemicalTableModel(session, sqlTableModel)
#         self.view.setModel(self.qtModel)
#         self.view.resizeColumnsToContents()
#         self.view.hideColumn(0)
#         self.view.setSelectionBehavior(self.view.SelectionBehavior.SelectRows)
    
#     def setupButtons(self):
#         self.buttonBox = QDialogButtonBox(Qt.Orientations.Vertical);
        
#         self.submitButton = QPushButton("Submit")
#         self.submitButton.setDefault(True)
        
#         self.revertButton = QPushButton("&Revert")
#         self.quitButton = QPushButton("Quit")
#         self.addRowButton = addItemButton(self.addBlankRow, parent=self.buttonBox)
#         self.deleteRowButton = deleteItemButton(self.deleteRow, parent=self.buttonBox)
    
#         self.buttonBox.addButton(self.submitButton, QDialogButtonBox.ButtonRole.ActionRole)
#         self.buttonBox.addButton(self.revertButton, QDialogButtonBox.ButtonRole.ActionRole)
#         self.buttonBox.addButton(self.quitButton, QDialogButtonBox.ButtonRole.RejectRole)
#         self.buttonBox.addButton(self.addRowButton, QDialogButtonBox.ButtonRole.ActionRole)
#         self.buttonBox.addButton(self.deleteRowButton, QDialogButtonBox.ButtonRole.ActionRole)
        
#         self.submitButton.clicked.connect(self.submit)
#         # self.revertButton.clicked.connect(self.session.rollback)
#         self.quitButton.clicked.connect(self.close)
#         # self.addRowButton.clicked.connect(self.addBlankRow)
#         # self.deleteRowButton.clicked.connect(self.deleteRow)
        
#     def setupLayout(self):
#         self.mainLayout = QHBoxLayout()
#         self.mainLayout.addWidget(self.view)
#         self.mainLayout.addWidget(self.buttonBox)
#         self.setLayout(self.mainLayout)
    
#     def submit(self):
#         log.debug("submit clicked.")
        
#         self.qtModel.submitAll()
#         with dbConnection.contextManager():
#             self.modelKlass.select()
    
#     def addBlankRow(self):
#         log.debug("addBlankRow")
#         # blankRecord = QSqlRecord()
        
#         worked = self.qtModel.insertRow(self.qtModel.rowCount())
#         log.debug("insertRow returned %s", worked)
        
#         # self.qtModel.insertRecord(-1, blankRecord)
#         self.qtModel.submitAll()
#         with dbConnection.contextManager():
#             self.modelKlass.select()
    
#     def deleteRow(self):
#         # determine the currently selected row
#         currentRow = self.view.currentIndex()
#         log.debug("currentRow is %s", currentRow)
        
#         yesno = SafeDeleteDlg.get_safe_confirmation_dialog("Delete row %d?" % currentRow.row())
#         log.debug("yesno is %s", yesno)
        
#         self.qtModel.removeRow(currentRow.row())
#         self.qtModel.submitAll()
#         with dbConnection.contextManager():
#             self.modelKlass.select()


# class VendorsView(QDialog):
#     def __init__(self, modelKlass, *args, **kwargs):
#         super(QDialog, self).__init__(*args, **kwargs)

#         self.model = modelKlass
#         # self.db = TestDataTable()
        
#         # self.db.checkContents()

#         self.setWindowTitle("Vendors")
        
#         self.createTableView()
#         self.setCentralWidget(self.tableView)
        
#     def createTableView(self):    
#         log.debug("VendorEditor.createTableView")
#         temp = TableEditor(self.modelKlass, self)
#         log.debug("temp is %s", temp)
#         self.tableView = TableEditor(self.modelKlass, self)
#         log.debug("self.tableView is %s", self.tableView)
        
#         self.tableView.show()
