# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 19:16:20 2021

@author: scott
"""

import logging
logging.basicConfig()

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.debug("begin usefuldialogs.py")

import sys

from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel, 
    QMainWindow,
    # QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget
)

from PyQt6.QtCore import Qt

class SafeDeleteDlg(QDialog):
    def __init__(self, i_description_str: str, i_parent=None) -> None:
        super(SafeDeleteDlg, self).__init__(i_parent)
        
        self.setModal(True)

        vbox = QVBoxLayout(self)

        self.description_qll = QLabel(i_description_str)
        vbox.addWidget(self.description_qll)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButtons.Ok | QDialogButtonBox.StandardButtons.Cancel,
            Qt.Orientations.Horizontal,
            self
        )
        vbox.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        # -accept and reject are "slots" built into Qt

    @staticmethod
    def get_safe_confirmation_dialog(i_description_str: str) -> bool:
        log.debug("get_safe_confirmation_dialog")
        
        confirmation_result_bool = False
        dialog = SafeDeleteDlg(i_description_str)
        dialog.exec()
        dialog_result = dialog.result()
        
        if dialog_result == QDialog.DialogCode.Accepted.value:
            confirmation_result_bool = True
        
        return confirmation_result_bool
