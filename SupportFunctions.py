##############################################################################
# Authors: Sandhya Saisubramanian, Sainyam Galhotra
# Description: Support functions for interpretable clustering.
#############################################################################
import numpy as np
import networkx as nx
from itertools import combinations_with_replacement,permutations

from Kcenter import *

# Calculates the interpretability score of each cluster
# as the fraction of nodes satisfying each feature value.
# The max score over these features values is the score of a cluster
#  and the min over max score across the clusters is the final score.
def interpretabilityScore(G,domain, aff_array,k):
    score = np.zeros((k))
    for cluster in range(k):
        val = []
        if domain == "sanitation":
            val = interpretabilityScore_sanitation(G,aff_array,cluster)
        elif domain == "accident":
            val = interpretabilityScore_accident(G,aff_array,cluster)
        elif domain == "crime":
            val = interpretabilityScore_crime(G,aff_array,cluster)
        elif domain == "adult":
            val = interpretabilityScore_adult(G,aff_array,cluster)
        score[cluster] = max(val)
    return min(score)

# returns the scores of each cluster.
def interpretabilityScore_cluster(G,domain, aff_array,k):
    score = np.zeros((k))
    for cluster in range(k):
        val = []
        if domain == "sanitation":
            val = interpretabilityScore_sanitation(G,aff_array,cluster)
        elif domain == "accident":
            val = interpretabilityScore_accident(G,aff_array,cluster)
        elif domain == "crime":
            val = interpretabilityScore_crime(G,aff_array,cluster)
        elif domain == "adult":
            val = interpretabilityScore_adult(G,aff_array,cluster)
        score[cluster] = max(val)
    return score



def interpretabilityScore_adult(G,aff_array,k):
    nodes_in_cluster = 0
    adult = np.zeros((4)) #corresponding to each feature value
    attr = nx.get_node_attributes(G,'attributes')
    for node in G.nodes():
        if aff_array[node] == k:
            nodes_in_cluster += 1
            attributes = attr[node]
            if(float(attributes[0]) <= 40 and float(attributes[14]) == 50):
                adult[0] += 1
            elif (float(attributes[0]) <= 40 and float(attributes[14]) == 100):
                adult[1] += 1
            elif (float(attributes[0]) >40 and float(attributes[14]) == 50):
                adult[2] += 1
            elif (float(attributes[0]) >40 and float(attributes[14]) == 100):
                adult[3] += 1
    return (adult/nodes_in_cluster)

def interpretabilityScore_crime(G,aff_array,k):
    nodes_in_cluster = 0
    crime = np.zeros((4)) #corresponding to each feature value
    attr = nx.get_node_attributes(G,'attributes')
    for node in G.nodes():
        if aff_array[node] == k:
            nodes_in_cluster += 1
            attributes = attr[node]
            # attribute_id = 16 # for median income. 
            attribute_id = len(attributes)-1
            if(float(attributes[attribute_id]) <= .25):
                crime[0] += 1
            elif(float(attributes[attribute_id]) > .25 and float(attributes[attribute_id]) <= .50):
                crime[1] += 1
            elif(float(attributes[attribute_id]) > .50 and float(attributes[attribute_id]) <= .75):
                crime[2] += 1
            else:
                crime[3] += 1
    return (crime/nodes_in_cluster)


def interpretabilityScore_accident(G,aff_array,k):
    nodes_in_cluster = 0
    accident = np.zeros((4)) #corresponding to each feature value
    attr = nx.get_node_attributes(G,'attributes')
    for node in G.nodes():
        if aff_array[node] == k:
            nodes_in_cluster += 1
            attribute = attr[node]
            if subGraph_accident_support(attribute[10],1):
                accident[0] += 1
            elif subGraph_accident_support(attribute[10],1) == False and \
                subGraph_accident_support(attribute[10],2) == True:
                accident[1] += 1
            elif subGraph_accident_support(attribute[10],1) == False and\
                subGraph_accident_support(attribute[10],2) == False and \
                subGraph_accident_support(attribute[10],3) == True:
                accident[2] += 1
            elif subGraph_accident_support(attribute[10],1) == False and\
                subGraph_accident_support(attribute[10],2) == False and \
                subGraph_accident_support(attribute[10],3) == False:
                accident[3] += 1
    # print("k =",k,"accident=",accident)
    return (accident/nodes_in_cluster)


