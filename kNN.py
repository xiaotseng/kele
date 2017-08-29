#coding: utf-8
from numpy import *
from os import listdir
def classify0(inX,dataSet,labels,k):
    '''输入向量与样本数组相减求距离，然后用距离排序得序号列表，取前K个成员用序号查标签，统计满足相应标签的个数，
    取个数多的返回'''
    dataSetSize=dataSet.shape[0]
    diffMat=tile(inX,(dataSetSize,1))-dataSet
    sqDiffMat=diffMat**2
    sqDistances=sqDiffMat.sum(axis=1)
    distances=sqDistances**0.5#向量差的模
    sortedDisIndicies=distances.argsort()#对向量差的模排序，得到序号数组（从小到大）
    classCount={}#空字典
    #取序号数组前k个成员查标签，并计算对应标签的个数
    for i in range(k):
        voteIlabel=labels[sortedDisIndicies[i]]#用序号查标签
        classCount[voteIlabel]=classCount.get(voteIlabel,0)+1#get获得指定键的值，如果没有值不存在返回默认值

    # 字典排序,返回组元数组，第一个参数是一个迭代器，第二个参数是
    sortedClassCount=sorted(classCount.iteritems(),key=lambda x:x[1],reverse=True)
    return sortedClassCount[0][0]#返回类型标签
def file2matrix(filename):
    fr=open(filename)#打开文件
    arrayOlines=fr.readlines()#读取所有行反回数组
    numberOfLines=len(arrayOlines)#文本的行数作为数组的行数
    returnMat=zeros((numberOfLines,3))#构建初始数组
    classLabelVector=[]#初始标签数组
    index=0
    #遍历每一行文本内容，放入数组
    for line in arrayOlines:
        line=line.strip()#去回车字符
        listFromLine=line.split('\t')#用table分割字符串
        returnMat[index,:]=listFromLine[0:3]#取前三个放入returnMat的当前行
        classLabelVector.append(int(listFromLine[-1]))#取最后个放入classLabelVector
        index +=1
    return returnMat,classLabelVector

#归一化数组的数值 :   (当前值-最小值)/(最大值-最小值)
def autoNorm(dataSet):
    minVals=dataSet.min(0)#列最大值
    maxVals=dataSet.max(0)#列最小值
    ranges=maxVals-minVals#区间大小
    normalDataSet=zeros(shape(dataSet))#初始化数组的shape
    m=dataSet.shape[0]#行数，用以确定平铺次数
    normalDataSet=dataSet-tile(minVals,(m,1))
    normalDataSet=normalDataSet/tile(ranges,(m,1))
    return normalDataSet,ranges,minVals

#分类器测试代码,计算样本的错误率
def datingClassTest():
    hoRation=0.10#取1/10的样本
    #读取文本构建样本数组和标签数组
    datingDataMat,datingLabels=file2matrix('F:\machinelearninginaction\Ch02\datingTestSet2.txt')
    normMat,ranges,minVals=autoNorm(datingDataMat)#归一化数值，并取得第一列的取值范围及最小值
    m=normMat.shape[0]#行数
    numTestVecs=int(m*hoRation)#测试个数为总个数的1/10
    errorCount=0.0#错误计数
    for i in range(numTestVecs):#对前10%的本与后90%的样本进行比对
        classifierResult=classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print "The classifier came back with: %d, the real anser is: %d" %(classifierResult,datingLabels[i])
        if (classifierResult!= datingLabels[i]):
            errorCount+=1.0
    print "The toal error rate is: %f" %(errorCount/float(numTestVecs))
def classifyPerson():#对人分类
    resultList=['not at all','in small doses','in large doses']
    percentTats=float(raw_input("percentage of time spent playing video games?"))
    ffMiles=float(raw_input("frequent flier miles earend per year?"))
    iceCream=float(raw_input("liters of ice cream consumed per year?"))
    datingDataMat,datingLabels=file2matrix("F:\machinelearninginaction\Ch02\datingTestSet2.txt")
    normMat,ranges,minVals=autoNorm(datingDataMat)
    inArr=array([ffMiles,percentTats,iceCream])
    classifierResult=classify0((inArr-minVals)/ranges,normMat,datingLabels,3)
    print "You will probably lik this person:",resultList[classifierResult-1]


#以下是手写识别代码
def img2Vector(filename):#将图形文件读取成1*1024的向量
    '''将图形文件读取成1*1024的向量'''
    returnVect=zeros((1,1024))
    fr=open(filename)
    for i in range(32):
        lineStr=fr.readline()#每一行的字符串
        for j in range(32):
            returnVect[0,i*32+j]=int(lineStr[j])
    return returnVect
def handwritingClassTest():
    trainingFileDir="F:\\machinelearninginaction\Ch02\\trainingDigits\\"
    testFileDir="F:\\machinelearninginaction\Ch02\\testDigits\\"
    hwLabels=[]
    trainingFileList=listdir(trainingFileDir)
    m=len(trainingFileList)
    trainingMat=zeros((m,1024))
    #读取生成样本和标签
    for i in range(m):
        fileNameStr=trainingFileList[i]
        fileStr=fileNameStr.split('.')[0]
        classNumStr=int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:]=img2Vector(trainingFileDir+fileNameStr)
    testFileList=listdir(testFileDir)
    mTest=len(testFileList)
    errorCount=0.0
    #读取测试
    for i in range(mTest):
        fileNameStr=testFileList[i]
        fileStr=fileNameStr.split('.')[0]
        classNumStr=int(fileStr.split('_')[0])
        vectorUnderTest=img2Vector(testFileDir+testFileList[i])
        classifierResult=classify0(vectorUnderTest,trainingMat,hwLabels,3)
        print u'分类器结果是：%d;直实结果是：%d'%(classifierResult,classNumStr)
        if (classifierResult!=classNumStr):
            errorCount+=1.0
    print u"错误数为：%d" %(errorCount)
    print u"错率为：%d" % (errorCount/float(mTest))


