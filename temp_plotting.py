
from scipy.stats import chi2
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

CYCLES_SHIPS = 1
NUM = 50
cycles_currently = NUM / (2 * np.pi)
d = cycles_currently / CYCLES_SHIPS  # divisor_to_achieve_cycles
X = np.arange(0, NUM)
# X = np.linspace(0, np.pi, 10)
# Y = np.array([sigmoid(x, grad_magn_inv=-NUM/25, x_shift=-10, y_magn=1, y_shift=0) for x in X])  # alpha


# X = np.arange(0, (2 * CYCLES) * np.pi, 0.1)
X = np.arange(0, NUM, 2)
# Y = (np.tan(X/d )* 0.005 + 0.1 * np.sin(X/d) + 0.1 * np.log(X + 10)) + 0.3
# Y = np.sin(X/d)
# Y = np.clip(Y, 0.0, 1.0)

# X = np.linspace(chi2.ppf(0.01, 55),
#                 chi2.ppf(0.99, 55), 100)

Y = chi2.pdf(X/2, 5) * 10

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(X, Y)
plt.xlim([-1, 50])
plt.ylim([-0.5, 2.5])
plt.show()
