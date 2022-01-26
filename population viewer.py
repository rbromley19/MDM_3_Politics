# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 18:25:49 2021

@author: kiera
"""
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import sympy as sp
from ipywidgets import interactive   
import seaborn as sns
[xmin, xmax] = -2,2
[ymin, ymax] = -2,2
plt.xlim([xmin, xmax]), plt.ylim([ymin, ymax])

#ax = plt.axes(projection='3d')
n=20
centrepopulation =32       
values = np.linspace(2,-2,n)
i=-1
j=-1 
layers = 25#increase for better volume accuracy
population = [[0 for x in range(n)] for y in range(n)]
def popfunc(x,y):
    centrepopulation=32
    return centrepopulation-x**2-y**2
X = np.linspace(-2, 2, n)
Y = np.linspace(-2, 2, n)

#X, Y = np.meshgrid(x, y)   

for x in X:
    #print(x)
    i+=1
    for y in Y:
        j+=1
        print(y)
        print("i:"+str(i))
        print("j:"+str(j))
        population[i][j]=centrepopulation-x**2-y**2#population density function
        print(centrepopulation-x**4-y**4)
    j=-1
ax = sns.heatmap(population, xticklabels=X, yticklabels=Y)
xlabels = ['{:3.1f}'.format(x) for x in X]
ylabels = ['{:3.1f}'.format(y) for y in Y]
ax = sns.heatmap(population, xticklabels=xlabels, yticklabels=ylabels)
plt.show()

#plt.imshow((x,y,population[:,[3]]), cmap='hot', interpolation='nearest')
"""
print(population)
print(np.shape(population))
print(np.shape(values))
X, Y = np.meshgrid(values,values )
centrepopulation = popfunc(values,values)
ax.contour(X,Y,centrepopulation[:][:])

def f(x, y):
    centrepopulation=10
    return centrepopulation-x**2-y**2

x = np.linspace(-2, 2, n)
y = np.linspace(-2, 2, n)

X, Y = np.meshgrid(x, y)
Z = f(X, Y)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#ax = plt.axes(projection='3d')
#ax.contour3D(X, Y, Z, 50, cmap='binary')
#ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                #cmap='viridis', edgecolor='none')
ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1)
angles = np.linspace(0, 360,1000)
print(angles)
for angle in np.linspace(0, 360,1000):
    ax.view_init(angle, angle)
    print(angle)
    plt.draw()
    plt.show()
    plt.pause(0.001)


from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# load some test data for demonstration and plot a wireframe
X, Y, Z = axes3d.get_test_data(0.1)
ax.plot_wireframe(X, Y, Z, rstride=5, cstride=5)

# rotate the axes and update

for angle in range(0, 360):
    ax.view_init(30, angle)
    plt.draw()
    plt.pause(.001)
"""
