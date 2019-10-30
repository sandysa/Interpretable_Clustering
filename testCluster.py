##############################################################################
# Authors: Sandhya Saisubramanian, Sainyam Galhotra
# Description: Master file for interpretable clustering.
#############################################################################

import numpy as np
import networkx as nx
import time
import os

from Kcenter import *
from LoadData import *
from PatternMining import *
from SupportFunctions import *

# domains we use = {'accident','sanitation','crime','adult'}
# Corresponding distances:{Jaccard,euclidean,euclidean,euclidean}
domain = "accident"
domain_distance = "Jaccard"


def test_Kcenter(G, k,domain):
    # print("calling K-center")
    kc = K_center(G, k,domain_distance)
    start = time.time()
    kc.fit()
    print("time taken in seconds (KC)=", time.time() - start)
    print("Obj = ",kc.ObjValue())
    iscore = interpretabilityScore(G,domain, kc.getAffiliationArray(),k)
    print("Interpretability score=",iscore)
    calculate_composition(G,k,kc.getAffiliationArray(),domain) #In pattern mining.py
    del kc

# Euclidean and Jaccard distances defined in SupportFunctions.py
def getDistance(x_attr, y_attr):
    if domain_distance == "euclidean":
        return Euclidean_distance(x_attr, y_attr)
    return Jaccard_distance(x_attr, y_attr)

def raw_Interpretability(G,k,domain):
    print("clustering only with interpretable features")
    attr =  nx.get_node_attributes(G,'attributes')
    G_temp = interpretable_baseline_graph(G,domain)
    start_time = time.time()
    kc = K_center(G_temp, k, domain_distance)
    kc.fit()
    print("Time taken (s) = ", (time.time() - start_time))
    aff_array  = kc.getAffiliationArray()
    #calculate true obj value wrt. all features
    distances = []
    classes = kc.getClasses()
    centroids = kc.getCentroids()
    del kc
    for classification in classes:
        max_dist = 0
        for node in classes[classification]:
            dist = getDistance(attr[node], attr[centroids[aff_array[node]]])
            if(dist > max_dist):
                max_dist = dist
        distances.append(max_dist)
    print("Independent K center Obj=",max(distances))
    iscore = interpretabilityScore(G,domain, aff_array,k)
    print("Interpretability score=",iscore)
    calculate_composition(G,k,aff_array,domain)


# IC algorithm 1
def find_best_config(G,k,Features,feature_indices=[],distance_file=""):
    V  = getV(Features,k)
    temp_objective = np.zeros((len(V),len(Features)))
    kc_objective =  np.zeros((k,len(Features)))
    # Run k-center for all values from 1-k
    for i in range(len(Features)):
        print("precomputing kC values for feature", i)
        if domain == "accident":
            G_prime =  getAccidentSubGraph(G,Features,i)
        elif domain == "adult":
            G_prime  = getAdultSubGraph(G,Features,i)
        else:
            temp = Features[i].split("-")
            lb = temp[0].strip()
            ub = temp[1].strip()
            G_prime = getSubGraph_rangeValue(G,lb,ub,feature_indices[i])
        if G_prime.number_of_nodes() == 0:
            kc_objective[:,i] = 100000
            continue

        for trial_k in range(1, k+1):
            if G_prime.number_of_nodes() < trial_k:
                    kc_objective[trial_k-1][i] = float('inf')
                    continue
            kc = K_center(G_prime, trial_k,domain_distance,distance_file)
            kc.fit()
            kc_objective[trial_k-1][i] = kc.ObjValue()
            del kc
            print(trial_k)

    # for i in range(len(Features)):
    #     if domain == "accident":
    #         G_prime =  getAccidentSubGraph(G,Features,i)
    #     elif domain == "adult":
    #         G_prime  = getAdultSubGraph(G,Features,i)
    #     else:
    #         temp = Features[i].split("-")
    #         lb = temp[0].strip()
    #         ub = temp[1].strip()
    #         G_prime = getSubGraph_rangeValue(G,lb,ub,feature_indices[i])
    #     if G_prime.number_of_nodes() == 0:
    #         temp_objective[:,i] = 100000
    #         continue
        # Call K center for each config.
        print("Evaluating V")
        for v_index in range(len(V)):
            v = V[v_index]
            # Not enough points in dataset with this feature to form clusters.
            if G_prime.number_of_nodes() < int(v[i]):
                temp_objective[:,i] = float('inf')
                continue
            temp_objective[v_index][i] = kc_objective[int(v[i]-1)][i]

    best_obj = 10000000
    best_config = []
    for j in range(len(V)):
        if max(temp_objective[j]) < best_obj:
            best_obj = max(temp_objective[j])
            best_config = V[j]
    return best_config, best_obj


