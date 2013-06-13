# -*- coding: utf-8 -*-
"""
***************************************************************************
Name			 	 : QuickWKT
Description          : QuickWKT
Date                 : 11/Oct/2010
copyright            : (C) 2010 by ItOpen
email                : info@itopen.it
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4 import QtCore, QtGui
from Ui_QuickWKT import Ui_QuickWKT
# create the dialog


EXAMPLES = {
        '' : '',
        'POINT (WKT)' : 'POINT (30 10)',
        'LINESTRING (WKT)' : 'LINESTRING (30 10, 10 30, 40 40)',
        'POLYGON (WKT)' : 'POLYGON ((30 10, 10 20, 20 40, 40 40, 30 10))',
        'POINT (EWKT)' : 'SRID=4326;POINT (30 10)',
        'LINESTRING (EWKT)' : 'SRID=4326;LINESTRING (30 10, 10 30, 40 40)',
        'POLYGON (EWKT)' : 'SRID=4326;POLYGON ((30 10, 10 20, 20 40, 40 40, 30 10))',
        'POINT (WKB)' : r'0101000020E61000000000000000003E400000000000002440',
        'LINESTRING (WKB)' : r'0102000020E6100000030000000000000000003E40000000000000244000000000000024400000000000003E4000000000000044400000000000004440',
        'POLYGON (WKB)' : r'0103000020E610000001000000050000000000000000003E4000000000000024400000000000002440000000000000344000000000000034400000000000004440000000000000444000000000000044400000000000003E400000000000002440'
    }

class QuickWKTDialog(QtGui.QDialog, Ui_QuickWKT ):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.exampleComboBox.addItems(EXAMPLES.keys())

    @QtCore.pyqtSlot(str)
    def on_exampleComboBox_currentIndexChanged(self, index):
        """
        Set and loads examples
        """
        example = EXAMPLES[str(index)]
        self.wkt.setPlainText(example)

