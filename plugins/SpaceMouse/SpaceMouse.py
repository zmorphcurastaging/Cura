# Copyright (c) 2017 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher.


from threading import Thread

from UM.Extension import Extension
from UM.i18n import i18nCatalog
import sys


from UM.Platform import Platform

if Platform.isLinux():
    import evdev
else:
    from .SpaceNavigator import *  # the source coude is updated. For Windows. this class requires pip3 install pywinusb
    from time import sleep

from .SpaceMouseMovementHanlder import SpaceMouseMovementHanlder
i18n_catalog = i18nCatalog("cura")


class SpaceMouse(Extension):
    def __init__(self):
        super().__init__()
        self.state = False
        self.addMenuItem(i18n_catalog.i18nc("@item:inmenu", "Run Space Mouse"), self.start3dMouse)

    # TODO This method can be automated to check new connected devices, using external thread
    # and if one of new devices is space mouse restart "read" thread
    def start3dMouse(self):
        try:
            self.mouse_handler = SpaceMouseMovementHanlder()
            thread = None
            if Platform.isLinux():
                thread = Thread(target=self.readDataLinux, args=(10,))
            else:
                thread = Thread(target=self.readDataWindows, args=(10,))
            thread.start()

        except Exception as e:
            print(e)


    def readDataWindows(self, args):
        #TODO move open to separate class, the method open also let to use button callbacks
        #TODO the move of mouse is not smooth (for Z), check when the call back is triggered
        success = open(callback=self.mouseSensorCallBack)
        if success:
            self.state = read()
            while 1:
                sleep(0.5)

    # Mouse movement callback
    def mouseSensorCallBack(self, name, value):
        new_value = value * 1000 #  because on linux receives prime number
        self.mouse_handler.handleMouseMovement(type=name, value=new_value)


    # This method reads hid messages using evdev library (Ubuntu)
    def readDataLinux(self, args):
        device = evdev.InputDevice('/dev/input/event7')  # to find this id use sudo evtest
        pp = device.active_keys(verbose=True)

        s = device.read_loop()

        all_events = device.capabilities(verbose=False)

        for event in s:
            if event.type > 0 and event.type < 4:
                ev = evdev.categorize(event)
                msg = ev.__str__()

                rel_index = msg.find("REL")
                command = msg[rel_index:-1]

                self.mouse_handler.handleMouseMovement(type = command, value = event.value)
