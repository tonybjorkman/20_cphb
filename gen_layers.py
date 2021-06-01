
import random
import layers
import json
import numpy as np
from utils.several import generate_scaling
from utils.load_pics import load_pics
import PARAMS


# SCALING = np.linspace()

def gen_layers(ax, FRAMES_START, FRAMES_STOP, chronicle):
    waves = {}
    spls = {}  # splashes
    smokas = {}
    smokrs = {}
    ships = {}
    im_ax = {}
    explosions = {}

    pics = load_pics()

    backgr_ax = ax.imshow(pics['backgr'], zorder=0, alpha=0.9)
    backgr_ax.set_extent([0, pics['backgr'].shape[1], pics['backgr'].shape[0], 0])
    # im_ax['backgr'] = backgr
    # lays['backgr'].extent = [0, pics['backgr'].shape[1], pics['backgr'].shape[0], 0]

    scale_vector = generate_scaling(pics['backgr'])

    # WAVES =================================
    zorder = 3
    for i in range(0, PARAMS.NUM_WAVES_1):
        id = 'wave_' + str(i)
        found_coords = False
        while found_coords == False:
            if PARAMS.MAP_SIZE == 'small':
                try:
                    x = random.randint(0, pics['backgr'].shape[1] - pics['waves']['wave1s'].shape[1] * 1)
                    y = random.randint(int(pics['backgr'].shape[0] * 1 / 10),
                                       pics['backgr'].shape[0] - pics['waves']['wave1s'].shape[0] * 2)
                    found_coords = True
                except:
                    print("failed to find coords1")
        waves['wave_' + str(i)] = layers.Wave(id=id, tl=[x, y], pic=pics['waves']['wave1s'], zorder=zorder,
                                              FRAMES_START=FRAMES_START, FRAMES_STOP=FRAMES_STOP,
                                              scale_vector=scale_vector)
        wave_ax = ax.imshow(pics['waves']['wave1s'], zorder=zorder, alpha=1)
        im_ax['wave_' + str(i)] = wave_ax

    zorder = 3
    for i in range(len(waves), len(waves) + PARAMS.NUM_WAVES_2 - 1):
        id = 'wave_' + str(i)
        found_coords = False
        while found_coords == False:
            if PARAMS.MAP_SIZE == 'small':
                try:
                    x = random.randint(0, pics['backgr'].shape[1] - pics['waves']['wave2s'].shape[1])
                    y = random.randint(int(pics['backgr'].shape[0] * 1 / 6),
                                       pics['backgr'].shape[0] - pics['waves']['wave2s'].shape[0] * 2)
                    found_coords = True
                except:
                    print("failed to find coords2")
        waves['wave_' + str(i)] = layers.Wave(id=id, tl=[x, y], pic=pics['waves']['wave2s'], zorder=zorder,
                                              FRAMES_START=FRAMES_START, FRAMES_STOP=FRAMES_STOP,
                                              scale_vector=scale_vector)
        wave_ax = ax.imshow(pics['waves']['wave2s'], zorder=zorder, alpha=1)
        im_ax['wave_' + str(i)] = wave_ax

    # SPLASHES ================
    zorder=4
    for spl_id, spl_pic in pics['spls'].items():
        spls[spl_id] = layers.Splash(id=spl_id, zorder=zorder, tl=None, pic=spl_pic, scale_vector=scale_vector)
        im_ax[spl_id] = ax.imshow(spl_pic, zorder=zorder, alpha=0., extent=[0, 1, 1, 0])

    # SMOKRS ====================
    zorder = 5
    for smokr_id, smokr_pic in pics['smokrs'].items():
        smokrs[smokr_id] = layers.Smoke(id=smokr_id, zorder=zorder, tl=None, pic=pics['smokrs'][smokr_id],
                                  scale_vector=scale_vector, s_type='r', left_right='r')
        smoke_r_f = ax.imshow(pics['smokrs'][smokr_id], zorder=zorder, alpha=0., extent=[0, 1, 1, 0])
        im_ax[smokr_id] = smoke_r_f

    # SMOKAS ========
    zorder = 4
    for smoka_id, smoka_pic in pics['smokas'].items():
        smokas[smoka_id] = layers.Smoke(id=smoka_id, zorder=zorder, tl=None, pic=pics['smokas'][smoka_id],
                                  scale_vector=scale_vector, s_type='a', left_right='r')
        smoka = ax.imshow(pics['smokas'][smoka_id], zorder=zorder, alpha=0., extent=[0, 1, 1, 0])
        im_ax[smoka_id] = smoka

    # EXPLOSIONS =================================
    zorder = 99  # 6
    for expl_id, expl in pics['expls'].items():
        # id = 'explosion_0'
        explosions[expl_id] = layers.LayerAbstract(id=expl_id, zorder=zorder, tl=None, pic=None, scale_vector=None)
        im_ax[expl_id] = ax.imshow(pics['expls'][expl_id], zorder=zorder, alpha=0.9, extent=[0, 1, 1, 0])
    # im_ax['explosion'] = ax.imshow(pics['explosions']['explosion'], zorder=zorder, alpha=0.9, extent=[0, 1, 1, 0])

    # SHIPS ===================================
    with open('./utils/ships_info.json', 'r') as f:
        ships_info = json.load(f)
    ships_info = chronicle

    zorder = 6
    id = 'ship_3'
    sail_pics = {}  # for a specific ship (extra nesting needed)
    for sail_id in ships_info[id]['sails']:
        sail_pics[sail_id] = pics['sails'][sail_id]

    ships[id] = layers.Ship(id=id, zorder=zorder, tl=ships_info[id]['tl'], pic=pics['ships'][id],
                            FRAMES_START=FRAMES_START, FRAMES_STOP=FRAMES_STOP, scale_vector=scale_vector,
                            sail_pics=sail_pics, ship_info=ships_info[id])

    ship_ax = ax.imshow(pics['ships'][id], zorder=zorder, alpha=1)
    im_ax[id] = ship_ax
    for ship_id, ship in ships.items():
        for sail_id in ship.sails:
            sail_ax = ax.imshow(pics['sails'][sail_id], zorder=7, alpha=0)
            im_ax[sail_id] = sail_ax

    # ==================

    zorder = 6
    id = 'ship_1'
    sail_pics = {}  # for a specific ship (extra nesting needed)
    for sail_id in ships_info[id]['sails']:
        sail_pics[sail_id] = pics['sails'][sail_id]

    ships[id] = layers.Ship(id=id, tl=ships_info[id]['tl'], pic=pics['ships'][id], zorder=zorder,
                            FRAMES_START=FRAMES_START, FRAMES_STOP=FRAMES_STOP, scale_vector=scale_vector,
                            sail_pics=sail_pics, ship_info=ships_info[id])

    ship_ax = ax.imshow(pics['ships'][id], zorder=zorder, alpha=1)
    im_ax[id] = ship_ax
    for ship_id, ship in ships.items():
        for sail_id in ship.sails:
            sail_ax = ax.imshow(pics['sails'][sail_id], zorder=7, alpha=0)
            im_ax[sail_id] = sail_ax



    return backgr_ax, im_ax, waves, spls, smokas, smokrs, explosions, ships

