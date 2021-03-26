# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 13:36:30 2021

@author: scott
"""

from PyQt6.QtCore import Qt

from PyQt6.QtSql import (
    QSqlDatabase,
    QSqlTableModel
)

import constants

sqlDb = None

def createDatabaseConnection():
    """Open a seconds sqlite connection to the same database
       file.
    """
    sqlDb = QSqlDatabase.addDatabase("QSQLITE")
    sqlDb.setDatabaseName(constants.dbFileName)
    sqlDb.open()

def createSqlModel(peeweeModel):
    model = QSqlTableModel()
    model.setTable(peeweeModel._meta.table_name)
    
    for idx, i in enumerate(peeweeModel._meta.sorted_fields):
        model.setHeaderData(idx, Qt.Orientations.Horizontal, i.name, role=Qt.ItemDataRole.BackgroundRole)
    
    model.select()
    
    return model
