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

def slow_convex_hull(polygon):
    '''
    Takes as input a polygon of N vertices

    param polygon : numpy array; polygon.shape = (N,2)
    return: numpy array; The convex hull of polygon with shape = (n,2) with n <= N 
    '''
    N = polygon.shape[0]
    E = []
    for i in range(N) : 
        p = polygon[i,:] # select first point
        for j in range(1,N) : 
            j_bis = (i+j)%N
            q = polygon[j_bis,:] # selection second point
            hull_vector = True          
            for k in range(N) : 
                if k != i and k != j_bis : 
                    r = polygon[k,:]

                    if vec_product(p-q,r-q) < 0 :  # Check if there is a point at the left of the vector build from first and second point
                        hull_vector = False
            
            if hull_vector : # These two points are part of the convex hull
                E.append([p,q])
    

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

        if len(candidates_index) > 1 : # For the case of colinear vector hull, only the longest hull vector is kept
            for k in range(len(candidates_index)) : 
                if candidates_vec_distance[k] == max(candidates_vec_distance) : 
                    new_vector = E[candidates_index[k]]
                    new_polygon.append(new_vector[1])


        elif len(candidates_index) == 1 : 
            new_vector = E[candidates_index[0]]
            new_polygon.append(new_vector[1])
    
           
        
        
    return new_polygon

def half_hull(points):
    '''
    Takes as input N points

    param points : numpy array; points.shape = (N,2)
    return: numpy array; The convex hull of polygon with shape = (n,2) with n <= N 
    '''
    points_list = list(points)
    if len(points_list) == 2 : 
        return points
    
    half_hull = points_list[:3]
    points_list = points_list[3:]
    loop = True
    while loop : 
        if len(half_hull) == 2 : 
            half_hull.append(points_list.pop(0))

        a= half_hull[-3]
        b= half_hull[-2]
        c= half_hull[-1]
        vec_prod = vec_product(b-a,c-a)

        if len(points_list) == 0 and vec_prod < 0 : 
            loop = False

        if vec_prod >= 0 : 
            half_hull.pop(-2)
        else : 
            if len(points_list) > 0 :
                half_hull.append(points_list.pop(0))

    
    return np.array(half_hull)

def convex_hull(polygon) : 
    '''
    Takes as input a polygon of N vertices

    param polygon : numpy array; polygon.shape = (N,2)
    return: numpy array; The convex hull of polygon with shape = (n,2) with n <= N 
    '''

    
    left_most = polygon[np.argmin(polygon[:,0]),:]
    right_most = polygon[np.argmax(polygon[:,0]),:]

    # computing parameters of the linear cut, halfing the polygon into top and bottom part
    a_cut = (left_most[1] - right_most[1])/(left_most[0] - right_most[0])
    b_cut = left_most[1] - a_cut*left_most[0]
    top_points = polygon[polygon[:,1]> a_cut*polygon[:,0] + b_cut,:]
    bottom_points = polygon[polygon[:,1]< a_cut*polygon[:,0] + b_cut,:]

    extended_top_points = np.zeros((top_points.shape[0]+2,2))
    extended_top_points[1:-1,:] = top_points
    extended_top_points[0,:] = left_most
    extended_top_points[-1,:] = right_most
    
    extended_bottom_points = np.zeros((bottom_points.shape[0]+2,2))
    extended_bottom_points[1:-1,:] = bottom_points
    extended_bottom_points[0,:] = right_most
    extended_bottom_points[-1,:] = left_most
    
    # sorting  points by increasing x for top hull and decreasing x for bottom hull
    extended_bottom_points[1:-1,:] =   extended_bottom_points[np.lexsort((-extended_bottom_points[1:-1,1],-extended_bottom_points[1:-1,0]))+1,:]
    extended_top_points[1:-1,:] =   extended_top_points[np.lexsort((extended_top_points[1:-1,1],extended_top_points[1:-1,0]))+1,:]

    top_half_hull = half_hull(points=extended_top_points)
    bottom_half_hull = half_hull(points=extended_bottom_points)
    
    complete_hull = np.concatenate((top_half_hull[:-1,:],bottom_half_hull[:-1,:]), axis = 0)
    return complete_hull


if __name__ == "__main__":
    N = 8
        
    polygon = np.array([[-1,1],[1,1],[-1,0],[1,-1],[0,-1],[-1,-1],[-0.5,0]]) #/4 + 1/2
    polygon = np.random.rand(N, 2)

#### slow_convex_hull(.)
    patches = []
    hull = slow_convex_hull(polygon=polygon)
    patches.append(Polygon(polygon, closed=True))
    patches.append(Polygon(hull, closed=True))
    p = PatchCollection(patches, alpha=0.4)
    fig, ax = plt.subplots()
    ax.add_collection(p)
    fig.colorbar(p, ax=ax)
   

#### convex_hull(.)
    patches = []
    hull = convex_hull(polygon=polygon)
    patches.append(Polygon(polygon, closed=True))
    patches.append(Polygon(hull, closed=True))
    p = PatchCollection(patches, alpha=0.4)
    fig2, ax2 = plt.subplots()
    ax2.add_collection(p)
    fig2.colorbar(p, ax=ax2)
    plt.show()

