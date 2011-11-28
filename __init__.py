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
    return "1.7"

def qgisMinimumVersion():
    return "1.5"

def classFactory(iface):
    # load GeoCoding class from file GeoCoding
    from QuickWKT import QuickWKT
    return QuickWKT(iface)

def experimental():
    return False

def homepage():
    return 'http://www.itopen.it/2010/10/21/wkt-on-the-fly-qgis-plugin/'

def repository():
    return 'https://github.com/elpaso/quickwkt'

def tracker():
    return 'https://github.com/elpaso/quickwkt/issues'

def icon():
    return 'quickwkt_icon.png'

