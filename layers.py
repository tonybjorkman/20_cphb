import random
random.seed(2)
from copy import deepcopy
import numpy as np
from utils.several import *
import PARAMS
from scipy.stats import chi2

EXPLOSION_WIDTH = PARAMS.EXPLOSION_WIDTH
EXPLOSION_HEIGHT = PARAMS.EXPLOSION_HEIGHT
SMOKE_R_F_FRAMES = PARAMS.SMOKE_R_F_FRAMES
SMOKA_FRAMES = PARAMS.SMOKA_FRAMES
SAIL_CYCLES = PARAMS.SAIL_CYCLES

class LayerAbstract:
    def __init__(self, id, zorder, tl, pic, scale_vector, left_right=None, bc=False):
        self.id = id
        self.zorder = zorder
        self.tl = tl
        self.bc = bc  # background class (for less detailed smokes)
        self.bc_cur = False
        self.pic = pic
        self.scale_vector = scale_vector
        self.occupied = False
        if pic is not None:
            self.extent = [0, self.pic.shape[1], self.pic.shape[0], 0]
        self.left_right = left_right  # which direction the layer is moving
        # self.init_clock = 0  # each obj gets a default init clock, for whatever needs to be inited

    def gen_extent(self, num_frames, mov_x, mov_y):
        """
        Ship and waves
        :param num_frames:
        :param mov_x:
        :param mov_y:
        :return:
        """

        tl_mov = deepcopy(self.tl)  # changed below to generate extent through time

        for i in range(num_frames):

            if tl_mov[1] + self.pic.shape[0] > self.scale_vector.shape[0]:  # ONLY y
                print("gen_extent: outside pic")
                scaling_factor = 0.7
            else:  # obs currently it's always smaller than original pic, but should also be larger sometimes.
                scaling_factor = self.scale_vector[tl_mov[1] + self.pic.shape[0]]  # use bottom of ship

            width_scaled = self.pic.shape[1] * scaling_factor
            height_scaled = self.pic.shape[0] * scaling_factor

            x_ri_scaled = (tl_mov[0] + width_scaled)
            y_do_scaled = (tl_mov[1] + height_scaled)

            self.extent[i] = [tl_mov[0], x_ri_scaled, y_do_scaled, tl_mov[1]]

            tl_mov = [int(self.tl[0] + i * mov_x), int(self.tl[1] + i * mov_y)]


class Smoke(LayerAbstract):
    def __init__(self, id, zorder, tl, pic, scale_vector, s_type, left_right, bc):
        super().__init__(id, zorder, tl, pic, scale_vector, left_right, bc)
        self.smoke_frames = None
        self.s_type = s_type
        if s_type == 'r':
            self.smoke_frames = SMOKE_R_F_FRAMES
        elif s_type == 'a':
            self.smoke_frames = SMOKA_FRAMES
        if bc == True:
            self.left_right = 'l'
        else:
            self.left_right = 'r'
        self.bc_cur = bc
        self.extent_mov = deepcopy(self.extent)
        X = np.arange(0, self.smoke_frames)
        self.alpha_array = np.array([sigmoid(x, grad_magn_inv=-self.smoke_frames/25, x_shift=-10,
                                             y_magn=1, y_shift=0) for x in X])
        self.alpha_array[0] = 0.
        self.smoke_clock = 0
        X = np.arange(1, self.smoke_frames + 1)
        self.scale_vector_s = np.array([np.log(x) / np.log(self.smoke_frames) for x in X])
        # self.scale_vector = np.linspace(0.2, 1, SMOKE_R_F_FRAMES)

    def set_extent_smoke(self, left_right=None):
        scale_factor = self.scale_vector_s[self.smoke_clock] * self.scale_vector[int(self.tl[1])]
        width = self.extent[1] * scale_factor
        height = self.extent[2] * scale_factor

        if self.s_type == 'a':
            if left_right == 'r':
                self.extent_mov = [self.tl[0], self.tl[0] + width,
                                   self.tl[1] + 2 * height / 6, self.tl[1] - 4 * height / 6]  # prevent it to go far down
            elif left_right == 'l':  # still use tl but rename to tr
                self.extent_mov = [self.tl[0] - width, self.tl[0], self.tl[1] + 1 * height / 6,
                                   self.tl[1] - 5 * height / 6]  # prevent it to go far down
        elif self.s_type == 'r':
            if left_right == 'r':
                self.extent_mov = [self.tl[0], self.tl[0] + width,
                                   self.tl[1] + 1 * height / 6, self.tl[1] - 5 * height / 6]
            elif left_right == 'l':
                self.extent_mov = [self.tl[0], self.tl[0] - width,  # flipped horizontally
                                   self.tl[1] + 2 * height / 6, self.tl[1] - 3 * height / 6]

    def set_clock_smoke(self):
        if self.smoke_clock >= self.smoke_frames - 1:
            self.occupied = False
            self.extent_mov = deepcopy(self.extent)
            self.smoke_clock = 0
            self.bc_cur = False
        else:
            self.smoke_clock += 1


