import os
import ast
from ast import literal_eval
import tokenize
import string
import collections
from collections import Counter
import math
import Utilities
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import scipy.cluster.hierarchy as sch
import scipy.spatial.distance as ssd
from scipy.cluster.hierarchy import dendrogram, linkage, fclusterdata
from numpy.random import rand
from sklearn.metrics.pairwise import euclidean_distances
import sys
from itertools import groupby
#import PyClustering

sys.setrecursionlimit(100000)
EucDict = {}
Distances = {}
ClusterIDs = {}
#####################################################################
def euclidean(Shares, N, CantRelate):
	print("shares started")
	Utilities.t()
	Labels = []
	DataPoints = []
	done = []
	count = 0
	for S in Shares.items():
		count += 1
		print("post number: " + str(count) + " of " + str((len(Shares)-1)))
		A = []
		User = S[0]
		Entry = S[1]
		if User not in CantRelate:
			done.append(User)
			EucDict[User] = {}
			for E in Entry.items():
				Feature = E[0]
				Share = E[1]
				A.append(Share)
			A = np.array(A).reshape(-1,1)	
			v = 0
			for W in Shares.items():
				Candidate = W[0]
				if Candidate not in done:
					if Candidate not in CantRelate:
						B = []
						Entry = W[1]
						v += 1
						print("post number: " + str(count) + " pair number: " + str(v) + " of " + str((len(Shares)-count)))
						EucDict[User].update({Candidate: 0})
						for E in Entry.items():
							Feature = E[0]
							Share = E[1]
							B.append(Share)
						B = np.array(B).reshape(-1,1)
						Combo = (User, Candidate)
						Distance = ssd.euclidean(A, B)	
						EucDict[User][Candidate] = Distance
	print("shares completed")
	Utilities.t()
#	Utilities.WriteFile(EucDict, "JWEucDistances2.txt")
	print("write file called")
	Utilities.t()
	Utilities.WriteFile(EucDict, "EucDistances2")
	Utilities.t()
	print("write file completed ")
	Utilities.t()
	return EucDict
#####################################################################

def DeltaClean(N, FullData):
	print("delta called ")
	Utilities.t()
	if N == 500:
		print("Burrows500")
		Utilities.t()
	#	Dict = Utilities.LoadTexts("BurDistances2500.txt")
		ZScores = Utilities.LoadTexts("ZScores500.txt")
		CantRelate = Utilities.LoadTexts("NotEnough10outof500.txt")
		TopN = Utilities.LoadTexts("Top500DeltaFeatures.txt")
	if N == 1000:
		print("Burrows1000")
		Utilities.t()
	#	Dict = Utilities.LoadTexts("BurDistances2500.txt")
		ZScores = Utilities.LoadTexts("ZScores1000.txt")
		CantRelate = Utilities.LoadTexts("NotEnough10outof1000.txt")
		TopN = Utilities.LoadTexts("Top1000DeltaFeatures.txt")
	print("files loaded ")
	Utilities.t()
	count = 1
	done = []
	missing = []
	incomplete = []
	for Z in ZScores.items():  # {user: {word: score, word2, score2}}
		print("post number: " + str(count) + " of " + str((len(FullData)-1)))
		Utilities.t()
		count += 1
		A = Z[0] #user
		done.append(A)
		if A not in CantRelate:
			Distances[A] = {} #old style
			for Y in ZScores.items():
				B = Y[0] #users
				if B not in CantRelate:
					delta = 0
					if B not in done:
						Distances[A].update({B: 0}) #old style
						for T in TopN:
							AZ = ZScores[A][T]
							BZ = ZScores[B][T]
							delta += math.fabs((AZ - BZ))
					delta /= N
					if B not in done:
						Distances[A][B] = delta #old style
	with open("Distances3" + str(N) + ".txt", "w+") as f:
			f.write(str(Distances))
	return Distances
#####################################################################

