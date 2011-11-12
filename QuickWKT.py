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
        # store layer id
        self.layerid = ''

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



    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu("QuickWKT",self.action)
        self.iface.removeToolBarIcon(self.action)


    def about(self):
        infoString = QString(QCoreApplication.translate('QuickWKT', "Python QuickWKT Plugin<br />This plugin creates a set of temporary layers and populates them with WKT features that you can paste in a dialog window.<br /><strong>All layers created by this plugins are temporary layers, all data will be lost when you quit QGIS.</strong><br />Author: Dr. Alessandro Pasotti (aka: elpaso)<br />Mail: <a href=\"mailto:info@itopen.it\">info@itopen.it</a><br />Web: <a href=\"http://www.itopen.it\">www.itopen.it</a>\n"))
        QMessageBox.information(self.iface.mainWindow(), "About QuickWKT",infoString)


    # run
    def quickwkt(self):
        # create and show the dialog
        dlg = QuickWKTDialog()
        # show the dialog
        dlg.show()
        result = dlg.exec_()
        # See if OK was pressed
        if result == 1 and dlg.wkt.toPlainText():
            try:
                self.save_wkt(unicode(dlg.wkt.toPlainText()))
            except Exception, e:
                QMessageBox.information(self.iface.mainWindow(), QCoreApplication.translate('QuickWKT', "QuickWKT plugin error"), QCoreApplication.translate('QuickWKT', "There was an error with the service:<br /><strong>%1</strong>").arg(unicode(e)))
                return


            # Set the extent to our new rectangle
            #self.canvas.setExtent(rect)
            # Refresh the map
            #self.canvas.refresh()
            return

    # save wkt to file, wkt is in project's crs
    def save_wkt(self, wkt):
        qDebug('Saving WKT ')
        # create and add the point layer if not exists or not set
        if not QgsMapLayerRegistry.instance().mapLayer(self.layerid) :
            # create layer with same CRS as project
            self.point_layer = QgsVectorLayer("Point", "QuickWKT Point", "memory")
            self.line_layer = QgsVectorLayer("LineString", "QuickWKT Line", "memory")
            self.polygon_layer = QgsVectorLayer("Polygon", "QuickWKT Polygon", "memory")

            self.point_provider = self.point_layer.dataProvider()
            self.line_provider = self.line_layer.dataProvider()
            self.polygon_provider = self.polygon_layer.dataProvider()

            p = QgsProject.instance()
            (proj4string,ok) = p.readEntry("SpatialRefSys","ProjectCRSProj4String")
            crs = QgsCoordinateReferenceSystem()
            crs.createFromProj4(proj4string)

            self.point_layer.setCrs(crs)
            self.line_layer.setCrs(crs)
            self.polygon_layer.setCrs(crs)

            # add layer if not already
            QgsMapLayerRegistry.instance().addMapLayer(self.point_layer)
            QgsMapLayerRegistry.instance().addMapLayer(self.line_layer)
            QgsMapLayerRegistry.instance().addMapLayer(self.polygon_layer)

            # store layer id
            self.layerid = QgsMapLayerRegistry.instance().mapLayers().keys()[-1]



        # add a feature
        fet = QgsFeature()

        g = QgsGeometry.fromWkt(wkt)
        qDebug('Read WKT type : %s' % g.type())
        fet.setGeometry(g)

        if g.type() == 0:
            self.point_provider.addFeatures( [ fet ] )
            # update layer's extent when new features have been added
            # because change of extent in provider is not propagated to the layer
            self.point_layer.updateExtents()
        elif g.type() == 1:
            self.line_provider.addFeatures( [ fet ] )
            # update layer's extent when new features have been added
            # because change of extent in provider is not propagated to the layer
            self.line_layer.updateExtents()
        elif  g.type() == 2:
            self.polygon_provider.addFeatures( [ fet ] )
            # update layer's extent when new features have been added
            # because change of extent in provider is not propagated to the layer
            self.polygon_layer.updateExtents()
        else:
            infoString = QString(QCoreApplication.translate('QuickWKT', "Error: unknown geometry type"))
            QMessageBox.information(self.iface.mainWindow(), "Error QuickWKT",infoString)


        self.canvas.refresh()




if __name__ == "__main__":
    pass

