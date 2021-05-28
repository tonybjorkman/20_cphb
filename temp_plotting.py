
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
import matplotlib.animation as animation
from matplotlib.pyplot import imread
import math
import numpy as np

def sigmoid(x, grad_magn_inv=None, x_shift=None, y_magn=None, y_shift=None):
    """
    the leftmost dictates gradient: 75=steep, 250=not steep
    the rightmost one dictates y: 0.1=10, 0.05=20, 0.01=100, 0.005=200
    """
    return (1 / (math.exp(-x / grad_magn_inv + x_shift) + y_magn)) + y_shift  # finfin


NUM = 50
# X = np.arange(0, NUM)
X = np.linspace(0, np.pi, 10)
# Y = np.array([sigmoid(x, grad_magn_inv=-NUM/25, x_shift=-10, y_magn=1, y_shift=0) for x in X])  # alpha
# Y = np.array([inverted_square(x, grad=2, x_shift=5, y_magn=1, y_shift=0) for x in X])  # alpha

X = np.arange(0, 2 * np.pi, 0.1)
Y = np.sin(X) / 8 + 1
fig, ax = plt.subplots(figsize=(20, 12))

ax.plot(X, Y)
plt.xlim([-1, 10])
plt.ylim([-1.5, 1.5])
plt.show()
