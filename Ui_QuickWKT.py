# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_QuickWKT.ui'
#
# Created: Mon Nov 14 20:05:12 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class Ui_QuickWKT(object):
    def setupUi(self, QuickWKT):
        QuickWKT.setObjectName(_fromUtf8("QuickWKT"))
        QuickWKT.resize(490, 306)
        self.verticalLayout = QtGui.QVBoxLayout(QuickWKT)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.addressLabel = QtGui.QLabel(QuickWKT)
        self.addressLabel.setObjectName(_fromUtf8("addressLabel"))
        self.verticalLayout.addWidget(self.addressLabel)
        self.wkt = QtGui.QPlainTextEdit(QuickWKT)
        self.wkt.setObjectName(_fromUtf8("wkt"))
        self.verticalLayout.addWidget(self.wkt)
        self.cbxnewlayer = QtGui.QCheckBox(QuickWKT)
        self.cbxnewlayer.setObjectName(_fromUtf8("cbxnewlayer"))
        self.verticalLayout.addWidget(self.cbxnewlayer)
        self.buttonBox = QtGui.QDialogButtonBox(QuickWKT)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(QuickWKT)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), QuickWKT.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), QuickWKT.reject)
        QtCore.QMetaObject.connectSlotsByName(QuickWKT)

    def retranslateUi(self, QuickWKT):
        QuickWKT.setWindowTitle(QtGui.QApplication.translate("QuickWKT", "QuickWKT", None, QtGui.QApplication.UnicodeUTF8))
        self.addressLabel.setText(QtGui.QApplication.translate("QuickWKT", "Enter WKT:", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxnewlayer.setText(QtGui.QApplication.translate("QuickWKT", "Create new layer for every geometry type", None, QtGui.QApplication.UnicodeUTF8))
