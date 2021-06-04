import numpy as np
import time
import random

# # exercise 1
# my_set = {}
# my_list = []
#
# for i in range(100000):
#     my_set[str(i)] = {"my_val": str(i), "my_val2": random.randint(0, 60000)}
#     my_list.append({"my_val": str(i), "my_val2": random.randint(0, 60000)})
#
# time0 = time.time()
# for i in range(10000):
#     search_key = str(random.randint(0, 99999))
#     retrieved = my_set[search_key]
# print("final time: " + str(time.time() - time0))
#
# time0 = time.time()
# for i in range(10000):
#     retrieved = my_list.pop()
#     my_list.insert(0, retrieved)
# print("final time2: " + str(time.time() - time0))


# Exercise 2
my_list = list(range(0, 99999))

targets = []
for i in range(100):
    targets.append(random.randint(0, 99999))
targets = sorted(targets, reverse=False)

time0 = time.time()
for i in range(0, 9999):
    if i in targets:
        aa = 5
        # print("yes")
print("final time: " + str(time.time() - time0))

time0 = time.time()
index_holder = 0
for i in range(0, 9999):
    if targets[index_holder] == i:
        if len(targets) - 1 > index_holder:
            # print("yes")
            index_holder += 1

print("final time2: " + str(time.time() - time0))