def DenTexts(N, M):
	FullData = Utilities.LoadTexts("FullData.txt")
	if N == 500:
		CantRelate = Utilities.LoadTexts("NotEnough10outof500.txt")
	if M == "Euc" and N == 500:
		print("Euclidean500")
		Utilities.t()
	#	Dict = euclidean(Shares500, N, CantRelate)
		Dict = Utilities.LoadTexts("EucDistances2500.txt")
	if M == "Bur" and N == 500:
		print("Burrows500")
		Utilities.t()
		Dict = Utilities.LoadTexts("BurDistances3500.txt")
	#	Dict = DeltaClean(N, FullData)
	if N == 1000:
		CantRelate = Utilities.LoadTexts("NotEnough10outof1000.txt")
	if M == "Euc" and N == 1000:
		print("Euclidean1000")
		Utilities.t()
	#	Dict = euclidean(Shares1000, N, CantRelate)
		Dict = Utilities.LoadTexts("EucDistances21000.txt")
	if M == "Bur" and N == 1000:
		print("Burrows1000")
		Utilities.t()
		Dict = Utilities.LoadTexts("BurDistances31000.txt")
	#	Dict = DeltaClean(N, FullData)
	if N == "JW" and M == "Bur":
		print("BurrowsJW")
		Utilities.t()
		Dict = Utilities.LoadTexts("JWBurDistances.txt")
		CantRelate = Utilities.LoadTexts("NotEnough10outof1000.txt")
	if N == "JW" and M == "Euc":
		print("EuclidianJW")
		Utilities.t()
		Dict = Utilities.LoadTexts("JWEucDistances.txt")
		CantRelate = Utilities.LoadTexts("NotEnough10outof1000.txt")
	return Dict
	return CantRelate
	return Zscores
		
def Clean(Dict):
	dicto = {}
	for D in Dict.items(): 
		User = D[0]
		Data = D[1].items()
		if len(Data) != 0:
			for A in Data:
				Candidate = A[0]
				Score = A[1]
				Key = (User, Candidate)
				dicto[Key] = Score
	return dicto
	      
def DendoPlot(Data, N):
	keys = [sorted(k) for k in Data.keys()]
	values = Data.values()
	avclustermembers = math.sqrt(len(values))/12
	print(avclustermembers)
	sorted_keys, distances = zip(*sorted(zip(keys, values)))
##	Links = linkage(distances, 'single')
	Links = linkage(distances, 'ward')
	labels = sorted(set([key[0] for key in sorted_keys] + [sorted_keys[-1][-1]]))
#	ColourCode = {"JW": "#f10505", # red
 #                "FE": "#0527f1", # blue
  #               "FT": "##26904b", #green 
   #              "PT": "#0e0e0e", #black
    #             "SF": "#a90bfb", #purple
     #            "JW": "#fb740b", #orange
        #         }
#	D = dendrogram(Z=Z, labels=DF_dism.index, color_threshold=None, leaf_font_size=12, leaf_rotation=45, link_color_func=D_leaf_colors)
#	Dendrogram = dendrogram(Links, labels=labels, leaf_rotation=45, link_color_func=ColourCode)
	print("plot")
	Utilities.t()
	Dendrogram = dendrogram(Links, labels=labels, leaf_rotation=45)
##	Dendrogram = dendrogram(Links, p=avclustermembers, labels=labels, truncate_mode='lastp', count_sort='decending', distance_sort=False, leaf_rotation=90, show_contracted=True)
#	Dendrogram = sch.fcluster(Links, t=6, criterion='maxclust')
	plt.show()
#	group1 = np.where(Dendrogram == 1)
#	ClusterIDs["group1"] = group1
#	print("group1 is: " + str(len(group1)))
#	group2 = np.where(Dendrogram == 2)
#	ClusterIDs["group2"] = group2
#	print("group2 is: " + str(len(group2)))
#	group3 = np.where(Dendrogram == 3)
#	ClusterIDs["group3"] = group3
#	print("group3 is: " + str(len(group3)))
#	group4 = np.where(Dendrogram == 4)
#	ClusterIDs["group4"] = group4
#	print("group4 is: " + str(len(group4)))
#	group5 = np.where(Dendrogram == 5)
#	ClusterIDs["group5"] = group5
#	print("group5 is: " + str(len(group5)))
#	group6 = np.where(Dendrogram == 6)
#	ClusterIDs["group6"] = group6
#	print("group6 is: " + str(len(group6)))
#	print(ClusterIDs)
#	for Cluster in ClusterIDs.items():
#		C = Cluster[0]
#		IDs = Cluster[1]
#		for ID in IDs:
#			for I in range(len(ID)):
#				name = labels[I]
#				print(name)
		
