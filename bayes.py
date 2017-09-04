#coding:utf-8
from numpy import *

def loadDataSet():
    #记录
    postingList=[['my','dog','has','flea','problems','help','please'],
                 ['maybe','not','take','him','to','dog','park','stupid'],
                 ['my','dalmation','is','so','cute','I','love','him'],
                 ['stop','posting','stupid','worthless','garbage'],
                 ['mr','licks','ate','my','steak','how','to','stop','him'],
                 ['quit','buying','worthless','dog','food','stupid']
                 ]
    classVec=[0,1,0,1,0,1]
    return postingList,classVec
def createVocabList(dataSet):
    #得到不重复的单词列表
    #生词
    vocabSet=set([])
    for document in dataSet:
        vocabSet=vocabSet|set(document)
    return list(vocabSet)

def setOfWord2Vec(vocabList,inputSet):
    returnVec=[0]*len(vocabList)#向量维度等于记录里的单词数量
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]=1
        else:print 'the word: %s is not in my Vocabulary!'%word
    return returnVec

def trainNB0(trainMatrix,trainCategory):
    numTrainDocs=len(trainMatrix)#矩阵行数
    numWords=len(trainMatrix[0])#矩阵列数
    pAbusive=sum(trainCategory)/float(numTrainDocs)
