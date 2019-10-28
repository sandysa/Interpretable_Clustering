##############################################################################
# Authors: Sandhya Saisubramanian, Sainyam Galhotra
# Description: K-center implementation with Jaccard and Euclidean distances.
#############################################################################
import numpy as np
import math
import networkx as nx

def arreq_in_list(myarr, list_arrays):
    return next((True for elem in list_arrays if np.array_equal(elem, myarr)), False)
class K_center:
    def __init__(self, G, k=3, distance="", tolerance=0.0001, max_iterations=500):
        self.G = G
        self.k = k
        self.tolerance = tolerance
        self.max_iterations = max_iterations
        self.nodes_list = list(G.nodes)
        self.centroids = {}
        self.classes = {}
        self.affiliationArray = [-1 for n in self.G]
        self.distanceFunction = distance

    def distance(self,x,y):
        if self.distanceFunction == "Jaccard":
            return self.Jaccard_distance(x,y)
        distance = 0
        attr = nx.get_node_attributes(self.G,'attributes')
        x_attr =  attr[x]
        y_attr = attr[y]
        if (len(x_attr) != len(y_attr)):
            return -10000
        #check if the nodes are connected
        # Assuming correct input to the function where the lengths of two features are the same
        for i in range(len(x_attr)):
             distance += (x_attr[i]-y_attr[i])*(x_attr[i]-y_attr[i])
        return math.sqrt(distance)


    def Jaccard_distance(self, x, y):
        distance = 0
        attr = nx.get_node_attributes(self.G,'attributes')
        x_attr =  attr[x]
        y_attr = attr[y]
        if (len(x_attr) != len(y_attr)):
            return -10000
        #check if the nodes are connected
        # Assuming correct input to the function where the lengths of two features are the same
        for i in range(len(x_attr)):
            if(x_attr[i] == y_attr[i]):
                distance += 1
        distance = distance*1.0/(len(x_attr))
        return 1-distance


    def find_centers(self):
        for j in range(self.k):
                self.classes[j] = []
        temp_G = nx.Graph()
        temp_G = self.G.copy() #tracks data points that have been used as centroids.. to calculate distance.

        # initialize the first centroid to vertex 0 and remove it from temp_data.
        for n in self.G.nodes:
            self.centroids[0] = n
            temp_G.remove_node(n)
            break
        if self.k == 1:
            return
        #find the fathest point from this.
        distances = [self.distance(nodes, self.centroids[0]) for nodes in self.G.nodes]
        farthest = distances.index(max(distances))
        self.centroids[1] = self.nodes_list[farthest]
        temp_G.remove_node(self.nodes_list[farthest])

        # find the remaining centroids.
        for c in range(2,self.k):
            index = 0
            nodes_list = list(temp_G.nodes)
            min_distances  =  [100 for d in nodes_list]
            for t in temp_G:
                distances = [self.distance(t, self.centroids[centroid]) for centroid in self.centroids]
                min_distances[index] = min(distances)
                index +=1
            next_center = min_distances.index(max(min_distances))
            self.centroids[c] = nodes_list[next_center]
            temp_G.remove_node(nodes_list[next_center])

    def fit(self):
        self.find_centers()
        # Assign points to closest centers
        for features in self.nodes_list:
            if features in self.centroids.values():
                keyval = 0
                for p in self.centroids.values():
                    if p == features:
                        classification = keyval
                        self.classes[classification].append(features)
                        self.affiliationArray[features] = classification
                        break
                    keyval += 1

            else:
                distances = [self.distance(features, self.centroids[centroid]) for centroid in self.centroids]
                classification = distances.index(min(distances))
                self.classes[classification].append(features)
                self.affiliationArray[features] = classification
    
    def printAssignment(self):
        for classification in self.classes:
            print(self.classes[classification])

    def ObjValue(self):
        distances = []
        for classification in self.classes:
            max_dist = 0
            for node in self.classes[classification]:
                dist  = self.distance(node, self.centroids[self.affiliationArray[node]])#classification])
                if(dist > max_dist):
                    max_dist = dist
            distances.append(max_dist)
        return max(distances)

    def getCentroids(self):
        return self.centroids

    def getClasses(self):
        return self.classes
    def set_affiliation_array(self,arr):
        self.affiliationArray=arr
    def getAffiliationArray(self):
        return self.affiliationArray

    def getAffiliation(self, x):
        for classification in self.classes:
            if(arreq_in_list(x, self.classes[classification])):
                return classification
