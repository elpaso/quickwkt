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


class InvalidGeometry(ValueError):
    pass


class QuickWKT(object):

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = iface.mapCanvas()
        # TODO: remove: unused
        self.layerNum = 1
        iface.show_wkt = self.save_from_text
        iface.show_wkb = self.save_from_text
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
        result = self.dlg.exec()
        # See if OK was pressed
        if result == 1 and self.dlg.wkt.toPlainText():
            text = str(self.dlg.wkt.toPlainText().upper())
            layerTitle = self.dlg.layerTitle.text() or 'QuickWKT'
            try:
                self.save_from_text(text, layerTitle)
            except Exception:
                # Exception handled in save_from_text
                return

            # Refresh the map
            self.canvas.refresh()
            return

    def createLayer(self, typeString, layerTitle=None, crs=None):
        # Automatic layer title in case is None
        if not layerTitle:
            layerTitle = 'QuickWKT %s' % typeString
        if crs:
            crs = QgsCoordinateReferenceSystem(crs, QgsCoordinateReferenceSystem.CrsType.PostgisCrsId)
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

    def parseGeometryCollection(self, wkt):
        #Cannot use split as there are commas in the geometry.
        start = 20
        bracketLevel = -1
        pieces = []
        for i in range(len(wkt)):
            if wkt[i] == '(':
                bracketLevel += 1
            elif wkt[i] == ')':
                bracketLevel -= 1
            elif wkt[i] == ',' and bracketLevel == 0:
                yield wkt[start:i]
                start = i + 1

        yield wkt[start:-1]

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

    def constraintMessage(self, message):
        """return a shortened version of the message"""
        if len(message) > 128:
            message = message[:64] + ' [ .... ] ' + message[-64:]
        return message

    def geoms_from_wkb(self, wkb):
        """
        Given a single line of hex WKB input,
        returns a two-tuple:
            (SRID, [list containing one QgsGeometry instance])

        Raises InvalidGeometry on invalid input.

        TODO: Handle geometry collections.
        """
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
            raise InvalidGeometry('"%s" is invalid' % wkb)
        return srid, [geom]

    def geoms_from_wkt(self, wkt):
        """
        Given a single line of [E]WKT input,
        returns a two-tuple:
            (SRID, [list of QgsGeometry instances])

        Raises InvalidGeometry on invalid input.

        Generally only one QgsGeometry will be returned,
        but if the input has a geometry collection in it, multiple may be.
        """
        wkt = wkt.upper().replace("LINEARRING", "LINESTRING")
        regex = re.compile(r"([a-zA-Z]+)\s*(.*)|EMPTY")
        results = re.match(regex, wkt)
        wkt = results.group(1) + " " + results.group(2)
        qDebug("Attempting to save '%s'" % wkt)
        #EWKT support
        srid = ""
        if wkt.startswith("SRID"):
            srid, wkt = wkt.split(";")  # SRID number
            srid = int(re.match(r".*?(\d+)", srid).group(1))
            qDebug("SRID = '%d'" % srid)

        #Geometry Collections
        if wkt.startswith("GEOMETRYCOLLECTION ("):
            pieces = self.parseGeometryCollection(wkt)
        else:
            pieces = [wkt]

        geoms = []
        for piece in pieces:
            geom = QgsGeometry.fromWkt(wkt)
            if not geom and not geom.isEmpty():
                raise InvalidGeometry('"%s is invalid' % wkt)
            geoms.append(geom)
        return srid, geoms

    def save_from_text(self, text, layerTitle=None):
        """Shows the WKT geometry in the map canvas, optionally specify a
        layer name otherwise it will be automatically created.
        Returns the layer where features has been added (or None)."""
        # supported types as needed for layer creation
        typeMap = {0: "Point", 1: "LineString", 2: "Polygon"}
        newFeatures = {}
        errors = []
        text = re.sub('\n *(?![PLMC])', ' ', text)
        # Handle multiple lines, each with its own geometry.
        for i, line in enumerate(text.splitlines()):
            line = line.strip()
            if not line:
                continue

            try:
                if "(" in line or 'EMPTY' in line:
                    srid, geoms = self.geoms_from_wkt(line)
                else:
                    srid, geoms = self.geoms_from_wkb(line)

                for geom in geoms:
                    f = QgsFeature()
                    f.setGeometry(geom)
                    if geom.type() in newFeatures:
                        newFeatures.get(geom.type()).append((f, srid))
                    else:
                        newFeatures[geom.type()] = [(f, srid)]
            except InvalidGeometry as e:
                errors.append(str(e))
            except Exception as e:
                QgsMessageLog.logMessage("Error parsing line %d: %s" % (i + 1, str(e)), "QuickWKT", Qgis.Warning)
                errors.append(line)
        if errors:
            # TODO either quit or succeed ignoring the errors
            errors = self.constraintMessage('\n'.join('    - %s' % e for e in errors))
            infoString = QCoreApplication.translate(
                'QuickWKT',
                "These line(s) are not WKT/EWKT/HEXWKB:\n"
                + errors +
                "Do you want to ignore those lines (OK) \nor Cancel the operation (Cancel)?"
            )
            res = QMessageBox.question(self.iface.mainWindow(), "Warning QuickWKT", infoString, QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            if res == QMessageBox.StandardButton.Cancel:
                return

        layer = None
        for typ in list(newFeatures.keys()):
            for f in newFeatures.get(typ):
                try:
                    layer = self.createLayer(typeMap[typ], layerTitle , f[1])
                    layer.dataProvider().addFeatures([f[0]])
                    layer.updateExtents()
                    layer.reload()
                    try: # QGIS < 3
                        layer.setCacheImage(None)
                    except:
                        pass
                    self.canvas.refresh()
                except Exception as e:
                    QMessageBox.critical(self.iface.mainWindow(), "Error QuickWKT", "Error adding feature: %s" % str(e))
                    continue
        return layer


    def save_geometry(self, geometry, layerTitle=None):
        """Shows the QgsGeometry in the map canvas, optionally specify a
        layer name otherwise it will be automatically created.
        Returns the layer where features have been added (or None)."""
        if isinstance(geometry, QgsGeometry):
            return self.save_from_text(geometry.exportToWkt(), layerTitle)
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
