// Copyright (c) 2021 Ultimaker B.V.
// Cura is released under the terms of the LGPLv3 or higher.


import UM 1.2 as UM
import Cura 1.6 as Cura
import QtQuick.Controls 2.15
import QtQuick 2.15

Rectangle
{

    color: UM.Theme.getColor("primary")
    implicitHeight: infoText.lineCount * fontMetrics.height + 2 * UM.Theme.getSize("default_margin").height

    UM.RecolorImage
    {
        id: icon
        source: "../images/marketplace.svg"

        height: 24
        width: height
        anchors
        {
            top: parent.top
            left: parent.left
            margins: UM.Theme.getSize("default_margin").width
        }
    }


    FontMetrics
    {
        id: fontMetrics
        font: UM.Theme.getFont("default")
    }

    Label
    {
        id: infoText
        font: UM.Theme.getFont("default")
        anchors
        {
            right: parent.right
            left: icon.right
            top: parent.top
            margins: UM.Theme.getSize("default_margin").width
        }

        renderType: Text.NativeRendering
        color: "white"
        text: "Streamline your workflow and customize your Ultimaker Cura experience with plugins contributed by our amazing comunity of users and partners."
        wrapMode: Text.Wrap
        elide: Text.ElideRight
        property real lastLineWidth: 0; //Store the width of the last line, to properly position the elision.
        onLineLaidOut:
        {
            if(line.isLast)
            {
                let max_line_width = parent.width - learnMoreButton.width - 2 * UM.Theme.getSize("default_margin").width;
                if(line.implicitWidth > max_line_width)
                {
                    line.width = max_line_width;
                }
                else
                {
                    line.width = line.implicitWidth; //Truncate the ellipsis. We're adding this ourselves.
                }
                infoText.lastLineWidth = line.implicitWidth;
            }
        }
    }

    Cura.TertiaryButton
    {
        id: learnMoreButton
        text: "Learn More"
        textFont: UM.Theme.getFont("default")
        textColor: infoText.color // override normal link color
        leftPadding: 0
        rightPadding: 0
        iconSource: UM.Theme.getIcon("LinkExternal")
        isIconOnRightSide: true
        height: fontMetrics.height
        anchors.left: infoText.left
        anchors.leftMargin: infoText.lastLineWidth + UM.Theme.getSize("narrow_margin").width
        anchors.bottom: infoText.bottom

        onClicked: print("TODO")
    }
}
