

import random
import layers
import numpy as np
from utils.several import generate_scaling
from utils.load_pics import load_pics

NUM_WAVES_1 = 20
NUM_WAVES_2 = 40
# SCALING = np.linspace()

def gen_layers(ax, FRAMES_START, FRAMES_STOP):

    lays = {}  # stores all layer classes
    waves = {}
    ships = {}
    smokes = {}
    smokes_r_f = {}
    im_ax = {}

    pics = load_pics()

    # lays['backgr'] = layers.LayerAbstract(id=None, zorder=0, tl=None, pic=None)
    backgr_ax = ax.imshow(pics['backgr'], zorder=0, alpha=0.9)
    backgr_ax.set_extent([0, pics['backgr'].shape[1], pics['backgr'].shape[0], 0])
    # im_ax['backgr'] = backgr
    # lays['backgr'].extent = [0, pics['backgr'].shape[1], pics['backgr'].shape[0], 0]

    scale_vector = generate_scaling(pics['backgr'])

    # for i in range(1):
    #     lays['smoke' + str(i)] = layers.Smoke(id='0', extent=[604, 605, 512, 480], zorder=99)
    #     smoke_ax = ax.imshow(smoke, zorder=1, alpha=0)
    #     im_ax['smoke' + str(i)] = smoke_ax

    # WAVES =================================
    zorder = 3
    for i in range(0, NUM_WAVES_1):
        x = random.randint(50, 200)
        y = random.randint(20, 120)
        waves['wave_' + str(i)] = layers.Wave(id='wave_' + str(i), tl=[x, y], pic=pics['wave1'], zorder=zorder,
                                              FRAMES_START=FRAMES_START, FRAMES_STOP=FRAMES_STOP, scale_vector=scale_vector)
        wave_ax = ax.imshow(pics['wave2'], zorder=zorder, alpha=1)
        im_ax['wave_' + str(i)] = wave_ax

    zorder = 3
    for i in range(len(waves), len(waves) + NUM_WAVES_2 - 1):
        x = random.randint(50, 200)
        y = random.randint(20, 100)
        waves['wave_' + str(i)] = layers.Wave(id='wave_' + str(i), tl=[x, y], pic=pics['wave2'], zorder=zorder,
                                              FRAMES_START=FRAMES_START, FRAMES_STOP=FRAMES_STOP, scale_vector=scale_vector)
        wave_ax = ax.imshow(pics['wave2'], zorder=zorder, alpha=1)
        im_ax['wave_' + str(i)] = wave_ax

    # SHIPS ===================================
    zorder = 6
    tl = [100, 0]
    incr_x = 1

    ships['ship3'] = layers.Ship(id='ship3', tl=tl, pic=pics['ship3'], zorder=zorder,
                                 FRAMES_START=FRAMES_START, FRAMES_STOP=FRAMES_STOP, scale_vector=scale_vector,
                                 expl_offset=[80, 130])

    ship_ax = ax.imshow(pics['ship3'], zorder=zorder, alpha=1)
    im_ax['ship3'] = ship_ax

    # SMOKES ===================================
    zorder = 5
    smokes_r_f['smoke_r_f_3'] = layers.Smoke(id='smoke_r_f_3', zorder=zorder, tl=None, pic=['smoke_r_f'],
                                             scale_vector=None)
    smoke_r_f = ax.imshow(pics['smoke_r_f'], zorder=zorder, alpha=1., extent=[0, 1, 1, 0])
    im_ax['smoke_r_f_3'] = smoke_r_f

    smokes['smoke3'] = layers.Smoke(id='smoke3', zorder=zorder, tl=None, pic=pics['smoke3'], scale_vector=None)
    smoke3 = ax.imshow(pics['smoke3'])
    im_ax['smoke3'] = smoke3

    # EXPLOSION =================================
    zorder = 5
    lays['explosion'] = layers.LayerAbstract(id='explosion', zorder=zorder, tl=None, pic=None, scale_vector=None)
    explosion = ax.imshow(pics['explosion'], zorder=zorder, alpha=0.9, extent=[0, 1, 1, 0])
    im_ax['explosion'] = explosion
    # lays['explosion'].extent = [0, 10, 10, 0]

    return backgr_ax, im_ax, waves, ships, lays, smokes, smokes_r_f



