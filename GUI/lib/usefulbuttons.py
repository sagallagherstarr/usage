# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 11:56:16 2021

@author: scott
"""
import logging
log = logging.getLogger("main_window")
log.setLevel(logging.DEBUG)

from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
    QToolButton,
)

from PyQt6.QtGui import (
    QIcon,    
    # QAction,
)

from constants import iconHome

addItemIcon = str(iconHome / "plus-button.png")
deleteItemIcon = str(iconHome / "minus-button.png")

def createToolButton(icon, parent=None):
    log.debug("createToolButton")
    log.debug("icon is %r", icon)
    
    pixmap = icon.pixmap(16, 16)
    log.debug("icon pixmap.isNull is %r", pixmap.isNull())
    log.debug("icon pixmap size %r", pixmap.size())
    
    button = QToolButton(parent)
    button.setIcon(icon)
    
    button.setCheckable(True)
    button.setAutoRaise(True)
    
    button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
    
    log.debug("button is %r", button)

    return button

def addItemButton(slot, toolTip=None, parent=None):
    log.debug("addItemButton")
    log.debug("icon file is %s", addItemIcon)
    icon = QIcon(addItemIcon)

    button = createToolButton(icon, parent)
    
    button.setToolTip(toolTip)
    button.clicked.connect(slot)
    
    return button

def deleteItemButton(slot, toolTip=None, parent=None):
    log.debug("deleteItemButton")
    log.debug("icon file is %s", addItemIcon)
    icon = QIcon(deleteItemIcon)

    button = createToolButton(icon, parent)
    
    button.setToolTip(toolTip)
    button.clicked.connect(slot)
    
    return button