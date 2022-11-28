import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


alpha = 2


# make data

x = np.linspace(0, 180, 180)

#y = x * 100 * np.exp(-1/alpha * (x / 32.97)**alpha)
y_dev = ((100-0.091995*x**2)*(0.99954)**x**2)
# plot
fig, ax = plt.subplots()

#ax.plot(x, y, linewidth=1.0)
ax.plot(x, y_dev, linewidth=1.0)
ax.set_xlim([0, 180])
ax.set_ylim([0, 100])
plt.show()