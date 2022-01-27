# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 16:01:47 2021

@author: kiera
"""
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import sympy as sp

[xmin, xmax] = -2.1, 2.1
[ymin, ymax] = -2.1, 2.1
x = sp.symbols('x')
y = sp.symbols('y')
popfieldedge = 10
tacticalportion = 1/3

points = np.array([[-0.9,-0.9],[0,0],
                   [0.5,0.5],[-0.5,0.5],[-1.1,-1.1],[-1,-1],[-1.1,-1],[-1,-1.1]])

centroids = points
numberofregions = len(centroids)
points = np.append(points, [[1000, 1000], [-1000, 1000], [1000, -1000], [-1000, -1000]], axis=0)
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.spines['left'].set_position(('zero'))
ax.spines['bottom'].set_position('zero')

ax.set_xlabel("Economic Policy")
ax.set_ylabel("Social Policy")
ax.xaxis.set_label_coords(0.12, 0.55)
ax.yaxis.set_label_coords(0.55, 0.2)
vor = Voronoi(points)

fig = voronoi_plot_2d(vor, ax, show_vertices=True, point_size=0, zorder=1, )

plt.xlim([xmin, xmax]), plt.ylim([ymin, ymax])

colors = cm.rainbow(np.linspace(1, 0, len(points) - 4))
labels = []

centroids = []
for point in range(len(points[0:len(points) - 4])):
    centroids.append(points[point])
    temp = ("party:" + str(int(point)))
    plt.scatter(points[point][0],points[point][1],zorder =2,color=colors[point])

    labels.append(temp)

ax.legend(labels, fontsize="x-small")

coords = [[-2, 2], [2, 2], [2, -2], [-2, -2]]

# print(points)
points = []
lines = []
for i in coords:
    points.append(sp.Point(i))


# print(vor.vertices)
# print(vor.regions)
# print("___")
# print(vor.ridge_vertices)
realregions = []
for region in vor.regions:
    if -1 not in region and len(region) > 2:  # removes regions with vertex at infinity
        realregions.append(region)
# print(realregions)
vertexcoords = []
# print(points)
t = tuple(points)

square = sp.Polygon(*t)
originalregions = []
"""
for region in vor.regions:
    if not -1 in region:
        polygon = [vor.vertices[i] for i in region]
        plt.fill(*zip(*polygon))
