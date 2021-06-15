import sys

from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from loguru import logger

from database import psql_session

class StockDBMS_GUI(QMainWindow):

    # Declare GUI Attribute
    psql_session = None     # PostgreSQL session

    def __init__(self):
        super(StockDBMS_GUI, self).__init__() # Call the inherited classes __init__ method

        self.psql_session = psql_session.connect()
        logger.success("PostgreSQL session is connected now...")

        # UI operation
        uic.loadUi('accounting.ui', self) # Load the .ui file
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
        self.show() # Show the GUI

    def closeEvent(self, event):
        # Bypass Class QMainWindow Close Event
        QMainWindow.closeEvent(self, event)

        # StockDBMS_GUI QMainWindow Close Event
        psql_session.disconnect(self.psql_session)
        logger.success("PostgreSQL session is disconnected now...")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StockDBMS_GUI()
    window.show()
    sys.exit(app.exec_())
