import numpy as np
import math

def generate_scaling(backgr):

    y_pixels = backgr.shape[0]

    SCALE_MAX = 0.8
    SCALE_MIN = 0.6

    scale_vector = np.linspace(SCALE_MIN, SCALE_MAX, y_pixels)

    return scale_vector


def gen_offset_ratio(pic, offset):
    ratio_x = offset[0] / pic.shape[1]
    ratio_y = offset[1] / pic.shape[0]
    return [ratio_x, ratio_y]


def sigmoid(x, grad_magn_inv=None, x_shift=None, y_magn=None, y_shift=None):
    """
    the leftmost dictates gradient: 75=steep, 250=not steep
    the rightmost one dictates y: 0.1=10, 0.05=20, 0.01=100, 0.005=200
    """
    return (1 / (math.exp(-x / grad_magn_inv + x_shift) + y_magn)) + y_shift  # finfin

def get_possible_bc_locs(map_size):
    if map_size == 'small':
        li = [[405, 83], [288, 35], [49, 134]]
    else:
        li = [[1148, 466], [1168, 467], [1034, 456], [1015, 456]]
    return li