def getAccidentSubGraph(G,Features,i):
    G_prime = nx.Graph()
    attributes_prime = {}
    attr = nx.get_node_attributes(G,'attributes')
    index = 0
    for node in G.nodes():
        attributes = attr[node]
        if Features[i] == "Pedestrian hit":
            if('pedestrian' in attributes[10].lower() or "pedestrians" in attributes[10].lower() \
                       or "cyclist" in attributes[10].lower() or "fell from" in attributes[10].lower()):
                G_prime.add_node(index)
                attributes_prime[index] = attributes
                index += 1
            else:
                continue
        elif Features[i] == "Vehicle collision":
            if subGraph_accident_support(attributes[10],1) == False:
                if ('collided' in attributes[10].lower() or 'collision' in attributes[10].lower() \
                    or "rammed" in attributes[10].lower() or "crash" in attributes[10].lower() \
                     or "knocked" in attributes[10].lower()or "hit from the rear" in attributes[10].lower()\
                    or "ramming" in attributes[10].lower()):
                    G_prime.add_node(index)
                    attributes_prime[index] = attributes
                    index += 1
        elif Features[i] == "Death":
            if subGraph_accident_support(attributes[10],1) == False \
                    and subGraph_accident_support(attributes[10],2) == False:
                if ('body' in attributes[10].lower() or 'bodies' in attributes[10].lower()\
                    or "killed" in attributes[10].lower()):
                    G_prime.add_node(index)
                    attributes_prime[index] = attributes
                    index += 1
        elif Features[i] == "Others":
            if subGraph_accident_support(attributes[10],1) == False and \
                subGraph_accident_support(attributes[10],2) == False and \
                subGraph_accident_support(attributes[10],3) == False:
                G_prime.add_node(index)
                attributes_prime[index] = attributes
                index += 1
    nx.set_node_attributes(G_prime, attributes_prime, 'attributes')
    return G_prime

def getAdultSubGraph(G,Features,i):
    G_prime = nx.Graph()
    attributes_prime = {}
    attr = nx.get_node_attributes(G,'attributes')
    index = 0
    for node in G.nodes():
        attributes = attr[node]
        if(Features[i] == "age <= 40 and pay <= 50K"):
            if(float(attributes[0]) <= 40 and float(attributes[14]) == 50):
                G_prime.add_node(index)
                attributes_prime[index] = attributes
                index += 1
        elif Features[i] == "age <= 40 and pay >50K":
            if (float(attributes[0]) <= 40 and float(attributes[14]) == 100):
                G_prime.add_node(index)
                attributes_prime[index] = attributes
                index += 1
        elif Features[i] == "age >40 and pay <=50K":
            if (float(attributes[0]) > 40 and float(attributes[14]) == 50):
                G_prime.add_node(index)
                attributes_prime[index] = attributes
                index += 1
        elif Features[i] == "age >40 and pay >50K":
            if (float(attributes[0]) > 40 and float(attributes[14]) == 100):
                G_prime.add_node(index)
                attributes_prime[index] = attributes
                index += 1
    nx.set_node_attributes(G_prime, attributes_prime, 'attributes')
    return G_prime