#	Dendrogram = dendrogram(Links, color_threshold=0.13, distance_sort='ascending')
#	Dendrogram = sch.fcluster(Links, t=3, criterion='distance')
#	Scatter = plt.scatter(Links)
#	Dendrogram = sch.fcluster(Links, t=6, criterion='distance')
#	print(Dendrogram)
#	plt.show()
#	results = [list(group) for key, group in groupby(Dendrogram['ivl'],lambda x: x in Dendrogram['ivl'])]
#	print(results)
#	return Dendrogram

"""
set_link_color_palette(["#B061FF", "#61ffff"])
D = dendrogram(Z=Z, labels=DF_dism.index, color_threshold=.7, leaf_font_size=12, leaf_rotation=45, 
               above_threshold_color="grey")
"""

def DenProcess(Dict, N):
	print("clean called ")
	Utilities.t()
	dicto = Clean(Dict)
	print("dendo called ")
	Utilities.t()
	Dendrogram = DendoPlot(dicto, N)
	print("dendo complete ")
	Utilities.t()
	print("write dendrogram file ")
	Utilities.t()
	Utilities.WriteFile(Dendrogram, "Dendrogram2" + str(M) + str(N) + "cc.txt")	
	
def Den(N, M):
	M = str(M)
	N = int(N)
	print("Den texts start ")
	Utilities.t()
	Dict = DenTexts(N, M)
	print("Den text complete ")
	Utilities.t()
	print("Den process start ")
	Utilities.t()
	DenProcess(Dict, N)
	print("Den process complete ")
	Utilities.t()
	
#def Plot(N, M):
#	M = str(M)
#	N = int(N)
#	if N == 500 and M == "Euc":
#		Dendrogram = DenEuc500
#	if N == 1000 and M == "Euc":
#		Dendrogram = DenEuc500
#	if N == 500 and M == "Bur":
#		Dendrogram = DenEuc500
#	if N == 1000 and M == "Bur":
#		Dendrogram = DenEuc500
	
if __name__ == '__main__':
	print("load files called ")
	Utilities.t()
	M = sys.argv[1]
	N = int(sys.argv[2])
#	ZScores1000 = Utilities.LoadTexts("ZScores1000.txt")
#	ZScores500 = Utilities.LoadTexts("ZScores500.txt")
#	FullData = Utilities.LoadTexts("FullData.txt")
#	Shares1000 = Utilities.LoadTexts("Shares1000.txt")
#	Shares500 = Utilities.LoadTexts("Shares500.txt")
#	CantRelate1000 = Utilities.LoadTexts("NotEnough10outof1000.txt")
#	CantRelate500 = Utilities.LoadTexts("NotEnough10outof500.txt")
#	DenBur500 = Utilities.LoadTexts("DendrogramBur1000.txt")
#	DenBur1000 = Utilities.LoadTexts("DendrogramBur500.txt")
#	DenEuc500 = Utilities.LoadTexts("DendrogramEuc1000.txt")
#	DenEuc1000 = Utilities.LoadTexts("DendrogramEuc500.txt")
#	TopN500 = Utilities.LoadTexts("Top500DeltaFeatures.txt")
#	TopN1000 = Utilities.LoadTexts("Top1000DeltaFeatures.txt")
	Den(N, M)
	#Den(1000, "Euc") #these don't work
	#Den(500, "Euc")
	#Den(1000, "Bur")
	#Den(500, "Bur")
	#Den("JW", "Bur") #these work
	#Den("JW", "Euc")
#	print("plot")
#	Utilities.t()
#	Plot(N, M)
	print("all completed ")
	Utilities.t()
	#euclidean(Shares, N, CantRelate)
