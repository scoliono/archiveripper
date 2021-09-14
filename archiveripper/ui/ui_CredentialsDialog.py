# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CredentialsDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_CredentialsDialog(object):
    def setupUi(self, CredentialsDialog):
        if not CredentialsDialog.objectName():
            CredentialsDialog.setObjectName(u"CredentialsDialog")
        CredentialsDialog.resize(400, 100)
        self.verticalLayout = QVBoxLayout(CredentialsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.email = QLineEdit(CredentialsDialog)
        self.email.setObjectName(u"email")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.email)

        self.label = QLabel(CredentialsDialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.label_2 = QLabel(CredentialsDialog)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.password = QLineEdit(CredentialsDialog)
        self.password.setObjectName(u"password")
        self.password.setEchoMode(QLineEdit.Password)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.password)


        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(CredentialsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(CredentialsDialog)
        self.buttonBox.accepted.connect(CredentialsDialog.accept)
        self.buttonBox.rejected.connect(CredentialsDialog.reject)

        QMetaObject.connectSlotsByName(CredentialsDialog)
    # setupUi

    def retranslateUi(self, CredentialsDialog):
        CredentialsDialog.setWindowTitle(QCoreApplication.translate("CredentialsDialog", u"Enter Archive.org Credentials", None))
        self.label.setText(QCoreApplication.translate("CredentialsDialog", u"Archive.org email:", None))
        self.label_2.setText(QCoreApplication.translate("CredentialsDialog", u"Password:", None))
    # retranslateUi

