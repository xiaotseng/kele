#coding:utf-8
import matplotlib.pyplot as plt

#定义组件的格式
decisionNode=dict(boxstyle="sawtooth",fc='0.8')#决策节点
leafNode=dict(boxstyle="round4",fc="0.8")#叶子节点
arrow_args=dict(arrowstyle='<-')#连接箭头


def plotNode(nodeTxt, centerPt, parentPt, nodeType):#画一个节点，包括文本，边框，父节点到本身的箭头。
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction', xytext=centerPt,
                            textcoords='axes fraction',
                            va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)



def getUumLeafs(myTree):
    numLeafs=0
    firstStr=myTree.keys()[0]#键
    secondDict=myTree[firstStr]#下级字典
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            numLeafs+=getUumLeafs(secondDict[key])
        else:
            numLeafs+=1
    return numLeafs


def getTreeDepth(myTree, currentDepth=0):#计算树的深度
    currentDepth+=1#当前深度
    maxDepth = currentDepth # 临时最大深度，用来与遍历里面的进行比较

    firstStr=myTree.keys()[0]
    secondDict=myTree[firstStr]#下一级字典，不是当前字典

    for key in secondDict:
        if type(secondDict[key]).__name__=='dict':
            thisDepth=getTreeDepth(secondDict[key], currentDepth)
            maxDepth=max(maxDepth,thisDepth)
    #遍历完了才能返回各分枝中最大的值
    return maxDepth

def retrieveTree(i):#生成测试字典树
    listOfTrees=[{'no surfacing':{0:'no',1:{'flippers':{0:'no',1:'yes'}}}},
                 {'no surfacing':{0:'no',1:{'flippers':{0:{'head':{0:'no',1:'yes'}},1:'no'}}}}
                 ]
    return listOfTrees[i]

def plotMidText(cntrPt,parentPt,txtString):
    #计算线段的中点
    xMid=(parentPt[0]-cntrPt[0])/2+cntrPt[0]
    yMid=(parentPt[1]-cntrPt[1])/2+cntrPt[1]
    createPlot.ax1.text(xMid,yMid,txtString,va='center',ha='center',rotation=30)

#画树枝，myTree为一个树的节点，parentPt为父节点位置，nodeTxt为本节点上父节点中间的文字
def plotTree(myTree,paretntPt,nodeTxt):
    numLeafs=getUumLeafs(myTree)
    depth=getTreeDepth(myTree,0)
    firstStr=myTree.keys()[0]#得到键名
    cntrPt=(plotTree.xOff+(1.0+float(numLeafs))/2.0/plotTree.totalW,plotTree.yOff)
    plotMidText(cntrPt,paretntPt,nodeTxt)#画文字
    plotNode(firstStr,cntrPt,paretntPt,decisionNode)
    secondDict=myTree[firstStr]
    plotTree.yOff-=1.0/plotTree.totalD#竖向偏移
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            plotTree(secondDict[key],cntrPt,str(key))
        else:
            plotTree.xOff=plotTree.xOff+1.0/plotTree.totalW#水平位置偏移
            plotNode(secondDict[key],(plotTree.xOff,plotTree.yOff),cntrPt,leafNode)
            plotMidText((plotTree.xOff,plotTree.yOff),cntrPt,str(key))
    plotTree.yOff+=1.0/plotTree.totalD


def createPlot(inTree):
    fig=plt.figure(1,facecolor='white')
    fig.clf()
    axprops=dict(xticks=[],yticks=[])
    createPlot.ax1=plt.subplot(111,frameon=False,**axprops)
    plotTree.totalW=float(getUumLeafs(inTree))
    plotTree.totalD=float(getTreeDepth(inTree,0))
    plotTree.xOff=-0.5/plotTree.totalW;plotTree.yOff=1.0
    plotTree(inTree,(0.5,1.0),'')
    plt.show()





