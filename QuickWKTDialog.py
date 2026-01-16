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
from builtins import str

from qgis.PyQt import QtCore

try:
    from qgis.PyQt.QtGui import QDialog
except ImportError:
    from qgis.PyQt.QtWidgets import QDialog

from qgis.PyQt import uic
import os


EXAMPLES = {
        '' : '',
        'POINT (WKT)' : 'POINT (30 10)',
        'LINESTRING (WKT)' : 'LINESTRING (30 10, 10 30, 40 40)',
        'POLYGON (WKT)' : 'POLYGON ((30 10, 10 20, 20 40, 40 40, 30 10))',
        'POINT (EWKT)' : 'SRID=4326;POINT (30 10)',
        'LINESTRING (EWKT)' : 'SRID=4326;LINESTRING (30 10, 10 30, 40 40)',
        'POLYGON (EWKT)' : 'SRID=4326;POLYGON ((30 10, 10 20, 20 40, 40 40, 30 10))',
        'POLYHEDRALSURFACE Z (EWKT)' : 'SRID=3857;POLYHEDRALSURFACE Z (((0 0 0, 0 1 0, 1 1 0, 1 0 0, 0 0 0)), ((0 0 0, 0 1 0, 0 1 1, 0 0 1, 0 0 0)), ((0 0 0, 1 0 0, 1 0 1, 0 0 1, 0 0 0)), ((1 1 1, 1 0 1, 0 0 1, 0 1 1, 1 1 1)), ((1 1 1, 1 0 1, 1 0 0, 1 1 0, 1 1 1)), ((1 1 1, 1 1 0, 0 1 0, 0 1 1, 1 1 1)))',
        'TIN Z (EWKT)' : 'SRID=3857;TIN Z (((0 0 0, 1 0 0, 0.5 1 0, 0 0 0)), ((0 0 0, 1 0 0, 0.5 0.5 1, 0 0 0)), ((1 0 0, 0.5 1 0, 0.5 0.5 1, 1 0 0)), ((0 0 0, 0.5 1 0, 0.5 0.5 1, 0 0 0)))',
        'POINT (WKB)' : r'0101000020E61000000000000000003E400000000000002440',
        'LINESTRING (WKB)' : r'0102000020E6100000030000000000000000003E40000000000000244000000000000024400000000000003E4000000000000044400000000000004440',
        'POLYGON (WKB)' : r'0103000020E610000001000000050000000000000000003E4000000000000024400000000000002440000000000000344000000000000034400000000000004440000000000000444000000000000044400000000000003E400000000000002440'
    }

class QuickWKTDialog(QDialog ):
    def __init__(self):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        ui_path = os.path.join(os.path.dirname(__file__), 'Ui_QuickWKT.ui')
        uic.loadUi(ui_path, self)
        self.exampleComboBox.addItems(list(EXAMPLES.keys()))
        self.exampleComboBox.currentIndexChanged.connect(self.on_exampleComboBox_currentIndexChanged)

    def on_exampleComboBox_currentIndexChanged(self, index):
        """
        Set and loads examples
        """
        try: # Qt5
            example = EXAMPLES[list(EXAMPLES)[index]]
        except TypeError: # Qt4
            example = EXAMPLES[str(index)]
        self.wkt.setPlainText(example)
