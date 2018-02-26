#coding=utf-8
#from PyQt5 import QtWidgets, QtGui,QtCore
from PyQt5.QtWidgets import QAction,QInputDialog,QMessageBox,QMainWindow,QApplication
from PyQt5.QtCore import Qt, pyqtSignal,QObject,QThread
from PyQt5.QtGui import QIcon
import sys
import findMathRule as fmr
import DataCreate as dc
import magicTool
import preferencesDialog as pd
import time
#importmathasmts
import numpy as np


class Backend(QThread):
	update_msg = pyqtSignal(str)
	upDate_start = pyqtSignal(int)
	def run(self):
		#print('my 2')
		while True:
			test = fmr.sMsg[0]
			self.update_msg.emit(test)
			#print('fmr.sMsg',test)
			if test == '100%':
				self.upDate_start.emit(1)
				break
			time.sleep(1)
		print('end......')

class Calcule(QObject):
	running = False
	def setValue(self,trainFileName,powers):
		self.fileName = trainFileName
		self.powers = powers
		
	def setStartRun(self,isRuning):
		self.running = isRuning
	
	def run(self):
		while True:
			if self.running == False:
				time.sleep(1)
				continue
			fmr.trainData(self.fileName,self.powers)
			self.running = False

class myDailog(QMainWindow,pd.Ui_Dialog):
	highPower = pyqtSignal(str)
	lowPower = pyqtSignal(str)
	def __init__(self):
		QMainWindow.__init__(self)
		super(myDailog,self).__init__()
		self.setupUi(self) 
		
		
	def accept(self):
		a = self.textHighPower.toPlainText()
		b = self.textLowPower.toPlainText()
		self.highPower.emit(a)
		self.lowPower.emit(b)
		self.close()		
		return True

	def reject(self):
		self.close()
		return False		

class mywindow(QMainWindow,magicTool.Ui_MainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		super(mywindow,self).__init__()
		#ui = Ui_MainWindow()
		self.setupUi(self)
		self.dicWs = {}
		self.dicDel = {}
		self.iLowPower = -1
		self.iHighPower = 3
		self.fileTraining = ''
		self.fileTest = ''
		
		self.thread = QThread()
		
		
		self.runThread = Calcule()
		self.runThread.moveToThread(self.thread)
		self.thread.started.connect(self.runThread.run)		
		self.thread.start()
		
		
		self.updateThread = Backend()
		self.updateThread.update_msg.connect(self.handleDisplay)
		self.updateThread.upDate_start.connect(self.startPredict)
		#self.updateThread.moveToThread(self.thread1)
		#self.thread1.started.connect(self.updateThread.run)
		
		self.uiDialog = myDailog()
		self.uiDialog.highPower.connect(self.setHighPower)
		self.uiDialog.lowPower.connect(self.setLowPower)
		
		#initUI
		self.setFixedSize(self.width(), self.height())
		self.statusBar.setStyleSheet("color:rgb(255, 0, 0);background-color:rgba(108, 189, 216,0.5);")
		setAction = QAction(QIcon('./track.jpg'), '&参数设置', self)
		setAction.setShortcut('Ctrl+S')
		setAction.setStatusTip('参数设置')
		setAction.triggered.connect(self.setWindow)

		helpAction = QAction(QIcon('./track.jpg'), '&使用说明', self)
		helpAction.setShortcut('Ctrl+H')
		helpAction.setStatusTip('使用说明')
		helpAction.triggered.connect(self.helpWindow)

		menubar = self.menuBar
		fileMenu = menubar.addMenu('&设置参数')
		fileMenu.addAction(setAction)
		fileMenu = menubar.addMenu('&使用说明')
		fileMenu.addAction(helpAction)

	def create(self):
		listExpress = []
		iNum = int(self.textEdit.toPlainText())
		sExpress = self.textXExpress.toPlainText()
		if sExpress != '':
			listExpress.append(sExpress)
		sExpress = self.textYExpress.toPlainText()
		if sExpress != '':
			listExpress.append(sExpress)
		sExpress = self.textZExpress.toPlainText()
		if sExpress != '':		
			listExpress.append(sExpress)
		sExpress = self.textWExpress.toPlainText()
		if sExpress != '':			
			listExpress.append(sExpress)
		trainFileName = self.textTrainFileName.toPlainText()
		testFileName = self.textTestFileName.toPlainText()
		dc.writeData(trainFileName, testFileName, listExpress,iNum)
		self.statusBar.showMessage('生成成功')

	#定义槽函数
	def magicCalc(self):
		self.statusBar.showMessage('开始训练')
		self.labelResult.setText('')
		self.fileTraining = self.textTrainFileName.toPlainText()
		self.fileTest = self.textTestFileName.toPlainText()
		powers = (self.iLowPower,self.iHighPower)
		self.dicWs.clear()
		self.dicDel.clear()
			
		self.runThread.setValue(self.fileTraining,powers)
		
		
		self.updateThread.start()
		self.runThread.setStartRun(True)
		#self.thread.exec()
		#self.dicWs,self.dicDel = fmr.trainData(self.fileTraining, powers)
		#self.text_Result.setText(fmr.sMsg)

	def handleDisplay(self,data):
		self.labelRateOfProgress.setText(data)

	def setHighPower(self,data):
		self.iHighPower = int(data)
	
	def setLowPower(self,data):
		self.iLowPower = int(data)
	
	def startPredict(self,data):
		self.predict()
	
	def predict(self):
		self.statusBar.showMessage('训练完毕')
		sName = fmr.predictData(self.fileTest, (self.iLowPower,self.iHighPower))
		self.labelResult.setText('预测结果请看文件：'+sName)
		fmr.sMsg[0] = '0%'
		msg_box = QMessageBox(QMessageBox.Warning, "Alert", "Pleaseconfigurethebaseline!")		
		#self.thread.quit()
		return
	
	def setWindow(self, event):
		self.uiDialog.show()

	def helpWindow(self, event):
		reply = QMessageBox.information(self,
			"使用说明", 
			"按照提示在表达式框中输入x，y，z的表达式，比如要得到这样的样本数据：\n\
		    \t [[1,4,9,16],\n\
		    \t [4,9,16,25]]\t\n,则表达式为：\n\
		    \t x = x**2 \n\
		    \t y = (x**0.5+1)**2\n\
		    \t z = (y**0.5+1)**2\n\
		    \t w = (z**0.5+1)**2\
		    \n注意：因为程序会根据样本的特征数进行一元和二元，甚至三元预测，所以进度显示有时会突然减少。", 
			QMessageBox.Yes|QMessageBox.No)

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = mywindow()
	#wMain = QMainWindow()
	#window.setupUi(wMain)
	window.show()
	sys.exit(app.exec_())