def test_accident_IC1(G,k,distance_file):
     Features =['Pedestrian hit','Vehicle collision','Death','Others'] #accident types
     feature_indices = [10,10,10,10]
     start_time = time.time()
     best_config, best_obj = find_best_config(G,k,Features,feature_indices)
     print("KC objective = %f"%best_obj)
     print("best config = ", best_config)
     print("*************************************")
     #Rerun K center with the best config.
     for i in range(len(Features)):
        attr = nx.get_node_attributes(G,'attributes')
        G_prime = getAccidentSubGraph(G,Features,i)
        kc = K_center(G_prime, int(best_config[i]),domain_distance)
        kc.fit()
        centroids = kc.getCentroids()
        attr = nx.get_node_attributes(G_prime,'attributes')
        for cluster in range(best_config[i]):
            total_nodes_incluster = 0
            members = [] #collects features for frequent pattern mining
            accident_count  = np.zeros((len(Features)))
            for node in G.nodes():
                aff = kc.getAffiliation(node)
                if aff == cluster:
                    attributes = attr[node]
                    total_nodes_incluster += 1
                    if subGraph_accident_support(attributes[10],1):
                        accident_count[0] += 1
                        members.append('1')
                    elif subGraph_accident_support(attributes[10],2):
                        accident_count[1] += 1
                        members.append('2')
                    elif ('body' in attributes[10].lower() or 'bodies' in attributes[10].lower() \
                                  or "killed" in attributes[10].lower()):
                        accident_count[2] += 1
                        members.append('3')
                    else:
                        accident_count[3] += 1
                        members.append('4')
            print("**********************")
            print("Accident_type", Features)
            print("Accident type distribution in cluster = ", (accident_count/total_nodes_incluster))
            frequent_pattern_mining(members,Features)
        print("Total time taken for alg IC1 (s) = %f"%(time.time() - start_time))

def test_sanitation_IC1(G, k,distance_file):
    Features = ['0-25','25-50','50-75','75-100'] #pit latrines
    # correponding index of the features in the data.. pit latrine is 3 since string features are ignored.
    feature_indices = [4,4,4,4]
    start_time = time.time()
    best_config, best_obj = find_best_config(G,k,Features,feature_indices)
    print("Final objective = %f"%best_obj)
    print("best config = ", best_config)
    print("*************************************")
    #Rerun K center with the best config.
    for i in range(len(Features)):
        temp = Features[i].split("-")
        lb = temp[0].strip()
        ub = temp[1].strip()
        G_prime  = getSubGraph_rangeValue(G,lb,ub,feature_indices[i])
        kc = K_center(G_prime, int(best_config[i]),domain_distance)
        kc.fit()
        attr = nx.get_node_attributes(G_prime,'attributes')
        for cluster in range(best_config[i]):
            total_nodes_incluster = 0
            members = [] #collects features for frequent pattern mining
            districts_pit_latrine = np.zeros((len(Features)))
            for node in G.nodes():
                aff = kc.getAffiliation(node)
                if aff == cluster:
                    attributes = attr[node]
                    temp_attributes = '0'
                    total_nodes_incluster += 1
                    if(float(attributes[feature_indices[i]]) < 25):
                        districts_pit_latrine[0] += 1
                        temp_attributes = "1"
                    elif(float(attributes[feature_indices[i]]) >= 25 and float(attributes[feature_indices[i]]) < 50):
                        districts_pit_latrine[1] += 1
                        temp_attributes = "2"
                    elif(float(attributes[feature_indices[i]]) >= 50 and float(attributes[feature_indices[i]]) <= 75):
                        districts_pit_latrine[2] += 1
                        temp_attributes = "3"
                    elif(float(attributes[feature_indices[i]]) > 75):
                        districts_pit_latrine[3] += 1
                        temp_attributes = "4"

                    members.append(temp_attributes)
            print("**********************")
            print("pit_latrines_percentage:",Features)
            print("Number of nodes (districts) with %pit latrines:",(districts_pit_latrine/total_nodes_incluster))
            frequent_pattern_mining(members,Features)
        print("Total time taken for alg IC1 (s) = %f"%(time.time() - start_time))


