import random
from copy import deepcopy
import numpy as np


class LayerAbstract:
    def __init__(self):
        self.id = None
        self.top_left = []
        self.extent = []
        self.z = None
        self.left_right = 'right'  # which direction the layour is moving

class Smoke(LayerAbstract):
    def __init__(self, id, z):
        super().__init__()
        self.id = id
        self.z = z

class Wave(LayerAbstract):
    def __init__(self, id, top_left, pic, z,
                 FRAMES_START, FRAMES_STOP, scale_vector):
        super().__init__()
        self.id = id
        self.top_left = top_left
        # self.extent = [top_left[0], top_left[0] + pic.shape[1], top_left[1] + pic.shape[0], top_left[1]]
        self.z = z

        # ONE WAVE CYCLE
        x = np.arange(0, np.pi, 0.1)
        self.alpha_array = np.sin(2 * x) / 4 + 0.3
        self.wave_clock = random.randint(0, len(x) - 1)

        self.extent = np.zeros(shape=(len(x), 4), dtype=int)
        top_left_mov = deepcopy(top_left)

        scaling_factor = scale_vector[top_left_mov[1] + pic.shape[0]]  # use bottom of ship

        width_scaled = pic.shape[1] * scaling_factor
        height_scaled = pic.shape[0] * scaling_factor

        for i in range(len(x)):
            x_ri_scaled = (top_left_mov[0] + width_scaled)
            y_do_scaled = (top_left_mov[1] + height_scaled)

            self.extent[i] = [top_left_mov[0],
                              x_ri_scaled,
                              y_do_scaled,
                              top_left_mov[1]
                              ]

            top_left_mov = [int(top_left[0] + i * 0.1), int(top_left[1] + i * 0.1)]


class Ship(LayerAbstract):
    def __init__(self, id, top_left, pic, z,
                 FRAMES_START, FRAMES_STOP, scale_vector,
                 expl_offset):
        """
        :param id:
        :param top_left:
        :param pic: needed for scaling
        :param z:
        :param FRAMES_START:
        :param FRAMES_STOP:
        :param scale_vector:
        :param expl_offset:
        """
        super().__init__()
        total_frames = FRAMES_STOP - FRAMES_START + 5
        self.id = id
        self.top_left = top_left
        self.firing_frames = [5]
        # self.firing_extent = [[10, 40, 50, 10]]  # relative to top_left of current extent
        # self.expl_xy = expl_xy
        self.expl_extent = np.zeros(shape=(total_frames, 4))
        self.smoke_extent = np.zeros(shape=(total_frames, 4))
        top_left_mov = deepcopy(top_left)

        self.extent = np.zeros(shape=(total_frames, 4), dtype=int)

        for i in range(total_frames):

            if top_left_mov[1] + pic.shape[0] > scale_vector.shape[0]:
                print("outside pic")
                scaling_factor = 1.0
            else:
                scaling_factor = scale_vector[top_left_mov[1] + pic.shape[0]]  # use bottom of ship
            width_scaled = pic.shape[1] * scaling_factor
            height_scaled = pic.shape[0] * scaling_factor
            x_ri_scaled = (top_left_mov[0] + width_scaled)
            y_do_scaled = (top_left_mov[1] + height_scaled)

            self.extent[i] = [top_left_mov[0],
                              x_ri_scaled,
                              y_do_scaled,
                              top_left_mov[1]
                              ]

            self.expl_extent[i] = [self.extent[i][0] + scaling_factor * expl_offset[0],
                                self.extent[i][0] + scaling_factor * expl_offset[0] + scaling_factor * 20,
                                self.extent[i][3] + scaling_factor * expl_offset[1] + scaling_factor * 10,
                                self.extent[i][3] + scaling_factor * expl_offset[1]]

            self.smoke_extent[i] = [self.extent[i][0] + scaling_factor * expl_offset[0],
                                self.extent[i][0] + scaling_factor * expl_offset[0] + scaling_factor * 80,
                                self.extent[i][3] + scaling_factor * expl_offset[1] + scaling_factor * 20,
                                self.extent[i][3] + scaling_factor * expl_offset[1]]

            # HERE DECIDE HOW MUCH IN X AND Y IT MOVES

            top_left_mov = [int(top_left[0] + i * 0.3), int(top_left[1] + i * 0.1)]

        self.i_extent = 0
        self.z = z