"""
# loop for finding vertexes of regions elnclosed by square
for region in realregions:
    print(region)
    # print(region[0])
    vertexofregion = []
    originalregionpoints = []

    for coord in vor.vertices[region]:
        originalregionpoints.append(sp.Point(coord))  # creates sympy points array for region

    # print(originalregionpoints)
    currentregion = sp.Polygon(*originalregionpoints)  # creates sympy region of current region
    # originalregions.append(currentregion)
    [vertexofregion.append(i) for i in square.intersect(currentregion)]
    # adds all intersects of square with current region
    for i in points:
        if currentregion.encloses_point(i):
            vertexofregion.append(i)
    for point in range(len(region)):
        if square.encloses_point(sp.Point(vor.vertices[region[point - 1]])):
            # print((sp.Point(vor.vertices[region[point-1]])).evalf())
            # print("is already in square")
            vertexofregion.append(sp.Point(vor.vertices[region[point - 1]]))
    vertexcoords.append(vertexofregion)  # all coordinates of vertexes sorted by region
colors = cm.rainbow(np.linspace(1, 0, len(vertexcoords)))


yaxis = sp.Line(sp.Point(10, 10), sp.Point(-10, -10))
xaxis = sp.Line(sp.Point(10, 0), sp.Point(-10, 0))


def comparepoint(p1, p2, centroid):  # copied from stackoverflow
    # https://stackoverflow.com/questions/6989100/sort-points-in-clockwise-order
    x1 = p1.coordinates[0]
    x2 = p2.coordinates[0]
    y1 = p1.coordinates[1]
    y2 = p2.coordinates[1]
    cx = centroid.coordinates[0]
    cy = centroid.coordinates[1]
    if ((x1 - cx >= 0) and (x2 - cx < 0)):
        return True
    if (x1 - cx < 0 and x2 - cx >= 0):
        return False
    if (x1 - cx == 0 and x2 - cx == 0):
        if (y1 - cy >= 0 or y2 - cy >= 0):
            return y1 > x1;
        return y2 > y1
    det = (x1 - cx) * (y2 - cy) - (x2 - cx) * (y1 - cy)
    if (det < 0):
        return True
    if (det > 0):
        return False
    d1 = (x1 - cx) * (x1 - cx) + (y1 - cy) * (y1 - cy)
    d2 = (x2 - cx) * (x2 - cx) + (y2 - cy) * (y2 - cy)
    return d1 > d2;



"""uses comparepoints to order points in each region, by angle, allows drawing of shapes
just bubble sort but compare func instead of < or >"""
k = -1
for region in vertexcoords:
    k += 1

    centroid = sp.Point([sum(x) / len(x) for x in zip(*region)])
    # print(region)
    #finds new centroid as average of each vertex of region
    #for p in region:
    #print(sp.Line(centroid, p).angle_between(xaxis).evalf())
    for i in range(len(region)):        
        for j in range(len(region) - 1):
            if comparepoint(region[j], region[j + 1], centroid):
                # Swap
                region[j], region[j + 1] = region[j + 1], region[j]
                

    vertexcoords[k] = region

def popfunc(x, y, centrepopulation=8):
    return centrepopulation - x * 2 - y * 2

def popfield(centrepopulation=8,N=popfieldedge):
    X = np.linspace(-2, 2, N)
    Y = np.linspace(-2, 2, N)
    population = [[0 for x in range(N)] for y in range(N)]
    i=-1
    j=-1   
    for x in X:
        #print(x)
        i+=1
        for y in Y:
            j+=1            
            population[i][j]=popfunc(x,y)#population density function           
        j=-1
        population = np.asarray(population)
    return population



def tactical(pop,portion = tacticalportion):
    pop=np.array(pop)
    tacticalpop = pop*portion
    pop = pop -tacticalpop
    #print(tacticalpop)
    #print("--------------------------------------------------\n\n\n\n--------------------------------------------------------------")
    return pop, tacticalpop




"""
#will at some point be a recusive nd integration 
def integrate(region,n,pop,sregions,regionpops,dim,depth,current=np.zeros(dim)):#dim long list of 0s
    c=-1
    
    if len(region)!=0:
        for i in region:#each recursion layer 1 less dimension 
            depth=depth+1