def interpretabilityScore_sanitation(G,aff_array,k):
    nodes_in_cluster = 0
    districts_pit_latrine = np.zeros((4)) #corresponding to each feature value
    attr = nx.get_node_attributes(G,'attributes')
    for node in G.nodes():
        if aff_array[node] == k:
            nodes_in_cluster += 1
            attributes = attr[node]
            if(float(attributes[4]) < 25):
                districts_pit_latrine[0] += 1
            elif(float(attributes[4]) >= 25 and float(attributes[4]) < 50):
                districts_pit_latrine[1] += 1
            elif(float(attributes[4]) >= 50 and float(attributes[4]) <= 75):
                districts_pit_latrine[2] += 1
            elif(float(attributes[4]) > 75):
                districts_pit_latrine[3] += 1

    return (districts_pit_latrine/nodes_in_cluster)


def interpretable_baseline_graph(G,domain):
    G_temp = nx.Graph()
    attr =  nx.get_node_attributes(G,'attributes')
    temp_attr = {}
    if domain == "sanitation":
        for node in list(G.nodes):
            u_f = []
            G_temp.add_node(node)
            attribute = attr[node]
            u_f.append(attribute[4])
            temp_attr[node] = u_f
        nx.set_node_attributes(G_temp, temp_attr, 'attributes')
    elif domain == "adult":
        for node in list(G.nodes):
            u_f = []
            G_temp.add_node(node)
            attribute = attr[node]
            if(float(attribute[0]) <= 40 and float(attribute[14]) == 50):
                u_f.append(1)
            elif (float(attribute[0]) <= 40 and float(attribute[14]) == 100):
                u_f.append(2)
            elif (float(attribute[0]) >40 and float(attribute[14]) == 50):
                u_f.append(3)
            elif (float(attribute[0]) >40 and float(attribute[14]) == 100):
                u_f.append(4)
            temp_attr[node] = u_f
        nx.set_node_attributes(G_temp, temp_attr, 'attributes')
    elif domain == "crime":
        for node in list(G.nodes):
            u_f = []
            G_temp.add_node(node)
            attribute = attr[node]
            # attribute_id = 16 # for median income
            attribute_id = len(attribute)-1
            u_f.append(float(attribute[attribute_id]))
            temp_attr[node] = u_f
        nx.set_node_attributes(G_temp, temp_attr, 'attributes')
    elif domain == "accident":
        for node in list(G.nodes):
            u_f = []
            G_temp.add_node(node)
            attribute = attr[node]
            if subGraph_accident_support(attribute[10],1):
                u_f.append(1)
            elif subGraph_accident_support(attribute[10],1) == False and \
                subGraph_accident_support(attribute[10],2) == True:
                u_f.append(2)
            elif subGraph_accident_support(attribute[10],1) == False and\
                subGraph_accident_support(attribute[10],2) == False and \
                subGraph_accident_support(attribute[10],3) == True:
                u_f.append(3)
            elif subGraph_accident_support(attribute[10],1) == False and\
                subGraph_accident_support(attribute[10],2) == False and \
                subGraph_accident_support(attribute[10],3) == False:
                u_f.append(4)
            temp_attr[node] = u_f
        nx.set_node_attributes(G_temp, temp_attr, 'attributes')

    return G_temp

def Jaccard_distance(x_attr, y_attr):
        distance = 0
        if (len(x_attr) != len(y_attr)):
            return -10000
        # Assuming correct input to the function where the lengths of two features are the same
        for i in range(len(x_attr)):
            if(x_attr[i] == y_attr[i]):
                distance += 1
        distance = distance*1.0/(len(x_attr))
        return 1-distance

def Euclidean_distance(x_attr, y_attr):
        distance = 0
        if (len(x_attr) != len(y_attr)):
            return -10000
        for i in range(len(x_attr)):
            distance += (x_attr[i]-y_attr[i])*(x_attr[i]-y_attr[i])
        return math.sqrt(distance)

def getV(Features,k):
    V = []
    t = len(Features)
    comb = combinations_with_replacement([i for i in range(k)], t)
    for c in comb:
        # print(c)
        if sum(list(c)) == k and 0 not in list(c):
        # if sum(list(c)) == k:
            perm = permutations(list(c),t)
            for p in perm:
                if p not in V:
                    V.append(p)
    print("len of V:",len(V))
    return V