def test_crime_IC1(G,k,distance_file):
    Features = ['0-.25','.25-.50','.50-.75','.75-1.00']
    feature_indices = [16,16,16,16]
    start_time = time.time()
    best_config, best_obj = find_best_config(G,k, Features,feature_indices)
    print("Final objective = %f"%best_obj)
    print("Best config:", best_config)
    print("*************************************")
    #Rerun K center with the best config.
    for i in range(len(Features)):
        temp = Features[i].split("-")
        lb = temp[0].strip()
        ub = temp[1].strip()
        G_prime  = getSubGraph_rangeValue(G,lb,ub,feature_indices[i])
        kc = K_center(G_prime, int(best_config[i]),domain_distance)
        kc.fit()
        attr = nx.get_node_attributes(G_prime,'attributes')
        for cluster in range(best_config[i]):
            total_nodes_incluster = 0
            members = [] #collects features for frequent pattern mining
            median_income_count = np.zeros((len(Features)))
            for node in G.nodes():
                aff = kc.getAffiliation(node)
                if aff == cluster:
                    attributes = attr[node]
                    temp_attributes = '0'
                    total_nodes_incluster += 1
                    if(float(attributes[feature_indices[i]]) <= .25):
                        median_income_count[0] += 1
                        temp_attributes = "1"
                    elif(float(attributes[feature_indices[i]]) > .25 and float(attributes[feature_indices[i]]) <= .50):
                        median_income_count[1] += 1
                        temp_attributes = "2"
                    elif(float(attributes[feature_indices[i]]) > .50 and float(attributes[feature_indices[i]]) <= .75):
                        median_income_count[2] += 1
                        temp_attributes = "3"
                    else:
                        median_income_count[3] += 1
                        temp_attributes = "4"

                    members.append(temp_attributes)
            print("**********************")
            print("median_income:",Features)
            print("Median family income:",(median_income_count/total_nodes_incluster))
            # frequent_pattern_mining(members,Features)
        print("Total time taken for alg IC1 (s) = %f"%(time.time() - start_time))

def test_adult_IC1(G,k,distance_file):
    Features = ['age <= 40 and pay <= 50K', 'age <= 40 and pay >50K','age >40 and pay <=50K', 'age >40 and pay >50K']
    start_time = time.time()
    feature_indices = [16,16,16,16] #placeholder.
    best_config, best_obj = find_best_config(G,k, Features,feature_indices,distance_file)
    print("Final objective = %f"%best_obj)
    print("Best config:", best_config)
    print("*************************************")
    #Rerun K center with the best config.
    for i in range(len(Features)):
        attr = nx.get_node_attributes(G,'attributes')
        G_prime = getAdultSubGraph(G,Features,i)
        kc = K_center(G_prime, int(best_config[i]),domain_distance)
        kc.fit()
        centroids = kc.getCentroids()
        attr = nx.get_node_attributes(G_prime,'attributes')
        for cluster in range(best_config[i]):
            total_nodes_incluster = 0
            members = [] #collects features for frequent pattern mining
            agePay_count  = np.zeros((len(Features)))
            for node in G.nodes():
                aff = kc.getAffiliation(node)
                if aff == cluster:
                    attributes = attr[node]
                    total_nodes_incluster += 1
                    if(float(attributes[0]) <= 40 and float(attributes[14]) == 50):
                        agePay_count[0] += 1
                        members.append('1')
                    elif (float(attributes[0]) <= 40 and float(attributes[14]) == 100):
                        agePay_count[1] += 1
                        members.append('2')
                    elif (float(attributes[0]) >40 and float(attributes[14]) == 50):
                        agePay_count[2] += 1
                        members.append('3')
                    else:
                        agePay_count[3] += 1
                        members.append('4')
            print("**********************")
            print("Accident_type", Features)
            print("Accident type distribution in cluster = ", (agePay_count/total_nodes_incluster))
            frequent_pattern_mining(members,Features)
        print("Total time taken for alg IC1 (s) = %f"%(time.time() - start_time))



