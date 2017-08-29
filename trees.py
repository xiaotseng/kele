#coding:utf-8
#
from math import log
def calcShannonEnt(dataSet):#求熵
    numEntries=len(dataSet)#样本数
    labelCounts={}#空字典
    for dataLine in dataSet:#遍历每行数据
        labelKey=dataLine[-1]#得到键值
        labelCounts[labelKey]=labelCounts.get(labelKey,0)+1

    shannonEnt=0.0#熵
    for key in labelCounts:
        prob=float(labelCounts[key])/numEntries#概率
        shannonEnt-=prob*log(prob,2)
    return shannonEnt
def creatDataSet():
    dataSet=[[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
    labels=['no surfacing','flippers']
    return dataSet,labels
def splitDataSet(dataSet,axis,value):#切割数组
    retDataSet=[]
    for featVec in dataSet:
        if featVec[axis]==value:
            reducedFeatVec=featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet
def chooseBestFeatureToSplit(dataSet):
    #选择最好的特征
    #多种切割得到信息增益最大的特征
    numFeatures=len(dataSet[0])-1#数组的特征数量
    baseEntropy=calcShannonEnt(dataSet)#数组的原始熵，用于与划分后的数据集的熵进行比较
    bestInfoGain=0.0;bestFeature=-1
    for i in range(numFeatures):#遍历所以特征，比较哪一特征的信息增益大
        featList=[example[i] for example in dataSet]#得到前前列的值
        uniqueVals=set(featList)#排序并消重量
        newEntropy=0.0
        for value in uniqueVals:#遍历当前特征的所以值
            subDataSet=splitDataSet(dataSet,i,value)
            prob=len(subDataSet)/float(len(dataSet))
            newEntropy+=prob*calcShannonEnt(subDataSet)
        infoGain=baseEntropy-newEntropy
        if (infoGain>bestInfoGain):
            bestInfoGain=infoGain
            bestFeature=i
    return  bestFeature
def majorityCnt(classList):#统计各类别出现的次数，返回次数最多的类别
    classCount={}
    for vote in classList:
        if vote not in classCount.keys():classCount[vote]=0
        classCount[vote]+=1
    sortedClassCount=sorted(classCount.iteritems(),key=lambda x:x[1],reverse=True)
    return sortedClassCount
def creatTree(dataSet,labels):
    #构建决策树
    #递归过程中dataSet和labels会不段缩小

    # 两种情况直接返回值否则递归
    classList=[example[-1] for example in dataSet]#从数据表中得到类别列表
    if classList.count(classList[0])==len(classList):#类别列表里面全部值相同时
        return classList[0]
    if len(dataSet[0])==1:#所以特征遍历完成
        return majorityCnt(classList)

    #准备下一次递归
    bestFeat=chooseBestFeatureToSplit(dataSet)#获得增益最大的特征列
    bestFeatLabel=labels[bestFeat]#当前特征名，在字典里作键名用
    myTree={ bestFeatLabel:{}}
    '''每一次迭代生成一个字典，类型标签作键，下次的迭代的字典插入到值里面'''
    del(labels[bestFeat])#移除最大增益的标签，递归一次少一个特征标签
    featValues=[example[bestFeat] for example in dataSet]#得到最大增益列的所有特征值
    uniqueVals=set(featValues)#唯一值
    for value in uniqueVals:#遍历当前特征下的所有值，用它切割数据后递归结果
        subLabels=labels[:]#复制一份用于下一次递归
        # splitDataSet把与当前特征值相关的数据取出来 ，并当前特征去掉传到一下调用函数
        #将递归结果添加到字典
        myTree[bestFeatLabel][value]=creatTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree

def classify(inputTree,featLabels,testVec):#数据与决策树比对，得出分类结果
    firstStr=inputTree.keys()[0]
    secondDict=inputTree[firstStr]
    featID=featLabels.index(firstStr)
    classLabel=''
    for key in secondDict.keys():
        if key==featLabels[featID]:#特征相等有两种可能(叶子和树枝),得到结果和下一特征对比
            if type(secondDict[key]).__name__=='dict':
                classLabel=classify(secondDict[key],featLabels,testVec)
            else:
                classLabel=secondDict[key]
    return classLabel
def storeTree(inputTree,filename):#序列化保存决策树
    import pickle
    fw=open(filename,'w')
    pickle.dump(inputTree,fw)
    fw.close()
def grabTree(filename):#读取序列化数据
    import pickle
    fr=open(filename)
    return pickle.load(fr)

