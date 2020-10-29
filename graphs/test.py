import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from pathlib import Path

file = open("../..")

x = np.linspace(0, 10, num=11, endpoint=True)
y = np.cos(-x**2/9.0)
f = interp1d(x, y)
f2 = interp1d(x, y, kind='cubic')

xnew = np.linspace(0, 10, num=101, endpoint=True)
import matplotlib.pyplot as plt
plt.plot(xnew, f2(xnew))
plt.show()
