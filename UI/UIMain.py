import sys

from xml.dom.minidom import parseString
from dicttoxml import dicttoxml
from collections import OrderedDict

from PyQt5.QtWidgets import (QMainWindow, QAction, QMenu, QApplication,qApp,
                             QStackedWidget)

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from InputFrame import InputWidget
from OpenWindow import OpenFileUI
from SaveWindow import SaveFileUI

# class OpenFileUI(QMainWindow):
#     def __init__(self, parent=None):
#         super(OpenFileUI, self).__init__(parent)
#
#         self.openFileNameDialog()
#
#         self.show()
#
#     def openFileNameDialog(self):
#         options = QFileDialog.Options()
#         options |= QFileDialog.DontUseNativeDialog
#         self.FileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Input files (*.xml)", options=options)

class Main(QMainWindow):

    def __init__(self):
        super().__init__()

        self.MenUI()
        self._FileName=None
        self.NewUI()
        self.setGeometry(200, 200, 400, 500)
        self.setWindowTitle('OOC Drill Model')
        self.show()

    def OpenUI(self):

        FileInput = OpenFileUI(self)
        self._FileName=FileInput.FileName
        self.NewUI()

    def SaveInputUI(self):

        outputname = SaveFileUI(self)
        self._FileOutput = outputname.FileName

        xml = dicttoxml(self.inputs,
                        custom_root='test',
                        attr_type=False)
        
        dom = parseString(xml)
        f = open(self._FileOutput,'w')
        f.write(dom.toprettyxml())
        f.close()

    def NewUI(self):
        self.centralWidget = QStackedWidget()
        self.setCentralWidget(self.centralWidget)

        inputs = InputWidget(self,self._FileName)

        elements=[
            'Discharge',
            'Grid',
            'Ambient',
            'Information'
        ]

        # add atributes in main class
        self.inputs=dict.fromkeys(elements)
        for key in elements:
            self.inputs[key]=dict()

        for attr in inputs.__dir__():
            if any([element in attr for element in elements]):
                value = getattr(inputs,attr)
                label=[attr.replace(ele,'') for ele in elements if ele in attr]
                label=label[0]

                self.inputs[attr.replace(label,'')].update({
                    label:value.text()
                    })


        scrollArea=QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(inputs)

        self.centralWidget.addWidget(scrollArea)
        self.centralWidget.setCurrentWidget(scrollArea)
        self._FileName=None

    def MenUI(self):

        menubar = self.menuBar()
        # Options roots
        fileMenu = menubar.addMenu('&File')
        InMenu = menubar.addMenu('&Inputs')
        OutMenu = menubar.addMenu('&Outputs')

        # file Menu
        newAct = QAction('&New/Restore Default', self)
        newAct.triggered.connect(self.NewUI)
        fileMenu.addAction(newAct)
        openAct = QAction('&Open', self)
        openAct.triggered.connect(self.OpenUI)
        fileMenu.addAction(openAct)
        fileMenu.addSeparator()
        StocSaveAct = QAction('Save &Stochastic', self)
        StocSaveAct.triggered.connect(self.SaveInputUI)
        fileMenu.addAction(StocSaveAct)
        DetSaveAct = QAction('Save &Deterministic', self)
        fileMenu.addAction(DetSaveAct)
        fileMenu.addSeparator()
        GDbAct = QAction('&Grain Data Base', self)
        fileMenu.addAction(GDbAct)
        fileMenu.addSeparator()
        quitAct = QAction('&Quit', self)
        quitAct.triggered.connect(qApp.quit)
        fileMenu.addAction(quitAct)

        # Input Menu
        woa13Act = QAction('Gets &WOA13 Profile', self)
        InMenu.addAction(woa13Act)
        HycomAct = QAction('Gets &Hycom Currents', self)
        InMenu.addAction(HycomAct)
        GebcoAct = QAction('Gets GebCo &Bathymetry', self)
        InMenu.addAction(GebcoAct)
        InMenu.addSeparator()

        ShpPointAct = QAction('&Export Shape Point', self)
        InMenu.addAction(ShpPointAct)
        CurrMenu = QMenu('&Currents Plot', self)
        profileAct = QAction('&All Profile', self)
        CurrMenu.addAction(profileAct)
        StickAct = QAction('&Stickplot', self)
        CurrMenu.addAction(StickAct)
        InMenu.addMenu(CurrMenu)
        InMenu.addSeparator()

        GrainAct = QAction('&Grain Size', self)
        InMenu.addAction(GrainAct)
        InMenu.addSeparator()
        runAct = QAction('&Run Scenario', self)
        InMenu.addAction(runAct)

        # Output Menu
        StocAct = QAction('Stochastic &Calculation', self)
        OutMenu.addAction(StocAct)
        SumAct = QAction('Sum &Scenarios', self)
        OutMenu.addAction(SumAct)
        OutMenu.addSeparator()
        DOAct = QAction('Read &Deposition Output', self)
        OutMenu.addAction(DOAct)
        WCAct = QAction('Read &Water Column Output', self)
        OutMenu.addAction(WCAct)
        OutMenu.addSeparator()

        ExpShpAct = QAction('&Export Shape', self)
        OutMenu.addAction(ExpShpAct)
        FplotAct = QAction('Export Fast &Plot', self)
        OutMenu.addAction(FplotAct)
        CalcAct = QAction('Calcualte Statistics', self)
        OutMenu.addAction(CalcAct)


def main():

    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
