from PySide2 import QtWidgets, QtCore, QtGui
import configparser, datetime
import appVars


columnHeaders = ['Cumulative Personal\nAllownace', 'Basic Salary', 'Bonus', 'Total Salary', 'Pension Contribution',
                'Cumulative Salary', 'Cumulative Taxable\nIncome', 'Cumulative Tax', 'Tax in Month',
                'NI Payable', 'Student Loan\nPayable (Month)', 'Take-home Pay']
rowHeaders = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Total']

fName = appVars.configFile
config = configparser.ConfigParser()
config.read(fName)

class mainWidgets(QtWidgets.QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.settings = self.parent().settings
        self.numOnly = QtGui.QDoubleValidator()
        self.numOnly.setBottom(0)

        self.setContentsMargins(30, 10, 30, 10)

        self.initUI()

    def initUI(self):

        numOnly = QtGui.QDoubleValidator()
        numOnly.setBottom(0)

        # hbox = QtWidgets.QHBoxLayout()
        vbox = QtWidgets.QVBoxLayout()

        # postgraduateCheckBox = QtWidgets.QCheckBox(self)
        # postgraduateCheckBox.setCheckState(QtCore.Qt.CheckState.Unchecked)

        # pensionBox = QtWidgets.QLineEdit(self)
        # pensionBox.setValidator(numOnly)
        self.data = dataClass(self, data = self.settings.value('salaryData/bonuses', [0]*12))
        # self.data.setBonuses(self.settings.value('salaryData/bonuses', [0]*12))
        # self.data.setupData()
        tableV = yearTableView()
        tableV.setModel(self.data)
        tableV.resizeTable()
        self.data.connectTable(tableV)

        vbox.addSpacing(20)
        vbox.addLayout(self.makeTopRow())
        vbox.addWidget(self.salaryGroup())
        vbox.addWidget(self.studentLoanGroup())
        vbox.addWidget(tableV)
        # vbox.addStretch(1)

        self.setLayout(vbox)
        self.data.recalculate()

    def makeTopRow(self):
        hbox = QtWidgets.QHBoxLayout()

        yearLabel = QtWidgets.QLabel('Select Year: ')
        yearLabel.setStyleSheet('font-size: xx-large; font: bold;')

        self.yearBox = QtWidgets.QComboBox(self)
        self.yearBox.addItems(config.sections())
        self.yearBox.setStyleSheet('font-size: xx-large; font: bold;')
        self.yearBox.setCurrentIndex(int(self.settings.value('salaryData/year', 1)))
        self.yearBox.currentIndexChanged.connect(self.data.recalculate)

        hbox.addWidget(yearLabel)
        hbox.addWidget(self.yearBox)
        hbox.addStretch(1)

        return hbox


    def salaryGroup(self):
        payGroupBox = QtWidgets.QGroupBox("Salary")
        
        self.basicPay = getExtraLine('Basic (Pensionable) Pay')
        self.basicPay.getUI(linedata = self.settings.value('salaryData/basicpay', str(29000)))
        self.basicPay.lineBox.setValidator(self.numOnly)
        self.basicPay.lineBox.textChanged.connect(self.data.recalculate)
        self.bonusBox = getExtraLine('Annual Bonus')
        self.bonusBox.getUI(linedata = self.settings.value('salaryData/annualbonus', str(2349)))
        self.bonusBox.lineBox.setValidator(self.numOnly)
        self.bonusBox.lineBox.textChanged.connect(self.data.recalculate)

        self.startMonthBox = QtWidgets.QComboBox(self)
        self.startMonthBox.addItems(rowHeaders[:-1])
        self.startMonthBox.setCurrentIndex(int(self.settings.value('salaryData/startmonth', 0)))
        self.startMonthBox.currentIndexChanged.connect(self.data.recalculate)
        self.startMonthBox.setMinimumWidth(60)


        hbox = QtWidgets.QHBoxLayout()
        hbox.addLayout(self.basicPay)
        hbox.addSpacing(20)
        hbox.addLayout(self.bonusBox)
        hbox.addSpacing(20)
        hbox.addWidget(QtWidgets.QLabel('Starting Month: '))
        hbox.addWidget(self.startMonthBox)
        hbox.addStretch(1)
        payGroupBox.setLayout(hbox)
        
        return payGroupBox


    def studentLoanGroup(self):
        studentLoanGroupBox = QtWidgets.QGroupBox("Deductions")
        
        self.pensionPerc = getExtraLine('Pension Contribution (%)')
        self.pensionPerc.getUI(linedata = self.settings.value('salaryData/pensionperc', str(6)))
        self.pensionPerc.lineBox.setValidator(self.numOnly)
        self.pensionPerc.lineBox.textChanged.connect(self.data.recalculate)

        slLabel = QtWidgets.QLabel('Student Loan Plan: ')
        slLabel.setStyleSheet('font-size: xx-large; font: bold;')

        self.studentLoanPlanBox = QtWidgets.QComboBox(self)
        self.studentLoanPlanBox.addItems(['None', 'Plan 1', 'Plan 2'])
        self.studentLoanPlanBox.currentTextChanged.connect(self.data.recalculate)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addLayout(self.pensionPerc)
        hbox.addSpacing(20)
        hbox.addWidget(slLabel)
        hbox.addWidget(self.studentLoanPlanBox)
        hbox.addStretch(1)
        studentLoanGroupBox.setLayout(hbox)
        
        return studentLoanGroupBox

    def saveData(self):
        self.settings.setValue('salaryData/year', self.yearBox.currentIndex())
        self.settings.setValue('salaryData/basicpay', self.basicPay.lineBox.text())
        self.settings.setValue('salaryData/annualbonus', self.bonusBox.lineBox.text())
        self.settings.setValue('salaryData/startmonth', self.startMonthBox.currentIndex())
        self.settings.setValue('salaryData/pensionperc', self.pensionPerc.lineBox.text())
        self.settings.setValue('salaryData/studentloanplan', self.studentLoanPlanBox.currentIndex())
        bonusList = [self.data.item(a, 2).data(0) for a in range(12)]
        self.settings.setValue('salaryData/bonuses', bonusList)


# %% table UI
        #This is the class that holds the table view in the tab
class yearTableView(QtWidgets.QTableView):
    
    def __init__(self, parent = None, data = []):
        super().__init__(parent)
        #self.data = data[0] if data else []
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.setItemDelegate(tableNumberDelegate())
        
    
    def resizeTable(self):
        # self.setSelectionMode(4)

        self.resizeColumnsToContents()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setColumnHidden(0, True)
        self.setColumnHidden(5, True)
        self.setColumnHidden(6, True)
        self.setColumnHidden(7, True)


# %% Item Model Class
#This is the class that holds the cell items of the QTableView
#so any changes to the values have to be made to this class and not the table view class
class dataClass(QtGui.QStandardItemModel):
    def __init__(self, parent = None, data = []):
        super().__init__(parent)
        self.setHorizontalHeaderLabels(columnHeaders)
        self.setVerticalHeaderLabels(rowHeaders)
        
        for rowno in range(len(rowHeaders)):
            for colno, a in enumerate(columnHeaders):
                item = QtGui.QStandardItem()
                item.setEditable(False)
                if 'bonus' in a.lower() and rowno < 12:
                    item.setEditable(True)
                    item.setData(data[rowno], 0)
                
                if rowno == 12:
                    f = item.font()
                    f.setBold(True)
                    item.setFont(f) 
                    
                self.setItem(rowno, colno, item)

        
        self.dataChanged.connect(self.itemDataChanged)
        #class variables for shared use across methods, other methods also need 



    def recalculate(self):
        #disconnect signal to when cell is updated
        self.dataChanged.disconnect(self.itemDataChanged)

        par = self.parent()
        bPay = float(par.basicPay.lineBox.text())
        tBonus = float(par.bonusBox.lineBox.text())
        startM = par.startMonthBox.currentIndex()
        penPerc = float(par.pensionPerc.lineBox.text())
        taxYear = config[f'{par.yearBox.currentText()}']
        slPlan = par.studentLoanPlanBox.currentIndex()

        culPay = 0
        culTax = 0

        for m in range(12):
            culPA = int(taxYear.get('personalallowance')) / 12 * (m+1)

            #set cumulative personal allowance
            self.item(m, 0).setData(f'{culPA:.2f}', 0)

            #set basic pay
            basicP = bPay/12 if m >= startM else 0
            self.item(m, 1).setData(f'{basicP:.2f}', 0)

            #set total pay
            mBonus = tBonus/12 if m >= startM else 0
            totalPay = basicP + mBonus + float(self.item(m, 2).data(0))
            self.item(m, 3).setData(f'{totalPay:.2f}', 0)

            #set pension
            pension = basicP * penPerc / 100
            self.item(m, 4).setData(f'{pension:.2f}', 0)
            #calculate cumulative pay after pension deduction
            culPay += totalPay - pension
            self.item(m, 5).setData(f'{culPay:.2f}', 0)
            #calculate cumulative taxable income
            culTaxPay = culPay - culPA
            culTaxPay = 0 if culTaxPay < 0 else culTaxPay
            self.item(m, 6).setData(f'{culTaxPay:.2f}', 0)
            #calculate the tax owed
            prevCulTax = culTax
            culTax = 0
            higherLim = int(taxYear.get('higherlimit'))/12 * (m+1) - culPA
            #check if pay is higher than higher limit
            #if yes, calculate higher rate tax, then minus off the higher rate taxable pay
            if culTaxPay > higherLim:
                culTax += (culTaxPay - higherLim) * float(taxYear.get('higherrate'))/100
                culTaxPay = higherLim
            #cal
            culTax += culTaxPay * float(taxYear.get('basicrate')) / 100
            self.item(m, 7).setData(f'{culTax:.2f}', 0)

            #calculate the monthly tax payable
            self.item(m, 8).setData(f'{culTax - prevCulTax:.2f}', 0)
            #calculate monthly NI payable
            niLower = int(taxYear.get('NIlower'))
            niUpper = int(taxYear.get('NIupper'))
            niPay = totalPay - pension
            niPayable = 0
            if niPay > niUpper:
                niPayable += (niPay - niUpper) * float(taxYear.get('NIupperrate')) / 100
                niPay = niUpper
            niPayable += (niPay - niLower) * float(taxYear.get('NIlowerrate')) / 100
            niPayable = 0 if niPayable < 0 else niPayable
            self.item(m, 9).setData(f'{niPayable:.2f}', 0)
            #calculate monthly student loan payable
            slLimit = int(taxYear.get(f'plan{slPlan}limit', 1e9))
            slPayable = 0
            if totalPay - pension > slLimit / 12:
                slPayable += (totalPay - pension - slLimit/12) * int(taxYear.get('slrate', 9))/100
            self.item(m, 10).setData(f'{slPayable:.2f}', 0)

            #calculate take-home pay
            finalPay = totalPay - pension - niPayable - slPayable - culTax + prevCulTax
            self.item(m, 11).setData(f'{finalPay:.2f}', 0)
                

            self.calculateColumnTotal(m)
        #reconnect the signal to itemDataChanged
        self.dataChanged.connect(self.itemDataChanged)
    
    def calculateColumnTotal(self, colno):
        total = 0
        for a in range(12):
            try:
                total += float(self.item(a, colno).data(0))
            except TypeError:
                pass

        self.item(12, colno).setData(f'{total:.2f}', 0)
        



    def itemDataChanged(self, item):
        #get the selected cells from the tableview
        selectedIndexes = self.tableW.selectionModel().selectedIndexes()
        no = item.column()

        #if the row is not associated with any month or the number of selected items is 1 or 0
        if no is not 2 or len(selectedIndexes) <= 1:
            # self.updateGraphData(item)
            self.recalculate()
            return
        
        #disconnect slot to stop updated cells to call this method repeatedly
        self.dataChanged.disconnect(self.itemDataChanged)
        
        #for each selected cells
        for a in selectedIndexes:
            #if the cell do not have matching rows, can't set the same value
            if a.column() != no:
                continue
            else:
                #set the itemmodel cells to be the same data
                a.model().itemFromIndex(a).setData(item.data(),0)

        #reconnect the signal to this method
        self.dataChanged.connect(self.itemDataChanged)
        self.recalculate()

    #need to connect to the table object in the parent class (smoothAvgTab)
    def connectTable(self, tableViewObj):
        self.tableW = tableViewObj


# %% item delegate for tableview
class tableNumberDelegate(QtWidgets.QItemDelegate):
    
    def createEditor(self, parent, option, index):
        lineEdit = QtWidgets.QLineEdit(parent)
        
        numOnly = QtGui.QDoubleValidator()
        numOnly.setBottom(0)
        lineEdit.setValidator(numOnly)
        
        return lineEdit

    def setEditorData(self, lineEdit, index):
        value = index.model().data(index, QtCore.Qt.EditRole)
        
        lineEdit.setText(value)
    
    def setModelData(self, lineEdit, model, index):
        value = lineEdit.text()
        
        model.setData(index, value, QtCore.Qt.EditRole)
        model.recalculate()
        # model.dataChanged.emit(index, index)
        
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
        
        return
    

# %% UI elements
class getExtraLine(QtWidgets.QHBoxLayout):
    
    def __init__(self, label = ''):
        super().__init__()
        label = label
        self.lineBox = QtWidgets.QLineEdit() 
        self.labelW = QtWidgets.QLabel(f'{label}: ')
        self.labelW.setStyleSheet('font: bold;')
        
    def getUI(self, linedata = ''):
        self.lineBox.setText(linedata)
        

        self.addWidget(self.labelW)
        self.addWidget(self.lineBox)
   