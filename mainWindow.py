# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 12:27:40 2019

@author: JLUK
"""

import sys, os
# import appOptions
from PySide2 import QtWidgets, QtCore
from mainUI import mainWidgets
# import processAvgTab.tabUI as tab3
import pickle


# %% class that holds the main window
class App(QtWidgets.QMainWindow):
    
    themeSignal = QtCore.Signal(bool)
    
    def __init__(self, settings):
        super().__init__()
        
        self.settings = settings
        #set default geometry for the main window (distance from left edge, top edge, width, height)
        #Initial window size/pos last saved
        self.setGeometry(self.settings.value("mainWindow/geometry", QtCore.QRect(20, 50, 1850, 1030)))
        self.initUI()
 
    def initUI(self):       
        
        darkThemeAct = QtWidgets.QAction('Dark', self, checkable = True)        
        darkThemeAct.setToolTip('Toggle Dark Theme')
        darkThemeAct.triggered.connect(self.themeToggle)
        state = True if self.settings.value('app/darkstyle', False) else False #set option from saved config file
        darkThemeAct.setChecked(state)
        
        saveDataAct = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_DialogSaveButton), 'Save Data', self)
        saveDataAct.setToolTip('Save the current state of data processing')
        saveDataAct.triggered.connect(self.saveData)
        saveDataAct.setEnabled(False)
        
        loadDataAct = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_DialogOpenButton), 'Load Data', self)
        loadDataAct.setToolTip('Load previously saved data state')
        loadDataAct.triggered.connect(self.loadData)
        
        fileMenu = self.menuBar().addMenu('&File')
        fileMenu.addAction(loadDataAct)
        fileMenu.addAction(saveDataAct)
        
        optMenu = self.menuBar().addMenu('&Options')
        optMenu.addAction(darkThemeAct)
        
        self.mainUI = mainWidgets(self)
        
        self.setWindowIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_TitleBarMenuButton))
        self.setCentralWidget(self.mainUI)
        self.setWindowTitle('UK Tax Calculator')
        
        self.show()
        

        #FOR DEBUGGING
        # if self.settings.value('Debugging/state', False):
        #     fname = 'C:/Users/jluk/Codes/CAE_Curve_Generation/testsave.dat'
        #     self.table.loadData([fname])
    
    def saveData(self):
        self.table.saveData()
        
    def loadData(self):
        self.table.loadData()
        
    #Actions for when the dark theme is toggled in the menu bar 
    def themeToggle(self, state):
        self.settings.setValue("app/darkstyle", state)  #change the settings file
        self.themeSignal.emit(state)    #send signal to change theme from outside the qmainwindow class
    
    def closeEvent(self, event):
        #save state when closing
        self.settings.setValue("mainWindow/geometry", self.geometry())
        self.mainUI.saveData()

    
        
# %% class that holds the tab group
# class tabGroup(QtWidgets.QWidget):
    
#     fileRead = QtCore.Signal(bool)
    
#     def __init__(self, parent, settings):
#         super().__init__(parent)
#         self.settings = settings
#         #setting up the main layout for the tab
#         layout = QtWidgets.QVBoxLayout()
        
#         #initialising the first unremovable read file tab
#         self.tab1 = readTab.readTab(self.settings)
#         self.tab1.readingFile.connect(self.fileReadSuccess)

#         self.tabs = QtWidgets.QTabWidget()
#         self.tabs.setTabsClosable(True)             #set all tabs to be closable
#         self.tabs.addTab(self.tab1, 'Read Data')    #adding read file tab to tab group
#         self.tabs.tabBar().setTabButton(0, QtWidgets.QTabBar.RightSide, None)   #set the first tab to be unclosable
#         self.tabs.tabCloseRequested.connect(self.closeTab)                      #assigning callback for closing tab
#         layout.addWidget(self.tabs)
#         self.setLayout(layout)
    
#     # def makeProgressDlg(self, labelText, title = '', maxVal = 0):
#     #     self.progressDlg = QtWidgets.QProgressDialog(labelText, None,  0, maxVal, self)
#     #     self.progressDlg.setMinimumDuration(2000)
#     #     self.progressDlg.setWindowModality(QtCore.Qt.WindowModal)
#     #     self.progressDlg.resize(600, 100)
#     #     self.progressDlg.setWindowTitle(title)
#     #     self.progressDlg.setWindowIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_TitleBarMenuButton))
#     #     self.progressDlg.show()
#     #     self.progressDlg.setValue(0)
#     #     QtWidgets.QApplication.processEvents()
    
    
#     #slot to obtain signal that file was finished reading, and add then change to tab 2
#     @QtCore.Slot(list)
#     def fileReadSuccess(self, dataList, data = [], progressBar = True):
#         if progressBar:
#             self.makeProgressDlg('Plotting Data')
        
#         self.tab2 = smoothAvg.smoothAvgTab(settingsFromMain=self.settings)
#         self.tab2.initUI(dataList, data = data)

#         if progressBar:
#             self.progressDlg.setValue(100)
            
#         self.tabs.insertTab(1, self.tab2, f'Smooth/Avg Data ({dataList[0]})')
#         self.tabs.setCurrentIndex(1)
#         self.tab2.curvesToProcess.connect(self.processCurvesExported)

#         if progressBar:
#             self.progressDlg.close()

#         self.fileRead.emit(True)

#     #slot that gets single loop data from max stress/N tab and output to new tab
#     @QtCore.Slot(list)
#     def processCurvesExported(self, avgMasterData, data = []):
#         self.tab3 = tab3.processAvgUI(self.settings)
#         self.tab3.initUI(avgMasterData, data)

#         #add the new tab to the right of the current tab that sent the signal
#         self.tabs.insertTab(self.tabs.currentIndex() + 1, self.tab3, f'Process Avg. Data')
#         self.tabs.setCurrentIndex(self.tabs.currentIndex() + 1)

    
#     def closeTab(self, tabIdx):
#         self.tabs.removeTab(tabIdx)

# #    def changeReadBox(self, val):
# #        self.tab1.setFileSourceBox(val)
    
#     def saveData(self):
#         fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', 
#                                                          f'{self.tab1.filePath}/saveState',
#                                                          "CAE Curve Data (*.dat)")
#         if fname[0] == '':
#             return
        
#         #save data from each tab
#         tabData = []
#         for a in range(1, self.tabs.count()):
#             tabData.append(self.tabs.widget(a).saveData())
        
#         #prepare messagebox to display
#         saveStatusBox = QtWidgets.QMessageBox()
#         saveStatusBox.setStandardButtons(QtWidgets.QMessageBox.Ok)

#         #stop execution and displa message if no tabs are open
#         if not tabData:
#             saveStatusBox.setIcon(QtWidgets.QMessageBox.Warning)
#             saveStatusBox.setText(f'No active tabs to be saved')
#             saveStatusBox.setWindowTitle('Data Not Saved')
#             saveStatusBox.setWindowIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_TitleBarMenuButton))
#             saveStatusBox.exec()
#             return

#         with open(fname[0], 'wb') as output:         
#             pickle.dump(tabData, output, -1)
        
#         saveStatusBox.setIcon(QtWidgets.QMessageBox.Information)
#         saveStatusBox.setText(f'Data saved to {fname[0]}')
#         saveStatusBox.setWindowTitle('Save Successful')
#         saveStatusBox.setWindowIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_TitleBarMenuButton))
#         saveStatusBox.exec()
        
        
#     def loadData(self, loadfile = None):
#         if not loadfile:
#             fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 
#                                                        self.settings.value('readTab/defdir', 'C:\\'),
#                                                        "Data File (*.dat)")
        
#             if fname[0] == '':
#                 return
#         else:
#             fname = loadfile

#         self.makeProgressDlg('Loading Data')
#         with open(fname[0], 'rb') as loadFile:
#             data = pickle.load(loadFile)        
        
#         for a in data:
#             #check which tab type the data is by the length of masterdata (3 of avgmasterdata, 7 for raw data)
#             if len(a[0]) == 3:
#                 self.processCurvesExported(a[0], a[1:])
#             elif len(a[0]) == 7:
#                 self.fileReadSuccess(a[0], data = a[1:], progressBar = False)
        
#         #self.fileReadSuccess(data, data = smoothParam, progressBar = False)
#         self.progressDlg.close()


