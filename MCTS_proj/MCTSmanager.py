
import pickle
from copy import deepcopy
import math
import numpy as np
import os
import shutil
import random
import time
# random.seed(3)
# np.random.seed(3)

from utils_model import *
import PARAMS
# from ENV import *  # DIMS, e_sun, e_water, e_occupied, START_COORDS, LITE, ground_y, update_env  # these are inited in the class
import ENV
from State import State

class MCTSmanager:
	"""
	action-selection in SELECT and EXPAND are in this version governed by different processes
	"""
	def __init__(self, PM, ENV, RESULTS, _pickle=False):
		# self.root = {'id': str(DIMS[0]) + '_' + DIMS[1]}

		# self.S_in_tree = self.root


		# self.e_s = deepcopy(e_sun)
		# self.e_w = deepcopy(e_water)
		# self.e_o = deepcopy(e_o)
		# self.e_tp = deepcopy(e_tp)
		
		self.root = State({'id': str(ENV.START_COORDS[0]) + '_' + str(ENV.START_COORDS[1]), 'coords': ENV.START_COORDS, 'parent': None, 'd': 0})
		self.VALUE_DISTR = deepcopy(PM.VALUE_DISTR)

		self.value_aggregate = 0
		self.num_expands = 0
		self.num_expand_fails = 0
		self.perc_expand_fails = 0
		self.num_sel_fails = 0
		self.num_default_up_exp = 0
		self.num_left_up_exp = 0
		self.num_right_up_exp = 0
		self.num_default_exp = 0
		self.num_down_exp = 0
		self.important_log_event = ""
		self.aggregate_imbalance = 0
		# self.result_log =

		self.logger = []
		for i in range(1, PM.NUM_ITERS + 1):  # 1 needed cuz mod won't work otherwise

			PM.VALUE_DISTR = [PM.v_schedule_sun[i - 1],
								PM.v_schedule_tp[i - 1],
								PM.v_schedule_dist_from_root_y[i - 1],
								PM.v_schedule_dist_from_root_x[i - 1],
								PM.VALUE_DISTR[4],
								PM.VALUE_DISTR[5]]  # this one is set dynamically (???)

			if len(self.logger) == 62:  # TO DEBUG GUI STDOUT. i CANNOT BE USED DUMB IDIOT!
				ff = 9999
			if i == 8:
				fgfg = 5
			self.S_E_S_B(PM, ENV)
			if i % PM.PRUNING_FREQ_MOD == 0:
				self.PRUNE(PM)

			print("i: " + str(i) + "  " + self.important_log_event)
			self.important_log_event = ""

		self.S_E_S_B(PM, ENV)

		# os.remove('./print_dump.txt')
		print("\n\n\nRESULTS ---------------------------", file=open("print_dump.txt", "a"))
		print("Value aggregate: " + str(self.value_aggregate), file=open("print_dump.txt", "a"))
		print("num_exp_success: " + str(self.num_expands) + "   num_exp_fail: " + str(self.num_expand_fails) + " num_sel_fails: " + str(self.num_sel_fails), file=open("print_dump.txt", "a"))
		print("rat_expand_fails: " + str(self.num_expand_fails / (self.num_expand_fails + self.num_expands)), file=open("print_dump.txt", "a" ))
		print("num_default_up_exp: " + str(self.num_default_up_exp) +
			  "  num_left_up_exp: " + str(self.num_left_up_exp) +
			  "  num_right_up_exp: " + str(self.num_right_up_exp) +
			  "  num_default_exp: " + str(self.num_default_exp) +
			  "  num_down_exp: " + str(self.num_down_exp), file=open("print_dump.txt", "a"))

		self.postporicesslog_ep()

		if _pickle == True:
			self.save_everything(ENV)

	def S_E_S_B(self, PM, ENV):
		"""
		Both SELECT and EXPAND may return parent node (BUT THIS CAN NEVER BE ROOT)
		"""
		def helper(s, mnc):  # mnc HAS TO start at > 2  184, 207
			""" OBS this is a 1 step at a time recursion. Each returned state is only 1 step deeper"""

			if len(s.children) < PM.NUM_BRANCHES_PER_NODE and s.can_expand == True:
				s = self.EXPAND(PM, ENV, s)
			elif len(s.children) > 0:
				# GO DOWN AS FAR AS POSSIBLE WHILE TRYING TO EXPAND
				while len(s.children) > 0:
					s_ = self.SELECT(PM, s, type='max', min_num_choices=1)
					if s_ is s:  # SELECTION FAILED (HAPPENS WHEN CHILDREN CAN'T EXPAND)
						self.num_sel_fails += 1
						s.can_expand = False
						break
					if s_.can_expand and len(s_.children) < 2:
						s_ = self.EXPAND(PM, ENV, s_)
					s = s_

				# IF THE LAST REACHED NODE CAN'T EXPAND IT MAKES SENSE TO PUNISH IT
				if s.can_expand == False:
					# print("couldn't SELECT or EXPAND leaf state: " + s_.id)
					self.num_expand_fails += 1
					self.important_log_event = "FAILED TO SELECT OR EXPAND from " + s.id

					if PM.CRAZY_RECURSIVE_NODE_SADISM == 'just_torture' or PM.CRAZY_RECURSIVE_NODE_SADISM == 'anathema':
						# PUNUSH --------
						s.V = (s.V + 0.0001) / 5
						s.can_expand = False

					# # KILL (prob not good to do it here
					if PM.CRAZY_RECURSIVE_NODE_SADISM == 'just_murder' or PM.CRAZY_RECURSIVE_NODE_SADISM == 'anathema':
						id_to_kill = s.id  # CANT DELETE BECAUSE
						if s is not self.root:
							sp = s.parent
							del sp.children[id_to_kill]  # only works if it's deleted from parents point of view.
							self.log_ep.append({'type': 'PRUNE_stuck', 'id': id_to_kill})
							print("Prune stuck")
							sp.V += 0.001  # since parent may have 0 val
							s = sp
							s.can_expand = False
				# else:
				# 	s = self.EXPAND(s, temp)

			elif len(s.children) < 1 and s.can_expand == False:  # not sure about this one. Prob happens due to pruning
				if s is self.root:
					raise Exception("joEx you're killing yourself")
				self.num_expand_fails += 1

				if PM.CRAZY_RECURSIVE_NODE_SADISM == 'just_torture' or PM.CRAZY_RECURSIVE_NODE_SADISM == 'anathema':
					# ## PUNISH
					s.can_expand = False
					s.V = (s.V + 0.0001) / 18
					print("faile in expand")
					self.important_log_event = "FAILED TO SELECT OR EXPAND from " + s.id

				if PM.CRAZY_RECURSIVE_NODE_SADISM == 'just_murder' or PM.CRAZY_RECURSIVE_NODE_SADISM == 'anathema':
					## KILL
					id_to_kill = s.id
					if s is not self.root:
						ENV.e_o[
						s.coords[0] - PM.LOW_MID_Y_kernel // PM.PRU_o_DIV:s.coords[0] + PM.LOW_MID_Y_kernel // PM.PRU_o_DIV + 1,
						s.coords[1] - PM.MID_X_kernel // PM.PRU_o_DIV:s.coords[1] + PM.MID_X_kernel // PM.PRU_o_DIV + 1] = False
						s = s.parent
						del s.children[id_to_kill]  # only works if it's deleted from parents point of view.
						self.log_ep.append({'type': 'PRUNE', 'id': id_to_kill})

				return s
			else:  # algo never goes here
				raise Exception("joExc algo should never go here")
			return s

		self.log_ep = [{'type': 'START', 'id': self.root.id}]

		# G_POINT = update_g_p(self.e_o)  # this does not necessarily have to take place each iteration
		s = self.root  # should always be root
		s_ = helper(s, 4)
		if s_.coords == [14, 19]:
			hghg = 6
		if s_ is not self.root:
			V = self.SIMULATE(PM, ENV, s_)
			self.root = self.BACKUP(PM, s_, V)  # # s is state from which rollout was launched. returns root.
		self.logger.append(self.log_ep)

		if s_.parent is not None and s_.id not in s_.parent.children:
			raise Exception("wtf is going on")

	def PRUNE(self, PM, temp=None):
		"""
		Find the worst leaf and delete it
		"""
		self.log_ep = [{'type': 'START', 'id': self.root.id}]
		s = self.root  # should always be root
		rand_id = random.choice(list(s.children))
		s = s.children[rand_id]
		self.log_ep.append({'type': 'SELECT', 'id': s.id})

		while len(s.children) > 0:  # no stupid recursion
			s = self.SELECT(PM, s, type='min', min_num_choices=1)

		if s is not self.root:
			if s.parent is not self.root:
				id_to_kill = s.id
				s = s.parent
				del s.children[id_to_kill]  # only works if it's deleted from parents point of view.
				self.log_ep.append({'type': 'PRUNE', 'id': id_to_kill})
			else:
				s = s.parent

		if s is not self.root and s.parent is not self.root:
			self.root = self.BACKUP(PM, s, 0.001)  # 0 since it's a pruned node

		self.logger.append(self.log_ep)

	def SELECT(self, PM, s_parent, type, min_num_choices=1):
		"""
		input is parent, output is either some descendant - if selection worked, or parent if it didn't
		:param type: max or min i.e. find best or worst child
		:param min_num_choices: How many children there must be to trigger expansion
		"""
		_s = None
		if len(s_parent.children) >= min_num_choices:  # WILL ONLY OPERATE WHEN THERE ARE CHILDREN
			good_children = []
			all_children = []
			for _, child in s_parent.children.items():  # computes best Q among children
				all_children.append(child)
				if child.can_expand == True:
					good_children.append(child)
			if len(good_children) > 0 and type == 'max':
				_s = self.action_selection(PM, good_children, type_as=type)  # requires plausible children
				self.log_ep.append({'type': 'SELECT', 'id': _s.id})
			elif type == 'min' and len(all_children) > 0:
				# _s = self.action_selection(PM, all_children, type_as=type)
				_s = random.choice(all_children)
				self.log_ep.append({'type': 'SELECT', 'id': _s.id})
			else:
				_s = s_parent
		else:
			_s = s_parent
		return _s  # this happens often the more discretization used.

	def EXPAND(self, PM, ENV, sp):  # returns action
		"""
		sp: state parent
		# will try multiple locations to expand and if this fails it will be set to can't expand
		"""
		## ACTION OVER JUST EXPANDED NODES (done before all other nodes expanded since s_for_sim needs deepcopy) ==========================
		s = {}
		flag_can_expand = False

		if sp.coords == [184, 207]:
			fdf  = 5

		action_coords, status = get_possible_action(self, PM, ENV, sp)

		if status == 'could_not_find_free_coords':
			# PUNISH
			sp.can_expand = False
			sp.V = (sp.V + 0.0001) / 8
			# print("faile in expand")
			self.important_log_event = "FAILED to EXPAND from " + sp.id
			return sp

		# BY NOW EXPANSION WILL HAPPEN
		if action_coords[0] < 0 or action_coords[1] < 0 or action_coords[0] > ENV.ground_y:
			raise Exception("joException tree growing too large")
		if action_coords == [12, 17]:
			gg = 5
		self.num_expands += 1
		action_id = str(action_coords[0]) + '_' + str(action_coords[1])  # [0] because they are in list
		ENV.e_o[action_coords[0], action_coords[1]] = True

		# self.e_o[action_coords[0]-LOW_MID_Y_kernel//EXP_o_DIV:action_coords[0]+LOW_MID_Y_kernel//EXP_o_DIV + 1,
		# action_coords[1]-MID_X_kernel//EXP_o_DIV:action_coords[1]+MID_X_kernel//EXP_o_DIV + 1] = True  # don't know what this is PENDING DELETION

		ENV.update_env(PM, action_coords, type='occupy')

		# # # SHADOW PART
		ENV.e_s[action_coords[0]:self.root.coords[0], action_coords[1]] -= \
			PM.SHADOW_AMOUNT * ENV.e_s[action_coords[0]:self.root.coords[0], action_coords[1]]

		s = State({'id': action_id, 'coords': action_coords, 'parent': sp, 'd': sp.d + 1})  # new state
		sp.children[s.id] = s

		self.log_ep.append({'type': 'EXPAND', 'id': s.id})
		self.important_log_event = "EXPAND: " + s.id

		return s

	def SIMULATE(self, PM, ENV, s):
		"""
		Value computation gona be pretty complex
		NO NEED TO PUT THIS IN LOGGER (whatever)
		Prob skip value, use control instead (too easy problem)
		"""

		sun = ENV.e_s[s.coords[0], s.coords[1]]
		tp = ENV.e_tp[s.coords[0], s.coords[1]]

		# HERER CHECK EXTREMITIES TO SEE IF NODE IS BEYOND REASONABLE EXTENTS

		dist_y_to_root = s.coords[0] - self.root.coords[0]
		# COMPUTE IMBALANCE
		dist_x_to_root = s.coords[1] - self.root.coords[1]  # if pos: s to right, if neg: s to left.
		_imb_pen = 0
		imbalance_ = 0.00001 * abs(self.num_left_up_exp - self.num_right_up_exp)  # the more dist the more penalty
		if self.num_left_up_exp > self.num_right_up_exp and dist_x_to_root < 0\
				or self.num_right_up_exp > self.num_left_up_exp and dist_x_to_root > 0:
			_imb_pen = min(self.VALUE_DISTR[5] * abs(dist_x_to_root) * imbalance_, 1)
			print("imb_pen: " + str(_imb_pen))

		# DENOMINATOR HAS TO BE > 1
		V = (PM.VALUE_DISTR[0] * sun + PM.VALUE_DISTR[1] * tp)  / \
			max(1., (PM.VALUE_DISTR[2] * abs(dist_y_to_root) +
					 PM.VALUE_DISTR[3] * abs(dist_x_to_root) +
					 PM.VALUE_DISTR[4] * s.d +
					 _imb_pen)
				)
		self.value_aggregate += V
		self.aggregate_imbalance += imbalance_

		return V

	def BACKUP(self, PM, s, V):
		"""
		s: the state which is updated.  can be any state including just expanded ones. root returned
		Everything that needs to be written to a state is done here
		The root never gets anythin written to it, so this needs to be added manually
		THIS MAY PERHAPS NOT NEED BE LOGGED, BUT GOOD TO HAVE IN CASE VALUE WILL BE USED
		INCLUDES G_POINT UPDATE
		"""
		if s.parent == None:  # backup CANNOT be launched from root itself
			raise Exception("joExc")

		while s.parent is not None:
			s.N += 1  # incremental mean
			s.V = s.V + (1/s.N) * (V - s.V)

			if random.random() < PM.REINCARNATION_P and s.N > 10:  # resetting of expansion for promising nodes
				s.can_expand = True

			self.log_ep.append({'type':'BACKUP',
								'V': round(s.V, 1), 'N': s.N, 'id': s.id})
			s = s.parent

		return s

	def action_selection(self, PM, children, type_as='max'):
		"""
		the "min" case is treated separately for now below
		:param children:
		:param type_as:
		:return:
		"""

		# NORMALIZE =============================
		# max_Q_prev = max(children, key=lambda x: children[x].V)

		# if type == 'max':
		# 	sign = 1
		# else:
		# 	sign = -1
		child = children[0]
		# if len(children) == 1:
		# 	child_id = list(children.keys())[0]
		# 	child = children[0]
		if type_as == 'max':
			max_Q_prev = -999999
			sum_N = 0

			# TWO THINGS ARE DONE IN HERE, N AND MAX_V
			# for _, child in children.items():  # computes best Q among children
			for child in children:  # computes best Q among children
				sum_N += child.N
				if child.V > max_Q_prev:
					max_Q_prev = child.V

			if max_Q_prev == -999999:
				raise Exception("joEXP action-selection")

			# best_child_id = None
			best_child = None
			best_Q = -99999
			# for child_id in children:
			for child in children:
				# child = children[child_id]
				# Q_prev_norm = -child.V / max_Q_prev  # negative !!!
				Q_prev_norm = child.V / max_Q_prev  # these should be positive when values are positive
				sum_b = max(sum_N - child.N, 0)  # all the visits apart from this child
				UCT = (math.sqrt(sum_b) / (1 + child.N))
				# P = random.random()
				P = 1
				Q = Q_prev_norm + PM.C * P * UCT
				if Q > best_Q:
					best_Q = Q
					# best_child_id = child_id
					best_child = child

			# if best_child_id == None:
			if best_child == None:
				raise Exception("EXCEPT action_selection")

			# child_id = best_child_id
			child = best_child  # for return

		elif type_as == 'min':  # find the worst child (for now just the least visited one)
			min_Q_prev = 9999999999
			sum_N = 0

			for child in children:  # computes best Q among children
				sum_N += child.N
				if child.V < min_Q_prev:
					min_Q_prev = child.V

			if min_Q_prev == 9999999999:
				raise Exception("joEXP action-selection")

			# worst_child_id = None
			worst_child = None
			worst_Q = 99999
			# for child_id in children:
			for child in children:
				# child = children[child_id]
				# Q_prev_norm = -child.V / max_Q_prev  # negative !!!
				Q_prev_norm = child.V / (min_Q_prev +0.001)  # TEMP  # these should be positive when values are positive
				sum_b = max(sum_N - child.N, 0)  # all the visits apart from this child
				UCT = (math.sqrt(sum_b) / (1 + child.N))
				P = random.random()
				# P = 1
				Q = Q_prev_norm + PM.C * P * UCT
				if Q < worst_Q:
					worst_Q = Q
					# worst_child_id = child_id
					worst_child = child
			child = worst_child

		return child

	def postporicesslog_ep(self):

		self.logger_flat = []

		for i in range(len(self.logger)):  # FOR EACH SESB
			log_ep = self.logger[i]
			self.logger_flat.extend(log_ep)  # the key here is using extend instead of append

	def save_everything(self, ENV):

		# folder = "/" + ENV.tp_name[0:5]  # epilogue
		folder = "/epilogue"

		# if ENV.tp_name[0:5] == "tree0":
		# 	folder = "/tree0"
		# elif ENV.tp_name[0:5] == "tree2":
		# 	folder = "/tree1"
		# elif ENV.tp_name[0:5] == "root0":
		# 	folder = "/root0"
		# elif ENV.tp_name[0:5] == "root1":
		# 	folder = "/root1"

		with open("./files" + folder + "/logger_S3", 'wb') as f:
			pickle.dump(self.logger, f)

		with open("./files" + folder + "/logger_flat_S3", 'wb') as f:
			pickle.dump(self.logger_flat, f)

		with open("./files" + folder + "/tree_S3", 'wb') as f:
			pickle.dump(self.root, f)

		with open("./files" + folder + "/e_o", 'wb') as f:
			pickle.dump(ENV.e_o, f)


# p_delete_old_files(pickle_dir)
if __name__ == "__main__":  # without this variables cannot be imported from this module without running the optimization

	start_time = time.time()
	RESULTS = []
	# RESULTS = np.load("./RESULTS.npy")
	# aa = aa[aa[:, 1].argsort()]
	num_fails = 0
	NUM_RUNS = 50
	run_single = True
	if run_single is True:
		NUM_RUNS = 1
	for i in range(NUM_RUNS):  # 300 took 379

		print("\n\n\n\n\n\n\n" + str(i))

		if run_single:
			_rand_seed = 6
			_picc = True
		else:
			_rand_seed = random.randint(1, 99999)
			_picc = False
		_pm = PARAMS.Params(_rand_seed)
		_env = ENV.ENV(_pm)

		_mcts = MCTSmanager(_pm, _env, RESULTS, _pickle=_picc)
		score = (_mcts.num_expand_fails + _mcts.num_sel_fails) / (_mcts.num_expand_fails + _mcts.num_sel_fails + _mcts.num_expands)
		entry = [_rand_seed, score, _pm.NUM_BRANCHES_PER_NODE, _pm.C, _pm.EXPANSION_BIAS_P, _pm.NODE_DEPTH_V, _pm.IMBALANCE_V,
				 _pm.SHADOW_AMOUNT, _pm.PRUNING_FREQ_MOD, _pm.EXPAND_KERNEL_DEF_DEPTH, _pm.NUM_ROUND_SUN_LOOPS,
				 _pm.MID_X_kernel, _pm.LOW_MID_Y_kernel, _pm.EXP_o_DIV, _pm.PRU_o_DIV,
				 _pm.REINCARNATION_P, _pm.SUN_FROM, _pm.SUN_TO, _pm.TP_FROM, _pm.TP_TO, _pm.NUM_ITERS]
		# 6: imbalance 9: EXPAND_KERNEL 12: LOW_MID_Y_kernel   16: SUN_FROM   18: TP_FROM
		RESULTS.append(entry)
		# except:
		# 	print("EXCEPT MCTS")
		# 	entry = [_rand_seed, 0, _pm.NUM_BRANCHES_PER_NODE, _pm.C, _pm.EXPANSION_BIAS_P, _pm.NODE_DEPTH_V,
		# 			 _pm.IMBALANCE_V,
		# 			 _pm.SHADOW_AMOUNT, _pm.PRUNING_FREQ_MOD, _pm.EXPAND_KERNEL_DEF_DEPTH, _pm.NUM_ROUND_SUN_LOOPS,
		# 			 _pm.MID_X_kernel, _pm.LOW_MID_Y_kernel, _pm.EXP_o_DIV, _pm.PRU_o_DIV,
		# 			 _pm.REINCARNATION_P, _pm.SUN_FROM, _pm.SUN_TO, _pm.TP_FROM, _pm.TP_TO, _pm.NUM_ITERS]
		# 	RESULTS.append(entry)
		# 	num_fails += 1

	for entry in RESULTS:
		print(entry)
	print("time it took: " + str(time.time() - start_time))
	print("num_fails: " + str(num_fails))



	# [14467, 0.14150943396226415, 3, 0.4604589853904191, 0.8142317323759325, 0.1, 25, 5, 500, 4, 8, 2, 2]

	if run_single is False:
		res = np.asarray(RESULTS)
		res_sort = res[res[:, 1].argsort(axis=0)[::-1]]  # to reverse order res[res[:, 1].argsort(axis=0)[::-1]]
		np.save('./RESULTS3', res)



# sortedArr = arr2D[arr2D[:,columnIndex].argsort()]


