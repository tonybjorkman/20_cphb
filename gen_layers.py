

import random
import layers
import json
import numpy as np
from utils.several import generate_scaling
from utils.load_pics import load_pics

NUM_WAVES_1 = 5
NUM_WAVES_2 = 10
# SCALING = np.linspace()

def gen_layers(ax, FRAMES_START, FRAMES_STOP):

    lays = {}  # stores all layer classes
    waves = {}
    smokas = {}
    smokrs = {}
    ships = {}
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
        id = 'wave_' + str(i)
        found_coords = False
        while found_coords == False:
            try:
                x = random.randint(pics['waves']['wave1'].shape[1], pics['backgr'].shape[1] - pics['waves']['wave1'].shape[1] * 1)
                y = random.randint(int(pics['backgr'].shape[0] * 1/10), pics['backgr'].shape[0] - pics['waves']['wave1'].shape[0] * 2)
                found_coords = True
            except:
                print("failed to find coords1")
        waves['wave_' + str(i)] = layers.Wave(id=id, tl=[x, y], pic=pics['waves']['wave1'], zorder=zorder,
                                              FRAMES_START=FRAMES_START, FRAMES_STOP=FRAMES_STOP, scale_vector=scale_vector)
        wave_ax = ax.imshow(pics['waves']['wave1'], zorder=zorder, alpha=1)
        im_ax['wave_' + str(i)] = wave_ax

    zorder = 3
    for i in range(len(waves), len(waves) + NUM_WAVES_2 - 1):
        id = 'wave_' + str(i)
        found_coords = False
        while found_coords == False:
            try:
                x = random.randint(0, pics['backgr'].shape[1] - pics['waves']['wave2'].shape[1])
                y = random.randint(int(pics['backgr'].shape[0] * 1 / 6), pics['backgr'].shape[0] - pics['waves']['wave2'].shape[0] * 1)
                found_coords = True
            except:
                print("failed to find coords2")
        waves['wave_' + str(i)] = layers.Wave(id=id, tl=[x, y], pic=pics['waves']['wave2'], zorder=zorder,
                                              FRAMES_START=FRAMES_START, FRAMES_STOP=FRAMES_STOP, scale_vector=scale_vector)
        wave_ax = ax.imshow(pics['waves']['wave2'], zorder=zorder, alpha=1)
        im_ax['wave_' + str(i)] = wave_ax

    # SMOKRS ====================
    zorder = 5
    for i in range(5):
        id = 'smokr_' + str(i)
        smokrs[id] = layers.Smoke(id=id, zorder=zorder, tl=None, pic=pics['smokrs'][id],
                                      scale_vector=scale_vector, s_type='r', direction='r')
        smoke_r_f = ax.imshow(pics['smokrs']['smokr_3'], zorder=zorder, alpha=0., extent=[0, 1, 1, 0])
        im_ax[id] = smoke_r_f

    # SMOKAS ========
    zorder = 4
    for i in range(5):
        id = 'smoka_' + str(i)
        smokas[id] = layers.Smoke(id=id, zorder=zorder, tl=None, pic=pics['smokas'][id],
                                  scale_vector=scale_vector, s_type='a', direction='r')
        smoka = ax.imshow(pics['smokas'][id], zorder=zorder, alpha=0., extent=[0, 1, 1, 0])
        im_ax[id] = smoka

    # smokas['smoke3'] = layers.Smoke(id='smoke3', zorder=zorder, tl=None, pic=pics['smoke3'],
    #                                 scale_vector=scale_vector, s_type='a')
    # smoke3 = ax.imshow(pics['smoke3'], zorder=zorder, alpha=0., extent=[0, 1, 1, 0])
    # im_ax['smoke3'] = smoke3

    # EXPLOSION =================================
    zorder = 6
    lays['explosion'] = layers.LayerAbstract(id='explosion', zorder=zorder, tl=None, pic=None, scale_vector=None)
    explosion = ax.imshow(pics['explosions']['explosion'], zorder=zorder, alpha=0.9, extent=[0, 1, 1, 0])
    im_ax['explosion'] = explosion

    # SHIPS ===================================
    with open('./utils/ships_info.json', 'r') as f:
        ships_info = json.load(f)
    zorder = 6
    id = 'ship_3'
    sail_pics = {}  # for a specific ship (extra nesting needed)
    for sail_id in ships_info[id]['sails']:
        sail_pics[sail_id] = pics['sails'][sail_id]

    ships[id] = layers.Ship(id=id, tl=ships_info[id]['tl'], pic=pics['ships'][id], zorder=zorder,
                            FRAMES_START=FRAMES_START, FRAMES_STOP=FRAMES_STOP, scale_vector=scale_vector,
                            explosion_offset=[80, 130], sail_pics=sail_pics, ship_info=ships_info[id])

    ship_ax = ax.imshow(pics['ships'][id], zorder=zorder, alpha=1)
    im_ax[id] = ship_ax
    for ship_id, ship in ships.items():
        for sail_id in ship.sails:
            sail_ax = ax.imshow(pics['sails'][sail_id], zorder=7, alpha=1)
            im_ax[sail_id] = sail_ax

    # # GEN SAIl FOR EACH SHIP inside same iteration
    # zorder = 7
    # id = 'sail_3'
    # sails[id] = layers.Sail(id=id, tl=tl, pic=pics['sails'][id], zorder=zorder, scale_vector=scale_vector)

    return backgr_ax, im_ax, waves, lays, smokas, smokrs, ships

