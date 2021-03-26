# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 14:17:10 2021

@author: scott
"""
import logging
logging.basicConfig()

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.debug("begin main")

from datetime import datetime

from PyQt6.QtCore import (
    Qt,
    QAbstractTableModel,
    QModelIndex,
    # QVariant,
)

from PyQt6.QtGui import (
    QStandardItemModel,
    QStandardItem
)

# from PyQt6.QtWidgets import (
    # QApplication,
    # QDialog,
    # QDialogButtonBox,
    # QHBoxLayout,
    # QLabel, 
    # QMainWindow,
    # # QMessageBox,
    # QPushButton,
    # QStandardItemModel,
    # QStandardItem,
    # QTableView,
    # QVBoxLayout,
    # QWidget
# )


from db import (
    registerModel, 
    DatabaseConnection
)

from db.models import ModelBase

class PeeWeeTableModel(QStandardItemModel):
    def __init__(self, modelClass : ModelBase, *args, **kwargs):
        log.debug("PeeWeeTableModel.init")
        log.debug("  modelClass is %s", modelClass.__class__)
        columns = len(modelClass._meta.sorted_fields)
        
        super(QStandardItemModel, self).__init__(0, columns, *args, **kwargs)
        self.modelClass = modelClass
        
        self.row_to_id = dict()
        self.row_count = 0
        
        # neither of these queries are active until used
        self.activeModelsOnly = self.modelClass.select().where(self.modelClass.active == True)
        self.allModels = self.modelClass.select()
        
        self.collection = None
        
        self.setCollection(self.allModels)

    def setCollection(self, query):
        self.collection = query.execute()
        
        self.row_count = len(self.collection)
        for idx, i in enumerate(self.collection):
            self.row_to_id[idx] = i.id
            self.insertRow(idx, self.modelToStandardItems(i))

    def createStandardItemByType(self, value):
        item = QStandardItem()
        item.setEditable(False)

        if isinstance(value, bool):
            item.setCheckable(True)
            if value is True:
                cs = Qt.CheckState.Checked
            else:
                cs = Qt.CheckState.UnChecked

            item.setCheckState(cs)
        else:
            if isinstance(value, datetime):
                value = str(value)

        item.setData(value, Qt.ItemDataRole.DisplayRole)

        return item

    def modelToStandardItems(self, model):
        return [ self.createStandardItemByType(model.__data__[i]) for i in model._meta.sorted_field_names ]

    def updateModel(self, modelDict : dict):
        id = modelDict.pop("id")

        existing = self.modelClass.get_by_id(id)

        if existing is not None:
            for i in model._meta.sorted_field_names[1:]:
                setattr(existing, i, existing._meta.fields[i].db_value(modelDict[i]))

        return existing

    def headerData(self, section, orientation, role):
        if orientation == Qt.Orientations.Horizontal:
            if role == Qt.ItemDataRole.DisplayRole:
                return self.modelClass.headerNames[section]
        
        if orientation == Qt.Orientations.Vertical:
            if role == Qt.ItemDataRole.DisplayRole:
                return section + 1 # row number for people
        
        return None