# Copyright (c) 2018 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher.

from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty, QTimer

from UM.Qt.Duration import Duration
import tensorflow as tf

##  A class for calculating the estimated print time, given a model an a bunch of settings.
class PrintEstimation(QObject):

    MODEL_FILE = "cura_datamodel"

    def __init__(self, application, parent = None) -> None:
        super().__init__(parent)
        self._application = application
        self._estimated_print_time = Duration(None, self)   # type: Duration

        self._update_time_estimation = QTimer()
        self._update_time_estimation.setInterval(500)
        self._update_time_estimation.setSingleShot(True)
        self._update_time_estimation.timeout.connect(self._updateTimeEstimation)

        self._application.getController().getScene().sceneChanged.connect(self._updateTimeEstimationDelayed)

    estimatedPrintTimeChanged = pyqtSignal()

    @pyqtProperty(Duration, notify = estimatedPrintTimeChanged)
    def estimatedPrintTime(self):
        return self._estimated_print_time

    def updateTimeEstimationDelayed(self) -> None:
        self._update_time_estimation.start()

    def updateTimeEstimation(self) -> None:
        self._estimated_print_time.setDuration(10)
        self.estimatedPrintTimeChanged.emit()
