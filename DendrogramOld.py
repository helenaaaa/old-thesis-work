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
sys.setrecursionlimit(100000)
EucDict = {}
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
	Utilities.WriteFile(EucDict, "EucDistances2" + str(N) + ".txt")
	print("write file completed")
	Utilities.t()
	return EucDict
#####################################################################
def DenTexts(N, M):
	if N == 500:
		CantRelate = Utilities.LoadTexts("NotEnough10outof500.txt")
	if M == "Euc" and N == 500:
		print("Euclidean500")
		Utilities.t()
	#	Dict = euclidean(Shares500, N, CantRelate)
		Dict = (Utilities.LoadTexts("EucDistances2500.txt"))
	if M == "Bur" and N == 500:
		print("Burrows500")
		Utilities.t()
		Dict = Utilities.LoadTexts("BurDistances2500.txt")
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
		Dict = Utilities.LoadTexts("BurDistances21000.txt")
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
	sorted_keys, distances = zip(*sorted(zip(keys, values)))
	Links = linkage(distances, 'single')
	labels = sorted(set([key[0] for key in sorted_keys] + [sorted_keys[-1][-1]]))
	Dendrogram = dendrogram(Links, labels=labels, leaf_rotation=45)
	print("plot")
	Utilities.t()
	plt.show()
	return Dendrogram

def DenProcess(Dict, N):
	print("clean called")
	Utilities.t()
	dicto = Clean(Dict)
	print("dendo called")
	Utilities.t()
	Dendrogram = DendoPlot(dicto, N)
	print("dendo complete")
	Utilities.t()
	print("write dendrogram file")
	Utilities.WriteFile(Dendrogram, "Dendrogram" + str(M) + str(N) + "cc.txt")
	Utilities.t()
	
	
def Den(N, M):
	M = str(M)
	N = int(N)
	print("Den texts start")
	Utilities.t()
	Dict = DenTexts(N, M)
	print("Den text complete")
	Utilities.t()
	print("Den process start")
	Utilities.t()
	DenProcess(Dict, N)
	print("Den process complete")
	Utilities.t()
	
def Plot(N, M):
	M = str(M)
	N = int(N)
	if N == 500 and M == "Euc":
		Dendrogram = DenEuc500
	if N == 1000 and M == "Euc":
		Dendrogram = DenEuc500
	if N == 500 and M == "Bur":
		Dendrogram = DenEuc500
	if N == 1000 and M == "Bur":
		Dendrogram = DenEuc500
		
	plt.show()
	
if __name__ == '__main__':
	print("load files called")
	Utilities.t()
	M = sys.argv[1]
	N = int(sys.argv[2])
#	Shares1000 = Utilities.LoadTexts("Shares1000.txt")
#	Shares500 = Utilities.LoadTexts("Shares500.txt")
#	CantRelate1000 = Utilities.LoadTexts("NotEnough10outof1000.txt")
#	CantRelate500 = Utilities.LoadTexts("NotEnough10outof500.txt")
	DenBur500 = Utilities.LoadTexts("DendrogramBur1000.txt")
	DenBur1000 = Utilities.LoadTexts("DendrogramBur500.txt")
	DenEuc500 = Utilities.LoadTexts("DendrogramEuc1000.txt")
	DenEuc1000 = Utilities.LoadTexts("DendrogramEuc500.txt")
	print("files loaded")
	Utilities.t()
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
	print("all completed")
	Utilities.t()
	#euclidean(Shares, N, CantRelate)

