
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *

class SaveFileUI(QMainWindow):
    def __init__(self, parent):
        super(SaveFileUI, self).__init__(parent)

        self.saveFileDialog()

        self.show()

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.FileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","Text Files (*.xml)", options=options)
