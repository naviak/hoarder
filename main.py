import sys
from PyQt5.QtWidgets import QApplication, QDialog
import pandas as pd
from ui import *
from mdialog import *
import qtmodern.styles
import qtmodern.windows
import utils
import os


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
        # data (pandas rn)
        if os.path.isfile('data.csv'):
            self.df = pd.read_csv('data.csv')
        else:
            self.df = pd.DataFrame(columns=['Type', 'Amount', 'Time'])
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
            self.df.loc[len(self.df.index)] = [action, dialog.lineEdit.text(), utils.get_today_data()]
            dialog.lineEdit.clear()
            self.updateGraph()

    def closeEvent(self, event):
        close = QtWidgets.QMessageBox.question(self,
                                               "QUIT",
                                               "Are you sure want to stop Hoarder?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if close == QtWidgets.QMessageBox.Yes:
            self.df.to_csv('data.csv', index=False)
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
