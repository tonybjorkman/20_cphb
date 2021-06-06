# geometric image transformations.

import numpy as np
import random
import time
import json

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import gen_layers
import chronicler
import PARAMS
import os
import matplotlib.transforms as mtransforms

FPS = 20
FRAMES_START = PARAMS.FRAMES_START
FRAMES_STOP = PARAMS.FRAMES_STOP
ANIMATE_WAVES = 0  # ONLY HANDLED FOR LARGE MAP FROM NOW ON
ANIMATE_SMOKR = 0
ANIMATE_SMOKA = 0
ANIMATE_SAILS = 0
ANIMATE_EXPLOSIONS = 0
ANIMATE_SPL = 0
ANIMATE_BC = 0  # backround class
bc_clock = 0  # since bc does not have a class

chronicler.Chronicler()

Writer = animation.writers['ffmpeg']
writer = Writer(fps=FPS, metadata=dict(artist='Me'), bitrate=3600)  # 20, 3600, codec="libx264", extra_args=["-preset", "veryslow","-crf","0"]

# fig, ax = plt.subplots(figsize=(20, 12))
fig, ax = plt.subplots(figsize=(10, 6))

# TEMP
# plt.axis([0, 1280, 0, 720])
# plt.gca().invert_yaxis()
ax.axis('off')
# plt.gca().set_position([0, 0, 1, 1])  # FILLS WHOLE FIG

with open('./utils/chronicle.json', 'r') as f:
    chronicle = json.load(f)

backgr_ax, im_ax, waves, spls, smokas, smokrs, expls, ships = \
    gen_layers.gen_layers(ax, FRAMES_START, FRAMES_STOP, chronicle)

plt.axis(backgr_ax.get_extent())
smokes_occupied = []
# explosion_occupied = False

