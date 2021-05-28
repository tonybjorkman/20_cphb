import numpy as np
import random
import time

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import gen_layers

FPS = 20
FRAMES_START = 0
FRAMES_STOP = 100

Writer = animation.writers['ffmpeg']
writer = Writer(fps=FPS, metadata=dict(artist='Me'), bitrate=3600)  # 20, 3600, codec="libx264", extra_args=["-preset", "veryslow","-crf","0"]

fig, ax = plt.subplots(figsize=(20, 12))
# fig, ax = plt.subplots(figsize=(10, 6))

# plt.axis([0, 1280, 0, 720])
# plt.gca().invert_yaxis()
# ax.axis('off')
# plt.gca().set_position([0, 0, 1, 1])  # FILLS WHOLE FIG

backgr_ax, im_ax, waves, lays, smokes, smokes_r_f, ships = \
    gen_layers.gen_layers(ax, FRAMES_START, FRAMES_STOP)

plt.axis(backgr_ax.get_extent())
smokes_occupied = []

def animate(i):
    if i % 10 == 0:
        print(i)

    for wave_id, wave in waves.items():
        wave_ax = im_ax[wave_id]
        wave_ax.set_alpha(wave.alpha_array[wave.wave_clock % len(wave.alpha_array)])
        wave_ax.set_extent(wave.extent[wave.wave_clock % len(wave.alpha_array)])
        wave.wave_clock += 1

    # SHIP  ======
    for ship_id, ship in ships.items():
        ship_ax = im_ax[ship_id]
        ship_ax.set_extent(ship.extent[ship.extent_clock])  # obs tl not updated for ship
        ship.extent_clock += 1
        explosion_ax = im_ax['explosion']
        # smoke_ax = im_ax['smoke_r_f']

        if i in ship.firing_init_frames:
            expl_extent = ship.get_extent_explosion()
            explosion_ax.set_extent(expl_extent)

            for smoke_r_f_id, smoke_r_f in smokes_r_f.items():  # find smoke_r_f
                # todo to animate chunks this prob has to be moved inside gen_layers -> JUST USE FIRING FRAME
                if smoke_r_f.occupied == False:
                    smoke_r_f.occupied = True
                    smoke_r_f.tl = [expl_extent[0], expl_extent[2]]
                    break

        else:  # todo instead put them in separate dict that takes care of them
            explosion_ax.set_extent([0, 1, 1, 0])  # this one is unique tho since it only happens 1 frame (for now)

        if i in ship.smoka_init_frames:
            for smoke_id, smoke in smokes.items():
                if smoke.occupied == False:
                    smoke.occupied = True
                    smoke.tl = ship.get_tl_smoka()

                # else:
        ext = ship.get_extent_sail()
        sail_ax = im_ax['sail_3']
        sail_ax.set_extent(ext)
        sail_ax.set_alpha(ship.sail_0.alpha_array[ship.sail_0.sail_clock % len(ship.sail_0.alpha_array)])  # just scalar
        ship.sail_0.sail_clock += 1

    for smokr_id, smokr in smokes_r_f.items():  # move smokas occupied inside gen_layers (or use padding and loop through all)
        if smokr.occupied == True:
            smokr.set_extent_smoke()
            smokr.set_clock_smoke()

            smoke_ax = im_ax[smokr_id]
            smoke_ax.set_extent(smokr.extent_mov)
            smoke_ax.set_alpha(smokr.alpha_array[smokr.smoke_clock])

    for smoke_id, smoka in smokes.items():
        if smoka.occupied == True:
            smoka.set_extent_smoke()
            smoka.set_clock_smoke()

            smoke_ax = im_ax[smoke_id]
            smoke_ax.set_extent(smoka.extent_mov)
            smoke_ax.set_alpha(smoka.alpha_array[smoka.smoke_clock])

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