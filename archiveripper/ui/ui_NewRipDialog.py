# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'NewRipDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_NewRipDialog(object):
    def setupUi(self, NewRipDialog):
        if not NewRipDialog.objectName():
            NewRipDialog.setObjectName(u"NewRipDialog")
        NewRipDialog.resize(400, 137)
        self.verticalLayout = QVBoxLayout(NewRipDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(NewRipDialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.label_2 = QLabel(NewRipDialog)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.label_3 = QLabel(NewRipDialog)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_3)

        self.bookUrl = QLineEdit(NewRipDialog)
        self.bookUrl.setObjectName(u"bookUrl")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.bookUrl)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.filePath = QLineEdit(NewRipDialog)
        self.filePath.setObjectName(u"filePath")

        self.horizontalLayout.addWidget(self.filePath)

        self.fileBrowseBtn = QPushButton(NewRipDialog)
        self.fileBrowseBtn.setObjectName(u"fileBrowseBtn")

        self.horizontalLayout.addWidget(self.fileBrowseBtn)


        self.formLayout.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout)


        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(NewRipDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(NewRipDialog)
        self.buttonBox.accepted.connect(NewRipDialog.accept)
        self.buttonBox.rejected.connect(NewRipDialog.reject)

        QMetaObject.connectSlotsByName(NewRipDialog)
    # setupUi

    def retranslateUi(self, NewRipDialog):
        NewRipDialog.setWindowTitle(QCoreApplication.translate("NewRipDialog", u"New Rip", None))
        self.label.setText(QCoreApplication.translate("NewRipDialog", u"Paste the book's URL here:", None))
        self.label_2.setText("")
        self.label_3.setText(QCoreApplication.translate("NewRipDialog", u"Save pages to:", None))
        self.bookUrl.setPlaceholderText(QCoreApplication.translate("NewRipDialog", u"https://archive.org/details/ ...", None))
        self.fileBrowseBtn.setText(QCoreApplication.translate("NewRipDialog", u"Browse...", None))
    # retranslateUi

