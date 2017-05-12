from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt

class Editor(QtWidgets.QDialog):
    def __init__(self, parent = None):
        QtWidgets.QDialog.__init__(self, parent)

        self.parent = parent
        self.initUI()

    def initUI(self):
        loadButton = QtWidgets.QPushButton("Load", self)
        loadButton.setStyleSheet('font: 14px')
        loadButton.clicked.connect(self.load)

        saveButton = QtWidgets.QPushButton("Save && Close", self)
        saveButton.setStyleSheet('font: 14px')
        saveButton.clicked.connect(self.save)

        self.codeEditorField = QtWidgets.QTextEdit(self)
        self.codeEditorField.resize(250, 50)
        self.codeEditorField.setStyleSheet('font: 14px; font-family: "Courier New"')
        self.codeEditorField.setTabStopWidth(4 * 4 * 2)

        layout = QtWidgets.QGridLayout()

        layout.addWidget(self.codeEditorField, 1, 0, 1, 4)
        layout.addWidget(loadButton, 4, 0, 1, 2)
        layout.addWidget(saveButton, 4, 2, 1, 2)

        self.setGeometry(300,300,450,290)
        self.setWindowTitle("Code Editor")
        self.setLayout(layout)
        self.load()

    def center(self):
        frameGm = self.frameGeometry()

        screen = self.desktop().screenNumber(self.desktop().cursor().pos())
        centerPoint = self.desktop().screenGeometry(screen).center()

        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def load(self):
        file = QtCore.QFile('custom.py')
        if not file.open(QtCore.QIODevice.ReadOnly):
            QtGui.QMessageBox.information(None, 'info', file.errorString())
        stream = QtCore.QTextStream(file)
        self.codeEditorField.setText(stream.readAll())

    def save(self):
        with open('custom.py', 'w') as file:
            file.write(str(self.codeEditorField.toPlainText()))
        self.close()