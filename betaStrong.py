import numpy as np
import sys
import time

from SupportFunctions import *

class betaStrong():
    def __init__(self, domain,G, aff_array,k, beta, distance):
        self.domain = domain
        self.G = G
        self.aff_array = aff_array
        self.k = k
        self.beta = beta
        self.distanceFunction = distance
        self.pairwiseDistance = np.zeros((len(self.G.nodes()), len(self.G.nodes())))

    def precompute_pairwiseDistances(self):
        for i in self.G.nodes():
            for j in self.G.nodes():
                self.pairwiseDistance[i][j] = self.getdistance(i,j)

    def ClusterNodes(self, cluster_id, aff_array):
        nodeList = []
        for node in self.G.nodes():
            if aff_array[node] == cluster_id:
                nodeList.append(node)
        return nodeList


    def getdistance(self,x,y):
        distance = 0
        attr = nx.get_node_attributes(self.G,'attributes')
        x_attr = attr[x]
        y_attr = attr[y]
        if self.distanceFunction == "Jaccard":
            for i in range(len(x_attr)):
                if(x_attr[i] == y_attr[i]):
                    distance += 1
            distance = distance*1.0/(len(x_attr))
            return 1-distance

        for i in range(len(x_attr)):
             distance += (x_attr[i]-y_attr[i])*(x_attr[i]-y_attr[i])
        return math.sqrt(distance)

    def identifyMinScoreCluster(self):
        score = interpretabilityScore_cluster(self.G, self.domain, self.aff_array, self.k)
        return np.argmin(score)

    def get_majority_feature_index(self, target_cluster):
        if self.domain == "sanitation":
            f_score = interpretabilityScore_sanitation(self.G,self.aff_array, target_cluster)
        elif self.domain == "adult":
            f_score = interpretabilityScore_adult(self.G,self.aff_array, target_cluster)
        elif self.domain == "crime":
            f_score = interpretabilityScore_crime(self.G,self.aff_array, target_cluster)
        elif self.domain == "accident":
            f_score = interpretabilityScore_accident(self.G,self.aff_array, target_cluster)
        return np.argmax(f_score)+1

    def indexed_partition(self, nodesList,limit1,limit2):
        R1 = []
        R2 = []
        if limit1+ limit2 != len(nodesList):
            print('error in indexed partition.')
        R1 = nodesList[:limit1]
        R2 = nodesList[limit1:]
        return R1, R2

    def greedy_partition(self,nodeList):
        L = [] #stores number of nodes
        node_set = {} # stores the actual nodes
        # all domains have 4 features (values) of interest.
        for f_index in range(1,5):
            node_set[f_index-1] = features_nodes(nodeList, f_index,self.domain,self.G)
            L.append(len(node_set[f_index-1]))
        sorted_L = L.copy()
        sorted_L.sort(reverse=True)
        l0 = sorted_L[0]
        l1 = sorted_L[1]
        # indices of top 2 feature values in terms of size.
        c1_findex = L.index(l0)
        c2_findex = L.index(l1)
        c1_c2_union = self.union(node_set[c1_findex],node_set[c2_findex])
        R = list(set(nodeList).difference(set(c1_c2_union)))
        limit1 = int(round((l0 * len(R))/(l0+l1)))
        limit2 = int(round((l1 * len(R))/(l0+l1)))
        r1,r2 = self.indexed_partition(R,limit1, limit2)
        c1 = node_set[c1_findex] + r1
        c2 = node_set[c2_findex] + r2
        return c1, c2

    def union(self, a, b):
        return list(set(a) | set(b))

    def kcenterValue(self):
        centroid = np.zeros((self.k))
        cluster_distances = np.zeros((self.k))
        affiliation = {}
        for i in range(self.k):
            affiliation[i] = []
        for node in self.G.nodes():
            aff = self.aff_array[node]
            affiliation[aff].append(node)

        for cluster in range(self.k):
            members = affiliation[cluster]
            best_centroid = -1
            best_obj = 1000000000
            #  find the best centroid
            for m in members:
                distances = [self.pairwiseDistance[m][n] for n in members]
                maxdist = max(distances)
                if maxdist < best_obj:
                    best_obj = maxdist
                    best_centroid = m
            centroid[cluster] = best_centroid
            cluster_distances[cluster] = best_obj
        print("Final K-center objective value=",max(cluster_distances))

    def shrinkingClusters(self, target_cluster,majority_feature_index):
        centroid = np.zeros((self.k))
        affiliation = {}
        for i in range(self.k):
            affiliation[i] = []
        for node in self.G.nodes():
            aff = self.aff_array[node]
            affiliation[aff].append(node)

        nodeList = affiliation[target_cluster]
        iscore = interpretabilityScore(self.G,self.domain, self.aff_array,self.k)
        # print(self.beta, iscore, len(nodeList))
        discard_count =  int(round((self.beta - iscore) * len(nodeList)))
        if discard_count == 0: #can happen due to round off.
            discard_count = 1
        print("Discard count  = ", discard_count)
        # Find a centroid in majority class:
        majorityNodes = features_nodes(nodeList,majority_feature_index,self.domain,self.G)
        best_obj = float('inf')
        best_centroid = -1
        for m in majorityNodes:
            distances = [self.pairwiseDistance[m][n] for n in majorityNodes]
            maxdist = max(distances)
            if maxdist < best_obj:
                best_obj = maxdist
                best_centroid = m
        centroid[target_cluster] = best_centroid
        discard_pile = list(set(nodeList).difference(set(majorityNodes)))
        print("discard pile size=", len(discard_pile))
        if(discard_count > len(discard_pile)):
            print("Error in discard pile calculation")

        # Find distance of all discard nodes wrt. new centroid.
        distances = [self.pairwiseDistance[m][best_centroid]  for m in discard_pile]
        sorted_discard_pile = [x for _,x in sorted(zip(distances,discard_pile),reverse=True)]
        discard_nodes = sorted_discard_pile[:discard_count]

        # Find centroids of other clusters to move these points.
        for cluster in range(self.k):
            if cluster == target_cluster:
                continue
            members = affiliation[cluster]
            best_centroid = -1
            best_obj = 10000000
            #  find the best centroid
            for m in members:
                distances = [self.pairwiseDistance[m][n] for n in members]
                maxdist = max(distances)
                if maxdist < best_obj:
                    best_obj = maxdist
                    best_centroid = m
            centroid[cluster] = best_centroid
        print("Centroids found")
        # Find closest cluster to move each node in discard pile
        moved = 0
        for m in discard_nodes:
            distances = [self.pairwiseDistance[m][centroid[c]] for c in range(self.k)]
            distances[target_cluster] =  float('inf')# because we want to remove the node.
            min_dist = float('inf')
            best_fit = -1
            while best_fit == -1:
                temp_aff_array = self.aff_array.copy()
                for i in range(self.k):
                    if distances[i] < min_dist:
                        min_dist = distances[i]
                        best_fit = i
                temp_aff_array[m] = best_fit
                orig_score = interpretabilityScore_cluster(self.G,self.domain, self.aff_array,self.k)
                new_score = interpretabilityScore_cluster(self.G,self.domain, temp_aff_array,self.k)
                if orig_score[best_fit] > self.beta  and new_score[best_fit] < self.beta:
                    distances[best_fit] = float('inf')
                    best_fit = -1
                    min_dist = float('inf')
                    # No cluster exists.. Should be a rare case.
                    if min(distances) == float('inf'):
                        print("No C' prime cluster found - exiting")
                        sys.exit()
                else:
                    self.aff_array[m] = best_fit
                    moved += 1
                    # print("Nodes Moved so far:",moved)


    def beta_IC(self):
        self.precompute_pairwiseDistances()
        start =  time.time()
        iscore = interpretabilityScore(self.G,self.domain, self.aff_array,self.k)
        print("Current interpretability score = ",iscore )
        iter_index = 0
        while( iscore < self.beta):
            iter_index += 1
            print("Iteration:",iter_index)
            target_cluster = self.identifyMinScoreCluster()
            majority_feature_index = self.get_majority_feature_index(target_cluster)
            minority_nodes = member_nodes(target_cluster, majority_feature_index,self.domain,self.G,self.aff_array)
            min_distance = float("inf")
            min_distance_cluster = -1
            for c_prime in range(self.k):
                if c_prime == target_cluster:
                    continue

                member_nodes_prime = member_nodes(c_prime, majority_feature_index,self.domain,self.G,self.aff_array)
                if len(member_nodes_prime) == 0:
                    continue
                distances_intercluster = []
                for s in minority_nodes:
                    for s_prime in member_nodes_prime:
                        distances_intercluster.append(self.getdistance(int(s),int(s_prime)))
                if min(distances_intercluster) < min_distance:
                    min_distance = min(distances_intercluster)
                    min_distance_cluster = c_prime

            if min_distance_cluster == -1:
                self.shrinkingClusters(target_cluster,majority_feature_index)
            # print("C' cluster id:", min_distance_cluster)
            # score = interpretabilityScore_cluster(self.G, self.domain, self.aff_array, self.k)
            # print("Interpretability score of C'=",score[min_distance_cluster] )
            else:
                a = self.ClusterNodes(target_cluster,self.aff_array)
                b = self.ClusterNodes(min_distance_cluster,self.aff_array)
                union_cluster = self.union(a,b)

                nodes_c, nodes_cPrime = self.greedy_partition(union_cluster)
                for node in nodes_c:
                    self.aff_array[node] = target_cluster
                for node in nodes_cPrime:
                    self.aff_array[node] = min_distance_cluster

            iscore = interpretabilityScore(self.G,self.domain, self.aff_array,self.k)
            print("Current interpretability score = ",iscore )
        print("Time taken in beta strong=",(time.time()-start))
        self.kcenterValue()
        return self.aff_array







