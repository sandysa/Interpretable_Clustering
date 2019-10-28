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

# domain  = {"crime","adult", "household","sanitation","accident","pokec","dblp"}
# domains we use = {'accident','sanitation','crime','adult'}
# Corresponding distances:{Jaccard,euclidean,euclidean,euclidean}
domain = "crime"
domain_distance = "euclidean"

def test_Kcenter(G, k,domain):
    print("calling K-center")
    kc = K_center(G, k,domain_distance)
    start = time.time()
    kc.fit()
    print("time taken in seconds (KC)=", time.time() - start)
    # print("Obj = ",kc.ObjValue())
    # calculate_composition(G,k,kc.getAffiliationArray(),domain) #In pattern mining.py
    aff_array = kc.getAffiliationArray()
    del kc
    # iscore = interpretabilityScore(G,domain, aff_array,k)
    # print("Interpretability score = ",iscore )
    return aff_array


def main():
    Ld = LoadData(domain)
    G  = Ld.readFile()
    k = 5
    beta = 1.0
    print("Dataset:",domain, "K = ",k, "Distance:", domain_distance, "beta=", beta)
    aff_array = test_Kcenter(G,k,domain)
    print("\n")
    print("#######################################################################\n")
    bs = betaStrong(domain,G, aff_array,k, beta, domain_distance)
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


