import sys
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtWidgets
from ui import *
from mdialog import *
import qtmodern.styles
import qtmodern.windows
import utils
import matplotlib.pyplot as plt
from pathlib import Path


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # dialogs
        self.wdialog = QDialog(self)
        self.mdialog = MDialog()
        self.mdialog.setupUi(self.wdialog, text="Waste")
        self.wdialog.setWindowFlags(self.wdialog.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        self.pdialog = QDialog(self)
        self.mpdialog = MDialog()
        self.mpdialog.setupUi(self.pdialog, text="Payment")
        self.pdialog.setWindowFlags(self.pdialog.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        # data
        data = Path("info.txt")
        self.file = open(data, "a+")
        self.file.seek(0)
        self.data = self.file.read()
        # signals
        self.ui.pushButton_4.clicked.connect(self.addNewWaste)
        self.ui.pushButton_5.clicked.connect(self.addNewPayment)
        finish = QtWidgets.QAction("Quit", self)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def updateGraph(self):
        pass

    def addNewWaste(self):
        self.addNewAction('W')

    def addNewPayment(self):
        self.addNewAction('P')

    def addNewAction(self, action: str):  # payment or waste
        if action == 'W':
            resp = self.wdialog.exec_()
            dialog = self.mdialog
        elif action == 'P':
            resp = self.pdialog.exec_()
            dialog = self.mpdialog
        else:
            raise Exception("Wrong type of action")
        if resp == QtWidgets.QDialog.Accepted:
            res = f"{action}\t{dialog.lineEdit.text()}\t{utils.get_today_data()}"
            print(res, file=self.file)
            dialog.lineEdit.clear()
            self.data += res + '\n'
            self.updateGraph()

    def closeEvent(self, event):
        close = QtWidgets.QMessageBox.question(self,
                                               "QUIT",
                                               "Are you sure want to stop Skimper?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if close == QtWidgets.QMessageBox.Yes:
            self.file.close()
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyWindow()

    qtmodern.styles.dark(app)
    mw = qtmodern.windows.ModernWindow(win)
    mw.show()
    sys.exit(app.exec_())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
