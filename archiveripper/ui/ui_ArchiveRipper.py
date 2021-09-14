# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ArchiveRipper.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_ArchiveRipper(object):
    def setupUi(self, ArchiveRipper):
        if not ArchiveRipper.objectName():
            ArchiveRipper.setObjectName(u"ArchiveRipper")
        ArchiveRipper.resize(640, 480)
        self.actionExit = QAction(ArchiveRipper)
        self.actionExit.setObjectName(u"actionExit")
        self.actionPreferences = QAction(ArchiveRipper)
        self.actionPreferences.setObjectName(u"actionPreferences")
        self.actionAbout = QAction(ArchiveRipper)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionNew_Rip = QAction(ArchiveRipper)
        self.actionNew_Rip.setObjectName(u"actionNew_Rip")
        self.actionOpen_Rip = QAction(ArchiveRipper)
        self.actionOpen_Rip.setObjectName(u"actionOpen_Rip")
        self.actionExport = QAction(ArchiveRipper)
        self.actionExport.setObjectName(u"actionExport")
        self.actionSave = QAction(ArchiveRipper)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSave_As = QAction(ArchiveRipper)
        self.actionSave_As.setObjectName(u"actionSave_As")
        self.centralwidget = QWidget(ArchiveRipper)
        self.centralwidget.setObjectName(u"centralwidget")
        ArchiveRipper.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(ArchiveRipper)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 640, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        ArchiveRipper.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(ArchiveRipper)
        self.statusbar.setObjectName(u"statusbar")
        ArchiveRipper.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionNew_Rip)
        self.menuFile.addAction(self.actionOpen_Rip)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionPreferences)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(ArchiveRipper)

        QMetaObject.connectSlotsByName(ArchiveRipper)
    # setupUi

    def retranslateUi(self, ArchiveRipper):
        ArchiveRipper.setWindowTitle(QCoreApplication.translate("ArchiveRipper", u"ArchiveRipper", None))
        self.actionExit.setText(QCoreApplication.translate("ArchiveRipper", u"Exit", None))
#if QT_CONFIG(shortcut)
        self.actionExit.setShortcut(QCoreApplication.translate("ArchiveRipper", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.actionPreferences.setText(QCoreApplication.translate("ArchiveRipper", u"Preferences...", None))
#if QT_CONFIG(shortcut)
        self.actionPreferences.setShortcut(QCoreApplication.translate("ArchiveRipper", u"Ctrl+,", None))
#endif // QT_CONFIG(shortcut)
        self.actionAbout.setText(QCoreApplication.translate("ArchiveRipper", u"About", None))
        self.actionNew_Rip.setText(QCoreApplication.translate("ArchiveRipper", u"New Rip...", None))
        self.actionOpen_Rip.setText(QCoreApplication.translate("ArchiveRipper", u"Open Rip...", None))
        self.actionExport.setText(QCoreApplication.translate("ArchiveRipper", u"Export...", None))
        self.actionSave.setText(QCoreApplication.translate("ArchiveRipper", u"Save", None))
        self.actionSave_As.setText(QCoreApplication.translate("ArchiveRipper", u"Save As...", None))
        self.menuFile.setTitle(QCoreApplication.translate("ArchiveRipper", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("ArchiveRipper", u"Help", None))
    # retranslateUi

