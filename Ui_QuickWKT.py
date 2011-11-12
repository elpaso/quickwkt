# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_QuickWKT.ui'
#
# Created: Thu Oct 14 11:48:01 2010
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_QuickWKT(object):
    def setupUi(self, QuickWKT):
        QuickWKT.setObjectName("QuickWKT")
        QuickWKT.resize(513, 280)
        self.verticalLayoutWidget = QtGui.QWidget(QuickWKT)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 491, 241))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.addressLabel = QtGui.QLabel(self.verticalLayoutWidget)
        self.addressLabel.setObjectName("addressLabel")
        self.verticalLayout.addWidget(self.addressLabel)
        self.wkt = QtGui.QPlainTextEdit(self.verticalLayoutWidget)
        self.wkt.setObjectName("wkt")
        self.verticalLayout.addWidget(self.wkt)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(QuickWKT)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), QuickWKT.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), QuickWKT.reject)
        QtCore.QMetaObject.connectSlotsByName(QuickWKT)

    def retranslateUi(self, QuickWKT):
        QuickWKT.setWindowTitle(QtGui.QApplication.translate("QuickWKT", "QuickWKT", None, QtGui.QApplication.UnicodeUTF8))
        self.addressLabel.setText(QtGui.QApplication.translate("QuickWKT", "Enter WKT:", None, QtGui.QApplication.UnicodeUTF8))

