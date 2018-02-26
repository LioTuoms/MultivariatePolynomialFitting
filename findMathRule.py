#coding=utf-8

import csv
import numpy as np

global sMsg

sMsg = ['0%']
dicWsData = {}
dicDelIndex = {}

def loadCsvData(fileName):
    fr = open(fileName,'r')
    fr_read = csv.reader(fr)
    data = []
    for row in fr_read:
        data.append(list(map(float,row)))
    data = np.asarray(data,'f')
    fr.close()
    return data

def preDealData(inputData,Powers = (-1,3)):
    temp = list(range(Powers[0],Powers[1]+1))
    for i in range(Powers[0],Powers[1]+1):
        '''(temp[i] < 1/3 and temp[i+1] > 1/3):
            temp.insert(i+1,1/3)
            i+=1
        elif'''
        if (temp[i] < 0.5 and temp[i+1] > 0.5):
            temp.insert(i+1,0.5)
            i += 1
    #print('temp:',temp)
    listPower = np.asarray(temp)
    dicPowerData = {}
    num = listPower.shape[0]
    listPower = listPower.reshape((1,num))
    inputData = np.mat(inputData)
    dataShape = inputData.shape
    inputData = np.asarray(inputData,'f')
    for i in range(dataShape[0]):
        for j in range(dataShape[1]-1):
            skeys = (i,j)
            data = np.asarray(np.ones((1,num)))
            data[0] = inputData[i,j]
            if inputData[i,j] == 0:
                dicPowerData[skeys] = data[0]
                continue
            data[0] = data[0] ** listPower
            dicPowerData[skeys] = data
    return dicPowerData,dataShape,num

def calMouldData(dicPowerData,dataShape,num,polynomiaNum = 2):
    m,n = dataShape
    trainingData = np.mat(np.ones((m,num**polynomiaNum)))
    for i in range(m):
        m1 = np.mat(dicPowerData[(i,0)])
        for j in range(1,polynomiaNum):
            m1 = m1.T
            mData = np.mat(dicPowerData[(i,j)])
            #WriteData('mData:',mData)
            m1 = m1 * mData
            m1 = m1.reshape((1,num**(j+1)))
            #WriteData('m1Reshape:',m1)
        trainingData[i] = m1[0]
        #print('m1.shape:',m1.shape[0],' ',m1.shape[1])
        #WriteData(np.str(np.ones((1,100))))
    return trainingData

def varError(yTest,yLabel):
    error = (np.square(yTest - yLabel)).sum()
    #print('error:',error)
    return error
    

def getWs(trainingData,trainingLabel,numV = 30):
    ws = np.mat(np.ones((numV,np.shape(trainingData)[1])))
    for i in range(numV):
        xTx = trainingData.T.dot(trainingData)
        xTx = xTx + np.eye(np.shape(trainingData)[1])*np.exp(i - 20) #8,14
        #sTemp = np.linalg.det(xTx)
        if np.linalg.det(xTx) is np.nan or np.linalg.det(xTx) is np.inf or np.linalg.det(xTx) == 0.0:
            np.delete(ws,i,0)
            i = i - 1
            numV = numV - 1
            continue
        temp = np.linalg.inv(xTx).dot(trainingData.T).dot(trainingLabel)
        ws[i] = temp.T
        #print(np.linalg.inv(xTx)*xTx)
    #print('ws:',ws)
    return ws

