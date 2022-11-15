import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

ax = plt.axes(projection="3d")

x_data = np.arange(0, 10, 0.1)
y_data = np.arange(0, 50, 0.1)

X, Y = np.meshgrid(x_data, y_data)
Z = X * Y
ax.plot_surface(X, Y, Z)
plt.show()