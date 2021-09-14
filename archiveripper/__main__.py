# This directory contains the GUI version of archiveripper

import sys
from PySide6.QtWidgets import QApplication
from .ripper import ArchiveRipper

app = QApplication(sys.argv)
widget = ArchiveRipper()
widget.show()
sys.exit(app.exec())
