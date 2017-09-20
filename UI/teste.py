import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.openFileNameDialog()

        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
#
# # import sys
# # from PyQt4.QtCore import SIGNAL
# # from PyQt4.QtGui import QDialog, QApplication, QPushButton, QLineEdit, QFormLayout
# #
# # class Form(QDialog):
# #     def __init__(self, parent=None):
# #         super(Form, self).__init__(parent)
# #
# #         self.le = QLineEdit()
# #         self.le.setObjectName("host")
# #         self.le.setText("Host")
# #
# #         self.pb = QPushButton()
# #         self.pb.setObjectName("connect")
# #         self.pb.setText("Connect")
# #
# #         layout = QFormLayout()
# #         layout.addWidget(self.le)
# #         layout.addWidget(self.pb)
# #
# #         self.setLayout(layout)
# #         self.connect(self.pb, SIGNAL("clicked()"),self.button_click)
# #         self.setWindowTitle("Learning")
# #
# #     def button_click(self):
# #         # shost is a QString object
# #         shost = self.le.text()
# #         print shost
# #
# #
# # app = QApplication(sys.argv)
# # form = Form()
# # form.show()
# # app.exec_()
#
#
# # import sys
# # from PyQt4.QtGui import *
# # from PyQt4 import QtGui, QtCore
#
# import sys
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
#
# import sys, os
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
#
# # DECIMAL SIDE
# def ddecimal(decimalin):
#     a = True #This mades work the while
#     rest ="" #needed to work
#     while not a == False:
#         rest = str(int(decimalin % 2)) + rest #here I grab the rest of the division
#         decimalin= decimalin / 2  #here we made the division
#         if decimalin < 1:
#             a = False #stops the while
#     print("This is your decimal to binary result " + rest ) #result output
#
# # BINARY SIDE
#
# def binary(binaryin):
#     binaryin = str(binaryin)
#     i=0
#     i = len(binaryin) -1
#     binarynum = 0
#     binarydecimal = 0
#     binaryintra = ""
#     #
#     # The next While turns arround the input
#     # Example: if you introduce a 1010 to make easy to use the string and numbers
#     # I rotate it to 0101 trying to learn how to make it less botched XDDD
#     #
#     while i>= 0:
#         binaryintra = binaryintra + binaryin[i]
#         i = i -1
#     #
#     # Here I made the binary to decimal, as you can see i use the normal used formula
#     # (1, 0) * 2^X
#     # X is for the possision of the binary number
#     while not binarynum == len(binaryin):
#
# ##        print(binarynum)        #test
#         binarydecimal1=int(binaryintra[binarynum])*2**binarynum
# ##        print(binarydecimal1) #test
#         binarydecimal=binarydecimal+binarydecimal1
#         binarynum = binarynum +1
#     print("This is your binary to decimal result " + str(binarydecimal))
#
#
#
#
# if __name__ == "__main__":
#     # Create an PyQT5 application object.
#     a = QApplication(sys.argv)
#
#     # The QWidget widget is the base class of all user interface objects in PyQt4.
#     w = QWidget()
#
#     # Set window size.
#     w.resize(320, 240)
#
#     # Set window title
#     w.setWindowTitle("GUI!")
#
#     btn = QPushButton('Hello World!', w)
#     btn.setToolTip('Click to quit!')
#     btn.clicked.connect(exit)
#     btn.resize(btn.sizeHint())
#     btn.move(100, 100)
#
#      # Create textbox
#     textbox = QLineEdit(w)
#     textbox.move(20, 20)
#     textbox.resize(280,40)
#
#     textbox.textChanged.connect(ddecimal)
#
#     w.show()
#
#     sys.exit(a.exec_())
#
#
# # class MainWindow(QMainWindow):
# #     def __init__(self, parent=None):
# #         super(MainWindow, self).__init__(parent)
# #         self.central_widget = QStackedWidget()
# #         self.setCentralWidget(self.central_widget)
# #         login_widget = LoginWidget(self)
# #         login_widget.button.clicked.connect(self.login)
# #         self.central_widget.addWidget(login_widget)
# #     def login(self):
# #         logged_in_widget = LoggedWidget(self)
# #         self.central_widget.addWidget(logged_in_widget)
# #         self.central_widget.setCurrentWidget(logged_in_widget)
# #
# #
# # class LoginWidget(QWidget):
# #     def __init__(self, parent=None):
# #         super(LoginWidget, self).__init__(parent)
# #         layout = QHBoxLayout()
# #         self.button = QPushButton('Login')
# #         layout.addWidget(self.button)
# #         self.setLayout(layout)
# #         # you might want to do self.button.click.connect(self.parent().login) here
# #
# #
# # class LoggedWidget(QWidget):
# #     def __init__(self, parent=None):
# #         super(LoggedWidget, self).__init__(parent)
# #         layout = QHBoxLayout()
# #         self.label = QLabel('logged in!')
# #         layout.addWidget(self.label)
# #         self.setLayout(layout)
# #
# #
# #
# # if __name__ == '__main__':
# #     app = QApplication([])
# #     window = MainWindow()
# #     window.show()
# #     app.exec_()
