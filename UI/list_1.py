# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'list_1.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(895, 560)


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.tijiao_2.setText(_translate("Form", "使用"))
        self.shiyonglv_2.setText(_translate("Form", "使用率:99.99%"))
        self.shenglv_2.setText(_translate("Form", "胜 率:99.99% "))
