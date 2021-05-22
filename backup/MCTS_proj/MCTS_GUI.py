"""
EPILOGUE: the things added or commented out for the epilogue video

SWITCHING BETWEEN TREES:
1. ENV: Rename tp
2. MCTS_GUI Scatter Section: check temp CHECK VIBRATIONS
3 UG -> hardcoded_size_control: fix
4 UG -> init top: check loaded backgr map : fix ALSO init_e_n_root_and_st  ALSO STX enable/disable (only '0') AND tp_pic
5 MCTS_GUI: zooming AND flipping AND "PERM LINES"
6 MCTS_GUI -> EXPAND AND "BOTTOM tree1"
8 MCTS_GUI -> STX AND SNOW (slightly below)
9 MCTS_GUI far down -> disable/enable ground
"""

import time

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import PARAMS
import ENV
import utils_gui
import random

PM = PARAMS.Params(_rand_seed=4)
ENV = ENV.ENV(PM)
UG = utils_gui.UtilsGui(PM, ENV)

from State import State

Writer = animation.writers['ffmpeg']
writer = Writer(fps=10, metadata=dict(artist='Me'), bitrate=3600)  # 20, 3600, codec="libx264", extra_args=["-preset", "veryslow","-crf","0"]

# e_o = np.zeros((DIMS[0], DIMS[1]), dtype=bool)
e_N = np.zeros((ENV.DIMS[0], ENV.DIMS[1]), dtype=int)  # ONLY FOR GUI
# UG.init_e_n_root_and_st(e_N)  # EPILOGUE

logger, logger_flat, root_b, e_o_fin, img = UG.load_stuff(ENV)

# INIT MPL ===================================
my_ax_objs2 = {}
my_ax_objs_st = {}  # small Tree
my_ax_objs_perm = {}
fig = plt.figure(figsize=(12.8, 3.6))  # WRITER OUTPUTS THIS! This is also the extent on the display
# fig.set_size_inches(8, 5)  # temp 8, 5
fig.tight_layout(True)

mngr = plt.get_current_fig_manager()

# to put it into the upper left corner for example:
mngr.window.setGeometry(200, 200, 1280 + 300,360 + 300)  # works
# mngr.window.setGeometry(10,10,2560,1440)  # works

# ax = fig.add_subplot(111, autoscale_on=True)  # , xlim=(0, DIMS[1]), ylim=(0, DIMS[0]))  # this is just the x and y axis extents of the plot, has nothing to do with with what will actually be saved in the end
# ax = fig.add_subplot(111, autoscale_on=True, xlim=(0, DIMS[1]), ylim=(0, DIMS[0]))  # this is just the x and y axis extents of the plot, has nothing to do with with what will actually be saved in the end
ax = fig.add_subplot(111, autoscale_on=True)  # this is just the x and y axis extents of the plot, has nothing to do with with what will actually be saved in the end
ax.axis('off')
plt.gca().set_position([0, 0, 1, 1])  # FILLS WHOLE FIG
# plt.axis([0, 100, 0, 100])
# plt.gca().invert_yaxis()
# ax.set_xlim([0, 1280])
plt.axis([0, 40, 25, 0])  # epilogue up
# plt.axis([0, 1280, 720, 0])  # up
# plt.axis([0, 1280, 0, 720])  # do SHOULD WORK
plt.rcParams['toolbar'] = 'None'
# mngr.window.showMaximized()

# plt.grid()

ax.imshow(img, alpha=1)  #, extent=[0, 1280, 0, 720])

CURRENT_LINE_COUNTER = 0
DOT_GROWTH = 1
if ENV.LITE == '25_40':
	DOT_GROWTH = 100
	SIZE_e_o = 200
elif ENV.LITE == '250_400':
	DOT_GROWTH = 1.2
	SIZE_e_o = 200
elif ENV.LITE == 'fin':
	DOT_GROWTH = 0.05
	SIZE_e_o = 200

