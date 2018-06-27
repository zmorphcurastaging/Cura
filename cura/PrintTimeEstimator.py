# Copyright (c) 2018 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher.
from typing import List

import os
import numpy as np
import tensorflow as tf

from UM.Logger import Logger
from UM.Resources import Resources


class PrintTimeEstimator:

    CURA_NN_FILE = "cura_datamodel.ckpt"
    CURA_NN_META_FILE = "cura_datamodel.ckpt.meta"

    def __init__(self) -> None:
        from cura.CuraApplication import CuraApplication
        self._nn_filepath = os.path.join(Resources.getPath(CuraApplication.ResourceTypes.Misc), "time_estimation", self.CURA_NN_FILE)   # type: str
        self._nn_meta_filepath = os.path.join(Resources.getPath(CuraApplication.ResourceTypes.Misc), "time_estimation", self.CURA_NN_META_FILE)   # type: str

    ##  Returns the predicted time given some input data
    def predict(self, data_input: List[float]) -> int:
        data_input_norm = self._normalize(data_input)

        Logger.log("d", "Predicting time using the following data: {data} -> {norm}".format(data = data_input, norm = data_input_norm))
        # tf.reset_default_graph()

        with tf.Session() as sess:
            # Initialize the variables
            try:
                saver = tf.train.import_meta_graph(self._nn_meta_filepath)
                saver.restore(sess, self._nn_filepath)
                # Get the tensors
                graph = tf.get_default_graph()
                input = graph.get_tensor_by_name("input:0")
                output = graph.get_tensor_by_name("output:0")
                # Validate the NN with the provided test data
                predicted_value = sess.run(output, feed_dict = {input: [data_input_norm]})
                Logger.log("d", "{output}".format(output = predicted_value))
            except Exception as e:
                Logger.log("i", "No model file found in {path}. Can't continue the prediction. Exception:\n{exc}".format(path = self._nn_filepath, exc=str(e)))
                return -1

        return int(predicted_value[0][0] * 3600)    # The result is in hours, so convert it to seconds

    ##  Normalize the input data between 0 and 1 since it is the input of the NN
    #   TODO Now it is done manually, in the future it must be done in a different way
    def _normalize(self, data: List[float]) -> np.ndarray:
        Logger.log("d", "Normalizing time using the following data: {}".format(input))

        ## HACK: Hardcoded normalize matrix: TODO
        min = np.array([1.0, 6.0, 0.06, 0.4])
        max = np.array([1000.0, 600.0, 0.15, 8.0])

        return (data - min) / (max - min)