def getSubGraph_rangeValue(G,lb,ub, feature_index):
    attr = nx.get_node_attributes(G,'attributes')
    G_prime = nx.Graph()
    attributes_prime = {}
    index = 0
    for node in G.nodes():
        attribute = attr[node]
        if(float(attribute[feature_index]) >= float(lb) and float(attribute[feature_index]) < float(ub)):
            G_prime.add_node(index)
            attributes_prime[index] = attribute
            index += 1
    nx.set_node_attributes(G_prime, attributes_prime, 'attributes')
    return G_prime


def subGraph_accident_support(value, index):
    if index == 1:
        if('pedestrian' in value.lower() or "pedestrians" in value.lower() \
                       or "cyclist" in value.lower() or "fell from" in value.lower()):
            return True
    elif index == 2:
        if ('collided' in value.lower() or 'collision' in value.lower() \
                    or "rammed" in value.lower() or "crash" in value.lower() \
                     or "knocked" in value.lower()or "hit from the rear" in value.lower()\
                    or "ramming" in value.lower()):
            return True
    elif index == 3:
        if ('body' in value.lower() or 'bodies' in value.lower()\
                or "killed" in value.lower()):
            return True

    return False

def member_nodes_sanitation(cluster_id,aff_array,feature_index,G):
    members = []
    attr = nx.get_node_attributes(G,'attributes')
    for node in G.nodes():
        if aff_array[node] == cluster_id:
            attributes = attr[node]
            if feature_index == 1:
                if(float(attributes[4]) < 25):
                    members.append(node)
            elif feature_index == 2:
                if(float(attributes[4]) >= 25 and float(attributes[4]) < 50):
                    members.append(node)
            elif feature_index == 3:
                if (float(attributes[4]) >= 50 and float(attributes[4]) <= 75):
                    members.append(node)
            elif feature_index == 4:
                if(float(attributes[4]) > 75):
                    members.append(node)
    return members

def member_nodes_accident(cluster_id,aff_array,feature_index,G):
    members = []
    attr = nx.get_node_attributes(G,'attributes')
    for node in G.nodes():
        if aff_array[node] == cluster_id:
            attribute = attr[node]
            if feature_index == 1:
                if subGraph_accident_support(attribute[10],1):
                    members.append(node)
            elif feature_index == 2:
                if subGraph_accident_support(attribute[10],1) == False and \
                subGraph_accident_support(attribute[10],2) == True:
                    members.append(node)
            elif feature_index == 3:
                if subGraph_accident_support(attribute[10],1) == False and\
                subGraph_accident_support(attribute[10],2) == False and \
                subGraph_accident_support(attribute[10],3) == True:
                    members.append(node)
            elif feature_index == 4:
                if subGraph_accident_support(attribute[10],1) == False and\
                subGraph_accident_support(attribute[10],2) == False and \
                subGraph_accident_support(attribute[10],3) == False:
                    members.append(node)
    return members

def member_nodes_adult(cluster_id,aff_array,feature_index,G):
    members = []
    attr = nx.get_node_attributes(G,'attributes')
    for node in G.nodes():
        if aff_array[node] == cluster_id:
            attributes = attr[node]
            if feature_index == 1:
                if(float(attributes[0]) <= 40 and float(attributes[14]) == 50):
                    members.append(node)
            elif feature_index == 2:
                if (float(attributes[0]) <= 40 and float(attributes[14]) == 100):
                    members.append(node)
            elif feature_index == 3:
                if (float(attributes[0]) >40 and float(attributes[14]) == 50):
                    members.append(node)
            elif feature_index == 4:
                if (float(attributes[0]) >40 and float(attributes[14]) == 100):
                    members.append(node)
    return members

def member_nodes_crime(cluster_id,aff_array,feature_index,G):
    members = []
    attr = nx.get_node_attributes(G,'attributes')
    for node in G.nodes():
        if aff_array[node] == cluster_id:
            attributes = attr[node]
            # attribute_id = 16 # for median income
            attribute_id = len(attributes)-1
            if feature_index == 1:
                if(float(attributes[attribute_id]) <= .25):
                    members.append(node)
            elif feature_index == 2:
                if(float(attributes[attribute_id]) > .25 and float(attributes[attribute_id]) <= .50):
                    members.append(node)
            elif feature_index == 3:
                if(float(attributes[attribute_id]) > .50 and float(attributes[attribute_id]) <= .75):
                    members.append(node)
            elif feature_index == 4:
                if(float(attributes[attribute_id]) > .75):
                    members.append(node)
    return members


