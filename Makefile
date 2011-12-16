# Makefile for a PyQGIS plugin

all: compile

dist: package

install: copy2qgis

PY_FILES = QuickWKT.py QuickWKTDialog.py __init__.py
EXTRAS = about_icon.png quickwkt_icon.png
UI_FILES = Ui_QuickWKT.py
                                                                                                                                                                                                                                                                                                                                                                                                               RESOURCE_FILES = resources.py

compile: $(UI_FILES) $(RESOURCE_FILES)

%.py : %.qrc
	pyrcc4 -o $@  $<

%.py : %.ui
	pyuic4 -o $@ $<



clean:
	find ./ -name "*.pyc" -exec rm -rf \{\} \;
	rm -f ../QuickWKT.zip
	rm -f Ui_QuickWKT.py resources.py

package:
	cd .. && find QuickWKT/  -print|grep -v Make | grep -v zip | grep -v .git | zip QuickWKT.zip -@

localrepo:
	cp ../QuickWKT.zip ~/public_html/qgis/QuickWKT.zip

copy2qgis: package
	unzip -o ../QuickWKT.zip -d ~/.qgis/python/plugins

check test:
	@echo "Sorry: not implemented yet."
