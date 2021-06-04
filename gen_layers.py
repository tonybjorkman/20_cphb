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
    for wave_id, wave_pic in pics['waves'].items():
        found_coords = False
        wave_id_s = wave_id.split('_')
        while found_coords == False:
            try:
                if PARAMS.MAP_SIZE == 'small':
                    x = random.randint(0, pics['backgr'].shape[1] - wave_pic.shape[1] * 1)
                    y = random.randint(int(pics['backgr'].shape[0] * 1 / 10), pics['backgr'].shape[0] - wave_pic.shape[0] * 2)
                else:
                    x = int(wave_id_s[1]) + random.randint(-100, 100)
                    y = int(wave_id_s[2]) + random.randint(-50, 50)
                    # x = random.randint(0, pics['backgr'].shape[1] - wave_pic.shape[1] * 1)
                    # y = random.randint(int(pics['backgr'].shape[0] * 7 / 10), pics['backgr'].shape[0] - wave_pic.shape[0] * 2)
                found_coords = True

            except:
                print("failed to find coords1")

        waves[wave_id] = layers.Wave(id=wave_id, tl=[x, y], pic=wave_pic, zorder=zorder,FRAMES_START=FRAMES_START,
                                     FRAMES_STOP=FRAMES_STOP, scale_vector=scale_vector)
        wave_ax = ax.imshow(wave_pic, zorder=zorder, alpha=1)
        im_ax[wave_id] = wave_ax

    # SPLASHES ================
    zorder=4
    for spl_id, spl_pic in pics['spls'].items():
        spls[spl_id] = layers.Splash(id=spl_id, zorder=zorder, tl=None, pic=spl_pic, scale_vector=scale_vector)
        im_ax[spl_id] = ax.imshow(spl_pic, zorder=zorder, alpha=0., extent=[0, 1, 1, 0])

    # SMOKRS ====================
    zorder = 99  # 5
    for smokr_id, smokr_pic in pics['smokrs'].items():

        bc = False
        if smokr_id.split("_")[1] == 'bc':
            bc = True
        smokrs[smokr_id] = layers.Smoke(id=smokr_id, zorder=zorder, tl=None, pic=pics['smokrs'][smokr_id],
                                  scale_vector=scale_vector, s_type='r', left_right='r', bc=bc)
        im_ax[smokr_id] = ax.imshow(pics['smokrs'][smokr_id], zorder=zorder, alpha=0., extent=[0, 1, 1, 0])


    # SMOKAS ========
    zorder = 4
    for smoka_id, smoka_pic in pics['smokas'].items():
        smokas[smoka_id] = layers.Smoke(id=smoka_id, zorder=zorder, tl=None, pic=pics['smokas'][smoka_id],
                                  scale_vector=scale_vector, s_type='a', left_right='r', bc=False)
        smoka = ax.imshow(pics['smokas'][smoka_id], zorder=zorder, alpha=0., extent=[0, 1, 1, 0])
        im_ax[smoka_id] = smoka

    # EXPLOSIONS =================================
    zorder = 5  # 6
    for expl_id, expl_pic in pics['expls'].items():
        explosions[expl_id] = layers.LayerAbstract(id=expl_id, zorder=zorder, tl=None, pic=expl_pic, scale_vector=scale_vector)
        im_ax[expl_id] = ax.imshow(pics['expls'][expl_id], zorder=zorder, alpha=0.9, extent=[0, 1, 1, 0])

    # SHIPS ===================================
    ships_info = chronicle['ships']
    zorder = 6
    for ship_id, ship_pic in pics['ships'].items():

        if ship_id != "ship_1":  # and ship_id != "ship_3":
            continue

        # SAILS CREATED BEFORE SHIP (BECAUSE Ship class does not take pics as input)
        sail_pics = {}  # for a specific ship (extra nesting needed)
        for sail_id in ships_info[ship_id]['sails']:  # objects created in Sail class
            sail_pics[sail_id] = pics['sails'][sail_id]
            sail_ax = ax.imshow(pics['sails'][sail_id], zorder=7, alpha=0)
            im_ax[sail_id] = sail_ax

        ships[ship_id] = layers.Ship(id=ship_id, zorder=zorder, tl=ships_info[ship_id]['tl'], pic=ship_pic,
                            FRAMES_START=FRAMES_START, FRAMES_STOP=FRAMES_STOP, scale_vector=scale_vector,
                            sail_pics=sail_pics, ship_info=ships_info[ship_id])
        im_ax[ship_id] = ax.imshow(pics['ships'][ship_id], zorder=zorder, alpha=1)

    return backgr_ax, im_ax, waves, spls, smokas, smokrs, explosions, ships