`            integrate(i,n,pop,sregions,regionpops,dim,depth)
        for i in  range((len(current)-depth)):#after line/plane ect is completed 
            current[i]=0
        current[depth]+=1
    else:
        #region is now a point
        for i in sregion:
            c+=1
            if i.encloses_point(region):
                regionpops[c]+=pop(current)
                
                return depth - 1, 
"""

def volume2d(pop,sregions):
    """this is 99% of run time and disgustingly inneficient if someone could make it faster would be great"""
    #pop2d array of populations sregions regions as sympy 2dshapes
    regionvolumes= np.zeros(numberofregions)
    xcount=-1
    n=len(pop)
    values = np.linspace(-2,2,n)
    for x in values:
        xcount+=1
        ycount =-1
        for y in values:
            ycount+=1
            i=-1
            #print("checking:")
            #print(str((xcount,ycount)))
            #print("@")
            #print(str((x,y)))
            for region in sregions:
                i+=1
                if region.encloses_point(sp.Point(x,y)):
                    print(str((x,y)))
                    print("in")
                    regionvolumes[i]+=pop[xcount,ycount]
    regionvolumes = np.array(regionvolumes)
    print(regionvolumes)
    return regionvolumes            

def tactvoting(tacticalpop,regionvolumes,centroids):
    i=-1
    #tactical pop is 1/3 of total pop array
    n=np.shape(tacticalpop)[0]    
    values = np.linspace(-1.999,1.999,n)
    tacchoices = np.zeros(np.shape(tacticalpop))
    
    """for each row take each square and compare with each region"""
    for x in tacticalpop:
        #x is row of tactical population
        i+=1
        j=-1
        for y in x:
            #y is individual square on view space of those tactically voting
            j+=1
            maxratio=0
            coords = (values[i],values[j])
            
            regionindex =0
            actualbelief = np.pi#placeholder
            for region in sregions:
                regionindex +=1
                if region.encloses_point(coords):                
                    actualbelief = regionindex
                    regionchoice = regionindex
                    #print(coords)
            if actualbelief == np.pi: 
                print(coords)
                print("somehow not in any region")
                regionchoice = 1/0
            for k in range(len(regionvolumes)):
            #bigvolume high chance to win low distance better views                 
                   a = regionvolumes[k]/(((centroids[k][0]- coords[0])**2 +(centroids[k][1]- coords[1])**2)**(1/2))                  
                   if a>maxratio:
                       maxratio=a
                       regionchoice =(k)
            #print(tacchoices)
            #if regionchoice != actualbelief and regionchoice !=-1:
                #print("\n\n\n point at: "+str((coordx,coordy))+" inside region: "+str(regionindex))
                #print("will tactically vote for: "+str(regionchoice)+" ,but is closer in belief to: "+str(actualbelief))
                
            tacchoices[i][j]= regionchoice
    return tacchoices


#sets ordered lists of points to sympy 2d shapes
sregions=[]
regionvolumes=[]

for region in vertexcoords:
    sregions.append(sp.Polygon(*region))
    regionvolumes.append(0)
    
    
pop = popfield()#2d array of population at each view


print("finding volumes no tactical")                
regionvolumes = volume2d(pop,sregions)
print("found")
(popnotac,tacticalpop) = tactical(pop)
portionofvolumes = 2/3*np.array(regionvolumes)
tactchoices = tactvoting(tacticalpop,regionvolumes,centroids)


tacticalonly = np.zeros(np.shape(portionofvolumes))
k=-1

tactchoices
for row in tactchoices:
    k+=1
    j=0
    print(row)
    for choice in row:                   
        tacticalonly[int(choice)-1] += tacticalpop[k][j]#idk why all choices 1 to high
        j+=1
        
      
voteswithtactical = np.add(tacticalonly,portionofvolumes)        

n = -1


for region in vertexcoords:
    n += 1
    shape = [i.coordinates for i in region]
    plt.fill(*zip(*shape))
    print("--------")
    print("region:" + str(n))
    print("area:" + str(abs(sp.Polygon(*region).area.evalf())))
    
    print("volume/votes of region:" + str(regionvolumes[n]))
    print("Including Tactical voting:"+str(voteswithtactical[n]))
    print("region centroid"+str(centroids[n]))
    #for point in region:
        #print(point.evalf())
        #plt.scatter(point.coordinates[0], point.coordinates[1], color=colors[n], zorder=2)
    # plt.imshow(population, cmap='hot', interpolation='nearest')


#for i in range(len(points)):
    #lines.append(sp.Line(points[i - 1], points[i]))
    # print(lines[i].plot_interval())
    # print(lines[i].equation())

    #plt.plot([coords[i - 1][0], coords[i][0]], [coords[i - 1][1], coords[i][1]], color="black", zorder=3)

plt.show()
"""          
j = -1
sregion = []
i = -1
regionvolumes = []
for region in vertexcoords:
    i += 1
    sregion.append(sp.Polygon(*region))
    coordsinregion = []
    #print("in region: " + str(i))
    
    for x in values:

        for y in values:
            if sregion[i].encloses_point(sp.Point(x, y)):  # adds points in shape to 2d array
                coordsinregion.append((x, y))  # array of coordinates of points in current region

    volumeofregion = 0
    for layer in range(layers):
        #print("layer number" + str(layer))
        # print(volumeoflayer)
        volumeoflayer = 0
        for coord in coordsinregion:
            # evaluating at height of current layer = currentlayer*(height of max layer/numoflayers)
           
            heightatcord = popfunc(coord[0], coord[1]) - layer * centrepopulation / layers
            
            #rint(heightatcord)
            if heightatcord > 0:  # ignore negative volume
                volumeoflayer += heightatcord * centrepopulation / layers
        volumeofregion += volumeoflayer

    regionvolumes.append(volumeofregion)
n = -1
#print(regionvolumes)

"""