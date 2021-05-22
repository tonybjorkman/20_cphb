
from matplotlib.pyplot import imread
import random
import layers
from utils.several import generate_scaling

NUM_WAVES_1 = 20
NUM_WAVES_2 = 40
# SCALING = np.linspace()

def gen_layers(ax, FRAMES_START, FRAMES_STOP):

    lays = {}  # stores all layer classes
    waves = {}
    ships = {}
    smokes = {}
    im_ax = {}

    backgr = imread('./images/backgr_small1.png')  #482, 187
    # backgr = imread('./images/backgr_new1.png')  #482, 187
    smoke_r_f = imread('./images/smokes/smoke_r_f.png')
    wave1 = imread('./images/waves/wave1.png')  # 69, 35
    wave2 = imread('./images/waves/wave2.png')  # 69, 35
    ship3 = imread('./images/ships/ship3.png')  #  105, 145
    explosion = imread('./images/expls/explosion.png')

    lays['backgr'] = layers.LayerAbstract()
    backgr0 = ax.imshow(backgr, zorder=0, alpha=0.9)
    im_ax['backgr'] = backgr0
    lays['backgr'].extent = [0, backgr.shape[1], backgr.shape[0], 0]

    scale_vector = generate_scaling(backgr)

    # for i in range(1):
    #     lays['smoke' + str(i)] = layers.Smoke(id='0', extent=[604, 605, 512, 480], z=99)
    #     smoke_ax = ax.imshow(smoke, zorder=1, alpha=0)
    #     im_ax['smoke' + str(i)] = smoke_ax

    # WAVES =================================
    zorder = 3
    for i in range(0, NUM_WAVES_1):
        x = random.randint(50, 200)
        y = random.randint(20, 110)
        waves['wave_' + str(i)] = layers.Wave(id='wave_' + str(i), top_left=[x, y], pic=wave1, z=zorder,
                                              FRAMES_START=FRAMES_START, FRAMES_STOP=FRAMES_STOP, scale_vector=scale_vector)
        wave_ax = ax.imshow(wave2, zorder=zorder, alpha=1)
        im_ax['wave_' + str(i)] = wave_ax

    zorder = 3
    for i in range(len(waves), len(waves) + NUM_WAVES_2 - 1):
        x = random.randint(50, 200)
        y = random.randint(20, 100)
        waves['wave_' + str(i)] = layers.Wave(id='wave_' + str(i), top_left=[x, y], pic=wave2, z=zorder,
                                              FRAMES_START=FRAMES_START, FRAMES_STOP=FRAMES_STOP, scale_vector=scale_vector)
        wave_ax = ax.imshow(wave2, zorder=zorder, alpha=1)
        im_ax['wave_' + str(i)] = wave_ax

    # SHIPS ===================================
    zorder = 6
    top_left = [100, 0]
    incr_x = 1

    ships['ship3'] = layers.Ship(id='ship3', top_left=top_left, pic=ship3, z=zorder,
                                 FRAMES_START=FRAMES_START, FRAMES_STOP=FRAMES_STOP, scale_vector=scale_vector,
                                 expl_offset=[80, 130])

    ship_ax = ax.imshow(ship3, zorder=zorder, alpha=1)
    im_ax['ship3'] = ship_ax

    # SMOKES ===================================
    zorder = 5
    smokes['smoke_r_f'] = layers.Smoke(id='smoke_r_f', z=zorder)
    smoke_r_f = ax.imshow(smoke_r_f, zorder=zorder, alpha=1., extent=[0, 1, 1, 0])
    im_ax['smoke_r_f'] = smoke_r_f

    # EXPLOSION =================================
    zorder = 5
    lays['explosion'] = layers.LayerAbstract()
    explosion = ax.imshow(explosion, zorder=zorder, alpha=0.9, extent=[0, 1, 1, 0])
    im_ax['explosion'] = explosion
    # lays['explosion'].extent = [0, 10, 10, 0]

    return im_ax, waves, ships, lays, smokes



