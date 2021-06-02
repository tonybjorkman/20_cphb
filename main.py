import numpy as np
import random
import time
import json

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import gen_layers
import chronicler
import PARAMS

FPS = 20
FRAMES_START = PARAMS.FRAMES_START
FRAMES_STOP = PARAMS.FRAMES_STOP
ANIMATE_WAVES = 1  # ONLY HANDLED FOR LARGE MAP FROM NOW ON
ANIMATE_SMOKR = 1
ANIMATE_SMOKA = 1
ANIMATE_SAILS = 1
ANIMATE_EXPLOSIONS = 1
ANIMATE_SPL = 1

chronicler.Chronicler()

Writer = animation.writers['ffmpeg']
writer = Writer(fps=FPS, metadata=dict(artist='Me'), bitrate=3600)  # 20, 3600, codec="libx264", extra_args=["-preset", "veryslow","-crf","0"]

fig, ax = plt.subplots(figsize=(20, 12))
# fig, ax = plt.subplots(figsize=(10, 6))

# plt.axis([0, 1280, 0, 720])
# plt.gca().invert_yaxis()
# ax.axis('off')
# plt.gca().set_position([0, 0, 1, 1])  # FILLS WHOLE FIG

with open('./utils/chronicle.json', 'r') as f:
    chronicle = json.load(f)

backgr_ax, im_ax, waves, spls, smokas, smokrs, expls, ships = \
    gen_layers.gen_layers(ax, FRAMES_START, FRAMES_STOP, chronicle)

plt.axis(backgr_ax.get_extent())
smokes_occupied = []
# explosion_occupied = False

def animate(i):

    # global explosion_occupied
    if i % 10 == 0:
        print(i)

    # WAVES ===============
    if ANIMATE_WAVES:
        for wave_id, wave in waves.items():
            wave_ax = im_ax[wave_id]
            wave_ax.set_alpha(wave.alpha_array[wave.wave_clock % len(wave.alpha_array)])
            wave_ax.set_extent(wave.extent[wave.wave_clock % len(wave.alpha_array)])
            wave.set_wave_clock()

    # SHIP  ======
    for ship_id, ship in ships.items():
        ship_ax = im_ax[ship_id]
        ship_ax.set_extent(ship.extent[ship.extent_clock])  # obs tl not updated for ship
        ship.extent_clock += 1

        if i in ship.firing_init_frames:
            flag_found_free_expl = False
            expl_id = None
            expl = None
            for _ in range(5):  # ONLY FIVE ATTEMPTS
                expl_id = random.choice(list(expls))
                expl = expls[expl_id]
                if expl.occupied == False:
                    flag_found_free_expl = True
                    break

            if flag_found_free_expl == True:
                # expl.extent = ship.get_extent_explosion()
                ship.update_extent_explosion()
                expl.extent = ship.extent_explosion
                expl.occupied = True

            for smokr_id, smokr in smokrs.items():  # find smoke_r_f
                if smokr.occupied == False:
                    smokr.occupied = True
                    if ship.extent_explosion is None:  #
                        ship.update_extent_explosion()
                    expl_extent = ship.extent_explosion
                    smokr.tl = [expl_extent[0], expl_extent[2]]
                    break

            for spl_id, spl in spls.items():
                if spl.occupied == False:
                    spl.occupied = True
                    if ship.extent_explosion is None:
                        ship.update_extent_explosion()
                    expl_extent = ship.extent_explosion
                    spl.tl = [expl_extent[0] + 50, expl_extent[2] - 20]
                    # spl.tl = [20, 100]
                    break

        if i in ship.smoka_init_frames:
            smoka = smokas[ship.smoka_id]
            if smoka.occupied == False:
                smoka.occupied = True
                smoka.tl = ship.get_tl_smoka()

        if i in ship.sail_init_frames:
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
                    # ship.sails[sail_id].sail_clock += 1  # todo change to sail.sail_clock which stops
                    ship.sails[sail_id].update_sail_clock()

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
                smokr.set_extent_smoke()
                smokr.set_clock_smoke()

                smoke_ax = im_ax[smokr_id]
                smoke_ax.set_extent(smokr.extent_mov)
                smoke_ax.set_alpha(smokr.alpha_array[smokr.smoke_clock])

    if ANIMATE_SMOKA:
        for smoke_id, smoka in smokas.items():
            if smoka.occupied == True:
                smoka.set_extent_smoke()
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
    return im_ax,

sec_vid = ((FRAMES_STOP - FRAMES_START) / FPS)
min_vid = ((FRAMES_STOP - FRAMES_START) / FPS) / 60
print("len of vid: " + str(sec_vid) + " s" + "    " + str(min_vid) + " min")

WRITE = 0  # change IMMEDIATELY after set
start_t = time.time()
ani = animation.FuncAnimation(fig, animate, frames=range(FRAMES_START, FRAMES_STOP), interval=1, repeat=False)  # interval only affects live ani

if WRITE == 0:
    plt.show()
else:
    ani.save('./vid_81.mp4', writer=writer)

tot_time = round((time.time() - start_t) / 60, 4)
print("minutes to make animation: " + str(tot_time) + " |  min_gen/min_vid: " + str(tot_time / min_vid))  #