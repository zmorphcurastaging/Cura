# Copyright (c) 2017 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher.

from . import SpaceMouse

from UM.i18n import i18nCatalog
catalog = i18nCatalog("cura")

def getMetaData():
    return {}

def register(app):
    return { "extension": SpaceMouse.SpaceMouse() }
