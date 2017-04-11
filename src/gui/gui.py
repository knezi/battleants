#!/bin/env python3
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import gui_class
import os

class dialog(QDialog, gui_class.Ui_Dialog):
    def __init__(self, parent=None):
        super(dialog, self).__init__(parent)
        self.setupUi(self)
        self.colours=[ (QPen(QColor(0,0,0)), QBrush(QColor(0,0,0))),
            (QPen(QColor(197,119,0)), QBrush(QColor(197,119,0))) ]

        self.players=[]
        self.walls=[]
        self.states=[]
        self.val=None

        self.scene = QGraphicsScene()

        self.t=QTimer()
        self.t.setInterval(100)
        self.t.setSingleShot(False)
        self.t.timeout.connect(self.nextState)

    def load(self, data):
        with open(data, 'r') as r:
            l=r.readline().strip() # header - players' info
            while l!='':
                record=l.split(' ')
                self.players.append(record[0])
                record=[ int(x) for x in record[1:] ]
                self.colours.append((QPen(QColor(*record)), QBrush(QColor(*record)), QColor(*record)))
                l=r.readline().strip()

            l=r.readline().strip() # walls
            while l!='':
                self.walls.append(tuple(int(x) for x in l.split(' ')))
                l=r.readline().strip()


            l=r.readline().strip() # states
            while l!='': 
                self.states.append([])

                while l!='': # reading ants in a particular state
                    self.states[-1].append(tuple(int(x) for x in l.split(' ')))
                    l=r.readline().strip()

                l=r.readline().strip()

        self.horizontalSlider.setMaximum(len(self.states)-1)

    def drawState(self, state):
        self.scene.addRect(0,0,
                554,404,
                self.colours[1][0], self.colours[1][1])

        for i,pl in enumerate(self.players): # text info
            text=self.scene.addText(pl)
            text.setDefaultTextColor(self.colours[i+2][2])
            text.setX(i*100)

        text=self.scene.addText(str(state+1)+"/"+str(len(self.states)))
        text.setDefaultTextColor(QColor(255,255,255))
        text.setX(500)


        for x,y in self.walls: # walls
            self.drawBox(x,y, 0)

        for pl,x,y in self.states[state]: # ants
            self.drawBox(x,y, pl+1)

        self.graphicsView.setScene(self.scene)

    def click(self, btn):
        self.val=self.horizontalSlider.value()
        if self.val<len(self.states)-1:
            self.drawState(self.val)
            self.t.start()

    def nextState(self):
        self.val=self.horizontalSlider.value()+1
        self.horizontalSlider.setValue(self.val)
        self.drawState(self.val)

        if self.val>=len(self.states)-1:
            self.t.stop()

    def valChanged(self, val):
        if self.val!=val:
            self.t.stop()
        self.drawState(val)

    def drawBox(self, x,y,c):
        self.scene.addRect(x*10,y*10,
                10,10,
                self.colours[c][0], self.colours[c][1])


if len(sys.argv)!=2:
    raise Exception("Specify exactly one file of data")

if not os.path.exists(sys.argv[1]):
    raise Exception("Specified file does not exist")

app=QApplication(sys.argv)
form=dialog()
form.load(sys.argv[1])
form.pushButton.clicked.connect(form.click)
form.horizontalSlider.valueChanged.connect(form.valChanged)
form.show()
app.exec_()
