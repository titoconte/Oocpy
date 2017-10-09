
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *

class OpenFileUI(QMainWindow):
    def __init__(self, parent=None):
        super(OpenFileUI, self).__init__(parent)

        self.openFileNameDialog()

        self.show()


    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.FileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Input files (*.xml)", options=options)
