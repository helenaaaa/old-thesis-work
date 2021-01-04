# -*- coding: utf-8 -*-
import os
import ast
from ast import literal_eval
import tokenize
import string

directory = "/mount/studenten/arbeitsdaten-studenten1/vernonhn/Thesis/Texts"
#directory = "/Users/helenvernon/github/Thesis/Texts/"

JW = []
JWNames = []
JWList = []
JWPseudoNames = []
JWDict = {}

def LoadTexts():
	os.chdir(directory)
	with open("JW_Final_Text.txt") as f:
		text = f.read()
		tuples = ast.literal_eval(text)
	tuples = [t for sublist in tuples for t in sublist]
	for t in tuples:
		if t[0] not in JWNames:
			JWNames.append(t[0])
		if t not in JW:
			JW.append(t)
			
def Pseudonames():
	CountJW = 1
	for N in JWNames:
		PseudoName = "JWUser" + str(CountJW)
		JWPseudoNames.append(PseudoName)
		CountJW += 1
		


def NameReplace():
	Replacements = list(zip(JWNames,JWPseudoNames))
	for J in JW:
		for R in Replacements:
			if J[0] == R[0]:
				NewPair = []
				NewPair.append(R[1])
				NewPair.append(J[1])
				JWList.append(NewPair)
	return JWList
			
def Preprocess(JWList):
	for JWL in JWList:       
		for JW in JWL:
			if type(JW) == list:
				Deleted = []
				Deleted.append(JW)
				JWL.remove(JW)
				for D in Deleted:
					if len(D) > 0:
						NewPair = []
						NewPair.append(D[0])
						NewPair.append(D[1])
						JWList.append(NewPair)
	return JWList

def DeList(JWList):
	for JWL in JWList:
		for JWs in JWL:  #JWL is a list of len 2 containing the tuple, the next level should be string
			if type(JWs) == list and len(JWs) == 2: 
				NewPairs = []
				NewPairs.append(JWs)
				JWL.remove(JWs)
				NewPairs = [N for sublist in NewPairs for N in sublist]
				JWList.append(NewPairs)
			if type(JWs) == list and len(JWs) != 2:
				JWL.remove(JWs)
				JWs = [N for sublist in JWs for N in sublist]
				JWList.append(JWs)
				if type(JWs) == list and len(JWs) == 2:
					NewPairs = []
					NewPairs.append(JWs)
					JWL.remove(JWs)
					NewPairs = [N for sublist in NewPairs for N in sublist]
					JWList.append(NewPairs)
			
	return JWList
				
def Tokenize(JWList):
	for JWL in JWList:  #JWL is a list of len 2 containing the tuple, the next level are strings of names and content
		if len(JWL) !=2:
			JWList.remove(JWL)
		exclude = set(string.punctuation)
		JWL[1] = str(JWL[1])
		JWL[1] = JWL[1].split("..")
		JWL[1] = "".join(JWL[1])
		JWL[1] = ''.join(J for J in JWL[1] if J not in exclude)
		JWL[1] = JWL[1].lower()
		JWL[1] = JWL[1].split()	
	
	return JWList
	
def BuildDict(JWList):
	for JW in JWList:
		if JW[0] not in JWDict:
			JWDict[JW[0]] = []
		for U in JWDict:
			if U == JW[0]:
				JWDict[U].append(JW[1])
	return JWDict

def WriteFile(JWDict):
	with open("JW_data.txt",'w+') as datafile:
		datafile.write(str(JWDict))

LoadTexts()
Pseudonames()
JWList.append(NameReplace())
DeList(JWList)
Tokenize(JWList)
BuildDict(JWList)
WriteFile(JWDict)
