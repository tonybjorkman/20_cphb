import numpy as np
import random

class Params:

    def __init__(self, _rand_seed):
        random.seed(_rand_seed)
        np.random.seed(_rand_seed)

        # FIN
        # self.NUM_ITERS = 12000  # bcs it starts at 1 (due to mod)
        # self.NUM_BRANCHES_PER_NODE = 3  # root0: 4
        # self.C = 2.5  # 3.4   # tree0: 2.5  tree1: 1.8
        # self.EXPANSION_BIAS_P = 0.99  # temp: 0.5 tree0: 0.9  CAN BE IMPORTANT this just smoothes out branches  tree1: 0.99
        # self.SHADOW_AMOUNT = 0.01  # 0.01 more = more shadow underneath created neurons MORE SHADOW = CRAZIER SHAPES
        # self.NODE_DEPTH_V = 0.2  # tree0: 2  # root0: 5
        # self.IMBALANCE_V = 1.  # tree0/root0: 2.31 this one is normalized LATER
        # self.VALUE_DISTR = [None, None, None, None, self.NODE_DEPTH_V, self.IMBALANCE_V]  # sun, tp, dist_from_root_y, dist_from_root_x, node_depth, imbalance
        # self.PRUNING_FREQ_MOD = 45  # 45
        # self.CRAZY_RECURSIVE_NODE_SADISM = 'just_torture'
        # self.REINCARNATION_P = 0.1  # 0.1
        # self.SUN_FROM = 0.1  # tree0: 0.01 0.6  # root0: 0.1
        # self.SUN_TO = 0.1  # 0.1  # tree1: 0.01
        # self.TP_FROM = 0.7  # tree0: 0.01  root0: 0.99
        # self.TP_TO = 0.9  #0.01 0.99
        # self.TP_C = 0.7  # .001 if no tp found, what is likelihood no expansion will happen. More=more punishment  # tree1: 0.8 MORE: MAKES SHAPES MORE BEAUTIFUL
        # self.DIST_FROM_ROOT_X_FROM = 0.01
        # self.DIST_FROM_ROOT_X_TO = 0.01
        # self.DIST_FROM_ROOT_Y_FROM = 0.7
        # self.DIST_FROM_ROOT_Y_TO = 0.7
        # self.v_schedule_sun = np.linspace(self.SUN_FROM, self.SUN_TO, self.NUM_ITERS)  # the more late sun, the more spread it will be
        # self.v_schedule_tp = np.linspace(self.TP_FROM, self.TP_TO, self.NUM_ITERS)**2
        # self.v_schedule_dist_from_root_y = np.linspace(self.DIST_FROM_ROOT_X_FROM, self.DIST_FROM_ROOT_X_TO,
        #                                                self.NUM_ITERS)
        # self.v_schedule_dist_from_root_x = np.linspace(self.DIST_FROM_ROOT_Y_FROM, self.DIST_FROM_ROOT_Y_TO,
        #                                                self.NUM_ITERS)  # more = more punishment
        #
        # # PREVIOUSLY IN ENV
        # self.MID_X_kernel = 5  # 4 how much EXP search to left and right HAS TO BE ODD
        # self.LOW_MID_Y_kernel = 7  # 6how much EXP search to up
        # self.EXP_o_DIV = 7  # 5 the more the smaller the occupied area: EXPANSION DOES NOT USE THIS. Logic: large search area but only used location should be occupied
        # self.PRU_o_DIV = 7 # 5 the more the less area will be unoccupied
        # self.EXPAND_KERNEL_DEF_DEPTH = 1  # tree0: 10 root0: 1  tree1: 6 root1: 1
        # self.NUM_ROUND_SUN_LOOPS = 50  # 600 fin  # tree0: 600  root0: 100
        # self.ST_SEED = _rand_seed

        self.NUM_ITERS = 1500  # bcs it starts at 1 (due to mod)
        self.NUM_BRANCHES_PER_NODE = 3  # root0: 4
        self.C = 3.5  # 3.4   # tree0: 2.5  tree1: 1.8
        self.EXPANSION_BIAS_P = 0.3  # temp: 0.5 tree0: 0.9  CAN BE IMPORTANT this just smoothes out branches  tree1: 0.99
        self.SHADOW_AMOUNT = 0.01  # 0.01 more = more shadow underneath created neurons MORE SHADOW = CRAZIER SHAPES
        self.NODE_DEPTH_V = 0.2  # tree0: 2  # root0: 5
        self.IMBALANCE_V = 1.  # tree0/root0: 2.31 this one is normalized LATER
        self.VALUE_DISTR = [None, None, None, None, self.NODE_DEPTH_V,
                            self.IMBALANCE_V]  # sun, tp, dist_from_root_y, dist_from_root_x, node_depth, imbalance
        self.PRUNING_FREQ_MOD = 46  # 45
        self.CRAZY_RECURSIVE_NODE_SADISM = 'just_torture'
        self.REINCARNATION_P = 0.1  # 0.1
        self.SUN_FROM = 0.99  # tree0: 0.01 0.6  # root0: 0.1
        self.SUN_TO = 0.5  # 0.1  # tree1: 0.01
        self.TP_FROM = 0.01  # tree0: 0.01  root0: 0.99
        self.TP_TO = 0.012  # 0.01 0.99
        self.TP_C = 0.9  # .001 if no tp found, what is likelihood no expansion will happen. More=more punishment  # tree1: 0.8 MORE: MAKES SHAPES MORE BEAUTIFUL
        self.DIST_FROM_ROOT_X_FROM = 0.01
        self.DIST_FROM_ROOT_X_TO = 0.01
        self.DIST_FROM_ROOT_Y_FROM = 0.7
        self.DIST_FROM_ROOT_Y_TO = 0.7
        self.v_schedule_sun = np.linspace(self.SUN_FROM, self.SUN_TO,
                                          self.NUM_ITERS)  # the more late sun, the more spread it will be
        self.v_schedule_tp = np.linspace(self.TP_FROM, self.TP_TO, self.NUM_ITERS) ** 2
        self.v_schedule_dist_from_root_y = np.linspace(self.DIST_FROM_ROOT_X_FROM, self.DIST_FROM_ROOT_X_TO,
                                                       self.NUM_ITERS)
        self.v_schedule_dist_from_root_x = np.linspace(self.DIST_FROM_ROOT_Y_FROM, self.DIST_FROM_ROOT_Y_TO,
                                                       self.NUM_ITERS)  # more = more punishment

        # # PREVIOUSLY IN ENV
        self.MID_X_kernel = 7  # 4 how much EXP search to left and right HAS TO BE ODD
        self.LOW_MID_Y_kernel = 7  # 6how much EXP search to up
        self.EXP_o_DIV = 2  # 7  the more the smaller the occupied area: EXPANSION DOES NOT USE THIS. Logic: large search area but only used location should be occupied
        self.PRU_o_DIV = 2  # 7 the more the less area will be unoccupied
        self.EXPAND_KERNEL_DEF_DEPTH = 4  # tree0: 10 root0: 1  tree1: 6 root1: 1
        self.NUM_ROUND_SUN_LOOPS = 5  # 600 fin  # tree0: 600  root0: 100
        self.ST_SEED = _rand_seed

