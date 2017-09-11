#coding:utf-8
from numpy import *
'''贝叶斯'''
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

def setOfWord2Vec(vocabList,inputSet):#给定词汇表和单词数组，求单词数组的词条向量
    returnVec=[0]*len(vocabList)#向量维度等于记录里的单词数量
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]+=1
        else:print 'the word: %s is not in my Vocabulary!'%word
    return returnVec
'''核心公式P(c|w)=(P(w|c)*P(c))/P(w)'''
def trainNB0(trainMatrix,trainCategory):
    #训练算法
    #一个文档矩阵(词条向量)，一个分类列表
    numTrainDocs=len(trainMatrix)#矩阵行数
    numWords=len(trainMatrix[0])#矩阵列数
    pAbusive=sum(trainCategory)/float(numTrainDocs)#属于侮辱文档的总概率
    p0Num=ones(numWords);p1Num=ones(numWords)#分别统计各关键词在两个类别(条件)中的概率
    for i in range(numTrainDocs):
        #计算：P(w|c)
        #词条矩阵每一行
        if trainCategory[i]==1:#条件1：
            # 如果带有侮辱性
            p1Num+=trainMatrix[i]#向量相加各维度各自相加
        else:#条件0：
            p0Num+=trainMatrix[i]
    # 两者相除得出各关键词在以上两条件下的概率
    p1Vect=log(p1Num/sum(p1Num))#概率向量
    p0Vect=log(p0Num/sum(p0Num))
    return p0Vect,p1Vect,pAbusive#三个关键概率

def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
    p1=sum(vec2Classify*p1Vec)+log(pClass1)
    p0=sum(vec2Classify*p0Vec)+log(1-pClass1)
    if p1>p0:
        return 1
    else:
        return 0
def testingNB():
    listOPosts,listClasses=loadDataSet()
    myVocabList=createVocabList(listOPosts)
    trainMat=[]
    for postinDoc in listOPosts:
        trainMat.append(setOfWord2Vec(myVocabList,postinDoc))
    print trainMat
    p0V,p1V,pAb=trainNB0(trainMat,listClasses)
    testEntry=['love','my','dalmation']
    thisDoc=array(setOfWord2Vec(myVocabList,testEntry))
    print testEntry,'classified as:',classifyNB(thisDoc,p0V,p1V,pAb)
    testEntry=['stupid','garbage']
    thisDoc=array(setOfWord2Vec(myVocabList,testEntry))
    print testEntry,'classified as:',classifyNB(thisDoc,p0V,p1V,pAb)

def textParse(bigString):#解析文本到数组
    import re
    listOfTokens=re.split(r'\w*',bigString)
    return [tok.lower() for tok in listOfTokens if len(tok)>2]
def spamTest():
    import random
    docList=[];classList=[];fullText=[]
    for i in range(1,26):
        wordList=textParse(open('email/spam/%d.txt'%i).read())#读取整个文件
        docList.append(wordList)#二维
        fullText.extend(wordList)#一维
        classList.append(1)
        wordList=textParse(open('email/ham/%d.txt'%i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList=createVocabList(docList)#得到词汇列表
    trainingSet=range(50);testSet=[]
    #随机取10个样本序号分配到testSet作测试数据，剩下的40个作样本
    for i in range(10):
        randIndex=int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])

    #初始化训练矩阵和类别
    trainMat=[];trainClasses=[]
    for docIndex in trainingSet:
        trainMat.append(setOfWord2Vec(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])
    #计算概率量
    p0V,p1V,pSpam=trainNB0(trainMat,trainClasses)
    errorCount=0
    for docIndex in testSet:
        wordVector=setOfWord2Vec(vocabList,docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam)!=classList[docIndex]:
            errorCount+=1
    print 'the error rate is: ',float(errorCount)/len(testSet)

def calcMostFreq(vocabList,fullText):#计算高频单词
    freqDict={}
    for token in vocabList:
        freqDict[token]=fullText.count(token)
    sortedFreq=sorted(freqDict.iteritems(),key=lambda x :x[1],reverse=True)#排序
    return sortedFreq[:30]#出现次数排前30的单词

def localWords(feed1,feed0):
    import feedparser
    docList=[];classList=[];fullText=[]
    minLen=min(len(feed1['entries']),len(feed0['entries']))
    for i in range(minLen):
        wordList=textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList=textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
    vocabList=createVocabList(docList)
    top30Word=calcMostFreq(vocabList,fullText)
    for word in top30Word:
        if word[0] in vocabList:
            vocabList.remove(word[0])


    trainSet=range(2*minLen);testSet=[]
    #数组一分为二，部分训练，部分测试
    #随机取20个数放到testSet
    for i in range(20):
        randIndex=int(random.uniform(0,len(trainSet)))
        testSet.append(randIndex)
        del(trainSet[randIndex])

    #取得训练矩阵和训练类别
    trainMat=[];trainClasses=[]
    for docIndex in trainSet:
        trainMat.append(setOfWord2Vec(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])

    #计算样本概率
    p0V,p1V,pSpam=trainNB0(trainMat,trainClasses)

    #测试错误率
    errorCount=0
    for docIndex in testSet:
        wordVector=setOfWord2Vec(vocabList,docList[docIndex])
        if classifyNB(wordVector,p0V,p1V,pSpam)!=classList[docIndex]:
            errorCount+=1
    print 'the error rate is: ',float(errorCount)/len(testSet)
    return vocabList,p0V,p1V








