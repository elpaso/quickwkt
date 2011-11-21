# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                 : QuickWKT
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import sys, os

# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from QuickWKTDialog import QuickWKTDialog

class QuickWKT:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = iface.mapCanvas()

    def initGui(self):
        # Create action that will start plugin
        self.action = QAction(QIcon(":/plugins/QuickWKT/quickwkt_icon.png"), \
        "&QuickWKT", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("activated()"), self.quickwkt)

        # Add toolbar button and menu item

        self.aboutAction=QAction(QIcon(":/plugins/QuickWKT/about_icon.png"), QCoreApplication.translate('QuickWKT', "&About"), self.iface.mainWindow())
        QObject.connect(self.aboutAction, SIGNAL("activated()"), self.about)


        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("QuickWKT", self.action)
        self.iface.addPluginToMenu("QuickWKT", self.aboutAction)

        # create dialog
        examples = """examples:\nPOINT(-5 10)\nLINESTRING(-0 0, 10 10, 20 0, 0 -20)\nPOLYGON((-0 0, 10 10, 10 -10, 0 0))\nPOLYGON ((35 10, 10 20, 15 40, 45 45, 35 10), (20 30, 35 35, 30 20, 20 30)) polygon with hole\nMULTIPOINT ((10 40), (40 30), (20 20), (30 10))"""
        self.dlg = QuickWKTDialog()
        self.dlg.wkt.setPlainText(examples)


    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu("QuickWKT",self.action)
        self.iface.removeToolBarIcon(self.action)


    def about(self):
        infoString = QString(QCoreApplication.translate('QuickWKT', "Python QuickWKT Plugin<br />This plugin creates a set of temporary layers and populates them with WKT features that you can paste in a dialog window.<br /><strong>All layers created by this plugins are temporary layers, all data will be lost when you quit QGIS.</strong><br />Author: Dr. Alessandro Pasotti (aka: elpaso)<br />Mail: <a href=\"mailto:info@itopen.it\">info@itopen.it</a><br />Web: <a href=\"http://www.itopen.it\">www.itopen.it</a>\n"))
        QMessageBox.information(self.iface.mainWindow(), "About QuickWKT",infoString)


    # run
    def quickwkt(self):

        # show the dialog
        self.dlg.show()
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1 and self.dlg.wkt.toPlainText():
            try:
                self.save_wkt(unicode(self.dlg.wkt.toPlainText()))
            except Exception, e:
                QMessageBox.information(self.iface.mainWindow(), QCoreApplication.translate('QuickWKT', "QuickWKT plugin error"), QCoreApplication.translate('QuickWKT', "There was an error with the service:<br /><strong>%1</strong>").arg(unicode(e)))
                return
            # Refresh the map
            self.canvas.refresh()
            return


    def createLayer(self, typeString):
            layer = QgsVectorLayer(typeString, "QuickWKT "+typeString, "memory")
            # TODO this should come from mapcanvas, not from project file
 #           p = QgsProject.instance()
 #           (proj4string,ok) = p.readEntry("SpatialRefSys","ProjectCRSProj4String")
 #           crs = QgsCoordinateReferenceSystem()
 #           crs.createFromProj4(proj4string)
 #           layer.setCrs(crs)
            # add attribute id, purely to make the features selectable from within attribute table
            layer.dataProvider().addAttributes([QgsField("name", QVariant.String)])
            QgsMapLayerRegistry.instance().addMapLayer(layer)
            return layer


    # save wkt to file, wkt is in project's crs
    def save_wkt(self, wkt):

        # supported types as needed for layer creation
        typeMap = { 0:"Point", 1:"LineString", 2:"Polygon" }
        featuresByGType = {}
        errors = ""

        # check all lines in text adn try to make geometry of it, collecting errors and features
        for wktLine in wkt.split('\n'):
            try:
                g = QgsGeometry.fromWkt(wktLine)
                f = QgsFeature()
                f.setGeometry(g)
                if g.type() in featuresByGType:
                    featuresByGType.get(g.type()).append(f)
                else:
                    featuresByGType[g.type()]=[f]
            except:
                errors+=('-    '+wktLine+'\n')
        if len(errors)>0:
            # TODO either quit or succeed ignoring the errors
            infoString = QString(QCoreApplication.translate('QuickWKT', "These line(s) are not WKT or not a supported WKT type:\n" + errors + "Do you want to ignore those lines (OK) \nor Cancel the operation (Cancel)?"))
            res = QMessageBox.question(self.iface.mainWindow(), "Warning QuickWKT", infoString, QMessageBox.Ok | QMessageBox.Cancel)
            if res == QMessageBox.Cancel:
                return

        # create OR reuse a layer for every geometry type
        for typ in featuresByGType.keys():
            # it's possible that the user tried an exotic valid wkt which we cannot handle
            if not typ in typeMap.keys():
                infoString = "This type of WKT-geometry is not supported: " + typ
                QMessageBox.information(self.iface.mainWindow(), "Error QuickWKT", infoString)
            else:
                layer = self.getLayer( 'QuickWKT_'+typeMap[typ])
                if not layer or self.dlg.cbxnewlayer.isChecked():
                    layer = self.createLayer( typeMap[typ] )
                layer.dataProvider().addFeatures( featuresByGType.get(typ) )
                layer.updateExtents()
                layer.reload()
                self.canvas.refresh()


    def getLayer(self, layerId):
        for layer in QgsMapLayerRegistry.instance().mapLayers().values():
            if  layer.id().startsWith(layerId):
                return layer
        return None


if __name__ == "__main__":
    pass
