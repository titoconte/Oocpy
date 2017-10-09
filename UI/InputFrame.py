import sys
from collections import OrderedDict
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
    QTextEdit, QGridLayout, QApplication)
from PyQt5.QtCore import Qt

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *

class InputWidget(QWidget):

    def __init__(self,parent=None,FileName=None):
        super(InputWidget, self).__init__(parent)

        self.InputUI(FileName)
        self.setMinimumSize(300,700)
        self.setMaximumSize(300,700)

    @staticmethod
    # def ReadXML(Labels,FileName):
    #
    #
    #     return Labels

    def InputUI(self,FileName):
        grid = QGridLayout()
        grid.setSpacing(10)
        group='Information'
        Labels=OrderedDict([
            ('Scenario Name',['Default',0]),
            ('Grid Inputs',['',1]),
            ('Nx',[110,2]),
            ('Ny',[110,3]),
            ('EPSG Code',[32724,4]),
            ('Depth (m)',[700,6]),
            ('Resolution in (m)',[12.192,5]),
            ('Time Step (hours)',[1,7]),
            ('Duration (hours)',[75,8]),
            ('Discharge Inputs',['',9]),
            ('X (Grid cell value)', [55,10]),
            ('Y (Grid cell value)',[55,11]),
            ('Longitude',[70000,12]),
            ('Latitude',[50000,13]),
            ('Rate (kg/m³)',[16,14]),
            ('Ratio (m)',[0.5,15]),
            ('Depth (m)',[0.5,16]),
            ('Angle (degrees)',[90,17]),
            ('Time (hours)',[60,18]),
            ('Bulk kg/m³',[20,19]),
            ('Grain file',['',20]),
            ('Ambient Inputs',['',21]),
            ('Current File',['',22]),
            ('Density Profile File',['',23]),
            ('Hs',[0,24]),
            ('Tp',[1,25])])
        if isinstance(FileName,str):
            Labels = self.ReadXML(Labels,FileName)

        title=QFont()
        title.setBold(True)
        i=0
        for label,items in Labels.items():
            item,pos=items
            qlabel = QLabel(label)
            if 'Inputs' not in label:
                variable=label.split(' ')[0]
                setattr(self,group+variable,QLineEdit())
                eval('self.{}{}.setText(str(item))'.format(group,variable))
                eval('grid.addWidget(self.{}{},pos,1)'.format(group,variable))
            else:
                qlabel.setFont(title)
                group=label.split(' ')[0]
            grid.addWidget(qlabel, pos, 0)


        self.setLayout(grid)
