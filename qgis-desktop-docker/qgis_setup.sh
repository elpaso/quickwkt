#!/bin/bash
# Setup QGIS
# - disable tips
# - enable the plugin

PLUGIN_NAME=$1
CONF_FOLDER="/root/.config/QGIS"
CONF_FILE="${CONF_FOLDER}/QGIS2.conf"
PLUGIN_FOLDER="/root/.qgis2/python/plugins"


# Creates the config file
mkdir -p $CONF_FOLDER
if [ -e "$CONF_FILE" ]; then
    rm -f $CONF_FILE
fi
touch $CONF_FILE

# Creates plugin folder
mkdir -p $PLUGIN_FOLDER

# Disable tips
printf "[Qgis]\n" >> $CONF_FILE
SHOW_TIPS=`qgis --help 2>&1 | head -2 | grep 'QGIS - ' | perl -npe 'chomp; s/QGIS - (\d+)\.(\d+).*/showTips\1\2=false/'`
printf "$SHOW_TIPS\n\n" >> $CONF_FILE


if [ -n "$VAR" ]; then
    # Enable plugin
    printf '[PythonPlugins]\n' >> $CONF_FILE
    printf "${PLUGIN_NAME}=true\n\n" >> $CONF_FILE
fi
