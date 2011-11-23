# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name			 	 : QuickWKT
Description          : GQuick WKT viewer
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
 This script initializes the plugin, making it known to QGIS.
"""
def name():
  return "QuickWKT"
def description():
  return "Quick WKT viewer"
def version():
  return "Version 1.5"
def qgisMinimumVersion():
  return "1.0"
def classFactory(iface):
  # load GeoCoding class from file GeoCoding
  from QuickWKT import QuickWKT
  return QuickWKT(iface)
