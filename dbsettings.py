from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
import pyodbc

class DBSettings(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

        self.parent = parent
        self.initUI()

    def initUI(self):
        label_Driver = QtWidgets.QLabel("Driver:", self)
        self.comboBox_Driver = QtWidgets.QComboBox(self)
        self.comboBox_Driver.setStyleSheet('font: 14px')
        for col in pyodbc.drivers():
            self.comboBox_Driver.addItem('{'+str(col)+'}')

        label_Server = QtWidgets.QLabel("Server:", self)
        self.lineEdit_Server = QtWidgets.QLineEdit(self)
        self.lineEdit_Server.setStyleSheet('font: 14px')

        label_Port = QtWidgets.QLabel("Port:", self)
        self.lineEdit_Port = QtWidgets.QLineEdit(self)
        self.lineEdit_Port.setStyleSheet('font: 14px')

        label_Database = QtWidgets.QLabel("Database:", self)
        self.lineEdit_Database = QtWidgets.QLineEdit(self)
        self.lineEdit_Database.setStyleSheet('font: 14px')

        label_Uid = QtWidgets.QLabel("User:", self)
        self.lineEdit_Uid = QtWidgets.QLineEdit(self)
        self.lineEdit_Uid.setStyleSheet('font: 14px')

        label_Pwd = QtWidgets.QLabel("Password:", self)
        self.lineEdit_Pwd = QtWidgets.QLineEdit(self)
        self.lineEdit_Pwd.setEchoMode(QtWidgets.QLineEdit.EchoMode('2'))
        self.lineEdit_Pwd.setStyleSheet('font: 14px')

        self.checkBox_CustomArgs = QtWidgets.QCheckBox("Custom arguments string:", self)
        self.checkBox_CustomArgs.stateChanged.connect(self.handleCustomArgsCheckBox)
        self.lineEdit_CustomArgs = QtWidgets.QLineEdit(self)
        self.lineEdit_CustomArgs.setEnabled(False)
        self.lineEdit_CustomArgs.setStyleSheet('font: 14 px')

        pushButton_Load = QtWidgets.QPushButton("Load", self)
        pushButton_Load.setStyleSheet('font: 14px')
        pushButton_Load.clicked.connect(self.loadCFG)

        pushButton_Save = QtWidgets.QPushButton("Save && Close")
        pushButton_Save.setStyleSheet('font: 14 px')
        pushButton_Save.clicked.connect(self.saveCFG)

        layout = QtWidgets.QGridLayout()

        layout.addWidget(label_Driver, 1, 0, 1, 1)
        layout.addWidget(self.comboBox_Driver, 1, 1, 1, 1)
        layout.addWidget(label_Server, 2, 0, 1, 1)
        layout.addWidget(self.lineEdit_Server, 2, 1, 1, 1)
        layout.addWidget(label_Port, 3, 0, 1, 1)
        layout.addWidget(self.lineEdit_Port, 3, 1, 1, 1)
        layout.addWidget(label_Database, 4, 0, 1, 1)
        layout.addWidget(self.lineEdit_Database, 4, 1, 1, 1)
        layout.addWidget(label_Uid, 5, 0, 1, 1)
        layout.addWidget(self.lineEdit_Uid, 5, 1, 1, 1)
        layout.addWidget(label_Pwd, 6, 0, 1, 1)
        layout.addWidget(self.lineEdit_Pwd, 6, 1, 1, 1)
        layout.addWidget(self.checkBox_CustomArgs, 7, 0, 1, 2)
        layout.addWidget(self.lineEdit_CustomArgs, 8, 0, 1, 2)
        layout.addWidget(pushButton_Load, 9, 0, 1, 1)
        layout.addWidget(pushButton_Save, 9, 1, 1, 1)

        self.setGeometry(300, 300, 270, 230)
        self.setWindowTitle("Database Settings")
        self.setLayout(layout)
        self.loadCFG()

    def handleCustomArgsCheckBox(self):
        if self.checkBox_CustomArgs.isChecked():
            self.comboBox_Driver.setEnabled(False)
            self.lineEdit_Server.setEnabled(False)
            self.lineEdit_Port.setEnabled(False)
            self.lineEdit_Database.setEnabled(False)
            self.lineEdit_Uid.setEnabled(False)
            self.lineEdit_Pwd.setEnabled(False)
            self.lineEdit_CustomArgs.setEnabled(True)
        else:
            self.comboBox_Driver.setEnabled(True)
            self.lineEdit_Server.setEnabled(True)
            self.lineEdit_Port.setEnabled(True)
            self.lineEdit_Database.setEnabled(True)
            self.lineEdit_Uid.setEnabled(True)
            self.lineEdit_Pwd.setEnabled(True)
            self.lineEdit_CustomArgs.setEnabled(False)

    def saveCFG(self):
        with open('dbconfig', 'w') as file:
            file.write('DRIVER|'+self.comboBox_Driver.currentText()+'\n')
            file.write('SERVER|' + self.lineEdit_Server.text() + '\n')
            file.write('PORT|'+self.lineEdit_Port.text()+'\n')
            file.write('DATABASE|'+self.lineEdit_Database.text()+ '\n')
            file.write('UID|'+self.lineEdit_Uid.text()+'\n')
            file.write('PWD|'+self.lineEdit_Pwd.text()+'\n')
            file.write('CUSTOMARGS|'+str(self.checkBox_CustomArgs.isChecked())+'\n')
            file.write('CUSTOMLINE|'+self.lineEdit_CustomArgs.text()+'\n')

        self.close()

    def loadCFG(self):
        with open('dbconfig', 'r') as file:
            content = file.readlines()
        content = [x.strip() for x in content]

        for x in content:
            first, second = str(x).split("|")
            if first == 'DRIVER':
                if self.comboBox_Driver.findText(second) != -1:
                    self.comboBox_Driver.setCurrentIndex(self.comboBox_Driver.findText(second))
                else:
                    self.comboBox_Driver.addItem(second)
                    self.comboBox_Driver.setCurrentIndex(self.comboBox_Driver.count()-1)
                self.driver = second
            elif first == 'SERVER':
                self.lineEdit_Server.setText(second)
                self.server = second
            elif first == 'PORT':
                self.lineEdit_Port.setText(second)
                self.port = second
            elif first == 'DATABASE':
                self.lineEdit_Database.setText(second)
                self.db = second
            elif first == 'UID':
                self.lineEdit_Uid.setText(second)
                self.uid = second
            elif first == 'PWD':
                self.lineEdit_Pwd.setText(second)
                self.pwd = second
            elif first == 'CUSTOMARGS':
                if (second == 'True') | (second == 'true'):
                    self.checkBox_CustomArgs.setChecked(True)
                    self.customargs = True
                else:
                    self.checkBox_CustomArgs.setChecked(False)
                    self.customargs = False
            elif first == 'CUSTOMLINE':
                self.lineEdit_CustomArgs.setText(second)
                self.customline = second

    def connect(self):
        self.loadCFG()
        if self.customargs:
            try:
                cnxn = pyodbc.connect(self.customline, autocommit=True)
            except:
                cnxn = pyodbc.connect(self.customline, autocommit=False)
        else:
            try:
                cnxn = pyodbc.connect('DRIVER='+str(self.driver)+\
                                    ';SERVER='+str(self.server)+\
                                    ';PORT='+str(self.port)+\
                                    ';DATABASE='+str(self.db)+\
                                    ';UID='+str(self.uid)+\
                                    ';PWD='+str(self.pwd)+'OPTION=3',  autocommit=True)
            except:
                cnxn = pyodbc.connect('DRIVER='+str(self.driver)+\
                                    ';SERVER='+str(self.server)+\
                                    ';PORT='+str(self.port)+\
                                    ';DATABASE='+str(self.db)+\
                                    ';UID='+str(self.uid)+\
                                    ';PWD='+str(self.pwd)+'OPTION=3',  autocommit=False)

        return cnxn
