import cv2
import numpy as np

class KalmanBox:
    def __init__(self):
        self.kf = cv2.KalmanFilter(4, 2)

        self.kf.measurementMatrix = np.array([[1,0,0,0],
                                              [0,1,0,0]], np.float32)

        self.kf.transitionMatrix = np.array([[1,0,1,0],
                                             [0,1,0,1],
                                             [0,0,1,0],
                                             [0,0,0,1]], np.float32)

        self.kf.processNoiseCov = np.eye(4, dtype=np.float32) * 0.05
        self.kf.measurementNoiseCov = np.eye(2, dtype=np.float32) * 0.5

    def update(self, cx, cy):
        measured = np.array([[np.float32(cx)], [np.float32(cy)]])
        self.kf.correct(measured)
        pred = self.kf.predict()
        return int(pred[0][0]), int(pred[1][0])