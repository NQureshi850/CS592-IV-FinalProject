from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.patches import Circle
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
import numpy as np
import mplcursors as mplc
import geopandas
import PyQt5 as pq
import json
import math
import pandas as pd
from sklearn.neighbors import KernelDensity
import seaborn as sns

world = geopandas.read_file('us_states.json')
fig, ax = plt.subplots(1,1)

frackingData = pd.read_csv('subsetFracking.csv')
print(frackingData['Longitude'])
print(frackingData['Latitude'])


X = []
Y = []

for x in frackingData['Longitude']:
    X.append(x)

#print(X)

for y in frackingData['Latitude']:
    Y.append(y)

X = np.array([X])
Y = np.array([Y])

xgrid = np.arange(-126, -66, .05)
ygrid = np.arange(23.9, 50, .05)
Xtemp, Ytemp = np.meshgrid(xgrid[::5], ygrid[::5][::-1])
print(Ytemp)
xytemp = np.vstack([Ytemp.ravel(), Xtemp.ravel()]).T
xytemp *= np.radians(xytemp)
print(xytemp.shape)
#print(np.transpose(X))
XY = np.concatenate((np.transpose(Y),np.transpose(X)), axis=1)
print(XY.shape)
kde = KernelDensity(bandwidth=.1, metric='haversine', kernel='gaussian', algorithm='ball_tree')
#kde.fit(XY)

#Z = np.exp(kde.score_samples(xytemp))
#print(Z)
#Z = Z.reshape(Xtemp.shape)
#Z = abs(Z)
#print(Z.shape)
print(X.shape)
print(Y.shape)
#print(Z.max())

#levels = np.linspace(0, Z.max(), 40)
#print(levels)
#plt.contourf(Xtemp, Ytemp, Z, levels=levels, cmap=plt.cm.Greens)
sns.kdeplot(frackingData['Longitude'], frackingData['Latitude'], shade=True, thresh=.05, shade_lowest=False, alpha=1, fill=True, ax=ax, cmap='Greens')

ax.set(xlim=(-126, -66))
ax.set(ylim=(23.9, 50))
world.plot(ax = ax, legend=True, color='white', edgecolor='black', linewidth=1, alpha=.2)

#frackingPoints = plt.scatter(X, Y, s=4, color='green')
plt.show()
