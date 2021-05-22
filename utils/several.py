import numpy as np

def generate_scaling(backgr):

    y_pixels = backgr.shape[0]

    SCALE_MAX = 1.0
    SCALE_MIN = 0.001

    scale_vector = np.linspace(SCALE_MIN, SCALE_MAX, y_pixels)

    return scale_vector