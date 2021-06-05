import numpy as np
import time
import random
import os
# # # exercise 1
# my_set = {}
# my_list_1 = []
# my_list_2 = []
#
# for i in range(100000):
#     my_set[str(i)] = {"my_val": str(i), "my_val2": random.randint(0, 60000)}
#     my_list_1.append({"my_val": str(i), "my_val2": random.randint(0, 60000)})
#
# time0 = time.time()
# for i in range(100000):
#     search_key = str(random.randint(0, 99999))
#     retrieved = my_set[search_key]
# print("final time: " + str(time.time() - time0))
#
# time0 = time.time()
# current_list = my_list_1
# for i in range(100000):
#     retrieved = my_list_1.pop()
#     my_list_2.append(retrieved)
# print("final time2: " + str(time.time() - time0))


# # Exercise 2
# my_list = list(range(0, 9999))
#
# targets = []
# for i in range(100):
#     targets.append(random.randint(0, 9999))
# targets = sorted(targets, reverse=False)
#
# time0 = time.time()
# for i in range(0, 9999):
#     if i in targets:
#         aa = 5
#         # print("yes")
# print("final time: " + str(time.time() - time0))
#
# time0 = time.time()
# index_holder = 0
# latest_target = targets[0]
# for i in range(0, 9999):
#     if latest_target == i:
#         index_holder += 1
#         latest_target = targets[index_holder]
#
#
# print("final time2: " + str(time.time() - time0

# exercise 3: random.randint vs np.rand
# lower = np.random.randint(0, 5, size=(10, 1))
# upper = np.random.randint(5, size=(10, 1))
A = np.zeros((50, 2), dtype=int)
for i in range(50):
    a = random.randint(4, 10)
    b = random.randint(b, 3)
hh = 5
