#coding: utf-8
from numpy import *
from math import log

student=dtype({'names':['name','age','weight'],'formats':['S32','i','f']},align=True)
a=array([('Zhang',32,65.5),('Wang',24,55.2)],dtype=student)
#print a

def calcShannonEntropy(dataSet):
    labelList=[dataLine[-1] for dataLine in dataSet]
    numData=len(dataSet)
    labelCount={}
    reEntropy=0.0
    for Label in labelList:
        labelCount[Label]=labelCount.get(Label,0)+1
    for key in labelCount:
        prod=float(labelCount[key])/float(numData)
        reEntropy -= prod*log(prod,2)
    return reEntropy
def creatDataSet():
    dataSet=[[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
    labels=['no surfacing','flippers']
    return dataSet,labels

def test():
    test.a=1

def test2():
    print test.a