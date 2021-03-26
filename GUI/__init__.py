#
# GUI.__init__
# Contains ActiveRecordEditorDialog as the base for all editor windows
#

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

EditorItem = namedtuple("EditorItem", ["dataName", "labelText", "editWidget"])


def prepLineEditPairs(pwModel):
    retList = []

    for i in pwModel.getDataAsList()[3:]:  # list of Value tuples
        label = i.headerName
        lineEdit = QLineEdit(contents=i.data)

        retList.append(EditorItem(i.fieldName, label, lineEdit))
        retDict[i.fieldName] = lineEdit

    return retList


class ActiveRecordEditorDialog(QDialog):
    updateActiveState = Signal()

    def __init__(self, pwModel, *args, **kwargs):
        """Dialog superclass for handling active record style
           editors. Provides a top-level VBox layout, into
           which it places an record id label, and
           a checkbox for active/inactive, and provides a
           way to fill the inactive date label when the checkbox
           is unchecked/the record is inactive.

           Editors should set their forms up as a widget,
           attach their layouts to that widget,
           and then use self.mainLayout.addWidget to add
           their content to this base.
        """
        super(ActiveRecordEditorDialog, self).__init__(*args, **kwargs)

        self.model = pwModel

        # operate only on our field modelData, until we decide to save and exit
        self.modelData = self.model.__data__.copy()

        self.editWidgets = {}  # { fieldName: editWidget / labelWidget for display-only }

        self.content = QWidget(parent=self)

        self.mainLayout = QVBoxLayout(self.content)
        self.content.setLayout(self.mainLayout)

        self.mainLayout.addWidget(self.createActiveRecordWidget())
        self.mainLayout.addWidget(self.createContentWidget())
        self.mainLayout.addWidget(self.createButtonBar())

        self.updateActiveState.connect(self.activeStateChanged)

        self.revertModel()

    def createWidgets(self):
        # child classes call super() on this method to handle the
        self.editWidgets["id"] = QLabel()

        self.editWidgets["active"] = QCheckBox("Record is active")
        self.editWidgets["active"].connect(self.setActiveState)

        self.editWidgets["inactive_date"] = QLabel()

    @Slot
    def revertModel(self):
        self.modelData = self.model.__data__.copy()

        for i in self.modelData:
            w = self.editWidgets[i]
            d = self.modelData[i]

            if i == "active":
                self.setActiveState(d)
            elif isinstance(d, datetime.datetime):
                w.setText(str(d))
            else:
                w.setText(d)

    def createActiveRecordWidget(self):
        self.createWidgets()  # automagically create all of our edit/display widgets

        self.recordBox = QGroupBox("Record")
        self.recordBoxLayout = QGridLayout()
        self.recordBox.addLayout(self.recordBoxLayout)

        self.recordBoxLayout.addWidget(self.editWidgets["id"], 0, 0)
        self.recordBoxLayout.addWidget(self.editWidgets["active"], 1, 0)
        self.recordBoxLayout.addWidget(self.self.editWidgets["inactive_date"], 1, 1)

        return self.recordBox

    def saveEditsToModel(self):
        log.debug("ActiceRecordEditDialog.saveEditsToModel")

        self.editWidgets.pop("id")

        for i in self.editWidgets:
            setattr(self.model, i, self.editWidgets[i].text)

    def createContentWidget(self):
        # child classes must implement this function
        # to see their content
        self.editorContentWidget = QWidget()

    def createButtonBar(self):
        self.buttonBar = QWidget()
        self.buttonBarLayout = QHBoxLayout()

        self.okButton = QPushButton(text="Ok")
        self.revertButton = QPushButton(text="Revert")
        self.cancelButton = QPushButton(text="Cancel")

        self.buttonBarLayout.addWidget(self.okButton)
        self.buttonBarLayout.addWidget(self.revertButton)
        self.buttonBarLayout.addWidget(self.cancelButton)

        self.okButton.clicked.connect(self.okAction)
        self.revertButton.clicked.connect(self.revertAction)
        self.cancelButton.clicked.connect(self.cancelAction)

        return self.buttonBar

    def okAction(self):
        log.debug("ActiveRecordEditorDialog: clicked ok")

    def revertAction(self):
        log.debug("ActiveRecordEditorDialog: clicked revert")
        self.revertModel()

    def cancelAction(self):
        log.debug("ActiveRecordEditorDialog: clicked cancel")

    def setActiveState(self, newValue=None):
        if newValue == 1:
            newValue = True

        if newValue == 0:
            newValue = False

        if newValue is None:  # just flip the state
            if isinstance(self.model.active, bool):
                self.model.active = not self.model.active
        else:
            self.model.active = newValue

        if self.model.active is False:
            if self.model.inactiveDate is None:
                self.model.inactiveDate = datetime.datetime.now()
        else:
            self.model.inactiveDate = None

        self.updateActiveState.emit()

    @Slot()
    def activeStateChanged(self):
        if self.model.active:
            self.activeCheckBox.setChecked(True)
            self.activeLabel.setText(None)
        else:
            self.activeCheckBox.setChecked(False)
            self.activeLabel.setText(str(self.model.inactiveDate))