def member_nodes(cluster, feature_index,domain,G,aff_array):
    if domain == "sanitation":
        return member_nodes_sanitation(cluster,aff_array,feature_index,G)
    if domain == "adult":
        return member_nodes_adult(cluster,aff_array,feature_index,G)
    if domain == "accident":
        return member_nodes_accident(cluster,aff_array,feature_index,G)
    if domain == "crime":
        return member_nodes_crime(cluster,aff_array,feature_index,G)

# Given a list of nodes, it will return all the nodes that satisfy
# the values of the feature_index.
def features_nodes(nodeList, feature_index, domain,G):
     if domain == "sanitation":
        return features_nodes_sanitation(nodeList,feature_index,G)
     if domain == "adult":
        return features_nodes_adult(nodeList,feature_index,G)
     if domain == "accident":
        return features_nodes_accident(nodeList,feature_index,G)
     if domain == "crime":
        return features_nodes_crime(nodeList,feature_index,G)

def features_nodes_sanitation(NodeList,feature_index,G):
    members = []
    attr = nx.get_node_attributes(G,'attributes')
    for node in NodeList:
        attributes = attr[node]
        if feature_index == 1:
            if(float(attributes[4]) < 25):
                members.append(node)
        elif feature_index == 2:
            if(float(attributes[4]) >= 25 and float(attributes[4]) < 50):
                members.append(node)
        elif feature_index == 3:
            if (float(attributes[4]) >= 50 and float(attributes[4]) <= 75):
                members.append(node)
        elif feature_index == 4:
            if(float(attributes[4]) > 75):
                members.append(node)
    return members

def features_nodes_accident(NodeList,feature_index,G):
    members = []
    attr = nx.get_node_attributes(G,'attributes')
    for node in NodeList:
        attribute = attr[node]
        if feature_index == 1:
            if subGraph_accident_support(attribute[10],1):
                members.append(node)
        elif feature_index == 2:
            if subGraph_accident_support(attribute[10],1) == False and \
            subGraph_accident_support(attribute[10],2) == True:
                members.append(node)
        elif feature_index == 3:
            if subGraph_accident_support(attribute[10],1) == False and\
            subGraph_accident_support(attribute[10],2) == False and \
            subGraph_accident_support(attribute[10],3) == True:
                members.append(node)
        elif feature_index == 4:
            if subGraph_accident_support(attribute[10],1) == False and\
            subGraph_accident_support(attribute[10],2) == False and \
            subGraph_accident_support(attribute[10],3) == False:
                members.append(node)
    return members

def features_nodes_adult(NodeList,feature_index,G):
    members = []
    attr = nx.get_node_attributes(G,'attributes')
    for node in NodeList:
        attributes = attr[node]
        if feature_index == 1:
            if(float(attributes[0]) <= 40 and float(attributes[14]) == 50):
                members.append(node)
        elif feature_index == 2:
            if (float(attributes[0]) <= 40 and float(attributes[14]) == 100):
                members.append(node)
        elif feature_index == 3:
            if (float(attributes[0]) >40 and float(attributes[14]) == 50):
                members.append(node)
        elif feature_index == 4:
            if (float(attributes[0]) >40 and float(attributes[14]) == 100):
                members.append(node)
    return members

def features_nodes_crime(NodeList,feature_index,G):
    members = []
    attr = nx.get_node_attributes(G,'attributes')
    for node in NodeList:
        attributes = attr[node]
        # attribute_id = 16 # for median income
        attribute_id = len(attributes)-1
        if feature_index == 1:
            if(float(attributes[attribute_id]) <= .25):
                members.append(node)
        elif feature_index == 2:
            if(float(attributes[attribute_id]) > .25 and float(attributes[attribute_id]) <= .50):
                members.append(node)
        elif feature_index == 3:
            if(float(attributes[attribute_id]) > .50 and float(attributes[attribute_id]) <= .75):
                members.append(node)
        elif feature_index == 4:
            if(float(attributes[attribute_id]) > .75):
                members.append(node)
    return members
