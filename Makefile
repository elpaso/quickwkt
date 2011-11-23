# Makefile for a PyQGIS plugin

all: clean compile package

install: copy2qgis

compile:
	pyuic4 -o Ui_QuickWKT.py Ui_QuickWKT.ui
	pyrcc4 -o resources.py resources.qrc

clean:
	find ./ -name "*.pyc" -exec rm -rf \{\} \;
	rm -f ../QuickWKT.zip
	rm -f Ui_QuickWKT.py resources.py

package: clean
	cd .. && find QuickWKT/  -print|grep -v Make | grep -v zip | grep -v .git | zip QuickWKT.zip -@

localrepo:
	cp ../QuickWKT.zip ~/public_html/qgis/QuickWKT.zip

copy2qgis: package
	unzip -o ../QuickWKT.zip -d ~/.qgis/python/plugins

check test:
	@echo "Sorry: not implemented yet."
