import os
import ast
from ast import literal_eval
import tokenize
import string
import collections
from collections import Counter
import math
import Utilities
import time

wd = os.getcwd()
if "vernonhn" in wd:
	directory = "/mount/studenten/arbeitsdaten-studenten1/vernonhn/Thesis/Texts"
if "helenvernon" in wd:
	directory = "/Users/helenvernon/github/Thesis/Texts"

Features = {}
FullCorpus = {}
#N = 1000
N = 500
#M = 4
M = 10
TopN = []
Shares = {} #normalised author share of topN features - by user
CorpusMeanSD = {} #mean and SD of each topN feature - by word
ZScores = {} #z score of each topN feature - by user
Distances = {} #Deltas - by user
CantRelate = []
NotEnough = []

def t():
	ts = time.ctime()
	print(ts)

def LoadFiles():
	Utilites.InitialiseTexts()
#	Texts = (JW, SF, FE, IC, PH, FT)
	
	
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
		if "Shares" in str(file):
			Shares = text
			return Shares
		if "Top" in str(file):
			TopN = text
			return TopN
		else:
			file = text
			return file

#Data structure eg: {user1: {the words they use}, user2: {the different words this person uses}}

#get the top N features - most frequent in the whole data set
def Top(group, N):
	print(group)
	SortedGroup = collections.OrderedDict(sorted(group.items(), key=lambda t: t[1], reverse=True))
	print(SortedGroup)
	for S in SortedGroup:
		print(S)
		if len(TopN) <= (N - 1):	
			TopN.append(S)

	return TopN


#see what share of each authors words are made up of the n most frequent words
def FeatureShare(TopN):
	count = 1
	for Post in FullData.items():
		print("post number: " + str(count) + " of " + str(len(FullData)))
		t()
		count += 1
		Data = Post[1]
		ID = Post[0]
		AuthorData = [] #all words from one author
		for D in Data:
			if len(D) != 0: #some dict entries are empty so these are excluded
				for Dat in Data:  #post contents
					for D in Dat:
						AuthorData.append(D)
		Tokens  = len(AuthorData)	
		Features = dict.fromkeys(TopN, 0)
		Shares[ID] = Features
		for A in AuthorData:
			for F in Features.items():
				if A == F[0]:
					Features[A] += 1

		for S in Shares.items():
			if S[0] == ID:
				for F in Features.items():
					if Tokens != 0:
						Share = F[1]/Tokens*100
						Shares[ID].update({F[0]: Share})
					if Tokens == 0:
						if S[0] not in CantRelate:
							CantRelate.append(S[0])
							print(str(ID) + ": " + str(Tokens))					
	return Shares

#calculate mean and SD for each feature
def AvDev(Shares):
	Users = len(Shares)
	for N in TopN:
		CorpusMeanSD[N] = {}
	for C in CorpusMeanSD.items():
		C[1]["Av"] = 0
		C[1]["SD"] = 0
	for N in TopN:
		Av = 0
		for S in Shares.items():
			Data = S[1].items()
			for D in Data:
				if D[0] == N:
					Av += D[1]
		Av = Av/Users
		for C in CorpusMeanSD.items():
			if N == C[0]:
				C[1]["Av"] = Av
				
	for C in CorpusMeanSD.items():
		SD = 0
		for S in Shares.items():
			Data = S[1].items()
			for D in Data:
				if D[0] == C[0]:
					Diff = (D[1] - C[1]["Av"])
					SD += Diff ** 2
		SD = SD / (Users - 1)
		SD = math.sqrt(SD)
		for S in Shares.items():
			Data = S[1].items()
			for D in Data:
				if D[0] == C[0]:
					C[1]["SD"] = SD		
	return CorpusMeanSD

#get the z score for each user for each of the N words
def Z():
	for S in Shares.items():
		User = S[0]
		ZScores[User] = {}
		Data = S[1].items()
		for D in Data:
			Word = D[0]
			Share = D[1]
			for C in CorpusMeanSD.items():
				if C[0] == D[0]:
					Mean = C[1]["Av"]
					SD = C[1]["SD"]
					if SD != 0:
						Score = (Share - Mean)/SD
						ZScores[User].update({Word: Score})
					if SD == 0:
						Score = 0
						ZScores[User].update({Word: Score})
		
	
	return ZScores

