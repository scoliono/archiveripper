from PySide6.QtCore import Slot
from PySide6.QtWidgets import QDialog, QMainWindow, QMessageBox

from .api import ArchiveReaderClient
from .ui.ui_ArchiveRipper import Ui_ArchiveRipper
from .ui.ui_CredentialsDialog import Ui_CredentialsDialog
from .ui.ui_NewRipDialog import Ui_NewRipDialog


class ArchiveRipper(QMainWindow):

    def __init__(self):
        super(ArchiveRipper, self).__init__()
        self.ui = Ui_ArchiveRipper()
        self.ui.setupUi(self)

        # dialogs
        self.new_rip_dialog = QDialog()
        self.new_rip_dialog.ui = Ui_NewRipDialog()
        self.new_rip_dialog.ui.setupUi(self.new_rip_dialog)
        self.new_rip_dialog.accepted.connect(self.new_rip)

        self.credentials_dialog = QDialog()
        self.credentials_dialog.ui = Ui_CredentialsDialog()
        self.credentials_dialog.ui.setupUi(self.credentials_dialog)
        self.credentials_dialog.accepted.connect(self.update_credentials)


        # signals
        self.ui.actionNew_Rip.triggered.connect(self.new_rip_dialog.exec)
        self.ui.actionExit.triggered.connect(self.close)

        # api client
        self.client = ArchiveReaderClient()

        # application state
        self.credentials = {
            "email": None,
            "password": None
        }
        self.book_url = None
        self.dest_path = None
        self.start_page = None
        self.end_page = None

    @Slot()
    def new_rip(self):
        book_url = self.new_rip_dialog.ui.bookUrl.text()
        self.book_url = book_url[book_url.rfind("/") + 1:]
        self.dest_path = self.new_rip_dialog.ui.filePath.text()

        self.verify_login()
        msgbox = QMessageBox()
        msgbox.setWindowTitle("New Rip Status")
        try:
            self.client.schedule_loan_book(self.book_url)
            msgbox.setText("Borrowed book successfully")
            msgbox.setIcon(QMessageBox.Information)
        except Exception as e:
            msgbox.setText(f"Failed to borrow book!\n{e}")
            msgbox.setIcon(QMessageBox.Critical)
        finally:
            msgbox.exec()

    def verify_login(self):
        if not self.credentials["email"] or not self.credentials["password"]:
            self.credentials_dialog.exec()
            try:
                self.client.login(self.credentials["email"], self.credentials["password"])
            except Exception as e:
                msgbox = QMessageBox()
                msgbox.setText(f"Failed to log in!\n{e}")
                msgbox.setIcon(QMessageBox.Critical)
                msgbox.exec()

    @Slot()
    def update_credentials(self):
        self.credentials["email"] = self.credentials_dialog.ui.email.text()
        self.credentials["password"] = self.credentials_dialog.ui.password.text()
