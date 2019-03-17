import sys, os

if 'QT_API' not in os.environ: 
    os.environ['QT_API'] = 'pyside2'


from PySide2 import QtCore, QtWidgets
# from appOptions import configOptions
from mainWindow import App
import qdarkstyle

    
# MAIN APP
@QtCore.Slot(bool)
def changedTheme(state):
    if state:
        app.setStyleSheet(qdarkstyle.load_stylesheet_from_environment())
    else:
        app.setStyleSheet('')


if __name__ == '__main__':
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance() 

    #check whether config file exists
    try:
        open("./appConfig/UKTaxCalc_config.ini", 'r')
    except FileNotFoundError:
        errorBox = QtWidgets.QMessageBox()
        errorBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        errorBox.setIcon(QtWidgets.QMessageBox.Critical)
        errorBox.setText(f'CAECurveApp_config.ini not found in {os.getcwd()}\\appConfig')
        errorBox.exec_()
        #Quit app if config file not found   
        sys.exit()

    
    settings = QtCore.QSettings(QtCore.QSettings.IniFormat,QtCore.QSettings.SystemScope, 'lukJZu', 'taxCalc_savestate')
    settings.setFallbacksEnabled(False)    # File only, not registry or or.
    settings.setPath(QtCore.QSettings.IniFormat, QtCore.QSettings.SystemScope, './appConfig')

    ex = App(settings)
    ex.themeSignal.connect(changedTheme) #connect the changed theme signal in the instance to the slot in this main code
    changedTheme(settings.value('app/darkstyle', True)) #change the theme to the theme defined in the saved config file
    ex.show()
    app.exec_()

