import math
import pickle
import copy
from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
import scipy.integrate as integrate
import matplotlib.animation as animation
from matplotlib.pyplot import imread

import random
random.seed(7)

class UtilsGui:

	def __init__(self, PM, ENV):
		if ENV.LITE == '25_40':
			self.LINEWIDTH = 0.3
			self.O_SIZE = 100
			self.O_ALPHA = 0.9
			self.NUM_LINE_OBJS = 25
			self.img_path = './maps/mapSblack_40_25.png'
			self.NUM_LINE_OBJS_ST = 15
			self.NUM_SNOW_FLAKES = 10
		elif ENV.LITE == '250_400':
			self.LINEWIDTH = 1
			self.O_SIZE = 1
			self.O_ALPHA = 0.2
			self.NUM_LINE_OBJS = 15
			self.img_path = './maps/mapSblack_400_250.png'
			self.NUM_LINE_OBJS = 25
			self.NUM_LINE_OBJS_ST = 15
			self.NUM_SNOW_FLAKES = 10
		elif ENV.LITE == 'fin':
			self.LINEWIDTH = 0.3  #0.009  # 3  0.3
			self.O_SIZE = 15
			self.O_ALPHA = 0.01
			self.NUM_LINE_OBJS = 1000  # 0: 1000 perhaps 3000  tree1: 1000
			self.NUM_LINE_OBJS_ST = 50  #50 (?) ST = extra lines
			self.NUM_PERM_LINES = 500  # tree0/1: 1000
			self.NUM_SNOW_FLAKES = 10
			# self.img_path = './maps/root0_fin_inv.png'
			self.img_path = './maps/mapSblack_fin.png'
			# self.img_path = './maps/map_fin.png'   #  BOTH ROOT AND TREE  (NO GROUND bcs it's loaded elsewhere as raster)
		# self.img_path = './maps/tree_fin3_inv.png'

		self.ST_SEED = PM.ST_SEED
		# self.snow_yx = np.zeros((self.NUM_SNOW_FLAKES, 2))
		self.snow_yx = []
		# self.init_snow()

		ff = 4

	# from MCTSmanager import all_nodes

	def load_stuff(self, ENV):

		# folder = "/" + ENV.tp_name[0:5]  # epilogue
		folder = "/epilogue"

		with open('./files' + folder + '/logger_S3', 'rb') as f:
			logger = pickle.load(f)

		with open('./files/' + folder + '/logger_flat_S3', 'rb') as f:
			logger_flat = pickle.load(f)

		with open('./files' + folder + '/tree_S3', 'rb') as f:
			root_b = pickle.load(f)
		# root_b = []

		with open('./files' + folder + '/e_o', 'rb') as f:
			e_o_fin = pickle.load(f)
		# e_o = []

		img = imread(self.img_path)

		# return logger, [], root_b, e_o_fin, img
		return logger, logger_flat, root_b, e_o_fin, img

	def create_line_obj(self, ax, my_ax_objs, col=None):
		"""
		THIS ONLY INITS THE PLOTS, NNO DRAWING YET
		NOTE, AX PLOTTING IS BY [X, Y] whereas the logger comes in [row, col]
		"""
		p = len(my_ax_objs)  # 0: state_line, 1: Rect, 2: V, 3: N, 4: pr_line  5: pikk locs
		# _zorder = p  # FOOKING HELL
		# p = [p]

		## STATE CONNECTION LINE =====================================
		colors = ['xkcd:beige', 'beige', 'xkcd:ivory', 'ivory', 'xkcd:tan']
		# col = random.choice(colors)

		if col is None:
			col = 'white'
		# state_g_line, = ax.plot([0, 0], [0, 0], color=col, linewidth=1, visible=True)  # 'xkcd:orangered'   linewidth=1  0.06
		state_g_line, = ax.plot([0, 0], [0, 0], color=col, linewidth=self.LINEWIDTH, visible=True, alpha=0.8)  # 'xkcd:orangered'   linewidth=1  0.06

		my_ax_objs[str(p)] = state_g_line  # id cannot be coords since it will be reused

		return ax, my_ax_objs

	def init_ax_objects(self, PM, ax, my_ax_objs2, my_ax_objs_st, my_ax_objs_perm):  # small tree

		# BUILD BLINKER RECT 0 =============
		rect = patches.Rectangle(xy=[0, 0], width=1, height=1, linewidth=5, color='green', fill=True, visible=True, zorder=9, alpha=1)  # 40 70
		ax.add_patch(rect)
		# my_ax_objs.append(rect)
		my_ax_objs2['rect'] = rect

		my_scatter = ax.scatter([], [], color='white', marker='s', alpha=1, s=0, zorder=5)
		my_ax_objs2['scatter'] = my_scatter

		my_scatter_o = ax.scatter([], [], color='red', marker='s', alpha=self.O_ALPHA/6, s=self.O_SIZE, zorder=1)  # /10 bcs O_ALPHA is for pic
		my_ax_objs2['scatter_o'] = my_scatter_o

		my_scatter_snow = ax.scatter([], [], color='white', marker='s', alpha=1, s=10)  # /10 bcs O_ALPHA is for pic
		my_ax_objs2['scatter_snow'] = my_scatter_snow

		# STATES IN-TREE =============================
		for i in range(self.NUM_LINE_OBJS):  # len logger
			ax, my_ax_objs2 = self.create_line_obj(ax, my_ax_objs2, col='white')  # coords are lower left

		for i in range(self.NUM_LINE_OBJS_ST):  # len logger
			ax, my_ax_objs_st = self.create_line_obj(ax, my_ax_objs_st, col='white')  # obs LINEWIDTH

		# for i in range(self.NUM_PERM_LINES):  # len logger  epilogue
		# 	ax, my_ax_objs_perm = self.create_line_obj(ax, my_ax_objs_perm, col='white')  # obs LINEWIDTH

		return ax, my_ax_objs2, my_ax_objs_st, my_ax_objs_perm  # small tree

	def plot_tree(self, ENV, root_b, e_o, tp=None):

		def helper(s):  # necessary since N not stored in numpy array
			try:
				e_N[s.coords[0], s.coords[1]] = s.N
			except:
				fff = 5
			if len(s.children) > 0:
				for _, child in s.children.items():
					s = child
					helper(s)

		e_N = np.zeros(ENV.DIMS, dtype=int)
		helper(root_b)
		e_N[root_b.coords[0], root_b.coords[1]] = 100  # needed cuz root doesn't have any N and V

		# SCATTER ------------
		y, x = np.argwhere(e_N > 0).T  # try replacing with state list that keeps track of newly occupied ones ... SOMEHOW???
		s = []
		for i in range(len(y)):
			a = e_N[y[i], x[i]]
			s.append(self.sigmoid(a, ENV))
		_max = max(s)
		_min = min(s)
		ax = plt.scatter(x, y, color='white', marker='s', alpha=0.8)
		ax.set_sizes(s)

		if tp is not None:
			# SCATTER ------------
			y, x = np.argwhere(
				tp > 0).T  # try replacing with state list that keeps track of newly occupied ones ... SOMEHOW???
			s = []
			for i in range(len(y)):
				a = e_N[y[i], x[i]]
				s.append(self.sigmoid(a, ENV))
			_max = max(s)
			_min = min(s)
			ax = plt.scatter(x, y, color='white', marker='s', alpha=0.8)
			ax.set_sizes(s)
			# ax.imshow(tp, alpha=1)

		# # # OCCUPIED -------------
		# y, x = np.argwhere(e_o == True).T  # try replacing with state list that keeps track of newly occupied ones ... SOMEHOW???
		# s = []
		# for i in range(len(y)):
		# 	s.append(self.O_SIZE)
		# ax2 = plt.scatter(x, y, color='red', marker='s', alpha=self.O_ALPHA, s=self.O_SIZE)

		plt.show()

	def sigmoid(self, x, ENV, grad_magn_inv=None, x_shift=None, y_magn=None, y_shift=None):
		"""
		the leftmost dictates gradient: 75=steep, 250=not steep
		the rightmost one dictates y: 0.1=10, 0.05=20, 0.01=100, 0.005=200
		"""

		if grad_magn_inv == None:
			grad_magn_inv = 30  # 30
		if x_shift == None:
			x_shift = 0.8
		if y_magn == None:
			y_magn = 0.8  # 0.07
		if y_shift == None:
			y_shift = -0.0001  # 0.07

		if ENV.LITE == '25_40':
			return 10
		elif ENV.LITE == '250_400':
			return 1 / (math.exp(-x / 25 - 2) + 0.03)  # 250_400  (goes up fast for low N)
		elif ENV.LITE == 'fin':
			return (1 / (math.exp(-x/grad_magn_inv + x_shift) + y_magn)) + y_shift # finfin
		# return 1 / (math.exp(-a/10 + 3.7) + 0.1)  # finfin
		# return 1 / (math.exp(-a / 250 - 1) + 0.03)  # fin
		# return 1 / (math.exp(-a/250 - 1) + 0.03)  # fin fast

	def generate_st_xy(self, ENV, kk):

		xs = [ENV.START_COORDS[1] + random.randint(-5, 5)]
		ys = [ENV.START_COORDS[0]]
		xran = [-8, 8]
		yran = [3, 10]
		depth = max(3, kk // 10)
		depth = min(15, depth)

		# # TREE 1 (maybe root1)
		# if kk < 150 and ENV.tp_name[4] == '1':
		# 	xran = [-2, 3]
		# 	yran = [2, 5]
		# 	depth = random.randint(10, 20)
		# elif kk < 300 and ENV.tp_name[4] == '1':
		# 	xran = [-6, 3]
		# 	yran = [3, 6]
		# 	depth = max(3, kk // 10)
		# 	depth = min(15, depth)
		# elif kk < 600 and ENV.tp_name[4] == '1':
		# 	xran = [-4, 0]
		# 	yran = [4, 9]
		# 	depth = max(3, kk // 10)
		# 	depth = min(15, depth)
		# elif kk < 900 and ENV.tp_name[0:5] == 'tree1':
		# 	xran = [-4, 4]
		# 	yran = [3, 18]
		# 	depth = max(3, kk // 60)
		# 	depth = min(20, depth)
		# elif kk < 8001 and ENV.tp_name[0:5] == 'tree1':
		# 	xran = [-4, 4]
		# 	yran = [3, 18]
		# 	depth = max(3, kk // 60)
		# 	depth = min(20, depth)
		# elif ENV.tp_name[0:5] == 'tree1':
		# 	xran = [-4, 4]
		# 	yran = [3, 18]
		# 	depth = max(3, kk // 60)
		# 	depth = min(20, depth)

		# # ROOT 1  (ROOT 0 deleted here)
		if ENV.tp_name[0:5] == 'root1':
			xran = [-4, 2]
			yran = [3, 5]
			depth = max(3, kk // 3)
			depth = min(14, depth)
		# if kk > 8000 and ENV.tp_name[0:5] == 'tree0':  # ONLY tree0
		#
		# # TREE 0
		# if kk > 8000 and ENV.tp_name[4] == '0':  # ONLY tree0
		# 	xs = [ENV.START_COORDS_ST[1]]
		# 	ys = [ENV.START_COORDS_ST[0]]
		# 	xran = [-2, 2]
		# 	yran = [1, 2]
		# 	depth = max(1, (kk) // 340 - 20)
		# 	depth = min(30, depth)

		# return [xs] + [xs], [ys] + [ys]

		x_cur = xs[0]
		y_cur = ys[0]
		for k in range(depth):
			x_new = x_cur + random.randint(xran[0], xran[1])
			y_new = y_cur - random.randint(yran[0], yran[1])
			xs.append(x_new)
			ys.append(y_new)
			x_cur = x_new
			y_cur = y_new

		# pick a random line object using established random seed
		# gg = my_ax_objs_st.keys()  # outputs a set?
		return xs, ys

	def init_snow(self):
		for i in range(len(self.snow_yx)):
			y = random.randint(300, 450)
			x = random.randint(200, 300)
			self.snow_yx[i, 0] = y
			self.snow_yx[i, 1] = x

	def add_snow(self, CUR_STATE):
		self.snow_yx.append([CUR_STATE.coords[0], CUR_STATE.coords[1]])

	def get_snow(self, ENV):
		s_snow = 10
		snow_new = []
		s_snow = []  # sizes
		for i in range(len(self.snow_yx)):
			# old_y = self.snow_yx[i, 0]
			# old_x = self.snow_yx[i, 1]

			old_y = self.snow_yx[i][0]
			old_x = self.snow_yx[i][1]

			new_y = old_y + random.randint(0, 3)
			new_x = old_x + random.randint(-2, 6)
			if new_y < ENV.START_COORDS_ST[0] - 2:  # snow is above surface
				snow_new.append([new_y, new_x])
				s_snow.append(1)

				self.snow_yx[i][0] = new_y
				self.snow_yx[i][1] = new_x
			else:
				self.snow_yx[i][0] = ENV.START_COORDS[0]
				self.snow_yx[i][1] = ENV.START_COORDS[1]

		# yx = np.asarray(snow_new)
		# self.snow_yx = np.asarray(snow_new)

		# xy = []  # DELETE IT
		# for i in range(len(snow_new)):
		# 	xy.append([snow_new[i][1], snow_new[i][0]])

		xy = [[k[1], k[0]] for k in snow_new]
		xy = np.asarray(xy)
		# xy = np.asarray([self.snow_yx[:, 1], self.snow_yx[:, 0]]).T
		return xy, s_snow

	def hardcoded_size_control(self, kk, y, x, n, ENV):  # overwrites

		type = 'default'
		nnew = -999

		if (y > 682 and y < 9999) and (x > 0 and x < 636):  # bottom bottom left  less early  BOTH 1 and 2 ALL?
			# n = self.sigmoid(kk, ENV, grad_magn_inv=300, x_shift=5.8, y_magn=0.01, y_shift=-55)  # grad=300
			# OBS OBS this IS NOT THE PRODUCING THE ACTUAL THICKNESS BUT THE IMPUT TO ANOTHER SIGMOID
			# if random.random() < self.sigmoid(kk, ENV, 1500, 3, 1, -0.01):  # tree0
			# if random.random() < self.sigmoid(kk, ENV, 400, 3, 1, -0.01):  # tree1
			if random.random() < self.sigmoid(kk, ENV, 500, 2, 1, -0.01):  # root1
				nnew = 1

		elif (y > 682 and y < 9999) and (x > 635 and x < 900):  # bottom bottom right  more early
			# n = self.sigmoid(kk, ENV, grad_magn_inv=300, x_shift=5.8, y_magn=0.01, y_shift=-55)  # grad=300
			# OBS OBS this IS NOT THE PRODUCING THE ACTUAL THICKNESS BUT THE IMPUT TO ANOTHER SIGMOID
			# if random.random() < self.sigmoid(kk, ENV, 1700, 2, 1, -0.01):  # tree0
			# if random.random() < self.sigmoid(kk, ENV, 700, 2, 1, -0.01):  # tree1
			if random.random() < self.sigmoid(kk, ENV, 500, 2, 1, -0.01):  # root1
				nnew = 1
		#
		# elif (y > 600 and y < 720) and (x > 640 and x < 650):  # bottom right inner
		# 	# n = self.sigmoid(kk, ENV, grad_magn_inv=300, x_shift=5.8, y_magn=0.01, y_shift=-55)  # grad=300
		# 	# OBS OBS this IS NOT THE PRODUCING THE ACTUAL THICKNESS BUT THE IMPUT TO ANOTHER SIGMOID
		# 	# if random.random() < self.sigmoid(kk, ENV, 800, 6, 1, -0.01):  # tree0
		# 	if random.random() < self.sigmoid(kk, ENV, 600, 4.5, 1, -0.01):  # tree1
		# 		nnew = 1
		#
		# elif (y > 620 and y < 720) and (x > 649 and x < 680):  # bottom right outer
		#
		# 	# n = self.sigmoid(kk, ENV, grad_magn_inv=300, x_shift=5.8, y_magn=0.01, y_shift=-55)  # grad=300
		# 	# OBS OBS this IS NOT THE PRODUCING THE ACTUAL THICKNESS BUT THE IMPUT TO ANOTHER SIGMOID
		# 	# if random.random() < kk/12000:
		# 	# 	n = 1
		# 	# if random.random() < self.sigmoid(kk, ENV, 800, 10, 1, -0.01):  # tree0
		# 	if random.random() < self.sigmoid(kk, ENV, 700, 5.5, 1, -0.01):  # tree1
		# 		nnew = 1
		#
		# elif (y > 622 and y < 720) and (x > 0 and x < 639):  # bottom left
		# 	# n = self.sigmoid(kk, ENV, grad_magn_inv=300, x_shift=5.8, y_magn=0.01, y_shift=-55)
		# 	# OBS OBS this IS NOT THE PRODUCING THE ACTUAL THICKNESS BUT THE IMPUT TO ANOTHER SIGMOID
		# 	# if random.random() < self.sigmoid(kk, ENV, 800, 5, 1, -0.01):  # tree0
		# 	if random.random() < self.sigmoid(kk, ENV, 700, 0.5, 1, -0.01):  # tree1
		# 		nnew = 1
		#
		# elif (y > 544 and y < 569) and (x > 646 and x < 671):  # first cleavege right
		# 	# n = self.sigmoid(kk, ENV, grad_magn_inv=300, x_shift=5.8, y_magn=0.01, y_shift=-55)
		# 	# OBS OBS this IS NOT THE PRODUCING THE ACTUAL THICKNESS BUT THE IMPUT TO ANOTHER SIGMOID
		# 	if random.random() < self.sigmoid(kk, ENV, 700, 5.5, 1, -0.01):
		# 		nnew = 1
		#
		# elif (y > 500 and y < 557) and (x > 624 and x < 642):  # above first branch left
		# 	# n = self.sigmoid(kk, ENV, grad_magn_inv=300, x_shift=5.8, y_magn=0.01, y_shift=-55)
		# 	# if random.random() < self.sigmoid(kk, ENV, 600, 11, 1, -0.01):  # tree0
		# 	if random.random() < self.sigmoid(kk, ENV, 600, 5, 1, -0.01):  # tree1
		# 		nnew = 1
		#
		# elif (y > 383 and y < 463) and (x > 648 and x < 668):  # above second branch left
		# 	# n = self.sigmoid(kk, ENV, grad_magn_inv=300, x_shift=5.8, y_magn=0.01, y_shift=-55)
		# 	# if random.random() < self.sigmoid(kk, ENV, 600, 12, 1, -0.01):   # tree0
		# 	if random.random() < self.sigmoid(kk, ENV, 600, 5, 1, -0.01):   # tree1
		# 		nnew = 1
		#
		# elif (y > 238 and y < 300) and (x > 760 and x < 922):  # TOP RIGHT
		# 	# n = self.sigmoid(kk, ENV, grad_magn_inv=900, x_shift=6.8, y_magn=0.01, y_shift=-220)
		# 	type = 'top_right'
		# 	if random.random() < self.sigmoid(kk, ENV, 600, 15, 1, -0.01):
		# 		nnew = 1
		#
		# elif (y > 329 and y < 429) and (x > 852 and x < 922):  # TOP RIGHT LOWER
		# 	# n = self.sigmoid(kk, ENV, grad_magn_inv=900, x_shift=7.8, y_magn=0.01, y_shift=-340)
		# 	type = 'top_right'
		# 	if random.random() < self.sigmoid(kk, ENV, 600, 15, 1, -0.01):
		# 		nnew = 1
		#
		# # elif (y > 409 and y < 555) and (x > 350 and x < 481):  # WHOLE RIGHT BOTTOM LEFT BRANCH SECTION  tree0
		# # 	# n = self.sigmoid(kk, ENV, grad_magn_inv=900, x_shift=7.8, y_magn=0.01, y_shift=-340)
		# # 	type = 'top_right'
		# # 	# if random.random() < self.sigmoid(kk, ENV, 400, 15, 1, -0.01):
		# # 	nnew = 1
		#
		# elif (y > 409 and y < 9999) and (x > 900 and x < 9999):  # and kk > 8500:  # STX
		# 	if random.random() < self.sigmoid(kk, ENV, 450, 18, 1, -0.3):
		# 		nnew = 1
		# 		pass
		# else:
		# 	if kk < 1000 and y < 650 and x < 900: # make sure it's not st
		# 		if random.random() < self.sigmoid(0.6 * kk + n, ENV, 900, 2, 1, -0.01):
		# 			nnew = 1
		# 	elif y < 650 and x < 900:  # make sure it's not stx
		# 		if random.random() < self.sigmoid(0.6 * kk + n, ENV, 600, 2, 1, -0.01):
		# 			nnew = 1

		# ROOT0 AND 1 (2 top ones + this (?) ) =========================
		# elif y > 660 and (x < 613 or x > 660):
		# 	nnew = 1
		elif (y > 409 and y < 715) and (x > 930 and x < 970):  # and kk > 8500:  # STX
			if random.random() < self.sigmoid(kk, ENV, 450, 18, 1, -0.3):
				nnew = 1
				# pass

		elif x < 500:  # same as above but rest of OTHER TREE  # only root1
			# if random.random() < self.sigmoid(0.6 * kk + n, ENV, 900, 2, 1, -0.01):
			if random.random() < self.sigmoid(0.6 * kk + n, ENV, 700, 3.5, 1, -0.01):
				nnew = 1

		# elif random.random() < self.sigmoid(0.6 * kk + n, ENV, 900, 2, 1, -0.01):  # root0
		# elif random.random() < self.sigmoid(0.6 * kk + n, ENV, 600, 2.2, 1, -0.01):  # root1: DEFAULT
		elif random.random() < self.sigmoid(0.6 * kk + n, ENV, 600, 1.2, 1, -0.01):  # root1 new: DEFAULT
			nnew = 1

		# 450  584
		# # # TREE1 (SOME OF THE UPPER ONES + ONLY THIS SO FAR )===================================
		# elif x > 637 and x < 666 and y > 600:  # ONLY MAIN TRUNK
		# 	if random.random() < self.sigmoid(kk, ENV, 600, 3, 1, -0.01):
		# 		nnew = 1
		# elif y < 450 and x < 584:  # TOP LEFT OF THIS TREE (OTHER TREE)
		# 	if random.random() < self.sigmoid(0.6 * kk + n, ENV, 700, 4.5, 1, -0.01):
		# 		nnew = 1
		# elif x < 500:  # same as above but rest of OTHER TREE
		# 	# if random.random() < self.sigmoid(0.6 * kk + n, ENV, 900, 2, 1, -0.01):
		# 	if random.random() < self.sigmoid(0.6 * kk + n, ENV, 700, 3.5, 1, -0.01):
		# 		nnew = 1
		# elif random.random() < self.sigmoid(0.6 * kk + n, ENV, 600, 2.2, 1, -0.01):  #DEFAULT
		# 	nnew = 1

		return nnew, type

	def rasterize_line(self, kk, ys, xs):
		res = False
		if kk < 800:
			PROB = 0.03  #TREE0: 0.05 ROOT0: 0.05 (MAYBE LESS)  TREE1: 0.08
		elif kk >= 800 and kk < 3500:
			PROB = 0.2
		else:
			PROB = 0.02
		if random.random() < PROB and ys[0] < 710:  # tree0 583
			res = True
		# if (ys[0] > 238 and ys[0] < 368) and (xs[0] > 750 and xs[0] < 827) and random.random() < 0.01:  # TOP RIGHT
		# 	res = False
		#
		# if (ys[0] > 329 and ys[0] < 439) and (xs[0] > 812 and xs[0] < 922):  # TOP RIGHT LOWER
		# 	res = False
		return res

	def init_e_n_root_and_st(self, e_N):  # produce some gui fill for bottom

		for row in range(680, 719):
			for col in range(630, 660):  # root0
			# for col in range(622, 657):  # tree0:
			# for col in range(620, 650):  # tree10
			# 	if random.random() < 0.2:  # tree0 AND 1: 0.1  ROOT0: 0.2
				if random.random() < 0.07:  # tree0 AND 1: 0.1  ROOT1: 0.2
					e_N[row, col] = 1

		# # # # STX '0' ======================
		# for row in range(705, 719):
		# 	for col in range(956, 964):
		# 		if random.random() < 0.3:  # 0.05->shows nothing   tree0: 0.55
		# 			e_N[row, col] = 1

		# pass
	def ground(self):
		import cv2
		ground = cv2.imread('./maps/map_fin_r1.png', cv2.IMREAD_GRAYSCALE)
		ground[ground == 0] = 1
		ground[ground == 255] = 0
		return ground

	def tp_pic(self):
		import cv2
		tp = cv2.imread('./maps/mapSblack_fin.png', cv2.IMREAD_GRAYSCALE)  # root0_compl
		tp[tp == 0] = 1
		tp[tp == 255] = 0
		return tp



# def get_pick_loc