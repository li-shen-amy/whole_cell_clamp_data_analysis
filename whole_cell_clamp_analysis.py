# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'whole_cell_clamp_analysis.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from abf_functions import plot_oriabf
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 576)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.browse_abf_btn = QtWidgets.QPushButton(self.centralwidget)
        self.browse_abf_btn.setGeometry(QtCore.QRect(450, 10, 113, 41))
        self.browse_abf_btn.setObjectName("browse_abf_btn")
        self.browse_abf_btn.clicked.connect(self.browse_abf)

        self.load_abf_btn = QtWidgets.QPushButton(self.centralwidget)
        self.load_abf_btn.setGeometry(QtCore.QRect(70, 70, 113, 41))
        self.load_abf_btn.setObjectName("load_abf_btn")
        self.load_abf_btn.clicked.connect(self.load_abf)

        self.abf_filename_editor = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.abf_filename_editor.setGeometry(QtCore.QRect(80, 10, 361, 50))
        self.abf_filename_editor.setObjectName("abf_filename_editor")
        self.load_by_browser = False

        self.pltShowCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.pltShowCheckBox.setGeometry(QtCore.QRect(210, 80, 87, 20))
        self.pltShowCheckBox.setObjectName("pltShowCheckBox")
        self.saveFigCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.saveFigCheckBox.setGeometry(QtCore.QRect(310, 80, 91, 20))
        self.saveFigCheckBox.setObjectName("saveFigCheckBox")
        self.saveMatCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.saveMatCheckBox.setGeometry(QtCore.QRect(410, 80, 101, 20))
        self.saveMatCheckBox.setObjectName("saveMatCheckBox")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.browse_abf_btn.setText(_translate("MainWindow", "Browse"))
        self.load_abf_btn.setText(_translate("MainWindow", "Load Data"))
        self.pltShowCheckBox.setText(_translate("MainWindow", "Show Plot"))
        self.saveFigCheckBox.setText(_translate("MainWindow", "Save Figure"))
        self.saveMatCheckBox.setText(_translate("MainWindow", "Save to Mat"))

    def browse_abf(self):
        self.abf_filename, _ = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, "Open File", \
        "/Users/Emily/Dropbox/MS_Gaba_Reward/MS SOM rebound/", "*.abf")
        self.abf_filename_editor.setPlainText(self.abf_filename)
        self.load_by_browser = True

    def load_abf(self):
        if self.load_by_browser:
            self.abf_filename = self.abf_filename_editor.toPlainText()
        filename, _ = os.path.splitext(self.abf_filename)
        plt_show = self.pltShowCheckBox.isChecked()
        save_fig = self.saveFigCheckBox.isChecked()
        save_mat = self.saveMatCheckBox.isChecked()
        plot_oriabf(filename, plt_show, save_fig, save_mat)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

