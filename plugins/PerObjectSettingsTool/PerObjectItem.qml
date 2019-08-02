// Copyright (c) 2019 Ultimaker B.V.
// Uranium is released under the terms of the LGPLv3 or higher.

import QtQuick 2.10
import QtQuick.Controls 2.3

import UM 1.2 as UM
import Cura 1.0 as Cura

Cura.CheckBoxWithTooltip
{
    id: check
    x: model.depth * UM.Theme.getSize("default_margin").width
    checked: addedSettingsModel.getVisible(model.key)

    onClicked:
    {
        addedSettingsModel.setVisible(model.key, checked)
        UM.ActiveTool.forceUpdate()
    }
    text: definition.label
    tooltip: model.description

    Connections
    {
        target: addedSettingsModel
        onVisibleCountChanged:
        {
            checked = addedSettingsModel.getVisible(model.key)
        }
    }
}


