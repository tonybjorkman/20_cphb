import time

import matplotlib.pyplot as plt
import matplotlib.animation as animation

import gen_layers

FPS = 40
FRAMES_START = 0
FRAMES_STOP = 100

Writer = animation.writers['ffmpeg']
writer = Writer(fps=FPS, metadata=dict(artist='Me'), bitrate=3600)  # 20, 3600, codec="libx264", extra_args=["-preset", "veryslow","-crf","0"]


fig, ax = plt.subplots(figsize=(20, 12))


# plt.axis([0, 1280, 0, 720])
# plt.gca().invert_yaxis()
# ax.axis('off')
# plt.gca().set_position([0, 0, 1, 1])  # FILLS WHOLE FIG

# imobj = ax.imshow(img,extent=[0, img.shape[1], 136, 136+img.shape[0]], zorder=1)
# x = np.arange(0, np.pi, 0.1)
# x_alpha = np.sin(2 * x) / 4 + 0.3

im_ax, waves, ships, lays, smokes = gen_layers.gen_layers(ax, FRAMES_START, FRAMES_STOP)
smokes_li = []
smokes_li.append(smokes['smoke_r_f'])


plt.axis(lays['backgr'].extent)

# expl_ax = ax.imshow(explosion, zorder=2, alpha=0)
# lays['expl'] = {'xy': [604, 512], 'extent': [604, 625, 512, 480]}
# im_ax['expl'] = expl_ax

ship = ships['ship3']
explosion = lays['explosion']
hh = 5

def animate(i):
    if i % 10 == 0:
        print(i)

    for wave_id, wave in waves.items():
        wave_ax = im_ax[wave_id]

        wave_ax.set_alpha(wave.alpha_array[wave.wave_clock % len(wave.alpha_array)])
        wave_ax.set_extent(wave.extent[wave.wave_clock % len(wave.alpha_array)])
        wave.wave_clock += 1

    # if i % 8 == 0:
    for ship_id, ship in ships.items():
        ship_ax = im_ax[ship_id]
        ship_ax.set_extent(ship.extent[ship.i_extent])
        ship.i_extent += 1
        explosion_ax = im_ax['explosion']
        # smoke_ax = im_ax['smoke_r_f']

        if i in ship.firing_frames:
            smoke = smokes_li.pop()
            smoke_ax = im_ax[smoke.id]
            explosion_ax.set_extent(ship.expl_extent[ship.i_extent])
            smoke_ax.set_extent(ship.smoke_extent[ship.i_extent])
        else:  # todo instead put them in separate dict that takes care of them
            explosion_ax.set_extent([0, 1, 1, 0])
            # smoke_ax.set_extent([0, 1, 1, 0])

    return im_ax,

sec_vid = ((FRAMES_STOP - FRAMES_START) / FPS)
min_vid = ((FRAMES_STOP - FRAMES_START) / FPS) / 60
print("len of vid: " + str(sec_vid) + " s" + "    " + str(min_vid) + " min")

WRITE = 0
start_t = time.time()
ani = animation.FuncAnimation(fig, animate, frames=range(FRAMES_START, FRAMES_STOP), interval=1, repeat=False)  # interval only affects live ani

if WRITE == 0:
    plt.show()
else:
    ani.save('./vid_81.mp4', writer=writer)

tot_time = round((time.time() - start_t) / 60, 4)
print("minutes to make animation: " + str(tot_time) + " |  min_gen/min_vid: " + str(tot_time / min_vid))  #