def animate(i):

    def find_free_obj(type, bc=False):
        _di = None
        if type == 'expls':
            _di = expls
        elif type == 'smokrs':
            _di = smokrs
        elif type == 'smokas':
            _di = smokas
        elif type == 'spls':
            _di = spls

        obj = None
        for _ in range(5):  # ONLY FIVE ATTEMPTS
            id = random.choice(list(_di))
            if bc == True and _di[id].occupied == False:  # all items accepted
                obj = _di[id]
                break
            elif bc == False and _di[id].occupied == False and _di[id].bc == False:  # only non-bc's accepted
                obj = _di[id]
                break
        return obj

    global bc_clock
    if i % 10 == 0:
        print(i)

    # SHIP  ======
    for ship_id, ship in ships.items():
        ship_ax = im_ax[ship_id]
        ship_ax.set_extent(ship.extent[ship.extent_clock])  # obs tl not updated for ship
        ship.extent_clock += 1

        if ship.firing_init_frames[ship.expl_clock] == i:
            if len(ship.firing_init_frames) - 1 > ship.expl_clock:
                ship.expl_clock += 1

            expl = find_free_obj(type='expls')
            if expl is not None:
                ship.update_extent_explosion()
                expl.extent = ship.extent_explosion
                expl.occupied = True

            smokr = find_free_obj(type='smokrs')
            if smokr is not None:
                smokr.occupied = True
                if ship.extent_explosion is None:  #
                    ship.update_extent_explosion()
                expl_extent = ship.extent_explosion
                smokr.tl = [expl_extent[0], expl_extent[2]]

            spl = find_free_obj(type='spls')
            if spl is not None:
                spl.occupied = True
                if ship.extent_explosion is None:
                    ship.update_extent_explosion()
                expl_extent = ship.extent_explosion
                spl.tl = [expl_extent[0] + 50, expl_extent[2] - 20]

        if ship.smoka_init_frames[ship.smoka_init_clock] == i:
            if len(ship.smoka_init_frames) - 1 > ship.smoka_init_clock:
                ship.smoka_init_clock += 1
            smoka = smokas[ship.smoka_id]
            if smoka.occupied == False:
                smoka.occupied = True
                smoka.tl = ship.get_tl_smoka()

        if ship.sail_init_frames[ship.sail_init_clock] == i:
            if len(ship.sail_init_frames) - 1 > ship.sail_init_clock:
                ship.sail_init_clock += 1
            for sail_id, sail in ship.sails.items():
                if sail.occupied == False:
                    sail.occupied = True
                    break  # only does it for 1 of the sail animations.

        if ANIMATE_SAILS:  # owned by ship
            for sail_id, sail in ship.sails.items():
                if sail.occupied == True:
                    ext = ship.get_extent_sail(sail_id=sail_id)
                    sail_ax = im_ax[sail_id]
                    sail_ax.set_extent(ext)
                    sail_ax.set_alpha(ship.sails[sail_id].alpha_array[ship.sails[sail_id].sail_clock % len(ship.sails[sail_id].alpha_array)])  # just scalar
                    ship.sails[sail_id].update_sail_clock()

    if ANIMATE_BC:
        if chronicle['bc'][bc_clock]['frame'] == i:
            expl = find_free_obj(type='expls')
            if expl is not None:
                expl.occupied = True
                expl.tl = chronicle['bc'][bc_clock]['tl']
                scale_factor = expl.scale_vector[expl.tl[1]]
                width = PARAMS.EXPLOSION_WIDTH * scale_factor
                height = PARAMS.EXPLOSION_HEIGHT * scale_factor
                expl.extent = [expl.tl[0], expl.tl[0] + width, expl.tl[1], expl.tl[1] + height]

            smokr = find_free_obj(type='smokrs', bc=True)
            if smokr is not None:
                smokr.occupied = True
                smokr.bc_cur = True
                smokr.tl = chronicle['bc'][bc_clock]['tl']

            smoka = find_free_obj(type='smokas')
            if smoka is not None:
                smoka.occupied = True
                smoka.tl = chronicle['bc'][bc_clock]['tl']

            if len(chronicle['bc']) - 1 > bc_clock:
                bc_clock += 1

    if ANIMATE_EXPLOSIONS:
        for expl_id, expl in expls.items():
            expl_ax = im_ax[expl_id]
            if expl.occupied == True:
                expl_ax.set_extent(expl.extent)
                expl.occupied = False
            else:
                expl_ax.set_extent([0, 1, 1, 0])  # next iter

    if ANIMATE_SMOKR:
        for smokr_id, smokr in smokrs.items():  # move smokas occupied inside gen_layers (or use padding and loop through all)
            if smokr.occupied == True:
                if smokr.bc_cur == True:
                    left_right = 'l'
                else:
                    left_right = 'r'
                smokr.set_extent_smoke(left_right=left_right)
                smokr.set_clock_smoke()

                smoke_ax = im_ax[smokr_id]
                smoke_ax.set_extent(smokr.extent_mov)
                smoke_ax.set_alpha(smokr.alpha_array[smokr.smoke_clock])

    if ANIMATE_SMOKA:
        for smoke_id, smoka in smokas.items():
            if smoka.occupied == True:
                smoka.set_extent_smoke(left_right='r')
                smoka.set_clock_smoke()

                smoke_ax = im_ax[smoke_id]
                smoke_ax.set_extent(smoka.extent_mov)
                smoke_ax.set_alpha(smoka.alpha_array[smoka.smoke_clock])

    if ANIMATE_SPL:
        for spl_id, spl in spls.items():
            if spl.occupied == True:
                spl.set_extent_spl()
                spl.set_clock_spl()

                spl_ax = im_ax[spl_id]
                spl_ax.set_extent(spl.extent_mov)
                spl_ax.set_alpha(spl.alpha_array[spl.spl_clock])

    if ANIMATE_WAVES:
        for wave_id, wave in waves.items():
            wave_ax = im_ax[wave_id]
            wave_ax.set_alpha(wave.alpha_array[wave.wave_clock % len(wave.alpha_array)])
            wave_ax.set_extent(wave.extent[wave.wave_clock % len(wave.alpha_array)])
            wave.set_wave_clock()

    return im_ax,

sec_vid = ((FRAMES_STOP - FRAMES_START) / FPS)
min_vid = ((FRAMES_STOP - FRAMES_START) / FPS) / 60
print("len of vid: " + str(sec_vid) + " s" + "    " + str(min_vid) + " min")

WRITE = 0  # change IMMEDIATELY after set
start_t = time.time()
ani = animation.FuncAnimation(fig, animate, frames=range(FRAMES_START, FRAMES_STOP), interval=1, repeat=False)  # interval only affects live ani

if WRITE == 0:  # NOT HERE
    plt.show()
else:
    ani.save('./vid_81.mp4', writer=writer)

tot_time = round((time.time() - start_t) / 60, 4)
print("minutes to make animation: " + str(tot_time) + " |  min_gen/min_vid: " + str(tot_time / min_vid))  #