from PyQt5.uic import loadUiType
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox 

import pandas as pd
import numpy as np
import pandas_model
import importlib as imp
import custom as cst
import editor as code_editor
import dbsettings as db_settings
import pyodbc
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

UiMainWindow, QMainWindow = loadUiType('DatabaseGraphUtility.ui')

defaultUserDir = 'C:\\'

class Main(QMainWindow, UiMainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)
        self.fig_dict = {}
        fig = Figure()
        self.addmpl(fig)
        self.isTableListingClicked = False
        self.label_gridSize.setHidden(True)
        self.lineEdit_gridSize.setHidden(True)

        self.toolButton_fileChoose.clicked.connect(self.handleFileChoose)
        self.pushButton_tableListing.clicked.connect(self.handleTableListing)
        self.pushButton_5.clicked.connect(self.handleMakePlot)
        self.pushButton_codeEdit.clicked.connect(self.handleCodeEdit)
        self.pushButton_dbSettings.clicked.connect(self.handleDbSettings)
        self.pushButton_queryExec.clicked.connect(self.handleQueryExec)
        self.pushButton_clearPlot.clicked.connect(self.handleClearPlot)

        self.radioButton_custom.toggled.connect(self.handleCustomRadioButton)
        self.radioButton_pie.toggled.connect(self.handlePieRadioButton)
        self.radioButton_box.toggled.connect(self.handleBoxRadioButton)
        self.radioButton_hist.toggled.connect(self.handleHistRadioButton)
        self.radioButton_bar.toggled.connect(self.handleBarRadioButton)
        self.radioButton_hexbin.toggled.connect(self.handleHexbinRadioButton)

        self.checkBox_groupBy.stateChanged.connect(self.handleGroupByCheckBox)

    def handleFileChoose(self):
        try:
            fpath = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file',\
            defaultUserDir, "CSV or XLSX files (*.csv *.xlsx)")[0]
            if fpath:
                pwd = os.getcwd()
                os.chdir(os.path.dirname(fpath))
                ext = os.path.basename(fpath).split('.')[1]
                if ext == 'csv':
                    self.df = pd.read_csv(os.path.basename(fpath), sep=';')
                elif ext == 'xlsx':
                    self.df = pd.read_excel(os.path.basename(fpath))
                os.chdir(pwd)
            self.columnsToList(self.df)
            self.toTableView(self.df.head())
            #self.toWidgetPlot(self.df.plot())
        except Exception as ex:
            pass

    def columnsToList(self, dataframe):
        self.comboBox_chooseX.clear()
        self.comboBox_chooseY.clear()
        columns_list = dataframe.columns.tolist()
        self.comboBox_chooseX.addItem("Default")
        self.comboBox_chooseY.addItem("Default")

        for col in columns_list:
            self.comboBox_chooseX.addItem(col)
            self.comboBox_chooseY.addItem(col)

    def handleDbSettings(self):
        db_settings.DBSettings(self).show()

    def handleQueryExec(self):
        try:
            if self.plainTextEdit_query.toPlainText():
                crsr = db_settings.DBSettings(self).connect()
                sql = self.plainTextEdit_query.toPlainText()

                self.df = pd.read_sql_query(sql, crsr)
                crsr.close()
                del crsr

                self.columnsToList(self.df)
                self.toTableView(self.df.head())
                #self.toWidgetPlot(self.df.plot())
        except pd.io.sql.DatabaseError as pd_ex:
            self.label_Error.setText('Error: ' + str(pd_ex))
            self.label_Error.setStyleSheet('color: red')
            QMessageBox.critical(None, 'Error', 'Error occured when processing DB query!\n\nError:\n'+str(pd_ex))

    def handleTableListing(self):
        if hasattr(self, 'df'):
            if not self.isTableListingClicked:
                self.pushButton_tableListing.setText('Small Table Listing')
                self.toTableView(self.df)
                self.isTableListingClicked = True
            else:
                self.pushButton_tableListing.setText('Full Table Listing')
                self.toTableView(self.df.head())
                self.isTableListingClicked = False

    def handleHexbinRadioButton(self):
        if self.radioButton_hexbin.isChecked():
            self.label_gridSize.setHidden(False)
            self.lineEdit_gridSize.setHidden(False)
        else:
            self.label_gridSize.setHidden(True)
            self.lineEdit_gridSize.setHidden(True)

    def handleCustomRadioButton(self):
        if self.radioButton_custom.isChecked():
            self.checkBox_groupBy.setChecked(False)
            self.pushButton_codeEdit.setEnabled(True)
            self.comboBox_chooseX.setEnabled(False)
            self.comboBox_chooseY.setEnabled(False)
            self.checkBox_groupBy.setEnabled(False)
        else:
            self.pushButton_codeEdit.setEnabled(False)
            self.comboBox_chooseX.setEnabled(True)
            self.comboBox_chooseY.setEnabled(True)
            self.checkBox_groupBy.setEnabled(True)

    def handleBarRadioButton(self):
        if self.radioButton_bar.isChecked():
            self.label_chooseX.setText('Choose X labels:')
        else:
            self.label_chooseX.setText('Choose X axis:')

    def handlePieRadioButton(self):
        if self.radioButton_pie.isChecked():
            self.label_chooseY.setText('Choose labels:')
        else:
            self.label_chooseY.setText('Choose Y axis:')

    def handleBoxRadioButton(self):
        if self.radioButton_box.isChecked():
            self.comboBox_chooseY.setEnabled(False)
            self.comboBox_chooseY.setCurrentIndex(0)
        else:
            self.comboBox_chooseY.setEnabled(True)

    def handleHistRadioButton(self):
        if self.radioButton_hist.isChecked():
            self.comboBox_chooseY.setEnabled(False)
            self.comboBox_chooseY.setCurrentIndex(0)
        else:
            self.comboBox_chooseY.setEnabled(True)

    def handleGroupByCheckBox(self):
        self.comboBox_groupBy.clear()
        self.comboBox_aggFunc.clear()

        if hasattr(self, 'df'):
            if self.checkBox_groupBy.isChecked():
                self.comboBox_groupBy.setEnabled(True)
                self.label_aggFunc.setEnabled(True)
                self.comboBox_aggFunc.setEnabled(True)
                self.checkBox_groupBySizePlot.setEnabled(True)

                columns_list = self.df.columns.tolist()
                for col in columns_list:
                    self.comboBox_groupBy.addItem(col)

                for i in ['sum', 'min', 'max', 'mean']:
                    self.comboBox_aggFunc.addItem(i)
            else:
                self.comboBox_groupBy.setEnabled(False)
                self.label_aggFunc.setEnabled(False)
                self.comboBox_aggFunc.setEnabled(False)
                self.checkBox_groupBySizePlot.setChecked(False)
                self.checkBox_groupBySizePlot.setEnabled(False)

    def handleCodeEdit(self):
        code_editor.Editor(self).show()

    def handleClearPlot(self):
        if hasattr(self, 'user_plot'):
            self.user_plot.clear()
            self.canvas.draw()

    def toTableView(self, dataFrame):
        self.label_Error.setText('')
        self.model = pandas_model.PandasModel(dataFrame)
        self.tableView_table.setModel(self.model)

    def toWidgetPlot(self, plot):
        self.user_plot = plot
        try:
            self.label_Error.setText('')
            fig = plot.get_figure()
            main.changefig(fig)
        except Exception as ex:
            self.label_Error.setText('Error: ' + str(ex))
            self.label_Error.setStyleSheet('color: red')
            QMessageBox.critical(None, 'Error', 'Error occured when making plot!\n\nError:\n'+str(ex))

    def addmpl(self, fig):
        self.canvas = FigureCanvas(fig)

        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()
        self.toolbar = NavigationToolbar(self.canvas, self.widget_Plot, coordinates=True)
        self.mplvl.addWidget(self.toolbar)

    def rmmpl(self):
        self.mplvl.removeWidget(self.canvas)
        self.canvas.close()
        self.mplvl.removeWidget(self.toolbar)
        self.toolbar.close()

    def changefig(self, item):
        self.rmmpl()
        self.addmpl(item)

    def handleMakePlot(self):
        x_str = self.comboBox_chooseX.currentText()
        y_str = self.comboBox_chooseY.currentText()
        self.label_Error.setText('')
        if hasattr(self, 'df'):
            #если есть тик на группировке, то выполняем доп. действия
            if self.checkBox_groupBy.isChecked():
                backup_df = self.df.copy()
                aggregationFunction = self.comboBox_aggFunc.currentText()
                gb = self.df.groupby(self.comboBox_groupBy.currentText())

                if self.checkBox_groupBySizePlot.isChecked():
                    if hasattr(self, 'user_plot'):
                        self.user_plot.clear()
                    self.df = gb.size()
                    pass
                elif aggregationFunction == 'sum':
                    self.df = gb.sum()
                    self.df.sort()
                elif aggregationFunction == 'min':
                    self.df = gb.min()
                    self.df.sort()
                elif aggregationFunction == 'max':
                    self.df = gb.max()
                    self.df.sort()
                elif aggregationFunction == 'mean':
                    self.df = gb.mean()
                    self.df.sort()

            try:
                if (self.radioButton_box.isChecked() ^ self.radioButton_hist.isChecked())\
                    & ((x_str != "Default") & (y_str == "Default")): #проверка для функций, у которых нужно только значение Х
                    if self.radioButton_hist.isChecked():
                        self.toWidgetPlot(self.df[[x_str]].plot.hist())

                    elif self.radioButton_box.isChecked():
                        self.toWidgetPlot(self.df.plot.box())

                elif  (x_str == "Default") | (y_str == "Default"): #if case на дефолтные настройки
                    if self.radioButton_basic.isChecked():
                        self.toWidgetPlot(self.df.plot())

                    elif self.radioButton_bar.isChecked():
                        self.toWidgetPlot(self.df.plot(kind='bar'))

                    elif self.radioButton_hist.isChecked():
                        self.toWidgetPlot(self.df.plot.hist())

                    elif self.radioButton_scatter.isChecked():
                        QMessageBox.critical(None, 'Warning', 'X and Y axes must be specified!')

                    elif self.radioButton_pie.isChecked():
                        QMessageBox.critical(None, 'Warning', 'X axis and labels must be specified!')

                    elif self.radioButton_hexbin.isChecked():
                        QMessageBox.critical(None, 'Warning', 'X and Y axes must be specified!')

                    elif self.radioButton_box.isChecked():
                        self.toWidgetPlot(self.df.plot.box())

                    elif self.radioButton_area.isChecked():
                        self.toWidgetPlot(self.df.plot.area())

                    elif self.radioButton_custom.isChecked():
                        imp.reload(cst)
                        self.toWidgetPlot(cst.custom(self.df))
                else: #если заданы обе настройки Х и Y
                    if self.radioButton_basic.isChecked():
                        self.toWidgetPlot(self.df.plot(x_str, y_str))

                    elif self.radioButton_bar.isChecked():
                        if not  self.checkBox_groupBySizePlot.isChecked():
                            self.toWidgetPlot(self.df.plot(x_str, y_str, kind='bar'))
                        else:
                            self.toWidgetPlot(self.df.plot(kind='bar'))

                    elif self.radioButton_scatter.isChecked():
                        self.toWidgetPlot(self.df.plot.scatter(x_str, y_str))

                    elif self.radioButton_area.isChecked():
                        self.toWidgetPlot(self.df.plot.area(x_str, y_str))

                    elif self.radioButton_pie.isChecked():
                        if self.checkBox_groupBy.isChecked():
                            self.toWidgetPlot(self.df.plot.pie(y=x_str, labels=self.df.index))
                        else:
                            self.toWidgetPlot(self.df.plot.pie(y=x_str, labels=self.df[y_str]))

                    elif self.radioButton_hexbin.isChecked():
                        self.toWidgetPlot(self.df.plot.hexbin(x=x_str, y=y_str, gridsize=int(self.lineEdit_gridSize.text())))

                    elif self.radioButton_custom.isChecked():
                        imp.reload(cst)
                        graph = cst.custom(self.df)
                        self.toWidgetPlot(graph)

            except Exception as ex:
                self.label_Error.setText('Error: ' + str(ex))
                self.label_Error.setStyleSheet('color: red')
                QMessageBox.critical(None, 'Error', 'Error occured when making plot!\n\nError:\n'+str(ex))
            finally:
                if self.checkBox_groupBy.isChecked():
                    self.df = backup_df

if __name__ == "__main__":
    import sys
    import os

    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
