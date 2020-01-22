# Interpretable_Clustering
Python codebase for "Balancing the Tradeoff Between Clustering Value and Interpretability", published at AIES 2020.
Authors: Sandhya Saisubramanian*, Sainyam Galhotra*, and Shlomo Zilberstein

Link to paper: https://arxiv.org/pdf/1912.07820.pdf

Files:
Kcenter.py - Implements K-center algorithm 

LoadData.py - Loads data files and returns a graph used for clustering

PatternMining.py - Contains functions related to pattern mining for generating explanations

betaStrong.py - Implementation of Algorithm 4 in the paper

SupportFunctions.py - Functions to calculate interpretability score, sub-graphs and nodes that satisfy a feature value.



Dependencies: pyfpgrowth package for pattern mining, networkx for graph storage, numpy.

**Code Execution**:

"Domain num - 0 : accident, 1: sanitation, 2: crime, 3: adult"

"Approach - 0 : strong-interpretability (IKC), 1: k-center, 2: Partition, 3: KC_F"


To generate beta-interpretable clustering with varying beta (Algorithm 1):
python testBetaIC.py <k> <beta> <domain number>

To generate strongly interpretable clusters with Algorithm 4:
python testCluster.py <k> <domain number> 0

To generate clusters with k-center alone (baseline 1 in the paper):
python testCluster.py <k> <domain number> 1

To generate clusters with paritions over FoI (baseline 2 in the paper, denoted as P_F):
python testCluster.py <k> <domain number> 2

To generate clusters with k-center only using FoI (baseline 3 in the paper, denoted as KC_F):
python testCluster.py <k> <domain number> 3