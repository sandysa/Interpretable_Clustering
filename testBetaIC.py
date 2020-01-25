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
from betaStrong import *

import sys

domain_arr  = ['accident','sanitation','crime','adult']
distance_arr=["Jaccard",'euclidean','euclidean','euclidean']
# domains we use = {'accident','sanitation','crime','adult'}
# Corresponding distances:{Jaccard,euclidean,euclidean,euclidean}
domain = ""
domain_distance = ""

def test_Kcenter(G, k,domain, domain_distance):
    print("calling K-center"+domain_distance)
    kc = K_center(G, k,domain_distance)
    start = time.time()
    kc.fit()
    print("time taken in seconds (KC)=", time.time() - start)
    print("Obj = ",kc.ObjValue())
    calculate_composition(G,k,kc.getAffiliationArray(),domain) #In pattern mining.py
    aff_array = kc.getAffiliationArray()
    del kc
    iscore = interpretabilityScore(G,domain, aff_array,k)
    print("Interpretability score = ",iscore )
    return aff_array


def main():
    global domain
    global domain_distance
    global distance_file
    
    if not len(sys.argv)==4:
        print ("python testBetaIC.py <k> <beta> <domain number> \n Domain num: \n 0 : accident, 1: sanitation, 2: crime, 3: adult")
        return
    k = int(sys.argv[1])#50
    beta = float(sys.argv[2])
    domain_num=int(sys.argv[3])

    domain=domain_arr[domain_num]
    domain_distance=distance_arr[domain_num]
    print (domain+" "+ domain_distance)
    Ld = LoadData(domain)
    G  = Ld.readFile()
    distance_file = ""
    if (os.path.isfile(domain+"_distance.txt")):
        distance_file = domain+"_distance.txt"

    print("Dataset:",domain, "K = ",k, "Distance:", domain_distance, "beta=", beta)
    aff_array = test_Kcenter(G,k,domain,domain_distance)
    print("\n")
    print("#######################################################################\n")
    bs = betaStrong(domain,G, aff_array,k, beta, domain_distance,distance_file)
    aff_array = bs.beta_IC()
    calculate_composition(G,k,aff_array,domain)
    del Ld


def clean():
    if os.path.isfile("LoadData.pyc"):
        os.remove("LoadData.pyc")
    if os.path.isfile("Kcenter.pyc"):
        os.remove("Kcenter.pyc")
    if os.path.isfile("betaStrong.pyc"):
        os.remove("betaStrong.pyc")



if __name__ == '__main__':
    main()
    clean()


