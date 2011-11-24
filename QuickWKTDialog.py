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
# create the dialog for GeoCoding


class QuickWKTDialog(QtGui.QDialog, Ui_QuickWKT ):
  def __init__(self):
    QtGui.QDialog.__init__(self)
    # Set up the user interface from Designer.
    self.setupUi(self)
