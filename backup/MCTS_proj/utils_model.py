import numpy as np
import random
# from ENV import LOW_MID_Y_kernel, MID_X_kernel, ground_y, LITE, EXPAND_KERNEL_DEF_DEPTH



def get_possible_action(m, PM, ENV, sp):  # maybe also ground_y shoudl be used

    if sp is m.root:  # just go straight up
        # only gives one try for these nodes, after this they can't expand
        if ENV.LITE == '25_40':
            hardcoded_firsts = [[2, 2], [3, 0]]  # first one is both left and right. [y, x]
        elif ENV.LITE == '250_400':
            hardcoded_firsts = [[5, 8], [10, 0]]
        elif ENV.LITE == 'fin':
            hardcoded_firsts = [[5, 8], [10, 0]]  # first one is both left and right

        ac = None  # actionCoords
        if len(m.root.children) < 1:
            ac = [m.root.coords[0] - hardcoded_firsts[0][0], m.root.coords[1] - hardcoded_firsts[0][1]]
        elif len(m.root.children) < 2:
            ac = [m.root.coords[0] - hardcoded_firsts[1][0], m.root.coords[1]]
        elif len(m.root.children) < 3:
            ac = [m.root.coords[0] - hardcoded_firsts[0][0], m.root.coords[1] + hardcoded_firsts[0][1]]
        else:
            ac = [m.root.coords[0] - random.randint(5, 8), m.root.coords[1] + random.randint(-5, 5)]
        return ac, 'root_exp'


    kernel_type = 'right_up'  # default
    diff_x = sp.coords[1] - sp.parent.coords[1]  # if sp is to the right of sp.parent this is positive. if so do left move
    diff_x_g = sp.coords[1] - m.root.coords[1]
    if diff_x < 0:  # sp to the left: i.e. movement is right
        kernel_type = 'left_up'
    if sp.d < PM.EXPAND_KERNEL_DEF_DEPTH or abs(diff_x_g) < PM.MID_X_kernel*2:  # if it's centrally located
        kernel_type = 'default_up'  #
    elif sp.d > PM.EXPAND_KERNEL_DEF_DEPTH and random.random() < 0.4:
        kernel_type = 'default'  #

    hardcoded_area = check_hardcoded_area(sp.coords[0], sp.coords[1])
    if hardcoded_area == 'down':
        kernel_type = 'down'

    MULT_Y = 1
    MULT_X = 1  # epilogue. 3

    y_up = None
    y_do = None
    x_le = None
    x_ri = None

    if kernel_type == 'default_up': # UBE!!! will have to chagne for downward dir CHECK SIGN!
        y_up = -PM.LOW_MID_Y_kernel*MULT_Y  # 16
        y_do = 0  # UBE
        x_le = -PM.MID_X_kernel
        x_ri = PM.MID_X_kernel + 1 + 1  #  + 1 since this is positive, +1 UBE
    elif kernel_type == 'left_up':
        y_up = -PM.LOW_MID_Y_kernel
        y_do = 0  # UBE
        x_le = -PM.MID_X_kernel*MULT_X
        x_ri = 1
    elif kernel_type == 'right_up':
        y_up = -PM.LOW_MID_Y_kernel
        y_do = 0  # UBE
        x_le = 1
        x_ri = PM.MID_X_kernel*MULT_X + 1
    elif kernel_type == 'default':
        y_up = -PM.LOW_MID_Y_kernel * MULT_Y  # 16
        y_do = PM.LOW_MID_Y_kernel * MULT_Y  # UBE
        x_le = -PM.MID_X_kernel
        x_ri = PM.MID_X_kernel + 1 + 1  # + 1 since this is positive, +1 UBE
    elif kernel_type == 'down':
        y_up = -PM.LOW_MID_Y_kernel // 2
        y_do = PM.LOW_MID_Y_kernel * MULT_Y
        x_le = -PM.MID_X_kernel
        x_ri = PM.MID_X_kernel + 1 + 1  # + 1 since this is positive, +1 UBE

    pnc = ENV.e_o[(sp.coords[0] + y_up):min((sp.coords[0] + y_do), ENV.ground_y), (sp.coords[1] + x_le):(sp.coords[1] + x_ri)]  # possibleNewCoords
    sun_c = ENV.e_s[(sp.coords[0] + y_up):min((sp.coords[0] + y_do), ENV.ground_y), (sp.coords[1] + x_le):(sp.coords[1] + x_ri)]
    tp_c = ENV.e_tp[(sp.coords[0] + y_up):min((sp.coords[0] + y_do), ENV.ground_y), (sp.coords[1] + x_le):(sp.coords[1] + x_ri)]  # if tree_pic is gona be incorporated here

    pnc_li = np.argwhere(pnc == False)  # OBS this is from the perspective of sp

    if len(pnc_li) < 1:  # early exit; # nowhere to place child
        # sp.can_expand = False THIS IS HANDLED OUTSIDE
        # print("state " + sp.id + " is now not expandable")
        return None, 'could_not_find_free_coords'

    # SELECT BEST VALUE WITHIN PNC -----------------
    free_sun_c_vals_ss = sun_c[pnc_li[:, 0], pnc_li[:, 1]]  # these are organized as flattened array from the 2D one
    free_sun_c_vals = tp_c[pnc_li[:, 0], pnc_li[:, 1]]  # these are organized as flattened array from the 2D one
    free_sun_c_vals_tp = free_sun_c_vals_ss * free_sun_c_vals
    if np.amax(free_sun_c_vals_tp) < 0.001 and random.random() < PM.TP_C:  # the more TP_C, the more punishment
        return None, 'could_not_find_free_coords'
    # if random.random() < 0.99:
    best_c = np.argwhere(free_sun_c_vals_tp == np.amax(free_sun_c_vals_tp))[0][0]
    # else:
        # best_c = np.where(free_sun_c_vals == np.amax(free_sun_c_vals))[0][0]
    if random.random() < PM.EXPANSION_BIAS_P:
        pnc_coords = pnc_li[best_c]
    else:
        pnc_coords = random.choice(pnc_li)

    # 1. the kernel is placed on the env 2. ac starts at top left on the env-kernel. 3. ac is aligned.
    ac_start = [sp.coords[0] + y_up, sp.coords[1] + x_le]  #
    ac = [ac_start[0] + pnc_coords[0], ac_start[1] + pnc_coords[1]]

    if ac[0] < 0 or ac[1] < 0 or ac[0] > ENV.ground_y:
        raise Exception("joException tree growing too large")
    # logging
    if kernel_type == 'default_up':
        m.num_default_up_exp += 1
    elif kernel_type == 'left_up':
        m.num_left_up_exp += 1
    elif kernel_type == 'right_up':
        m.num_right_up_exp += 1
    elif kernel_type == 'default':
        m.num_default_exp += 1
    elif kernel_type == 'down':
        m.num_down_exp += 1

    return ac, 'sucess'


def get_pnc_li(m, sp, G_POINT):
    pnc = None
    kernel_type = 'right'
    diff_x = sp.coords[1] - G_POINT[1]  # if sp is to the right of G this is positive
    if diff_x < 0:  # sp to the left
        kernel_type = 'left'

    if kernel_type == 'right':
        pnc = m.e_o[(sp.coords[0] - LOW_MID_Y_kernel):sp.coords[0], (sp.coords[1] - MID_X_kernel):(
                    sp.coords[1] + MID_X_kernel + 1)]  # UBE!!! will have to chagne for downward dir CHECK SIGN!

    pnc_li = np.argwhere(pnc == False)  # OBS this is from the perspective of sp

    return None


def check_hardcoded_area(y, x):
    ha = {'down': [[(563, 700), (748, 787)]]}
    ha = ha['down'][0]
    if (y > ha[0][0] and y < ha[0][1]) and (x > ha[1][0] and x < ha[1][1]):
        return 'down'
    else:
        return False


