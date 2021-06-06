import numpy as np
from copy import deepcopy

"""
OBS STARTS AT TOP LEFT
"""

class ENV:

    def __init__(self, PM):

        self.LITE = '25_40'  # largest zoom in

        if self.LITE == '25_40':  # smallest level
            self.DIMS = (25, 40)  # map extent
            self.tp_name = 'tree_40_25'
            self.ground_y = 22
        elif self.LITE == '250_400':  # medium
            self.DIMS = (250, 400)
            self.tp_name = 'tree_400_250'
            self.ground_y = 248  # int(self.DIMS[0] - self.DIMS[0] / 6)
        elif self.LITE == 'fin':  # final (largest)
            self.DIMS = (720, 1280)
            self.tp_name = 'tree0_fin4'
            # self.tp_name = 'root0_fin2'
            # self.tp_name = 'tree1_fin'
            # self.tp_name = 'root1_fin'
            self.ground_y = 718  # int(self.DIMS[0] - self.DIMS[0] / 6)  # 718

        self.START_COORDS = [self.ground_y, self.DIMS[1] // 2]  # [ROW, COL] OVERWRITTEN
        self.START_COORDS_ST = [self.ground_y, (self.DIMS[1] // 2) + (self.DIMS[1] // 4)]
        # self.START_COORDS_ST = [200, 800]  # y, x
        # self.G_POINT = deepcopy(self.START_COORDS)  # START_COORDS are used to init root.coords (without copy) so... sigh

        # e_sun[0:ground_y, :] = 1
        # sun_lin = np.linspace(0.95, 0.2, ground_y)
        # _, yv = np.meshgrid(np.zeros((1, DIMS[1])), sun_lin)
        # e_sun[0:ground_y, :] = yv
        self.e_s = np.full(self.DIMS, 0.005, dtype=float)
        self.round_sun(PM)

        self.e_water = np.zeros(self.DIMS, dtype=float)
        self.e_water[self.ground_y:self.DIMS[0], :] = 1

        self.e_tp = self.tree_pic()

        self.e_o = np.zeros(self.DIMS, dtype=bool)
        self.update_env(PM, self.START_COORDS, type='occupy')  # occupies the root area

        self.define_hardcoded_areas()

    def round_sun(self, PM):
        size_up = self.START_COORDS[1]   # x used since
        # y = START_COORDS[0] - size // 2
        # x = START_COORDS[1] - size // 2
        # sun_lin = np.linspace(0.7, 0.95, size_up)


        sun_lin = np.linspace(0.7, 0.95, PM.NUM_ROUND_SUN_LOOPS)

        cur_sun = sun_lin[0]
        # cur_y_x = [START_COORDS[0], START_COORDS[1]-1]  # starts left
        # flag_circle_done = False
        for i in range(1, len(sun_lin)):
            cur_y_x = [self.START_COORDS[0], self.START_COORDS[1] - i]
            self.e_s[cur_y_x[0], cur_y_x[1]] = cur_sun  # left
            while cur_y_x[1] < self.START_COORDS[1]:  # direction up-right
                cur_y_x = [cur_y_x[0] - 1, cur_y_x[1] + 1]
                self.e_s[cur_y_x[0], cur_y_x[1]] = cur_sun
            while cur_y_x[0] < self.START_COORDS[0]: # direction down-right
                cur_y_x = [cur_y_x[0] + 1, cur_y_x[1] + 1]
                self.e_s[cur_y_x[0], cur_y_x[1]] = cur_sun
            # while cur_y_x[1] > START_COORDS[1]:  # direction down-left
            #     cur_y_x = [cur_y_x[0] + 1, cur_y_x[1] - 1]
            #     e_sun[cur_y_x[0], cur_y_x[1]] = cur_sun
            # while cur_y_x[0] > START_COORDS[0]:  # direction up-left
            #     cur_y_x = [cur_y_x[0] - 1, cur_y_x[1] - 1]
            #     e_sun[cur_y_x[0], cur_y_x[1]] = cur_sun

            cur_sun = sun_lin[i]

    def update_env(self, PM, a_coords, type=None):  # OW_MID_Y_kernel, MID_X_kernel, o_DIV,
        """
        the +1 is due to UBE
        """
        if type == 'occupy':
            self.e_o[int(a_coords[0] - PM.LOW_MID_Y_kernel / PM.EXP_o_DIV):int(a_coords[0] + PM.LOW_MID_Y_kernel / PM.EXP_o_DIV) + 1,
            int(a_coords[1] - PM.MID_X_kernel / PM.EXP_o_DIV):int(a_coords[1] + PM.MID_X_kernel / PM.EXP_o_DIV) + 1 + 1] = True  # +1 cuz float div, +1 UBE
        elif type == 'prune':
            self.e_o[int(a_coords[0] - PM.LOW_MID_Y_kernel / PM.PRU_o_DIV):int(a_coords[0] + PM.LOW_MID_Y_kernel / PM.PRU_o_DIV) + 1,
            int(a_coords[1] -PM.MID_X_kernel / PM.PRU_o_DIV):int(a_coords[1] + PM.MID_X_kernel / PM.PRU_o_DIV) + 1 + 1] = False

    def update_g_p(self, e_o):  # no N in this version
        e_o_li = np.argwhere(e_o == True)

        mean_y = int(np.mean(e_o_li[0]))
        mean_x = int(np.mean(e_o_li[1]))

        G_POINT = [mean_y, mean_x]

        return G_POINT

    def tree_pic(self):
        import cv2
        tp = cv2.imread('./maps/' + self.tp_name + '.png', cv2.IMREAD_GRAYSCALE)
        tp[tp == 0] = 1
        tp[tp == 255] = 0

        return tp

    def define_hardcoded_areas(self):
        "ONLY FOR THE ALGO, NOT FRONTEND"
        if self.LITE == '25_40':
            pass
        elif self.LITE == '250_400':
            pass
        elif self.LITE == 'fin':
            self.hardcoded_areas = {'down': [[(563, 700), (748, 787)]]}

            # # tree0
            # self.e_s[563:700, 748:787] = 0.7
            # self.e_s[575:580, 495:524] = 1.2

            # # root0
            # self.e_s[694:708, 566:599] = 3

            # tree1
            self.e_s[533:595, 746:] = 1.2 # lower right
            # self.e_s[564:, 778:] = 2.0  # not sure



