# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cut.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Cut(object):
    
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(323, 303)
        Form.setFixedSize(323, 303)
        Form.setWindowModality(QtCore.Qt.ApplicationModal)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(40, 40, 71, 21))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(120, 40, 113, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.toolButton = QtWidgets.QToolButton(Form)
        self.toolButton.setGeometry(QtCore.QRect(240, 40, 31, 20))
        self.toolButton.setObjectName("toolButton")
        self.toolButton_2 = QtWidgets.QToolButton(Form)
        self.toolButton_2.setGeometry(QtCore.QRect(240, 90, 31, 20))
        self.toolButton_2.setObjectName("toolButton_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(120, 90, 113, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(40, 90, 71, 21))
        self.label_2.setObjectName("label_2")
        self.radioButton = QtWidgets.QRadioButton(Form)
        self.radioButton.setGeometry(QtCore.QRect(70, 150, 89, 16))
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(Form)
        self.radioButton_2.setGeometry(QtCore.QRect(180, 150, 89, 16))
        self.radioButton_2.setObjectName("radioButton_2")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(80, 250, 171, 41))
        self.pushButton.setObjectName("pushButton")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setEnabled(False)
        self.widget.setGeometry(QtCore.QRect(80, 179, 171, 61))
        self.widget.setObjectName("widget")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_4.setGeometry(QtCore.QRect(50, 40, 51, 21))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setGeometry(QtCore.QRect(20, 40, 31, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setGeometry(QtCore.QRect(110, 40, 31, 21))
        self.label_5.setObjectName("label_5")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_5.setGeometry(QtCore.QRect(50, 10, 51, 21))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(20, 10, 31, 16))
        self.label_3.setObjectName("label_3")
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setGeometry(QtCore.QRect(110, 10, 31, 21))
        self.label_6.setObjectName("label_6")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "裁剪图片"))
        self.label.setText(_translate("Form", "导入图片路径"))
        self.toolButton.setText(_translate("Form", "..."))
        self.toolButton_2.setText(_translate("Form", "..."))
        self.label_2.setText(_translate("Form", "保存图片路径"))
        self.radioButton.setText(_translate("Form", "自动裁剪"))
        self.radioButton_2.setText(_translate("Form", "指定裁剪"))
        self.pushButton.setText(_translate("Form", "开始"))
        self.label_4.setText(_translate("Form", "高度："))
        self.label_5.setText(_translate("Form", "像素"))
        self.label_3.setText(_translate("Form", "宽度："))
        self.label_6.setText(_translate("Form", "像素"))
