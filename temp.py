
import numpy as np
import matplotlib.pyplot as plt

# x = np.arange(10, 110, 1)
# y = np.arange(10, 110, 1)

x = np.arange(0, 2 * np.pi, 0.1)
y = np.arange(0, 2 * np.pi, 0.1)

X, Y = np.meshgrid(x, y)
Z = (np.sin((X)/2 * Y/2))/3 + 0.5
A = np.ones([63, 63])

gg = X + A

fig = plt.figure(figsize=(12,10))
ax = fig.add_subplot(111, projection='3d')

# Plot a 3D surface
ax.plot_surface(X, Y, Z)
ax.set_xlabel("X")
ax.set_ylabel("Y")
plt.show()