################################################################################################################
"""
  
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
Eucdict = {}
Dict = {}
def euclidean(Shares, N):
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
				print(Combo)
				Distance = ssd.euclidean(A, B)	
				print(Distance)
				EucDict[User][Candidate] = Distance
#	Utilities.WriteFile(EucDict, "JWEucDistances.txt")
	Utilities.WriteFile(EucDict, "EucDistances" + str(N) + ".txt")
	return EucDict
"""
"""
def Clean(file, CantRelate):
	dicto = {}
	for D in file.items(): 
		User = D[0]
		if User not in CantRelate:
			Data = D[1].items()
			if len(Data) != 0:
				for A in Data:
					Candidate = A[0]
					Score = A[1]
					if Candidate not in CantRelate:
						if Score !=0:
							Key = (User, Candidate)
							dicto[Key] = Score
	return dicto
"""	
"""
def DendoPlot(Data, N):
	keys = [sorted(k) for k in Data.keys()]
	values = Data.values()
	sorted_keys, distances = zip(*sorted(zip(keys, values)))
	Links = linkage(distances, 'single')
	labels = sorted(set([key[0] for key in sorted_keys] + [sorted_keys[-1][-1]]))
	Dendrogram = dendrogram(Links, labels=labels)
	plt.show()
	return Dendrogram
def Den(N, M):
	print("start")
	Utilities.t()
	if N == 500:
		CantRelate = Utilities.LoadTexts("NotEnough10outof500.txt")
	if M == "Euc" and N == 500:
		print("Euclidean500")
		Utilities.t()
	#	Dict = euclidean(Shares500, N)
		Dict = Utilities.LoadTexts("EucDistances500.txt")
	if M == "Bur" and N == 500:
		print("Burrows500")
		Utilities.t()
		Dict = Utilities.LoadTexts("BurDistances500.txt")
	if N == 1000:
		CantRelate = Utilities.LoadTexts("NotEnough10outof1000.txt")
	if M == "Euc" and N == 1000:
		print("Euclidean1000")
		Utilities.t()
	#	Dict = euclidean(Shares1000, N)
		Dict = Utilities.LoadTexts("EucDistances1000.txt")
	if M == "Bur" and N == 1000:
		print("Burrows1000")
		Utilities.t()
		Dict = Utilities.LoadTexts("BurDistances1000.txt")
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
	print("data loaded")
	Utilities.t()
	print("clean called")
	Utilities.t()
	Dict = Clean(Dict, CantRelate)
	print("dendo called")
	Utilities.t()
	Dendrogram = DendoPlot(Dict, N)
	print("dendo complete")
	Utilities.t()
	print("write dendrogram file")
	Utilities.WriteFile(Dendrogram, "Dendrogram" + str(M) + str(N))
	Utilities.t()
	
def test(N, M):
	print("load data")
	Utilities.t()
	dicto = {}
	if N == 500:
		CantRelate = Utilities.LoadTexts("NotEnough10outof500.txt")
		Shares = Utilities.LoadTexts("Shares500.txt")
	if N == 1000:
		CantRelate = Utilities.LoadTexts("NotEnough10outof1000.txt")
		Shares = Utilities.LoadTexts("Shares1000.txt")
#	if M == "Bur":
#		Distance = Burrows()
	if M == "Euc":
		Distance = 'euclidean'
	print("data loaded")
	Utilities.t()
	
	print("cleaning started")
	Utilities.t()
	for S in Shares.items():
		User = S[0]
		Features = S[1].items()
		Counts = []
		for F in Features:
			Word = F[0]
			Count = F[1]
			Counts.append(Count)
		if User not in CantRelate:
			dicto.update({User: Counts})
	print("cleaning complete")
	Utilities.t()
	
	print("dendrogram started")
	Utilities.t()
	NoOfUsers = len(dicto)
	keys = dicto.keys()
	values = dicto.values()
#	distances = zip(keys, values)
	values = np.array(values)
	values = ssd.squareform(values)
	for v in values:
		print(v)
#	values = values.reshape((1000, NoOfUsers))   
#	distances = ssd.pdist(values, Distance)
	print(values[0])
	print("dendrogram complete")
	Utilities.t()
		
		
		
#Den(1000, "Bur")
"""
"""
try: Den(1000, "Euc")
except: pass
try: Den(500, "Euc")
except: pass
try: Den(1000, "Bur")
except: pass
try: Den(500, "Bur")
except: pass
try: Den("JW", "Bur")
except: pass
try Den("JW", "Euc")
except: pass
"""
"""
print("start")
Utilities.t()
test(1000, "Euc")
print("all completed")
Utilities.t()
"""	
"""
def JW(file):
	JWDict = {}
	Shares = Utilities.LoadTexts(file)
	for S in Shares.items():
		if "JW" in S[0]:
			Name = S[0]
			Post = S[1]
			if len(Post) != 0:
				JWDict[Name] = Post
	Utilities.WriteFile(JWDict, "SharesJW1000.txt")
	
#print("small set")
#Utilities.t()
#SmallSet = JW("Shares1000.txt")
"""

"""
print("load files called")
Utilities.t()
#Shares = Utilities.LoadTexts("SharesJW1000.txt")
#Shares1000 = Utilities.LoadTexts("Shares1000.txt")
#Shares500 = Utilities.LoadTexts("Shares500.txt")
#CantRelate1000 = Utilities.LoadTexts("NotEnough10outof1000.txt")
#CantRelate500 = Utilities.LoadTexts("NotEnough10outof500.txt")
#BurDistances1000 = Utilities.LoadTexts("BurDistances1000.txt")
#BurDistances500 = Utilities.LoadTexts("BurDistances500.txt")
#BurDistancesJW = Utilities.LoadTexts("JWEucDistances.txt")
print("files loaded")
Utilities.t()
"""
