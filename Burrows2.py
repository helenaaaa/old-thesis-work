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

#directory = "/mount/studenten/arbeitsdaten-studenten1/vernonhn/Thesis/Texts"
directory = "/Users/helenvernon/github/Thesis/Texts"
#directory = "/home/guest173/Helen/git/Thesis/Thesis/Texts"
os.chdir(directory)

Features = {}
FullCorpus = []
#N = 1000
#N = 500
N = 10
TopN = []
Shares = {} #normalised author share of topN features - by user
CorpusMeans = {} #mean and SD of each topN feature - by word
CorpusSDs = {}
ZScores = {} #z score of each topN feature - by user
Distances = {} #Deltas - by user

def LoadFullData(file):
	file = file
	os.chdir(directory)
	with open(file) as F:
		text = ast.literal_eval(F.read())
		if "FullData" in str(file):
			FullData = text
			return FullData
		if "raw" in str(file):
			FullCorpus = text
			return FullCorpus
		if "JW" in str(file): #smaller corpus for development
			FullData = text
			return FullData
		
"""
Data structure eg: {user1: {the words they use}, user2: {the different words this person uses}}

"""

#get the top N features - most frequent in the whole data set
def Top(group, N):
	SortedGroup = collections.OrderedDict(sorted(group.items(), key=lambda t: t[1], reverse=True))
	for S in SortedGroup:
		if len(TopN) <= (N - 1):	
			TopN.append(S)
			
	return TopN



#see what share of each authors words are made up of the n most frequent words
def FeatureShare(TopN, FullData):
	global Shares
	for Post in FullData.items():
		Data = Post[1]
		for D in Data:
			if len(D) != 0: #some dict entries are empty so these are excluded
				ID = Post[0]
				Shares[ID] = {}
				AuthorData = [] #all words from one author
				Types = [] #types from one author
				for Dat in Data:  #post contents
					for D in Dat:
						AuthorData.append(D)
				Tokens  = len(AuthorData)	
				Types = set(AuthorData)
				Types = dict.fromkeys(Types, 0)
				for A in AuthorData:
					if A in TopN:	#only do it for the topn features, not everything
						for T in Types.items():
							if A == T[0]:
								Types[T[0]] += 1
							for N in TopN:
								if N == T[0]:
									Share = T[1]/Tokens*100
									Shares[ID].update({T[0]: Share})
								if N not in Types:
									Shares[ID].update({N: 0})
	Shares = pd.DataFrame(data=Shares)
	return Shares

#calculate mean and SD for each feature
def AvDev(Shares):
	print(Shares)
	print(Shares.dtypes)
#	Shares = Shares[0:-1],[1:]
#	print(Shares)
	global CorpusMeans
	global CorpusSDs
#	Users = (len(Shares) - 2)
#	for F in range(len(Shares)): #words/features
#		print(Shares.loc[F,])
"""
		CorpusMeans[S] = {}
		CorpusSDs[S] = {}
	for C in CorpusMeans.items(): #words/features
		C[1] = 0
	for C in CorpusSDs.items(): #words/features
		C[1] = 0
	for F in Shares.iterrows(): #words/features
		Av = Shares.mean(F)
		SD = Shares.std(F)
		for C in CorpusMeans.items():
			if F == C[0]:
				C[1] = Av
		for C in CorpusSDs.items(): #words/features
			if F == C[0]:
				C[1] = SD

	CorpusMeans = pd.DataFrame(data=CorpusMeans)
	CorpusMeans = pd.DataFrame(data=CorpusSDs)
	return CorpusMeans
	return CorpusSDs
"""
#get the z score for each user for each of the N words
def Z():
	Users = list(Shares)
	for U in Users:
		for F in Shares.iterrows(): #words/features
			for M in CorpusMeans.iterrows():  #words/features
				Mean = M
				print(M)
			for S in CorpusSDs.iterrows():  #words/features
				SD = S
				print(S)
				
"""
		for D in Data:
			Word = D[0]
			Share = D[1]
			for C in CorpusMeanSD.items():
				if C[0] == D[0]:
					Mean = C[1]["Av"]
					SD = C[1]["SD"]
					Score = (Share - Mean)/SD
					ZScores[User].update({Word: Score})
"""
	
#	return ZScores
#compute the delta difference for each pair of users
def Delta():
	done = []
	for Z in ZScores.items():
		A = Z[0]
		done.append(A)
		Distances[A] = {}
		for Y in ZScores.items():
			delta = 0
			B = Y[0]
			if B not in done:
				Distances[A].update({B: 0})
				for T in TopN:
					AZ = ZScores[A][T]
					BZ = ZScores[B][T]
					delta += math.fabs((AZ - BZ))
			delta /= N
			if B not in done:
				Distances[A][B] = delta
	
	return Distances
#a record of the top n features for my reference
def writetopnfile(N):
	with open("Top" + str(N) + "DeltaFeatures.txt", "w+") as f:
		f.write(str(DeltaFeatures))
	with open("TopNCheck.txt", "w+") as F:
		F.write(str(TopN))
#write the distances file, which i need to upload to my next script, which will make the dendrogram.
def writedeltafile(Distances):
	with open("Distances" + str(N) + ".txt", "w+") as f:
		f.write(str(Distances))
		
def writeshares():
	with open("Shares.txt", "w+") as f:
		f.write(str(Shares))

def prepareshares():
	FullData = LoadFullData("FullData.txt")
	#FullData = LoadFullData("JW_data.txt")
	FullCorpus = LoadFullData("FullData_rawfrequencies.txt")
	DeltaFeatures = Top(FullCorpus, N)
	FeatureShare(TopN, FullData)
	writeshares()
	
#prepareshares()

Shares = pd.read_csv("Shares.txt", sep='\t')#, index_col=0)
AvDev(Shares)
#Z()
#print(Z())
#Delta()
#writetopnfile(N)
#writedeltafile(Distances)
#writeshares()
