# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_QuickWKT.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_QuickWKT(object):
    def setupUi(self, QuickWKT):
        QuickWKT.setObjectName(_fromUtf8("QuickWKT"))
        QuickWKT.resize(800, 400)
        self.verticalLayout = QtGui.QVBoxLayout(QuickWKT)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(QuickWKT)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.exampleComboBox = QtGui.QComboBox(self.tab)
        self.exampleComboBox.setObjectName(_fromUtf8("exampleComboBox"))
        self.horizontalLayout_4.addWidget(self.exampleComboBox)
        self.addressLabel = QtGui.QLabel(self.tab)
        self.addressLabel.setObjectName(_fromUtf8("addressLabel"))
        self.horizontalLayout_4.addWidget(self.addressLabel)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.wkt = QtGui.QPlainTextEdit(self.tab)
        self.wkt.setObjectName(_fromUtf8("wkt"))
        self.verticalLayout_2.addWidget(self.wkt)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label = QtGui.QLabel(self.tab)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        self.layerTitle = QtGui.QLineEdit(self.tab)
        self.layerTitle.setObjectName(_fromUtf8("layerTitle"))
        self.horizontalLayout_3.addWidget(self.layerTitle)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.cbxnewlayer = QtGui.QCheckBox(self.tab)
        self.cbxnewlayer.setObjectName(_fromUtf8("cbxnewlayer"))
        self.horizontalLayout_6.addWidget(self.cbxnewlayer)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.clearButton = QtGui.QPushButton(self.tab)
        self.clearButton.setObjectName(_fromUtf8("clearButton"))
        self.horizontalLayout_2.addWidget(self.clearButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.buttonBox = QtGui.QDialogButtonBox(self.tab)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout_2.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_2 = QtGui.QLabel(self.tab_2)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setWordWrap(True)
        self.label_2.setOpenExternalLinks(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_5.addWidget(self.label_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(QuickWKT)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), QuickWKT.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), QuickWKT.reject)
        QtCore.QMetaObject.connectSlotsByName(QuickWKT)

    def retranslateUi(self, QuickWKT):
        QuickWKT.setWindowTitle(_translate("QuickWKT", "QuickWKT", None))
        self.addressLabel.setText(_translate("QuickWKT", "Enter (E)WKT or WKB or load an example", None))
        self.label.setText(_translate("QuickWKT", "Layer title", None))
        self.cbxnewlayer.setText(_translate("QuickWKT", "Create new layer for every geometry type", None))
        self.clearButton.setText(_translate("QuickWKT", "Clear", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("QuickWKT", "WKT/WKB", None))
        self.label_2.setText(_translate("QuickWKT", "<html><head/><body><p><span style=\" font-size:xx-large; font-weight:600;\">Quick WKT </span></p><p>A plugin for quick WKT/WKB visualisation. </p>\n"
"<p>Also adds a couple of methods to <code>iface</code></p>\n"
"<pre style=\"background: white\">iface.show_wkt(\'POINT (9.0 45.0)\', \'optional layer title\')\n"
"iface.show_geometry(QgsGeometry.fromWKT(\'POINT (9.0 45.0)\'))</pre>\n"
"<p><a href=\"http://www.itopen.it/wkt-on-the-fly-qgis-plugin/\"><span style=\" text-decoration: underline; color:#0057ae;\">Plugin Home Page</span></a>  (feed-back is highly appreciated!)</p><p><a href=\"https://github.com/elpaso/quickwkt\"><span style=\" text-decoration: underline; color:#0057ae;\">Source Code and Bug Tracker</span></a></p><p><b>Do you like Quick WKT? Make a <a href=\"https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&amp;hosted_button_id=XEXYSQAQQYZGS\"><span style=\" text-decoration: underline; color:#0057ae;\">small donation</span></a> to keep this project alive! <a href=\"https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&amp;hosted_button_id=XEXYSQAQQYZGS\"><img src=\":/plugins/QuickWKT/paypal_icon.png\"/></a></b></p>\n"
"<p><i>Enjoy Quick WKT!<br>Made in Italy by<a href=\"http://www.itopen.it\"><span style=\" text-decoration: underline; color:#0057ae;\"> Alessandro Pasotti (ItOpen)</a></i></p> </body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("QuickWKT", "About", None))

