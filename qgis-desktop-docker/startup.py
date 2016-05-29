"""Disable QGIS modal error dialog"""
from qgis import utils

def _open_stack_dialog(type, value, tb, msg, pop_error=True):
    print(msg)

utils.open_stack_dialog=_open_stack_dialog
