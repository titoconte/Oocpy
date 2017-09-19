import sys
from PyQt5.QtWidgets import (QMainWindow, QAction, QMenu, QApplication,qApp,
                             QStackedWidget)

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from InputFrame import *

class Main(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.MenUI()
        self.centralWidget = QStackedWidget()
        self.setCentralWidget(self.centralWidget)
        inputs = InputWidget(self)

        scrollArea=QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(inputs)

        # self.centralWidget.addWidget(inputs)
        # self.centralWidget.setCurrentWidget(inputs)
        self.centralWidget.addWidget(scrollArea)
        self.centralWidget.setCurrentWidget(scrollArea)
        self.setGeometry(200, 200, 400, 500)
        self.setWindowTitle('OOC Drill Model')
        self.show()

    def MenUI(self):

        menubar = self.menuBar()
        # Options roots
        fileMenu = menubar.addMenu('&File')
        InMenu = menubar.addMenu('&Inputs')
        OutMenu = menubar.addMenu('&Outputs')

        # file Menu
        newAct = QAction('&New', self)
        fileMenu.addAction(newAct)
        openAct = QAction('&Open', self)
        fileMenu.addAction(openAct)
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
