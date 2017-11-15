# Copyright (c) 2017 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher.

from UM.Math.Vector import Vector
from UM.Math.Matrix import Matrix
from UM.Math.Quaternion import Quaternion
from UM.Application import Application

from UM.Operations.GroupedOperation import GroupedOperation
from UM.Scene.SceneNode import SceneNode
from UM.Operations.SetTransformOperation import SetTransformOperation

import math


##  Provides the tool to manipulate the camera adapted for space mouse

class SpaceMouseCameraTool():

    def __init__(self):
        self.viewController = Application.getInstance().getController()
        self._min_zoom = 1
        self._max_zoom = 2000.0 # the value come from CameraTool, Add gettter to read it from there


    def moveMyCamera(self, mouse_x = 0, mouse_y = 0):
        scene = self.viewController.getScene()
        camera = scene.getActiveCamera()

        if not camera or not camera.isEnabled():
            return

        scene.acquireLock()

        camera_position = camera.getWorldPosition()
        camera.translate(Vector(-mouse_x, mouse_y, 0))
        translation = camera.getWorldPosition() - camera_position

        origin = self.viewController.getCameraTool().getOrigin()
        origin += translation
        self.viewController.getCameraTool().updateOrigin(origin)

        scene.releaseLock()


    def rotateMyCamera(self, vectorUnit = Vector.Unit_Y, mouse_value = 0):

        scene = self.viewController.getScene()
        camera = scene.getActiveCamera()

        if not camera or not camera.isEnabled():
            return

        scene.acquireLock()
        rotation = Quaternion.fromAngleAxis(mouse_value, vectorUnit)

        world = SceneNode.TransformSpace.World  # TransformSpace.Local
        camera.rotate(rotation, world)

        scene.releaseLock()

    def zoomMyCamera(self, zoom_range):
        scene = self.viewController.getScene()
        camera = scene.getActiveCamera()
        origin = self.viewController.getCameraTool().getOrigin()


        if not camera or not camera.isEnabled():
            return

        scene.acquireLock()

        r = (camera.getWorldPosition() - origin).length()
        delta = r * (zoom_range / 128 / 10.0)
        r -= delta

        move_vector = Vector(0.0, 0.0, 1.0)

        move_vector = -delta * move_vector
        if delta != 0:
            if r > self._min_zoom or r < self._min_zoom:
                camera.translate(move_vector)

        scene.releaseLock()


    def thisfunctioncanbeusedForZoom(self, mouse_x: int = 0, mouse_y: int = 0, mouse_z: int = 0):

        scene = self.viewController.getScene()
        camera = scene.getActiveCamera()

        if not camera or not camera.isEnabled():
            return

        scene.acquireLock()

        camera_position = camera.getWorldPosition()
        camera.translate(Vector(-mouse_x, mouse_y, mouse_z, 3))
        translation = camera.getWorldPosition() - camera_position

        origin = self.viewController.getCameraTool().getOrigin()
        origin += translation
        self.viewController.getCameraTool().updateOrigin(origin)

        scene.releaseLock()



