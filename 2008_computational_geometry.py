import numpy as np 
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Wedge
from matplotlib.collections import PatchCollection
import os 


def vec_product(a,b) : 
    return a[0]*b[1] - a[1]*b[0]

def eucliean_distance(a,b) : 
    return np.sqrt((a[0]-b[0])**2 + (a[1]+b[1])**2)

def conv_hull_V0(polygon):
    '''
    Takes as input a polygon of N vertices
    param polygon : numpy array; polygon.shape = (N,2)
    '''
    N = polygon.shape[0]
    E = []
    for i in range(N) : 
        p = polygon[i,:] 
        for j in range(1,N) : 
            j_bis = (i+j)%N
            q = polygon[j_bis,:]
            hull_vector = True          
            for k in range(N) : 
                if k != i and k != j_bis : 
                    r = polygon[k,:]

                    if vec_product(p-q,r-q) < 0 :
                        hull_vector = False
            
            if hull_vector : 
                E.append([p,q])
    print(E)
    # Build convex hull polygon from vector hull
    start_vector = E.pop(0)
    new_polygon = [start_vector[0],start_vector[1]]
    for i in range(len(E)):
        candidates_index = []
        candidates_vec_distance = []
        for j in range(len(E)) :
            if new_polygon[-1][0] == E[j][0][0] and new_polygon[-1][1] == E[j][0][1] :
                candidates_index.append(j)
                candidates_vec_distance.append(eucliean_distance(E[j][0],E[j][1])) 

        if len(candidates_index) > 1 : 
            for k in range(len(candidates_index)) : 
                if candidates_vec_distance[k] == max(candidates_vec_distance) : 
                    new_vector = E[candidates_index[k]]
                    new_polygon.append(new_vector[1])


        elif len(candidates_index) == 1 : 
            new_vector = E[candidates_index[0]]
            new_polygon.append(new_vector[1])
    
           
        
        
    return new_polygon


N = 4
patches = []
fig, ax = plt.subplots()


a = np.array([1,1])
b = np.array([-1,-0.9])
print(vec_product(a,b))       
polygon_test = np.array([[-1,1],[1,1],[-1,0],[1,-1],[0,-1],[-1,-1],[-0.5,0]])/4 + 1/2


hull = conv_hull_V0(polygon=polygon_test)
print(hull)


polygon = np.random.rand(N, 2)
patches.append(Polygon(polygon_test, closed=True))
patches.append(Polygon(hull, closed=True))
p = PatchCollection(patches, alpha=0.4)
ax.add_collection(p)
fig.colorbar(p, ax=ax)
plt.show()