root = State({'id': str(ENV.START_COORDS[1]) + '_' + str(ENV.START_COORDS[0]), 'coords': ENV.START_COORDS, 'parent': None, 'd': 0})
ax, my_ax_objs2, my_ax_objs_st, my_ax_objs_perm = UG.init_ax_objects(PM, ax, my_ax_objs2, my_ax_objs_st, my_ax_objs_perm)  # my_ax_objs2 is just available drawing objects
# if thing in some_list: some_list.remove(thing)  # how to remove a string from list
p_occupied = []
p_free = [x for x in my_ax_objs2]
p_free.remove('rect')
p_free.remove('scatter')
p_free.remove('scatter_o')
p_free.remove('scatter_snow')

p_occupied_perm = []
p_free_perm = [x for x in my_ax_objs_perm]
p_occupied_st = []
p_free_st = [x for x in my_ax_objs_st]

INNER_COMP_F = 1  # 10 is for vids
breakpoint

def init():  # without this the animate loop seems to run some iterations at i=0 before starting
	return ax.patches + ax.lines + ax.collections

ii = 0  # ep_counter
zoom_k = 0
kk = 0
# for i in range(0, 313):  # debug
def animate(i):  # starts at 0.9i

	global kk
	global zoom_k
	#ZOOMING
	# global zoom_k
	# if i < 150:
	# 	zoom_k = 0
	# else:
	# 	zoom_k += 1
	# plt.axis([480 - kk * 0.053, 800 + kk * 0.053, 720, 360 - kk * 0.03])  # up # central zoom out OLD
	# plt.axis([575 - kk * (576/12000), 704 + kk * (576/12000), 720, 684 - kk * (684/12000)])  # up # central zoom out 128
	# plt.axis([575 - kk * (576/12000), 704 + kk * (576/12000), 720, 500 - kk * (500/12000)])  # up # central zoom out 128
	# plt.axis([544 - kk * (544/12000), 736 + kk * (404/12000), 720, 500 - kk * (500/12000)])  # up # central zoom out 256  # "tree1"
	# plt.axis([544 - kk * (544/12000), 736 + kk * (404/12000), 500 - kk * (500/12000), 720])  # up # central zoom out 256  # "root1"
	# plt.axis([544 - kk * (544/12000), 736 + kk * (350/12000), 500 - kk * (500/12000), 720])  # up # central zoom out 256  # "root1" new
	# plt.axis([0 + kk * (608/12000), 1280 - kk * (608/12000), 720, 0 + kk * (702/12000)])  # up # central zoom in
	# if kk > 2000:
	# plt.axis([0 + zoom_k * (928/4000), 1280 - zoom_k * (288/4000), 720, 0 + zoom_k * (702/4000)])  # up # right st zoom in NOT USED
	# plt.axis([0 + zoom_k * (896/4000), 1280 - zoom_k * (252/4000), 720, 0 + zoom_k * (684/4000)])  # up # right st zoom in 128   'tree0'
	# plt.axis([0 + zoom_k * (896/4000), 1280 - zoom_k * (252/4000), 0 + zoom_k * (684/4000), 720])  # up # right st zoom in 128   'root0'
	# zoom_k += 1  # INCREMENTED IN KK LOOP

	# plt.axis([100, 300, 250, 130])  # EPILOGUE

	# plt.axis([0 + 3.2 * i, 1280, 720, 0 + 1.8 * i])  # up
	# plt.axis([0 + 3.2 * i, 1280, 1.8 * i, 720])  # do

	# plt.gca().invert_yaxis()

	# globals are needed for variable modification. Instance variables can be created in the loop though
	global p_free
	global p_occupied
	global p_free_perm
	global p_occupied_perm
	global p_free_st
	global p_occupied_st
	global CUR_STATE  # where it's currently standing

	# for _ in range(INNER_COMP_F):  # EPILOGUE
		# for logger_entry in logger[kk]:  # EPILOGUE

	# logger_entry = logger[i][ii]
	logger_entry = logger_flat[i]  # EPILOGUE SHIFTED BACK FROM HERE
	log_id = logger_entry['id']
	print("kk: " + str(kk) + ", type: " + logger_entry['type'] + ", id: " + str(log_id))
	if kk == 311:
		fgf = 5

	if logger_entry['type'] == 'START':  # for now nothing
		CUR_STATE = root  # this will depend on whether it's down or up
		# e_N[CUR_STATE.coords[0], CUR_STATE.coords[1]] += 1
		ENV.e_o[CUR_STATE.coords[0], CUR_STATE.coords[1]] = True
		e_N[root.coords[0], root.coords[1]] += 100

	elif logger_entry['type'] == 'SELECT':
		CUR_STATE = CUR_STATE.children[log_id]
		# my_ax_objs2['rect'].set_xy([CUR_STATE.coords[1], CUR_STATE.coords[0]])

	elif logger_entry['type'] == 'EXPAND':  # node added to tree
		# PENDING DELETION
		# CUR_STATE = logger_entry[]
		# CUR_STATE = root
		# id = logger_flat[i]['id']


		id = logger_entry['id']
		splitted = id.split('_')
		col = int(splitted[0])
		row = int(splitted[1])

		s = State({'id': id, 'coords': [col, row], 'parent': CUR_STATE, 'p': None, 'd': CUR_STATE.d + 1})

		ENV.update_env(PM, s.coords, type='occupy')

		e_N[s.coords[0], s.coords[1]] += 1

		num_fill = 5  # ROOT0: 5   tree0: 5 always

		# # EXTRA VISUALIZATION BS BELOW TOOKEN OUT FOR NOW ----------------------
		# if kk < 1000:
		# 	num_fill = 10  # ROOT0: 3  TREE1: 5  root1:
		# elif kk < 2000:
		# 	num_fill = 5  # ROOT0: 2  TREE1: 5 root1:
		#
		# for _ in range(num_fill):
		# 	# e_N[s.coords[0] - random.randint(-2, 3), s.coords[1] + random.randint(-2, 3)] += 1  # tree0
		# 	# e_N[s.coords[0] - random.randint(-1, 2), s.coords[1] + random.randint(-1, 2)] += 1  # root0
		# 	e_N[s.coords[0] - random.randint(-2, 3), s.coords[1] + random.randint(-2, 3)] += 1  # "tree1 NOT SURE HOW GOOD
		#
		# # BOTTOM root/tree1
		# if kk < 200:
		# 	num = 2
		# elif kk < 1000:
		# 	num = 4
		# else:
		# 	num = 1
		# for _ in range(num):  # ONLY BOTTOM FILL
		# 	y = random.randint(700, 719)  # tree1: 640, 719
		# 	x = int(np.random.normal(640, 2))  # tree1: 640, 5
		# 	e_N[y, x] += 1  # "tree1 NOT SURE HOW GOOD

		CUR_STATE.children[id] = s

		CUR_STATE = s  # progress down the tree

		# # LINE PLOT -=---------------------------
		if CUR_STATE is root:
			raise Exception("joEx fuuuu")

		# # FOR BOTH RASTER AND LINES COMMENTED OUT FOR NOW -------------------
		if random.random() < 0.99:  # tree0: 0.8 PROB OF GEN EXTRA SHIT all of the below is extra raster and lines. above is only true raster

			# LINE =========
			if len(p_free) < 1:
				p_free = p_occupied
				p_occupied = []

			p = p_free.pop(0)
			p_occupied.append(p)

			xs, ys = CUR_STATE.xy_from_leaf_to_root(NUM_DEPTH=25, NUM_RAND=1)  # tree0: (25, 15) epilogue
		#
		# 	# # SPECIAL TREE 1 LINE APPEARANCE THING ========================
		# 	# if kk < 300 and xs[-2] == 640 and all(x < 641 for x in xs):
		# 	# 	xs, ys = CUR_STATE.xy_from_leaf_to_root(NUM_DEPTH=4,NUM_RAND=3)
		# 	# elif kk >= 300 and kk < 600 and xs[-2] < 641 and all(x < 650 for x in xs):
		# 	# 	xs, ys = CUR_STATE.xy_from_leaf_to_root(NUM_DEPTH=2, NUM_RAND=4)
		# 	# elif kk >= 600 and kk < 1000 and all(x < 750 for x in xs):
		# 	# 	xs, ys = CUR_STATE.xy_from_leaf_to_root(NUM_DEPTH=2, NUM_RAND=6)
		# 	# elif kk >=1000 and kk < 2000 and all(x < 760 for x in xs):
		# 	# 	xs, ys = CUR_STATE.xy_from_leaf_to_root(NUM_DEPTH=3, NUM_RAND=6)
		# 	# elif kk >= 2000 and kk < 7000:
		# 	# 	pass
		# 	# elif kk >= 7000:
		# 	# 	xs, ys = CUR_STATE.xy_from_leaf_to_root(NUM_DEPTH=5, NUM_RAND=3)
		# 	# else:
		# 	# 	continue
		#
			my_ax_objs2[p].set_data(xs, ys)
		#
		# 	n, type = UG.hardcoded_size_control(kk, CUR_STATE.coords[0], CUR_STATE.coords[1], n=0, ENV=ENV)  # n=0 since it was just created
		#
		# 	# THICKER LINES AT BEG (tree1)
		# 	if kk < 900 and random.random() < 0.3:
		# 		my_ax_objs2[p].set_linewidth(0.3)  # y  tree1: 0.6  root1: 0.4
		# 	else:
		# 		my_ax_objs2[p].set_linewidth(UG.sigmoid(n, ENV))  # y
		#
		# 	# RASTER ========
		# 	res = UG.rasterize_line(kk, ys, xs)  # CREATES PERMANENT THICK RANDOM LINES
		# 	if res is True:
		#
		# 		# if type != 'top_right':
		# 		e_N[ys, xs] += 1
		# 		for _ in range(1):  # tree0/1: 1  ROOT0: 0 root1:
		# 			# pass
		# 			e_N[np.asarray(ys) - np.random.randint(-1, 2, len(ys)), np.asarray(xs) + np.random.randint(-1, 2, len(xs))] += 1
		#
		# 		for _ in range(2):  # LEAFS  tree0/1: 3  ROOT0: 0  root1: 3
		# 			subsety = ys[0:1]
		# 			subsetx = xs[0:1]
		#
		# 			# NOT ROOTS FOR BELOW LINE
		# 			# e_N[np.asarray(subsety) - np.random.randint(-30, 20, len(subsety)), np.asarray(subsetx) + np.random.randint(-30, 30, len(subsetx))] += 1  # tree0
		#
		# 			if ys[0] > ENV.ground_y + 250:  # for ROOT0 there is risk of boundary overflow
		# 				e_N[np.asarray(ys) - np.random.randint(-10, 11, len(ys)), np.asarray(xs) + np.random.randint(-300, 310, len(xs))] += 1
		#
		# 		num_lines = 4  # tree1: 13
		# 		num_depth = 5  # tree1: 12
		# 		num_rand = 7  # tree1: 7
		# 		if kk < 5000:
		# 			num_lines = 8  # tree1: 16
		# 			num_depth = 5  # tree1: 5
		# 			num_rand = 8  # tree1: 5
		# 		for _ in range(num_lines):  # PERM LINES (ONLY FOR ONE EXPANSION LOCATION)  ROOT0: 0 tree0: 10 TREE1: 10
		# 			# produce more lines
		# 			# LINE =========
		# 			if len(p_free_perm) < 1:
		# 				p_free_perm = p_occupied_perm
		# 				p_occupied_perm = []
		#
		# 			p = p_free_perm.pop(0)
		# 			p_occupied_perm.append(p)
		#
		# 			xs, ys = CUR_STATE.xy_from_leaf_to_root(NUM_DEPTH=num_depth, NUM_RAND=num_rand)  # ROOT0: 0  tree0: 5, 12  tree1: 25, 12
		# 			my_ax_objs_perm[p].set_data(xs, ys)
		# 			my_ax_objs_perm[p].set_linewidth(UG.sigmoid(n, ENV))  # y

	# my_ax_objs2['2'].set_color('purple')
	# my_ax_objs2['2'].set_data([24, 17], [8, 13])
	#
	# my_ax_objs2['1'].remove()
	#
	# d = CUR_STATE.d + 1

	elif logger_entry['type'] == 'SIMULATE':
		pass

	elif logger_entry['type'] == 'BACKUP':

		CUR_STATE.N += 1
		e_N[CUR_STATE.coords[0], CUR_STATE.coords[1]] += 1

		# update_g_p(e_o)
		# my_ax_objs2['rect'].set_xy([G_POINT[1], G_POINT[0]])  # PENDING DEL

		# #SNOW ===
		# if ((kk > 2000 and kk < 6000) or (kk > 7000 and kk < 7500)) and kk % 1000 == 0 and CUR_STATE.d > 15:  # the mod thing gives amount of snow
		# # if random.random() < 0.01:  # TEMP TEST
		# 	UG.add_snow(CUR_STATE)

		CUR_STATE = CUR_STATE.parent

		# my_ax_objs2['rect'].set_xy([CUR_STATE.coords[1], CUR_STATE.coords[0]])
	# if CUR_STATE.p is not None:
	# 	old_linewidth = my_ax_objs2[CUR_STATE.p].get_linewidth()
	# 	new_linewidth = old_linewidth + 0.3  # * multiplier
	# my_ax_objs2[str(CUR_STATE.p)].set_linewidth(new_linewidth)

	# old_linewidth = my_ax_objs2['1'].get_linewidth()
	# new_linewidth = old_linewidth + 0.03  # * multiplier
	# my_ax_objs2['1'].set_linewidth(new_linewidth)

	# multiplier = math.log(math.e + old_linewidth * LINE_GROWTH_FACTOR)  # base e
	# if new_linewidth > 0.5:
	# 	new_linewidth = 0.5 + 0.005 * math.log(math.e + new_linewidth) / (CUR_STATE.d * 2)

	elif logger_entry['type'] == 'PRUNE':
		# p_to_kill = CUR_STATE.p
		# if p_to_kill in p_occupied:
		# 	p_occupied.remove(p_to_kill)
		# 	p_free.append(p_to_kill)
		# 	# s_to_kill = CUR_STATE.children[log_id]
		# e_o[CUR_STATE.coords[0], CUR_STATE.coords[1]] = False  # will not be in scatter
		# e_N[CUR_STATE.coords[0], CUR_STATE.coords[1]] = 0

		# if CUR_STATE.parent.children[log_id] == "165_190":
		# 	dfdf = 5
		#
		# if CUR_STATE.id == "165_190":
		# 	dfdf = 5

		# for CUR_STATE

		del CUR_STATE.parent.children[log_id]  # disconnected from tree

		# HERE delete THE WHOLE AREA
		# e_o[CUR_STATE.coords[0]-LOW_MID_Y_kernel // PRU_o_DIV:CUR_STATE.coords[0]+LOW_MID_Y_kernel // PRU_o_DIV + 1,
		# CUR_STATE.coords[1]-MID_X_kernel // PRU_o_DIV:MID_X_kernel // PRU_o_DIV + 1] = False  # will not be in scatter

		ENV.update_env(PM, CUR_STATE.coords, type='prune')

		e_N[CUR_STATE.coords[0], CUR_STATE.coords[1]] = 0



		CUR_STATE = CUR_STATE.parent

	elif logger_entry['type'] == 'PRUNE_stuck':
		del CUR_STATE.parent.children[log_id]  # disconnected from tree
		e_N[CUR_STATE.coords[0], CUR_STATE.coords[1]] = 0
		CUR_STATE = CUR_STATE.parent

	my_ax_objs2['rect'].set_xy([CUR_STATE.coords[1], CUR_STATE.coords[0]])
	# my_ax_objs2['rect'].set_xy([i, i])

	kk += 1
	if kk > 8000:
		zoom_k += 1
	# if kk + 200 > len(logger):
	#

	# # # LINES SECTION ------------
	if i % 19999 == 0:
		if len(p_free) < 1:
			p_free = p_occupied
			p_occupied = []

		p = p_free.pop(0)
		p_occupied.append(p)

		my_ax_objs2[p].set_visible(True)  # pick color from list

		# 	# THIS IS WHERE ALL THE X'S AND Y'S FOR THE CREATED LINE ARE PLOTTED
		xs, ys = root.get_branch_xs_ys()
		my_ax_objs2[p].set_data(xs, ys)  # x then y

	# # # # # STX (STX IS THE EXTRA LINES OR STUMP)  --------------------------------------------
	# num = 1
	# if kk < 150:
	# 	num = 30
	# for _ in range(num):
	# 	if i > 0:
	# 		if len(p_free_st) < 1:
	# 			p_free_st = p_occupied_st
	# 			p_occupied_st = []
	#
	# 		p_st = p_free_st.pop(0)
	# 		p_occupied_st.append(p_st)
	# 		xs, ys = UG.generate_st_xy(ENV, kk)
	#
	# 		my_ax_objs_st[p_st].set_visible(True)
	# 		my_ax_objs_st[p_st].set_data(xs, ys)
	#
	# 	# my_ax_objs2['rect'].set_xy([CUR_STATE.coords[1], CUR_STATE.coords[0]])

	# SCATTER SECTION -----------
	if i % 1 == 0:  # HERE SPEED UP
		y, x = np.argwhere(e_N > 0).T  # try replacing with state list that keeps track of newly occupied ones ... SOMEHOW???

		s = []
		for i in range(len(y)):
			n = e_N[y[i], x[i]]
			# if random.random() < 0.73 or (ENV.tp_name[4] == "0" and x[i] > 900):  # PROB OF VIBRATING NODES 2nd IS STX  0: 0.01  TREE1: 0.93 tried 0.01 but then nothing seems to happen ROOT0: 0.73
			# 	n, _ = UG.hardcoded_size_control(kk, y[i], x[i], n, ENV)  # returns -999 as default
			# if ground[y[i], x[i]] == 1:
			# 	n = 2

			# s.append(UG.sigmoid(n, ENV))  # sigmoid applied to everything
			s.append(100)  # TEMP for 25_40
			# if kk < 1000:  # 1 TEMP
			# 	s.append(UG.sigmoid(n, ENV) * 4)  # sigmoid applied to everything
			# else:
			# 	s.append(UG.sigmoid(n, ENV) * 2)

		# my_ax_objs2['scatter'].set_offsets(np.vstack((x[:i + 1], y[:i + 1])).T)  # the i+1 part allows for the group plotting thing (??)
		my_ax_objs2['scatter'].set_offsets(np.vstack((x, y)).T)
		my_ax_objs2['scatter'].set_sizes(s)

	# # # # # # SNOW -====================================
	# if len(UG.snow_yx) > 5:  # SET THIS
	# 	xy_snow, s_snow = UG.get_snow(ENV)
	# 	if len(xy_snow) > 0:
	# 		my_ax_objs2['scatter_snow'].set_offsets(xy_snow)
	# 		my_ax_objs2['scatter_snow'].set_sizes(s_snow)

	# # # # THIS PLOTS e_o i.e. OCCUPIED TERRITORY (more fancy animation )
	y, x = np.argwhere(ENV.e_o == True).T  # try replacing with state list that keeps track of newly occupied ones ... SOMEHOW???
	s = []
	for i in range(len(y)):
		s.append(SIZE_e_o)  # LITEA
	# my_ax_objs2['scatter_o'].set_offsets(np.vstack((x[:i + 1], y[:i + 1])).T)  # (??)
	my_ax_objs2['scatter_o'].set_offsets(np.vstack((x, y)).T)
	my_ax_objs2['scatter_o'].set_sizes(s)

	# my_ax_objs[0].set_xy(CUR_STATE.xy_rect)  # moving rect
	# 	# ii += 1

	return ax.patches + ax.lines + ax.collections

version = 13
if version == 1:
	# UG.plot_tree(ENV, root_b, e_o_fin, tp)
	UG.plot_tree(ENV, root_b, e_o_fin, None)  # epilogue
else:
	start_t = time.time()
	print("num iters: " + str(len(logger)))
	FRAMES = len(logger) // INNER_COMP_F
	ani = animation.FuncAnimation(fig, animate, interval=100, blit=True,
								  init_func=init, repeat=False, frames=FRAMES)  # len(logger_flat))  # 60, 70 # 84 # interval=MSPF  13   len(logger) WRITER  DOESN"T CARE ABOUT THIS

	# mngr.frame.Maximize(True)
	#
	#
	# plt.show()
	ani.save('./files/vid_80.mp4', writer=writer)

	tot_time = time.time() - start_t
	print("time to make animation: " + str(tot_time) + " |  s/1000 frames: " + str((tot_time/(FRAMES)) * 1000))  # 178s/1000  180/1000