def test_IKC1(G,k,distance_file):
    print("Interpretable Clustering Algorithm 1")
    print("Input distance file = ", distance_file)
    if domain == "sanitation":
        test_sanitation_IC1(G,k,distance_file)
    if domain == "crime":
        test_crime_IC1(G,k,distance_file)
    if domain == "accident":
        test_accident_IC1(G,k,distance_file)
    if domain == "adult":
        print("dist file in ikc",distance_file)
        test_adult_IC1(G,k,distance_file)

# This baseline partitions the data into |F| clusters by optimizing for
# interpretability (homogeneity) alone.
def find_interpretable_partition(G,k,Features,feature_indices=[],distance_file=""):
    final_obj = 0
    total_count = 0
    cluster_count = int(k/len(Features))
    for i in range(len(Features)):
        if domain == "accident":
            G_prime =  getAccidentSubGraph(G,Features,i)
        elif domain == "adult":
            G_prime  = getAdultSubGraph(G,Features,i)
        else:
            temp = Features[i].split("-")
            lb = temp[0].strip()
            ub = temp[1].strip()
            G_prime = getSubGraph_rangeValue(G,lb,ub,feature_indices[i])

        if(i+1 == len(Features)):
            cluster_count = k - total_count

        print(Features[i],cluster_count)
        kc = K_center(G_prime,cluster_count,domain_distance,distance_file)
        kc.fit()
        obj = kc.ObjValue()
        del kc
        total_count += cluster_count
        if obj > final_obj:
            final_obj = obj
    print("total clusters = ", total_count)
    return final_obj

def baseline_partition(G,k,distance_file):
    kc_obj = 0
    start_time = time.time()
    if domain == "accident":
        Features =['Pedestrian hit','Vehicle collision','Death','Others'] #accident types
        feature_indices = [10,10,10,10]
    elif domain == "adult":
        Features = ['age <= 40 and pay <= 50K', 'age <= 40 and pay >50K','age >40 and pay <=50K', 'age >40 and pay >50K']
        feature_indices = [16,16,16,16] #placeholder.
    elif domain == "crime":
        Features = ['0-.25','.25-.50','.50-.75','.75-1.00']
        feature_indices = [16,16,16,16]
    elif domain == "sanitation":
        Features = ['0-25','25-50','50-75','75-100'] #pit latrines
        feature_indices = [4,4,4,4]
    kc_obj = find_interpretable_partition(G,k,Features,feature_indices,distance_file)
    print("Objective value = ", kc_obj)
    print("Time taken (s) = ", time.time() - start_time)


def main():
    Ld = LoadData(domain)
    G  = Ld.readFile()
    k = 10
    distance_file = ""
    if (os.path.isfile(domain+"_distance.txt")):
        distance_file = domain+"_distance.txt"

    print("Dataset:",domain, "K = ",k, "Distance:", domain_distance)
    # test_IKC1(G,k,distance_file) #currently works for t <= k
    # test_Kcenter(G, k,domain)
    # raw_Interpretability(G,k,domain)
    baseline_partition(G,k,distance_file)
    del Ld


def clean():
    if os.path.isfile("LoadData.pyc"):
        os.remove("LoadData.pyc")
    if os.path.isfile("Kcenter.pyc"):
        os.remove("Kcenter.pyc")



if __name__ == '__main__':
    main()
    clean()
