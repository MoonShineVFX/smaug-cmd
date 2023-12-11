# -*- coding: utf8 -*-
from typing import Optional

from PySide6.QtCore import Signal, Slot, Qt, QSettings
from PySide6.QtWidgets import QDialog, QMessageBox, QLineEdit, QPushButton
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QFormLayout


class LogInDialog(QDialog):
    accountInfoRetrieved = Signal(str, str)
    loginCanceled = Signal()
    _section_name = "smaugLoginDialog"

    def __init__(self, parent=None, settings: Optional[QSettings] = None):
        super(LogInDialog, self).__init__(parent)
        self._settings = settings

        self.setWindowTitle("Log in")
        self.username_lineedit = QLineEdit("")
        self.remember_me_checkbox = QCheckBox()
        self.password_lineedit = QLineEdit("")

        self.password_lineedit.setEchoMode(QLineEdit.EchoMode.Password)
        self.log_in_button = QPushButton("Log in")
        self.log_in_button.clicked.connect(self.logIn)
        self.log_in_button.setDefault(True)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.rejected.connect(self.onRejection)
        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(self.log_in_button)
        hbox_layout.addWidget(self.cancel_button)
        form_layout = QFormLayout()
        form_layout.addRow("Username: ", self.username_lineedit)
        form_layout.addRow("Remember me: ", self.remember_me_checkbox)
        form_layout.addRow("Password: ", self.password_lineedit)
        form_layout.addRow(hbox_layout)
        self.setLayout(form_layout)
        self._read_settings()

    def _read_settings(self):
        if not self._settings:
            return
        remember_me = self._settings.value(self._section_name + "/remember_me", None)
        if remember_me == "true":
            self.remember_me_checkbox.setCheckState(Qt.CheckState.Checked)
            username = self._settings.value(self._section_name + "/username", None)
            if username:
                self.username_lineedit.setText(str(username))
            self.password_lineedit.setFocus(Qt.FocusReason.OtherFocusReason)
        else:
            self.remember_me_checkbox.setCheckState(Qt.CheckState.Unchecked)

    def _write_settings(self):
        if not self._settings:
            return
        key_remember = self._section_name + "/remember_me"
        key_username = self._section_name + "/username"
        self._settings.setValue(key_remember, self.remember_me_checkbox.isChecked())
        if self.remember_me_checkbox.isChecked():
            self._settings.setValue(key_username, self.username_lineedit.text())
        else:
            self._settings.remove(key_username)

    @Slot()
    def logIn(self):
        username = self.username_lineedit.text()
        if len(username) == 0:
            message_box = QMessageBox()
            message_box.setWindowTitle(self.tr("Error"))
            message_box.setText(self.tr("User name not specified"))
            message_box.exec_()
            return
        password = self.password_lineedit.text()
        if len(password) == 0:
            message_box = QMessageBox()
            message_box.setWindowTitle(self.tr("Error"))
            message_box.setText(self.tr("Password is missing"))
            message_box.exec_()
            return

        self.accountInfoRetrieved.emit(username, password)

    @Slot()
    def onRejection(self):
        self.loginCanceled.emit()

    def closeEvent(self, *args, **kwargs):
        self._write_settings()
        return QDialog.closeEvent(self, *args, **kwargs)

