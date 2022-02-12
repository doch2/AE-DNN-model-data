#Anaconda Virtual Environment: 64bit

import pandas as pd
import numpy as np
import os

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')


stockDataPath = "stock_data/"
stockDataFolderPath = "stock_data/stockPriceData/korea_kospi/kiwoom/"

for dataKind in ['train', 'test']: 
    df = pd.read_csv(stockDataPath + dataKind + "_dataFrame.csv")
    dfIndex = (df['stockIndex']).tolist()

    newStockDf = pd.DataFrame(columns=[
        'stockIndex', 'input1', 'input2', 'input3', 'input4', 'input5', 'input6', 'input7', 'input8', 'input9', 'input10', 'input11', 'input12'
    ])
    candleData = {}

    beforeTicker = ""

    for index in dfIndex:
        ticker = index[0:index.find('_')]
        date = index[index.find('_')+1:]

        if ticker != beforeTicker:
            for candleDataKind in ["day", "hour", "halfDay"]:
                candleData[candleDataKind] = (pd.read_csv(stockDataFolderPath + candleDataKind + 'Candle/' + ticker + ".csv"))[::-1]
                candleData[candleDataKind] = candleData[candleDataKind].reset_index()

            candleData[2] = candleData['halfDay']
            for candleAmount in range(3, 7):
                candleData[candleAmount] = (pd.read_csv(stockDataFolderPath + 'day' + str(candleAmount) + 'Candle/' + ticker + ".csv"))[::-1]
                candleData[candleAmount] = candleData[candleAmount].reset_index()
            candleData[7] = candleData['hour']
        
        newStockData = df.index[df['stockIndex'] == index].tolist()
        newDayDataFrame = df.loc[newStockData[0]:newStockData[0]]
        newDayDataFrame = newDayDataFrame.drop(['Unnamed: 0'], axis=1)

        try:
            stockDfIndex = candleData['day'].index[(candleData['day'])['일자'] == int(date)].tolist()
            nextDayDate = int((candleData['day']).loc[stockDfIndex[0]+1]['일자'])
            nextDayDataFrame = (candleData['day']).loc[stockDfIndex[0]+1:stockDfIndex[0]+1]
            calcNum = float(round(((nextDayDataFrame['현재가'] / nextDayDataFrame['시가']) - 1) * 100, 2)) #주가 등락 퍼센트

            newDayDataFrame.insert(18, "nextStockUpDown_1", [calcNum], True) #봉 1개

            tempInt = 0
            for candleAmount in range(2, 8): #봉 2개에서 7개까지
                stockDfIndex = candleData[candleAmount].index[(candleData[candleAmount])['체결시간'].astype(str).str.contains(str(nextDayDate))].tolist()
                nextDayDataFrame = candleData[candleAmount].loc[stockDfIndex[0]:stockDfIndex[candleAmount-1]]
                nextDayDataFrame = nextDayDataFrame.reset_index()
                for i in range(0, candleAmount):
                    if i != (candleAmount-1):
                        calcNum = round(((abs(nextDayDataFrame.loc[i+1]['시가']) / abs(nextDayDataFrame.loc[i]['시가'])) - 1) * 100, 2)
                    else:
                        calcNum = round(((abs(nextDayDataFrame.loc[i]['현재가']) / abs(nextDayDataFrame.loc[i]['시가'])) - 1) * 100, 2)
                    newDayDataFrame.insert(19+tempInt, "nextStockUpDown_"+ str(candleAmount) + "_" + str(i+1), [calcNum], True)
                    tempInt = tempInt + 1
                    

            #nextDayDataFrame['nextStockUpDown'] = calcNum

            newStockDf = newStockDf.append(newDayDataFrame, ignore_index=True)
        except (IndexError) as e:
            print(e)

        
        beforeTicker = ticker

        progress = (round((dfIndex.index(index) + 1) / len(dfIndex), 4) * 100)
        clearConsole()
        print("\nKOSPI 시장의 " + dataKind + "을(를) 진행할 차트 사진 리스트 로딩이 완료되었습니다. | 일별(시간봉) 차트 사진 개수: " + str(len(dfIndex)))
        print("\n\n[ " + ("=" * int(progress / 2)) + ("-" * (50 - int(progress / 2))) + " ] | 현재 불러온 차트의 주식 티커: " + index[0:index.find('_')] + " | 현재 불러온 사진의 날짜: " + date + " | 현재 진행률: " + str(round(progress, 4)) + "%")
    
    newStockDf.to_csv(stockDataPath + dataKind + "_dataFrame.csv")