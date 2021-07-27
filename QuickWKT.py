# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                 : QuickWKT
Description          : QuickWKT
Date                 : 25/Oct/2016
copyright            : (C) 2011-2016 by ItOpen
email                : elpaso@itopen.it
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
from __future__ import print_function
from __future__ import absolute_import
from builtins import str
from builtins import range
from builtins import object
# Import the PyQt and QGIS libraries
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
try:
    from qgis.PyQt.QtWidgets import *
except:
    pass
from qgis.core import *

import os
import re
import binascii
import inspect

# Import the code for the dialog
from .QuickWKTDialog import QuickWKTDialog


class QuickWKT(object):

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = iface.mapCanvas()
        # TODO: remove: unused
        self.layerNum = 1
        iface.show_wkt = self.save_wkt
        iface.show_wkb = self.save_wkb
        iface.show_geometry = self.save_geometry

    def initGui(self):
        current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        self.action = QAction(QIcon(os.path.join(current_directory, "icons", "quickwkt_icon.png")),
             "&QuickWKT", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.quickwkt)

        # Add toolbar button and menu item

        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("QuickWKT", self.action)

        # create dialog
        self.dlg = QuickWKTDialog()
        self.dlg.wkt.setPlainText("")
        self.dlg.layerTitle.setText('QuickWKT')

        self.dlg.clearButton.clicked.connect(self.clearButtonClicked)


    def clearButtonClicked(self):
        self.dlg.wkt.setPlainText('')

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu("QuickWKT", self.action)
        self.iface.removeToolBarIcon(self.action)

     # run
    def quickwkt(self):
        # show the dialog
        self.dlg.show()
        self.dlg.adjustSize()
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1 and self.dlg.wkt.toPlainText():
            text = str(self.dlg.wkt.toPlainText())
            layerTitle = self.dlg.layerTitle.text() or 'QuickWKT'
            try:
                if any(st in text for st in ["(", "EMPTY"]):
                    self.save_wkt(text, layerTitle)
                else:
                    self.save_wkb(text, layerTitle)
            except Exception as e:
                # Cut
                message = self.constraintMessage(str(e))
                QMessageBox.information(self.iface.mainWindow(), \
                QCoreApplication.translate('QuickWKT', "QuickWKT plugin error"), \
                QCoreApplication.translate('QuickWKT', "There was an error with the service:<br /><strong>{0}</strong>").format(message))
                return

            # Refresh the map
            self.canvas.refresh()
            return

    def createLayer(self, typeString, layerTitle=None, crs=None):
        # Automatic layer title in case is None
        if not layerTitle:
            layerTitle = 'QuickWKT %s' % typeString
        if crs:
            crs = QgsCoordinateReferenceSystem(crs, QgsCoordinateReferenceSystem.PostgisCrsId)
        else:
            crs = self.canvas.mapSettings().destinationCrs()

        typeString = "%s?crs=%s" % (typeString, crs.authid())

        layer = QgsVectorLayer(typeString, layerTitle, "memory")

        # add attribute id, purely to make the features selectable from within attribute table
        layer.dataProvider().addAttributes([QgsField("name", QVariant.String)])
        try:
            registry = QgsMapLayerRegistry.instance()
        except:
            registry = QgsProject.instance()
        # First search for a layer with this name and type if the cbx is not checked
        if not self.dlg.cbxnewlayer.isChecked():
            for l in registry.mapLayersByName(layerTitle):
                if l.dataProvider().dataSourceUri() == layer.dataProvider().dataSourceUri():
                    return l
        registry.addMapLayer(layer)
        return layer

    def parseGeometryCollection(self, wkt, layerTitle=None):
        #Cannot use split as there are commas in the geometry.
        start = 20
        bracketLevel = -1
        for i in range(len(wkt)):
            if wkt[i] == '(':
                bracketLevel += 1
            elif wkt[i] == ')':
                bracketLevel -= 1
            elif wkt[i] == ',' and bracketLevel == 0:
                self.save_wkt(wkt[start:i], layerTitle)
                start = i + 1

        self.save_wkt(wkt[start:-1], layerTitle)

    def decodeBinary(self, wkb):
        """Decode the binary wkb and return as a hex string"""
        value = binascii.a2b_hex(wkb)
        value = value[::-1]
        value = binascii.b2a_hex(value)
        return value.decode("UTF-8")

    def encodeBinary(self, value):
        wkb = binascii.a2b_hex("%08x" % value)
        wkb = wkb[::-1]
        wkb = binascii.b2a_hex(wkb)
        return wkb.decode("UTF-8")

    def saveFeatures(self, layer, features):
        layer.dataProvider().addFeatures(features)
        layer.updateExtents()
        layer.reload()
        self.canvas.refresh()

    def save_wkb(self, wkb, layerTitle=None):
        """Shows the WKB geometry in the map canvas, optionally specify a
        layer name otherwise it will be automatically created
        Returns the layer where features has been added (or None)."""
        SRID_FLAG = 0x20000000

        typeMap = {0: "Point", 1: "LineString", 2: "Polygon"}
        srid = ""
        qDebug("Decoding binary: " + wkb)

        geomType = int("0x" + self.decodeBinary(wkb[2:10]), 0)
        if geomType & SRID_FLAG:
            srid = int("0x" + self.decodeBinary(wkb[10:18]), 0)
            # String the srid from the wkb string
            wkb = wkb[:2] + self.encodeBinary(geomType ^ SRID_FLAG) + wkb[18:]

        geom = QgsGeometry()
        geom.fromWkb(binascii.a2b_hex(wkb))
        wkt = geom.asWkt()
        qDebug("As wkt = " + wkt)
        qDebug("Geom type = " + str(geom.type()))
        if not wkt:
            qDebug("Geometry creation failed")
            return None
        f = QgsFeature()
        f.setGeometry(geom)
        layer = self.createLayer(typeMap[geom.type()], layerTitle, srid)

        self.saveFeatures(layer, [f])
        return layer

    def constraintMessage(self, message):
        """return a shortened version of the message"""
        if len(message) > 128:
            message = message[:64] + ' [ .... ] ' + message[-64:]
        return message

    def save_wkt(self, wkt, layerTitle=None):
        """Shows the WKT geometry in the map canvas, optionally specify a
        layer name otherwise it will be automatically created.
        Returns the layer where features has been added (or None)."""
        # supported types as needed for layer creation
        typeMap = {0: "Point", 1: "LineString", 2: "Polygon"}
        newFeatures = {}
        errors = ""
        regex = re.compile("([a-zA-Z]+)[\s]*(.*)|EMPTY")
        # Clean newlines where there is not a new object
        wkt = re.sub('\n *(?![SPLMC])', ' ', wkt)
        qDebug("wkt: " + wkt)
        # check all lines in text and try to make geometry of it, collecting errors and features
        for wktLine in wkt.split('\n'):
            wktLine = wktLine.strip()
            if wktLine:
                try:
                    wktLine = wktLine.upper().replace("LINEARRING", "LINESTRING")
                    results = re.match(regex, wktLine)
                    wktLine = results.group(1) + " " + results.group(2)
                    qDebug("Attempting to save '%s'" % wktLine)
                    #EWKT support
                    srid = ""
                    if wktLine.startswith("SRID"):
                        srid, wktLine = wktLine.split(";")  # SRID number
                        srid = int(re.match(".*?(\d+)", srid).group(1))
                        qDebug("SRID = '%d'" % srid)

                    #Geometry Collections
                    if wktLine.startswith("GEOMETRYCOLLECTION ("):
                        self.parseGeometryCollection(wktLine, layerTitle)
                        continue

                    geom = QgsGeometry.fromWkt(wktLine)
                    if not geom and not geom.isEmpty():
                        errors += ('-    "' + wktLine + '" is invalid\n')
                        continue

                    f = QgsFeature()
                    f.setGeometry(geom)
                    if geom.type() in newFeatures:
                        newFeatures.get(geom.type()).append((f, srid))
                    else:
                        newFeatures[geom.type()] = [(f, srid)]
                except:
                    errors += ('-    ' + wktLine + '\n')
        if len(errors) > 0:
            # TODO either quit or succeed ignoring the errors
            errors = self.constraintMessage(str(errors))
            infoString = QCoreApplication.translate('QuickWKT', "These line(s) are not WKT or not a supported WKT type:\n" + errors + "Do you want to ignore those lines (OK) \nor Cancel the operation (Cancel)?")
            res = QMessageBox.question(self.iface.mainWindow(), "Warning QuickWKT", infoString, QMessageBox.Ok | QMessageBox.Cancel)
            if res == QMessageBox.Cancel:
                return

        layer = None
        for typ in list(newFeatures.keys()):
            for f in newFeatures.get(typ):
                layer = self.createLayer(typeMap[typ], layerTitle , f[1])
                layer.dataProvider().addFeatures([f[0]])
                layer.updateExtents()
                layer.reload()
                try: # QGIS < 3
                    layer.setCacheImage(None)
                except:
                    pass
                self.canvas.refresh()
        return layer


    def save_geometry(self, geometry, layerTitle=None):
        """Shows the QgsGeometry in the map canvas, optionally specify a
        layer name otherwise it will be automatically created.
        Returns the layer where features have been added (or None)."""
        if isinstance(geometry, QgsGeometry):
            return self.save_wkt(geometry.exportToWkt(), layerTitle)
        else:
            # fix_print_with_import
            print("Error: this is not an instance of QgsGeometry")
            return None


    def getLayer(self, layerId):
        for layer in list(QgsProject.instance().mapLayers().values()):
            if  layer.id().startsWith(layerId):
                return layer
        return None


if __name__ == "__main__":
    pass