class Wave(LayerAbstract):
    def __init__(self, id, zorder, tl, pic, scale_vector,
                 FRAMES_START, FRAMES_STOP):
        super().__init__(id, zorder, tl, pic, scale_vector)

        # ONE WAVE CYCLE
        cycles_currently = PARAMS.WAVES_STEPS_P_CYCLE / (2 * np.pi)
        X = np.arange(0, PARAMS.WAVES_STEPS_P_CYCLE)
        self.alpha_array = np.sin(X / cycles_currently) / 4 + 0.3
        self.wave_clock = random.randint(0, len(X) - 1)

        self.extent = np.zeros(shape=(len(X), 4), dtype=int)
        super().gen_extent(len(X), mov_x=0.05, mov_y=0.04)

    def set_clock_wave(self):

        if self.wave_clock == len(self.alpha_array) - 1:
            self.wave_clock = 0
        else:
            self.wave_clock += 1


class Ship(LayerAbstract):
    def __init__(self, id, zorder, tl, pic, scale_vector,
                 FRAMES_START, FRAMES_STOP,
                 sail_pics, ship_info):
        """
        :param pic: needed for scaling
        :param expl_offset: position relative to tl of ship
        """
        super().__init__(id, zorder, tl, pic, scale_vector)
        total_frames = FRAMES_STOP - FRAMES_START + 5
        self.firing_init_frames = ship_info['firing_frames']
        self.smoka_id = ship_info['smoka_id']
        self.smoka_init_frames = ship_info['smoka_init_frames']  #[12, 40, 80, 100]  # not smoke_r_f
        self.smoka_offset_ratio = gen_offset_ratio(pic, ship_info['smoka_offset'])

        self.smoke_r_f = None
        self.extent = np.zeros(shape=(total_frames, 4), dtype=int)

        super().gen_extent(total_frames, mov_x=ship_info['move_vector'][0], mov_y=ship_info['move_vector'][1])
        self.expl_offset_ratio = gen_offset_ratio(pic, ship_info['explosion_offset'])
        self.explosion_occupied = False  # needed to prevent removing it in animation
        self.extent_explosion = None
        self.extent_clock = 0
        self.expl_clock = 0
        self.smoka_init_clock = 0
        self.sail_init_clock = 0

        # SAILS =====
        self.sails = {}
        self.sail_init_frames = ship_info['sail_init_frames']
        for sail_id in ship_info['sails']:
            sail_offset_ratio = gen_offset_ratio(pic, ship_info['sails'][sail_id]['offset'])
            zorder = 7
            self.sails[sail_id] = Sail(id=sail_id, tl=tl, pic=sail_pics[sail_id], zorder=zorder, scale_vector=scale_vector,
                                       sail_offset_ratio=sail_offset_ratio)

    def update_extent_explosion(self):
        ship_extent = self.extent[self.extent_clock]
        width_ship = (ship_extent[1] - ship_extent[0]) * (1 - random.uniform(0.0, 0.3))
        height_ship = (ship_extent[2] - ship_extent[3]) * (1 - random.uniform(0.0, 0.1))
        expl_tl_x = ship_extent[0] + width_ship * self.expl_offset_ratio[0]
        expl_tl_y = ship_extent[3] + height_ship * self.expl_offset_ratio[1]
        scale_factor = self.scale_vector[self.extent[self.extent_clock, 2]]
        width = EXPLOSION_WIDTH * scale_factor
        height = EXPLOSION_HEIGHT * scale_factor
        self.extent_explosion = [expl_tl_x, expl_tl_x + width, expl_tl_y + height, expl_tl_y]

    def get_tl_smoka(self):
        """
        OBS ship tl not updated
        TODO merge with above.
        :return:
        """
        ship_extent = self.extent[self.extent_clock]
        width_ship = (ship_extent[1] - ship_extent[0]) #* (1 - random.uniform(0.0, 0.4))
        height_ship = (ship_extent[2] - ship_extent[3]) #* (1 - random.uniform(0.0, 0.1))
        smoka_tl_x = int(ship_extent[0] + width_ship * self.smoka_offset_ratio[0])
        smoka_tl_y = int(ship_extent[3] + height_ship * self.smoka_offset_ratio[1])
        return [smoka_tl_x, smoka_tl_y]

    def get_extent_sail(self, sail_id):
        s = self.sails[sail_id]
        ship_extent = self.extent[self.extent_clock]
        width_ship = ship_extent[1] - ship_extent[0]
        height_ship = ship_extent[2] - ship_extent[3]
        sail_tl_x = ship_extent[0] + width_ship * s.offset_ratio[0]
        sail_tl_y = ship_extent[3] + height_ship * s.offset_ratio[1]
        scale_factor = self.scale_vector[self.extent[self.extent_clock, 2]]  # only y
        width = s.extent[1] * scale_factor * s.scale_array[s.sail_clock % len(s.alpha_array)]
        if s.sail_clock > 999999:
            print("warning: sail clock growing very large")
        height = s.extent[2] * scale_factor
        return [sail_tl_x, sail_tl_x + width, sail_tl_y + height, sail_tl_y]