#compute the delta difference for each pair of users
def Delta(ZScores):
	count = 1
	done = []
	missing = []
	incomplete = []
	for Z in ZScores.items():  # {user: {word: score, word2, score2}}
		print("post number: " + str(count) + " of " + str((len(FullData)-1)))
		t()
		count += 1
		A = Z[0] #user
		done.append(A)
		Distances[A] = {}
		for Y in ZScores.items():
			delta = 0
			B = Y[0] #users
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

def notenough(Shares):
	for S in Shares.items():
		User = S[0]
		Count = 0
		Data = S[1].items()
		for D in Data:
			Word = D[0]
			Share = D[1]
			if Share != 0:
				Count += 1
		if Count < M:
			NotEnough.append(User)
	print(NotEnough)
	print(len(NotEnough))


#a record of the top n features for my reference
def writetopnfile(N):
	with open("Top" + str(N) + "DeltaFeatures.txt", "w+") as f:
		f.write(str(TopN))
#write the distances file, which i need to upload to my next script, which will make the dendrogram.
def writedeltafile(Distances):
	with open("Distances" + str(N) + ".txt", "w+") as f:
		f.write(str(Distances))
def writesharesfiles(Shares):
	with open ("Shares" + str(N) + ".txt", "w+") as f:
		f.write(str(Shares))
def writeAvDevfiles(CorpusMeanSD):
	with open ("AvDev" + str(N) + ".txt", "w+") as f:
		f.write(str(CorpusMeanSD))
def writeZfiles(ZScores):
	with open ("ZScores" + str(N) + ".txt", "w+") as f:
		f.write(str(ZScores))
def writeCantRelatefiles(CantRelate):
	with open ("CantRelate.txt", "w+") as f:
		f.write(str(CantRelate))
def writeNotEnoughfiles(NotEnough):
	with open ("NotEnough" + str(M) + "outof" + str(N) + ".txt", "w+") as f:
		f.write(str(NotEnough))



print("load files called")
t()
FullData = LoadFullData("FullData.txt")
#FullData = LoadFullData("JW_data.txt")
FullCorpus = LoadFullData("FullData_rawfrequencies.txt")
#Shares = LoadFullData("Shares1000.txt")
Shares = LoadFullData("Shares500.txt")
#TopN = LoadFullData("Top1000DeltaFeatures3.txt")
#CorpusMeanSD  = LoadFullData("AvDev.txt")
#ZScores = LoadFullData("ZScores.txt")
print("files loaded")
t()

def processing():
	print("topN features called")
	t()
	DeltaFeatures = Top(FullCorpus, N)
	print("writing feature file")
	t()
	writetopnfile(N)
	
def shares():
	print("shares called")
	t()
	FeatureShare(TopN)
	print("write shares file called")
	t()
	writesharesfiles(Shares)
	
def otherdata():
#	print("load shares")
#	t()
#	Shares = LoadFullData("Shares4.txt")
	print("avdev called")
	t()
	AvDev(Shares)
	print("writing avdev")
	t()
	writeAvDevfiles(CorpusMeanSD)
	print("z called")
	t()
	Z()
	print("write z file")
	t()
	writeZfiles(ZScores)
#	print("write cant relate file")
#	t()
#	writeCantRelatefiles(CantRelate)

def deltadiffs():
#	print("delta called")
#	t()
#	Delta(ZScores)
#	print("write topN file called")
#	t()
#	writetopnfile(N)
#	print("write delta file called")
#	t()
#	writedeltafile(Distances)
	print("not enough called")
	t()
	notenough(Shares)
	print("write not enough called")
	t()
	writeNotEnoughfiles(NotEnough)
	print("finished")
	t()
	
#processing()
#shares()
#otherdata()
deltadiffs()


	
			