def findMultyPolyFittingByL2(inputData,numVal = 30,Powers = (-1,3)):
    dicData,inputDataShape,num = preDealData(inputData, Powers)
    inputData = np.mat(inputData)
    m,n = inputDataShape
    lam = 8.0e-28
    indexList = list(range(m))    
    #只计算一元
    for i in range(0,n-1):
        trainingData = calMouldData(dicData, inputDataShape, num,i+1)
        delList = []
        minMean = np.Inf
        delCount = 1        
        errorMat = np.mat(np.zeros((numVal,numVal)))
        delIndex = num**(i+1)
        iCycle = int(delIndex/2)
        #iCycle = 2
        iDelCount = 0
        for iIndex in range(0,iCycle):
            minMean = np.Inf
            iDelCount = len(delList)
            delIndex = num**(i+1) - iDelCount
            delCount -= 1
            #print('delList:',delList)
            iErrorCount = 0
            iCount = 0
            while delIndex >= 0:
                #iCount = 0
                iCount += 1
                if (delIndex == (num**(i+1) - iDelCount)) :
                    delTrainingData = trainingData
                    #delCount -= 1
                else:
                    delTrainingData = np.delete(trainingData,delIndex,1)
                for j in range(numVal):
                    #print('j:',j)
                    np.random.shuffle(indexList)
                    #print('indexList:',indexList)
                    trainX = np.mat(np.ones((int(m*0.9),num**(i+1) - delCount)));trainY = np.mat(np.ones((int(m*0.9),1)))
                    testX =np.mat(np.ones((m - int(m*0.9),num**(i+1) - delCount)));testY = np.mat(np.ones((m - int(m*0.9),1)))
                    testIndex = 0
                    for index in range(m):
                        if index < int(m*0.9) :
                            trainX[index] = delTrainingData[indexList[index]]
                            trainY[index,0] = inputData[indexList[index],i+1]
                        else:
                            testX[testIndex] = delTrainingData[indexList[index]]
                            testY[testIndex,0] = inputData[indexList[index],i+1]
                            testIndex += 1
                    wMat = getWs(trainX, trainY,numVal)
                    #print('wMat:',wMat)
                    for k in range(numVal):
                        yEst = testX*wMat[k].T
                        errorMat[j,k] = varError(yEst,testY)
                meanErrors = np.mean(errorMat,0)
                #minMean = float(np.min(meanErrors))
                minError = float(np.min(meanErrors))
                
                rate = ((i+1)*(iIndex+1) + iCount/(num**(i+1)))/((n-1)*iCycle +1)
                #rate = 0.98*(i+1)/(n-1) + 0.02*(iIndex+1)*iCount/(iCycle*(num**(i+1)))
                sMsg[0] = str(int(rate*100)) + '%'
                #print('delIndex:',delIndex,'  minError:',minError)
                
                iErrorCount += 1
                if minError <= minMean*1.005 or np.isnan(minError):
                    minMean = minError
                    delCount += 1
                    if delIndex != num**(i+1) - iDelCount:
                        delList.append(delIndex)
                        trainingData = np.delete(trainingData,delIndex,1)                    
                    #print('meanErrors:',meanErrors)
                    #print('minMean:',minMean)
                    #print(np.nonzero(meanErrors == minMean))   
                    ws = wMat[np.nonzero(meanErrors == minMean)[1][0]]
                    dicWsData[i] = ws
                    iErrorCount = 0
                delIndex -= 1                
                if iErrorCount >= num * 2 :
                    break
            #sMsg[0] = str(int((i*iCycle + iIndex)/((n-1)*iCycle)*100)) + '%'
            #print('sMsg = ',sMsg[0])
            dicDelIndex[i+1] = delList
    sMsg[0] = '100%'
    return dicWsData,dicDelIndex

def writeResult(dataMat):
    import time,csv
    sFileName = 'result_' + time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time())) + '.csv'
    fr = open(sFileName,'w',newline='')
    fr_write = csv.writer(fr)
    listFirst = []
    for i in range(dataMat.shape[1]):
        strTemp = str(i+1) + '元模型预测'
        listFirst.append(strTemp)
    fr_write.writerow(np.asarray(listFirst,'str'))
    fr_write.writerows(dataMat.tolist())
    fr.close()
    return sFileName

def predict(inputData,dicWData,dicDel,powers =(-1, 3)):
    dicData,inputDataShape,num = preDealData(inputData,powers)
    writeData = np.mat(np.ones((inputDataShape[0],inputDataShape[1]-1)))
    for i in range(1,inputDataShape[1]):
        #print(dicWData[i-1].reshape((1,num**(i) - len(dicDel[i]))))
        trainingData = calMouldData(dicData,inputDataShape,num,i)
        #print(trainingData)
        #print('trainingData:',trainingData)
        #print(dicDel[i])
        for delIndex in dicDel[i]:
            trainingData = np.delete(trainingData,delIndex,1)
        writeData[:,i-1] = trainingData.dot(dicWData[i-1].T)
        #print('predict:',writeData[:,i-1])
    return writeResult(writeData)
        #print('predict:',trainingData.dot(dicWData[inputDataShape[1] - 2]))

#if __name__ == '__main__':
def trainData(trainFileName,powers):
    inputData = loadCsvData(trainFileName)
    dicWsData.clear()
    dicDelIndex.clear()    
    findMultyPolyFittingByL2(inputData,40,powers)
    #dicWsData.update(dicWs)
    #dicDelIndex.update(dicDel)

def predictData(testFileName,powers):
    testData = loadCsvData(testFileName)
    if len(dicWsData.keys()) == 0:
        return ''
    return predict(testData,dicWsData,dicDelIndex,powers)
    
