# Copyright (c) 2017 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher.

from .SpaceMouseCameraTool import SpaceMouseCameraTool
from UM.Math.Vector import Vector

class MovementType:

    REL_X  = "REL_X"
    REL_Y  = "REL_Y"
    REL_Z  = "REL_Z"
    REL_RX = "REL_RX"
    REL_RY = "REL_RY"
    REL_RZ = "REL_RZ"

class SpaceMouseMovementHanlder():

    SENSITY_DIVIDER = 500 # increase number to make mouse less sensitive

    mouse_x = 0
    mouse_y = 0
    mouse_z = 0
    mouse_rx = 0
    mouse_ry = 0
    mouse_rz = 0

    def __init__(self):
        self.camera_tool = SpaceMouseCameraTool()

    def handleMouseMovement(self, type: str, value: int):

        new_value = value / self.SENSITY_DIVIDER

        if type == MovementType.REL_X:
            self.camera_tool.moveMyCamera(mouse_x=new_value * 10, mouse_y=0)
        elif type == MovementType.REL_Y:
            self.camera_tool.moveMyCamera(mouse_x = 0, mouse_y = new_value * 10)
        elif type == MovementType.REL_Z:
            self.camera_tool.zoomMyCamera(zoom_range = -1 * new_value * 100)


        # TODO below types has wrong implementation
        # elif type == MovementType.REL_RX:
        #     self.camera_tool.rotateMyCamera(vectorUnit=Vector.Unit_X, mouse_value= -1 * new_value / 10)
        # elif type == MovementType.REL_RY:
        #     self.camera_tool.rotateMyCamera(vectorUnit=Vector.Unit_Y, mouse_value= -1 * new_value / 10)
        # elif type == MovementType.REL_RZ:
        #     self.camera_tool.rotateMyCamera(vectorUnit= Vector.Unit_Z, mouse_value = new_value)

