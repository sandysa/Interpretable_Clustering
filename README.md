# Interpretable_Clustering
Python codebase for "Balancing the Tradeoff Between Clustering Value and Interpretability", published at AIES 2020.
Authors: Sandhya Saisubramanian*, Sainyam Galhotra*, and Shlomo Zilberstein
Link to paper: https://arxiv.org/pdf/1912.07820.pdf

Files:
Kcenter.py - Implements K-center algorithm 

LoadData.py - Loads data files and returns a graph used for clustering

PatternMining.py - Contains functions related to pattern mining for generating explanations

betStrong.py - Implementation of Algorithm 4 in the paper

SupportFunctions.py - Functions to calculate interpretability score, sub-graphs and nodes that satisfy a feature value.



Dependencies: pyfpgrowth package for pattern mining, networkx for graph storage, numpy.