class Sail(LayerAbstract):
    def __init__(self, id, zorder, tl, pic, scale_vector, sail_offset_ratio):
        super().__init__(id, zorder, tl, pic, scale_vector)
        # self.sail_frames = SAIL_FRAMES
        self.offset_ratio = sail_offset_ratio  # relative to ship
        X = np.arange(0, PARAMS.SAIL_CYCLES * PARAMS.SAIL_STEPS_P_CYCLE)
        cycles_currently = PARAMS.SAIL_STEPS_P_CYCLE * PARAMS.SAIL_CYCLES / (2 * np.pi)
        d = cycles_currently / PARAMS.SAIL_CYCLES  # to achieve sought number of cycles
        self.alpha_array = np.sin(X/d) / 2 + 0.5
        self.alpha_array[0] = 0.0
        self.scale_array = np.sin(X/d) / 48 + 1
        self.sail_clock = 0
        # self.extent_mov = deepcopy(self.extent)

    def update_sail_clock(self):
        if self.sail_clock == len(self.alpha_array) - 1:
            self.sail_clock = 0
            self.occupied = False
        else:
            self.sail_clock += 1


class Splash(LayerAbstract):

    def __init__(self, id, zorder, tl, pic, scale_vector):
        super().__init__(id, zorder, tl, pic, scale_vector)
        self.extent_mov = deepcopy(self.extent)
        X = np.arange(0, PARAMS.SPLASH_STEPS_P_CYCLE)
        self.alpha_array = np.array([sigmoid(x, grad_magn_inv=-PARAMS.SPLASH_STEPS_P_CYCLE / 25, x_shift=-10,
                                             y_magn=1, y_shift=0) for x in X])
        self.alpha_array[0] = 0.
        self.scale_vector_s = chi2.pdf(X / 2, PARAMS.SPLASH_STEPS_P_CYCLE // 10) * 6  # obs starts at fire frame
        # self.scale_vector_s = np.array([np.log(x) / np.log(self.smoke_frames) for x in X])
        self.spl_clock = 0

    def set_extent_spl(self):
        scale_factor = self.scale_vector_s[self.spl_clock] * self.scale_vector[int(self.tl[1])]
        width = self.extent[1] * scale_factor
        height = self.extent[2] * scale_factor
        self.extent_mov = [self.tl[0] - width/2, self.tl[0] + width/2, self.tl[1],
                           self.tl[1] - height]  # prevent it to go far down

    def set_clock_spl(self):
        if self.spl_clock >= len(self.alpha_array) - 1:
            self.occupied = False
            self.extent_mov = deepcopy(self.extent)
            self.spl_clock = 0
        else:
            self.spl_clock += 1

