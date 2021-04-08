#from pyqtgraph.functions import traceImage
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from pyqtgraph import PlotWidget #,plot
import pyqtgraph
import pandas as pd
import numpy as np
import pyqtgraph as pg
import os
from scipy import signal
#from scipy.signal.spectral import spectrogram
import app_rc
from fpdf import FPDF
import pyqtgraph.exporters
fileName = 'PDFReport.pdf'
pdf = SimpleDocTemplate(fileName, pagesize=letter)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(300,100,920, 900)  # (1536,900)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/sig.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("")
        pyqtgraph.setConfigOptions(imageAxisOrder='row-major')

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Graph1 = PlotWidget(self.centralwidget)
        self.Graph1.setGeometry(QtCore.QRect(10, 10, 900,250))
        self.Graph1.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.Graph1.setObjectName("Graph1")
        self.Graph1.plotItem.showGrid(x=True, y=True)
        self.Graph1.setXRange(100,1000)
        self.data1 =[]
        self.Graph1.setBackground('w')
        self.pen = pg.mkPen(color=(0,0,0))


        self.Spectrograph1 = pyqtgraph.GraphicsLayoutWidget(self.centralwidget)
        self.Spectrograph1.setGeometry(QtCore.QRect(
            950, 10, 0,0))  # (950, 10, 520, 250)
        self.Spectroplot1 = PlotWidget(self.Spectrograph1)
        self.Spectroplot1.setYRange(100,1000)
        self.Spectroplot1.setGeometry(
            QtCore.QRect(0, 10, 490, 240))  # (0,10,490,240)
        self.img1 = pyqtgraph.ImageItem()
        self.Spectroplot1.addItem(self.img1)
        self.hist1 = pyqtgraph.HistogramLUTItem()
        self.hist1.setImageItem(self.img1)
        self.hist1.gradient.restoreState(
            {'mode': 'rgb',
                'ticks': [(0.5, (0, 182, 188, 255)),
                          (1.0, (246, 111, 0, 255)),
                          (0.0, (75, 0, 113, 255))]})


        self.Graph2 = PlotWidget(self.centralwidget)
        self.Graph2.setGeometry(QtCore.QRect(10, 280, 900, 250))
        self.Graph2.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.Graph2.setObjectName("Graph2")
        self.Graph2.plotItem.showGrid(x=True, y=True)
        self.Graph2.setXRange(100,1000)
        self.Graph2.setBackground('w')
        self.data2 =[]

        self.Spectrograph2 = pyqtgraph.GraphicsLayoutWidget(self.centralwidget)
        self.Spectrograph2.setGeometry(QtCore.QRect(
            950, 280, 0,0))  # (950, 280, 520, 250)
        self.Spectroplot2 = PlotWidget(self.Spectrograph2)
        self.Spectroplot2.setYRange(100, 1000)
        self.Spectroplot2.setGeometry(QtCore.QRect(
            0, 10, 490, 240))  # (0, 10, 490, 240)

        self.img2 = pyqtgraph.ImageItem()
        self.Spectroplot2.addItem(self.img2)
        self.hist2 = pyqtgraph.HistogramLUTItem()
        self.hist2.setImageItem(self.img2)
        self.hist2.gradient.restoreState(
            {'mode': 'rgb',
                'ticks': [(0.5, (0, 182, 188, 255)),
                          (1.0, (246, 111, 0, 255)),
                          (0.0, (75, 0, 113, 255))]})


        self.Graph3 = PlotWidget(self.centralwidget)
        self.Graph3.setGeometry(QtCore.QRect(10, 550, 900, 250))
        self.Graph3.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.Graph3.setObjectName("Graph3")
        self.Graph3.plotItem.showGrid(x=True, y=True)
        self.Graph3.setXRange(100,1000)
        self.data3 =[]
        self.Graph3.setBackground('w')
        self.Spectrograph3 = pyqtgraph.GraphicsLayoutWidget(self.centralwidget)
        self.Spectrograph3.setGeometry(QtCore.QRect(
            950, 550, 0,0))  # (950, 550, 520, 250)
        self.Spectroplot3 = PlotWidget(self.Spectrograph3)
        self.Spectroplot3.setYRange(100, 1000)
        self.Spectroplot3.setGeometry(QtCore.QRect(0, 10, 490, 240))
        self.Spectroplot3.setBackground('w')
        self.img3 = pyqtgraph.ImageItem()
        self.Spectroplot3.addItem(self.img3)
        self.hist3 = pyqtgraph.HistogramLUTItem()
        self.hist3.setImageItem(self.img3)
        self.hist3.gradient.restoreState(
            {'mode': 'rgb',
                'ticks': [(0.5, (0, 182, 188, 255)),
                          (1.0, (246, 111, 0, 255)),
                          (0.0, (75, 0, 113, 255))]})

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.Update)
        self.timer.setInterval(10)
        self.timer.start()
     
        self.Spectroplot1.setBackground('w')
        self.Spectroplot2.setBackground('w')
        self.Spectrograph1.setBackground('w')
        self.Spectrograph2.setBackground('w')
        self.Spectrograph3.setBackground('w')
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 960, 26))   #(960,26)
        self.menubar.setStyleSheet("QMenulBar{\n""border-bottom: 1px solid #888888;\n""}")
        self.menubar.setInputMethodHints(QtCore.Qt.ImhEmailCharactersOnly|QtCore.Qt.ImhFormattedNumbersOnly|QtCore.Qt.ImhUrlCharactersOnly)
        self.menubar.setObjectName("menubar")
        self.menus = QtWidgets.QMenu(self.menubar)
        self.menus.setEnabled(True)
        self.menus.setObjectName("menus")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuSelect_Signal = QtWidgets.QMenu(self.menuEdit)
        self.menuSelect_Signal.setObjectName("menuSelect_Signal")
        self.menuPlay_navigate = QtWidgets.QMenu(self.menubar)
        self.menuPlay_navigate.setObjectName("menuPlay_navigate")
        self.menuInstruments_markers = QtWidgets.QMenu(self.menubar)
        self.menuInstruments_markers.setObjectName("menuInstruments_markers")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setEnabled(True)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.toolBar.setFont(font)
        self.toolBar.setAutoFillBackground(False)
        self.toolBar.setStyleSheet("QToolBar{\n""background-color: rgb(255, 255, 255);\n""padding: 0px;\n""}\n""\n""")
        self.toolBar.setMovable(False)
        self.toolBar.setIconSize(QtCore.QSize(30, 30))
        self.toolBar.setFloatable(True)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setCheckable(False)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/newPrefix/open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon1)
        self.actionOpen.setObjectName("actionOpen")
        self.actionPlay_Pause = QtWidgets.QAction(MainWindow)
        self.actionPlay_Pause.setCheckable(True)
        self.actionPlay_Pause.setEnabled(True)
        self.actionPlay = QtWidgets.QAction(MainWindow)
        self.actionPlay.setCheckable(True)
        self.actionPlay.setEnabled(True)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/newPrefix/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPlay.setIcon(icon2)
        self.actionPlay.setObjectName("actionPlay")
        self.actionPlay_Pause.setIcon(icon2)
        self.actionPlay_Pause.setObjectName("actionPlay_Pause")
        self.actionPause = QtWidgets.QAction(MainWindow)
        self.actionPause.setCheckable(True)
        self.actionPause.setEnabled(True)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/newPrefix/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPause.setIcon(icon3)
        self.actionPause.setObjectName("actionPause")
        self.actionClear = QtWidgets.QAction(MainWindow)
        self.actionClear.setCheckable(False)
        self.actionClear.setEnabled(True)
        self.actionClear.setObjectName("actionClear")
        icon3 = QtGui.QIcon()
        self.actionBack = QtWidgets.QAction(MainWindow)
        self.actionBack.setCheckable(False)
        self.actionBack.setEnabled(True)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/newPrefix/back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionBack.setIcon(icon4)
        self.actionBack.setObjectName("actionBack")
        self.actionNext = QtWidgets.QAction(MainWindow)
        self.actionNext.setCheckable(False)
        self.actionNext.setEnabled(True)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/newPrefix/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNext.setIcon(icon5)
        self.actionNext.setObjectName("actionNext")
        self.actionZoom_In = QtWidgets.QAction(MainWindow)
        self.actionZoom_In.setCheckable(False)
        self.actionZoom_In.setEnabled(True)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/newPrefix/zoom in.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoom_In.setIcon(icon6)
        self.actionZoom_In.setObjectName("actionZoom_In")
        self.actionZoom_Out = QtWidgets.QAction(MainWindow)
        self.actionZoom_Out.setCheckable(False)
        self.actionZoom_Out.setEnabled(True)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/newPrefix/zoom out.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoom_Out.setIcon(icon7)
        self.actionZoom_Out.setObjectName("actionZoom_Out")
        self.actionSpectrogram = QtWidgets.QAction(MainWindow)
        self.actionSpectrogram.setCheckable(True)
        self.actionSpectrogram.setEnabled(True)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/newPrefix/spectr.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSpectrogram.setIcon(icon8)
        self.actionSpectrogram.setObjectName("actionSpectrogram")
        self.actionSave_Report = QtWidgets.QAction(MainWindow)
        self.actionSave_Report.setCheckable(False)
        self.actionSave_Report.setEnabled(True)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/newPrefix/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_Report.setIcon(icon9)
        self.actionSave_Report.setObjectName("actionSave_Report")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setCheckable(False)
        self.actionExit.setObjectName("actionExit")


        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("C:/Users/Youssef/Desktop/app/png/1.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("C:/Users/Youssef/Desktop/app/png/2.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(
            "C:/Users/Youssef/Desktop/app/png/3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)


        self.actionSignal_1 = QtWidgets.QAction(MainWindow)
        self.actionSignal_1.setCheckable(True)
        self.actionSignal_1.setChecked(True)
        self.actionSignal_1.setIcon(icon10)
        self.actionSignal_1.setObjectName("actionSignal_1")
        self.actionSignal_2 = QtWidgets.QAction(MainWindow)
        self.actionSignal_2.setCheckable(True)
        self.actionSignal_2.setIcon(icon11)
        self.actionSignal_2.setObjectName("actionSignal_2")
        self.actionSignal_3 = QtWidgets.QAction(MainWindow)
        self.actionSignal_3.setCheckable(True)
        self.actionSignal_3.setIcon(icon12)
        self.actionSignal_3.setObjectName("actionSignal_3")
        self.menus.addAction(self.actionOpen)
        self.menus.addSeparator()
        self.menus.addAction(self.actionSave_Report)
        self.menus.addSeparator()
        self.menus.addAction(self.actionClear)
        self.menus.addSeparator()
        self.menus.addAction(self.actionExit)
        self.menuSelect_Signal.addAction(self.actionSignal_1)
        self.menuSelect_Signal.addAction(self.actionSignal_2)
        self.menuSelect_Signal.addAction(self.actionSignal_3)
        self.menuEdit.addAction(self.menuSelect_Signal.menuAction())
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionZoom_In)
        self.menuEdit.addAction(self.actionZoom_Out)
        self.menuPlay_navigate.addAction(self.actionBack)
        self.menuPlay_navigate.addAction(self.actionNext)
        self.menuPlay_navigate.addSeparator()
        self.menuPlay_navigate.addAction(self.actionPlay_Pause)
        self.menuInstruments_markers.addAction(self.actionSpectrogram)
        self.menubar.addAction(self.menus.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuPlay_navigate.menuAction())
        self.menubar.addAction(self.menuInstruments_markers.menuAction())
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionSave_Report)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionZoom_Out)
        self.toolBar.addAction(self.actionZoom_In)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionBack)
        self.toolBar.addAction(self.actionPlay)
        self.toolBar.addAction(self.actionNext)
        self.toolBar.addAction(self.actionPause)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSignal_1)
        self.toolBar.addAction(self.actionSignal_2)
        self.toolBar.addAction(self.actionSignal_3)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSpectrogram)


        self.retranslateUi(MainWindow)
        self.actionSignal_1.triggered.connect(lambda checked: (self.Select_Signal(1)))
        self.actionSignal_2.triggered.connect(lambda checked: (self.Select_Signal(2)))
        self.actionSignal_3.triggered.connect(lambda checked: (self.Select_Signal(3)))
        self.actionExit.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.actionOpen.triggered.connect(self.getFile)
        self.actionZoom_In.triggered.connect(self.Zoom_in)
        self.actionZoom_Out.triggered.connect(self.Zoom_out)
        self.actionPlay.triggered.connect(self.play)
        self.actionPause.triggered.connect(self.pause)
        self.actionPlay_Pause.triggered.connect(self.play_pause)
        self.actionClear.triggered.connect(self.Clear)
        self.actionSave_Report.triggered.connect(self.PDF_Report)
        self.actionBack.triggered.connect(self.scroll_left)
        self.actionNext.triggered.connect(self.scroll_right)
        self.actionSpectrogram.triggered.connect(self.ShowSpectrogram)
        


    def Select_Signal(self,Signal):
        self.actionPlay.setChecked(False)
        if Signal ==1:
            self.actionSignal_1.setChecked(True)
            self.actionSignal_2.setChecked(False)
            self.actionSignal_3.setChecked(False)  
        elif Signal ==2:
            self.actionSignal_1.setChecked(False)
            self.actionSignal_2.setChecked(True)
            self.actionSignal_3.setChecked(False)
        elif Signal == 3:
            self.actionSignal_1.setChecked(False)
            self.actionSignal_2.setChecked(False)
            self.actionSignal_3.setChecked(True)

    #def ShiftSelection(self):

     #   if self.actionSignal_1.isChecked():
     #       self.Select_Signal(2)
     #   elif self.actionSignal_2.isChecked():
     #       self.Select_Signal(3)
     #   elif self.actionSignal_3.isChecked():
     #       self.Select_Signal(1)
     #   else :
     #       self.Select_Signal(1)


    def getFile(self):
        """ This function will get the address of the csv file location
			also calls PlotData function 
		"""
        #self.ShiftSelection()
        self.filePath = QFileDialog.getOpenFileName(filter="csv (*.csv)")[0]
        print("File :", self.filePath)
        self.reader = pd.read_csv(self.filePath, header=1)
        self.fileName = os.path.basename(self.filePath)
        self.plotData(self.fileName)



    def plotData(self,fileName):

        self.reader = self.reader[1:].astype(float)
        file = self.reader.iloc[:, 0]
        data = []
        styles = {"color": "#fff", "font-size": "12px"}
        for row in file:
            data.append(row)

        
        if self.actionSignal_1.isChecked():
            self.data1 = data
            self.Graph1.clear()
            self.Graph1.setTitle(fileName, color='w', size='12pt')
            self.Graph1.setLabel("left","volt",**styles, units = "mV")
            self.Graph1.setLabel("bottom", "Time(msec)", **styles,)
            self.Graph1.plot(self.data1)
            self.Spectrogram(file)
            self.play()
            
        elif self.actionSignal_2.isChecked():
            self.data2 = data
            self.Graph2.clear()
            self.Graph2.setTitle(fileName, **styles)
            self.Graph2.setLabel("left", 'mV', **styles)
            self.Graph2.setLabel("bottom", "Time(msec)", **styles)
            self.Graph2.plot(self.data2)
            self.Spectrogram(file)
            
        elif self.actionSignal_3.isChecked():
            self.data3 = data
            self.Graph3.clear()
            self.Graph3.setTitle(fileName, **styles)
            self.Graph3.setLabel("left", 'mV', **styles)
            self.Graph3.setLabel("bottom", "Time(msec)", **styles)
            self.Graph3.plot(self.data3)
            self.Spectrogram(file)

    def play_pause(self):
        if self.actionPlay_Pause.isChecked():
            self.timer.start()
            self.actionPause.setChecked(False)
            self.actionPlay.setChecked(True)
        else:
            self.timer.stop()
            self.actionPlay.setChecked(False)
            self.actionPause.setChecked(True)

    def play(self):
       
        self.timer.start()
        self.actionPause.setChecked(False)

    def pause(self):
        
        self.timer.stop()
        self.actionPlay.setChecked(False)

    def Clear(self):

        if self.actionSignal_1.isChecked():
            self.Graph1.clear()
            self.Spectroplot1.clear()
            self.Graph1.setTitle('')
            self.Graph1.setLabel("left", '',)
            self.Graph1.setLabel("bottom", "")
            self.Spectroplot1.setLabel("left", '',)
            self.Spectroplot1.setLabel("bottom", "")

        elif self.actionSignal_2.isChecked():
            self.Graph2.clear()
            self.Spectroplot2.clear()
            self.Graph2.setTitle('')
            self.Graph2.setLabel("left", '',)
            self.Graph2.setLabel("bottom", "")
            self.Spectroplot2.setLabel("left", '',)
            self.Spectroplot2.setLabel("bottom", "")

        elif self.actionSignal_3.isChecked():
            self.Graph3.clear()
            self.Spectroplot3.clear()
            self.Graph3.setTitle('')
            self.Graph3.setLabel("left", '',)
            self.Graph3.setLabel("bottom", "")
            self.Spectroplot3.setLabel("left", '',)
            self.Spectroplot3.setLabel("bottom", "")


    def Update(self):
        
        if len(self.data1) > 0 and self.actionPlay.isChecked() and self.actionSignal_1.isChecked():
            xrange1, yrange1 = self.Graph1.viewRange()
            self.Graph1.setXRange(xrange1[0]+1, xrange1[1] +1, padding=0)
            if xrange1[1]>len(self.data1)-100:
                self.timer.stop()

        if len(self.data2) > 0 and self.actionPlay.isChecked() and self.actionSignal_2.isChecked():
            xrange2, yrange2 = self.Graph2.viewRange()
            self.Graph2.setXRange(xrange2[0]+1, xrange2[1] + 1, padding=0)
            if xrange2[1] > len(self.data2)-100:
                self.timer.stop()

        if len(self.data3) > 0 and self.actionPlay.isChecked() and self.actionSignal_3.isChecked():
            xrange3, yrange3 = self.Graph3.viewRange()
            self.Graph3.setXRange(xrange3[0]+1, xrange3[1] + 1, padding=0)
            if xrange3[1] > len(self.data3)-100:
                self.timer.stop()

    def Zoom_in(self):
        if self.actionSignal_1.isChecked():
            xrange, yrange = self.Graph1.viewRange()
            self.Graph1.setXRange(xrange[0] / 2, xrange[1] / 2, padding=0)
            #self.Graph1.setYRange(yrange[0] / 2, yrange[1] / 2, padding=0)
        elif self.actionSignal_2.isChecked():
            xrange, yrange = self.Graph2.viewRange()
            self.Graph2.setXRange(xrange[0] / 2, xrange[1] / 2, padding=0)
            #self.Graph2.setYRange(yrange[0] / 2, yrange[1] / 2, padding=0)
        elif self.actionSignal_3.isChecked():
            xrange, yrange = self.Graph3.viewRange()
            self.Graph3.setXRange(xrange[0] / 2, xrange[1] / 2, padding=0)
            #self.Graph3.setYRange(yrange[0] / 2, yrange[1] / 2, padding=0)

    def Zoom_out(self):
        if self.actionSignal_1.isChecked():
            xrange, yrange = self.Graph1.viewRange()
            self.Graph1.setXRange(xrange[0] * 2, xrange[1] * 2, padding=0)
            #self.Graph1.setYRange(yrange[0] *2, yrange[1]*2, padding=0)
        elif self.actionSignal_2.isChecked():
            xrange, yrange = self.Graph2.viewRange()
            self.Graph2.setXRange(xrange[0] * 2, xrange[1] * 2, padding=0)
            #self.Graph2.setYRange(yrange[0] *2, yrange[1]*2, padding=0)
        elif self.actionSignal_3.isChecked():
            xrange, yrange = self.Graph3.viewRange()
            self.Graph3.setXRange(xrange[0] * 2, xrange[1] * 2, padding=0)
            #self.Graph3.setYRange(yrange[0] *2,  yrange[1]*2, padding=0)

    def scroll_right(self):
        if self.actionSignal_1.isChecked():
            xrange, yrange = self.Graph1.viewRange()
            self.Graph1.setXRange(xrange[0] +100, xrange[1] +100, padding=0)
            #self.Graph1.setYRange(yrange[0] +100, yrange[1]+100, padding=0)
        elif self.actionSignal_2.isChecked():
            xrange, yrange = self.Graph2.viewRange()
            self.Graph2.setXRange(xrange[0] +100, xrange[1] +100, padding=0)
            #self.Graph2.setYRange(yrange[0] +100, yrange[1]+100, padding=0)
        elif self.actionSignal_3.isChecked():
            xrange, yrange = self.Graph3.viewRange()
            self.Graph3.setXRange(xrange[0] +100, xrange[1] +100, padding=0)
            #self.Graph3.setYRange(yrange[0] +100,  yrange[1]+100, padding=0)

    def scroll_left(self):
        if self.actionSignal_1.isChecked():
            xrange, yrange = self.Graph1.viewRange()
            self.Graph1.setXRange(xrange[0] -100, xrange[1] -100, padding=0)
            #self.Graph1.setYRange(yrange[0] -100, yrange[1]-100, padding=0)
        elif self.actionSignal_2.isChecked():
            xrange, yrange = self.Graph2.viewRange()
            self.Graph2.setXRange(xrange[0] -100, xrange[1] -100, padding=0)
            #self.Graph2.setYRange(yrange[0] -100, yrange[1]-100, padding=0)
        elif self.actionSignal_3.isChecked():
            xrange, yrange = self.Graph3.viewRange()
            self.Graph3.setXRange(xrange[0] -100, xrange[1]-100 , padding=0)
            #self.Graph3.setYRange(yrange[0]-100,  yrange[1]-100, padding=0)

    def ShowSpectrogram(self):
        if self.actionSpectrogram.isChecked():
            MainWindow.resize(1500, 900)
            self.Spectrograph1.setGeometry(QtCore.QRect(
                950, 10, 520, 250))
            self.Spectrograph2.setGeometry(QtCore.QRect(
                950, 280, 520, 250))
            self.Spectrograph3.setGeometry(QtCore.QRect(
                950, 550, 520, 250))
        else:
            MainWindow.resize(920, 900)
            self.Spectrograph1.setGeometry(QtCore.QRect(
                950, 10,0,0))
            self.Spectrograph2.setGeometry(QtCore.QRect(
                950, 280,0,0))
            self.Spectrograph3.setGeometry(QtCore.QRect(
                950, 550,0,0))
        
    def Spectrogram(self, data):
        sampling_freq = 10e3

        if self.actionSignal_1.isChecked():
            freq, time, spectrogramPlot = signal.spectrogram(data, sampling_freq)
            self.img1.setImage(spectrogramPlot)
            self.img1.scale(time[-1]/np.size(spectrogramPlot, axis=1),
                            freq[-1]/np.size(spectrogramPlot, axis=0))
            self.Spectroplot1.setLimits(xMin=0, xMax=time[-1], yMin=0, yMax=freq[-1])
            self.Spectroplot1.setLabel('bottom', "Time")
            self.Spectroplot1.setLabel('left', "Frequency")

        if self.actionSignal_2.isChecked():
            freq, time, spectrogramPlot = signal.spectrogram(data, sampling_freq)
            self.img2.setImage(spectrogramPlot)
            self.img2.scale(time[-1]/np.size(spectrogramPlot, axis=1),
                            freq[-1]/np.size(spectrogramPlot, axis=0))
            self.Spectroplot2.setLimits(xMin=0, xMax=time[-1], yMin=0, yMax=freq[-1])
            self.Spectroplot2.setLabel('bottom', "Time")
            self.Spectroplot2.setLabel('left', "Frequency")

        if self.actionSignal_3.isChecked():
            freq, time, spectrogramPlot = signal.spectrogram(data, sampling_freq)
            self.img3.setImage(spectrogramPlot)
            self.img3.scale(time[-1]/np.size(spectrogramPlot, axis=1),
                            freq[-1]/np.size(spectrogramPlot, axis=0))
            self.Spectroplot3.setLimits(xMin=0, xMax=time[-1], yMin=0, yMax=freq[-1])
            self.Spectroplot3.setLabel('bottom', "Time")
            self.Spectroplot3.setLabel('left', "Frequency")


    def PDF_Report(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 15)
        pdf.set_xy(0,0)
        
        pdf.cell(0, 10, 'Graph1',ln=1,align='C')
        exporter = pg.exporters.ImageExporter(self.Graph1.plotItem)               
        exporter.parameters()['width'] = 500  
        exporter.parameters()['height'] = 250         
        exporter.export('fileName1.png')
        pdf.image('fileName1.png',x=None,y=None, w=180,h=70)
            
        pdf.cell(0, 10, 'spectrogram1',ln=1,align='C')


        exporter = pg.exporters.ImageExporter(self.Spectroplot1.plotItem)               
        exporter.parameters()['width'] = 500  
        exporter.parameters()['height'] = 250         
        exporter.export('fileName2.png')
        pdf.image('fileName2.png',x=None,y=None, w=180,h=70)
            
            
        pdf.cell(0, 10, 'Graph2',ln=1,align='C')
        exporter = pg.exporters.ImageExporter(self.Graph2.plotItem)               
        exporter.parameters()['width'] = 500 
        exporter.parameters()['height'] = 250         
        exporter.export('fileName3.png')
        pdf.image('fileName3.png',x=None,y=None, w=180,h=70)
            
            
        pdf.cell(0, 10, 'spectrogram2',ln=1,align='C')
        exporter = pg.exporters.ImageExporter(self.Spectroplot2.plotItem)               
        exporter.parameters()['width'] = 500  
        exporter.parameters()['height'] = 250         
        exporter.export('fileName4.png')
        pdf.image('fileName4.png',x=None,y=None, w=180,h=70)
            
            
        pdf.cell(0, 10, 'Graph3',ln=1,align='C')
        exporter = pg.exporters.ImageExporter(self.Graph3.plotItem)               
        exporter.parameters()['width'] = 500  
        exporter.parameters()['height'] = 250         
        exporter.export('fileName5.png')
        pdf.image('fileName5.png',x=None,y=None, w=180,h=70)
            
            
        pdf.cell(0, 10, 'spectrogram3',ln=1,align='C')
        exporter = pg.exporters.ImageExporter(self.Spectroplot3.plotItem)               
        exporter.parameters()['width'] = 500
        exporter.parameters()['height'] = 250         
        exporter.export('fileName6.png')
        pdf.image('fileName6.png',x=None,y=None, w=180,h=70)
            

        pdf.output('Report.pdf')

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SIGVIEW"))
        self.menus.setStatusTip(_translate("MainWindow", "Creates a new document"))
        self.menus.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuSelect_Signal.setTitle(_translate("MainWindow", "Select Signal"))
        self.menuPlay_navigate.setTitle(_translate("MainWindow", "Play && navigate"))
        self.menuInstruments_markers.setTitle(_translate("MainWindow", "Signal tools"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionOpen.setText(_translate("MainWindow", "Open signal..."))
        self.actionOpen.setStatusTip(_translate("MainWindow", "Opens new signal"))
        self.actionOpen.setShortcut(_translate("MainWindow", "O"))
        self.actionPlay_Pause.setText(_translate("MainWindow", "Play/Stop"))
        self.actionPlay_Pause.setShortcut(_translate("MainWindow", "Space"))
        self.actionPlay.setText(_translate("MainWindow", "Play/Stop"))
        self.actionPlay.setShortcut(_translate("MainWindow", "F5"))
        self.actionPause.setText(_translate("MainWindow", "Stop playing"))
        self.actionPause.setStatusTip(_translate("MainWindow", "Stops acqusition"))
        self.actionPause.setShortcut(_translate("MainWindow", "F6"))
        self.actionClear.setText(_translate("MainWindow", "Clear"))
        self.actionClear.setStatusTip(
            _translate("MainWindow", "Clear Graph"))
        self.actionClear.setShortcut(_translate("MainWindow", "Delete"))
        self.actionBack.setText(_translate("MainWindow", "<< Signal beginning"))
        self.actionBack.setShortcut(_translate("MainWindow", "Left"))
        self.actionNext.setText(_translate("MainWindow", "Signal end >>"))
        self.actionNext.setShortcut(_translate("MainWindow", "Right"))
        self.actionZoom_In.setText(_translate("MainWindow", "Zoom In"))
        self.actionZoom_In.setStatusTip(_translate("MainWindow", "Zoom selected part"))
        self.actionZoom_In.setShortcut(_translate("MainWindow", "Up"))
        self.actionZoom_Out.setText(_translate("MainWindow", "Zoom Out"))
        self.actionZoom_Out.setStatusTip(_translate("MainWindow", "Show previous zoom"))
        self.actionZoom_Out.setShortcut(_translate("MainWindow", "Down"))
        self.actionSpectrogram.setText(_translate("MainWindow", "FFT Spectrum analysis"))
        self.actionSpectrogram.setStatusTip(_translate("MainWindow", "Spectrum of the visible part of the signal"))
        self.actionSpectrogram.setShortcut(_translate("MainWindow", "F"))
        self.actionSave_Report.setText(_translate("MainWindow", "Save Report"))
        self.actionSave_Report.setShortcut(_translate("MainWindow", "S"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Alt+F4"))
        self.actionSignal_1.setText(_translate("MainWindow", "Signal 1"))
        self.actionSignal_1.setShortcut(_translate("MainWindow", "1"))
        self.actionSignal_2.setText(_translate("MainWindow", "Signal 2"))
        self.actionSignal_2.setShortcut(_translate("MainWindow", "2"))
        self.actionSignal_3.setText(_translate("MainWindow", "Signal 3"))
        self.actionSignal_3.setShortcut(_translate("MainWindow", "3"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
