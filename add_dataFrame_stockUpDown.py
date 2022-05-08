#Anaconda Virtual Environment: 64bit

import pandas as pd
import numpy as np
import os

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')


stockDataPath = "stock_data/"
stockDataFolderPath = "stock_data/stockPriceData/korea_kospi/kiwoom/"

for dataKind in ['train', 'test']: 
    df = pd.read_csv(stockDataPath + dataKind + "_dataFrame.csv") #기존 dataFrame 불러오기 (save_picture_autoEncoderResult.py만 실행한 상태의 dataFrame이여야 함)
    dfIndex = (df['stockIndex']).tolist()

    newStockDf = pd.DataFrame(columns=[ #결과값을 저장할 dataFrame Object 생성
        'stockIndex', 'input1', 'input2', 'input3', 'input4', 'input5', 'input6', 'input7', 'input8', 'input9', 'input10', 'input11', 'input12'
    ])
    candleData = {}

    beforeTicker = "" #이전에 작업하였던 주식 종목 티커 (for문 코드에서 사용)

    for index in dfIndex: #기존 dataFrame Index들 for문 구동 - index 예시: 000020_20210618
        ticker = index[0:index.find('_')] #주식 티커
        date = index[index.find('_')+1:] #캔들차트 주가 데이터 날짜

        if ticker != beforeTicker: #index가 새로운 주식 종목일 때 - 처음 종목을 불러올때만 주가 데이털르 불러오게 작동하여 코드 실행속도를 향상시켰음
            #시간봉, 일봉, 1/2봉, 2~7등분봉 주가 데이터 불러오기
            
            for candleDataKind in ["day", "hour", "halfDay"]:
                candleData[candleDataKind] = (pd.read_csv(stockDataFolderPath + candleDataKind + 'Candle/' + ticker + ".csv"))[::-1]
                candleData[candleDataKind] = candleData[candleDataKind].reset_index()

            candleData[2] = candleData['halfDay']
            for candleAmount in range(3, 7):
                candleData[candleAmount] = (pd.read_csv(stockDataFolderPath + 'day' + str(candleAmount) + 'Candle/' + ticker + ".csv"))[::-1]
                candleData[candleAmount] = candleData[candleAmount].reset_index()
            candleData[7] = candleData['hour']
        
        #index를 통해 불러온 날짜의 데이터를 newDayDataFrame 변수에 재구성하여 저장함
        newStockData = df.index[df['stockIndex'] == index].tolist()
        newDayDataFrame = df.loc[newStockData[0]:newStockData[0]]
        newDayDataFrame = newDayDataFrame.drop(['Unnamed: 0'], axis=1)

        try:
            stockDfIndex = candleData['day'].index[(candleData['day'])['일자'] == int(date)].tolist() #index를 통해 불러온 날짜의 일봉 주가 데이터의 index
            nextDayDate = int((candleData['day']).loc[stockDfIndex[0]+1]['일자']) #index를 통해 불러온 날짜의 다음날 날짜
            nextDayDataFrame = (candleData['day']).loc[stockDfIndex[0]+1:stockDfIndex[0]+1] #index를 통해 불러온 날짜의 다음날 날짜의 주가 일봉 데이터 dataFrame
            calcNum = float(round(((nextDayDataFrame['현재가'] / nextDayDataFrame['시가']) - 1) * 100, 2)) #계산된 주가 등락 퍼센트

            newDayDataFrame.insert(18, "nextStockUpDown_1", [calcNum], True) #봉 1개의 주가 등락 퍼센트 dataFrame에 추가

            tempInt = 0
            for candleAmount in range(2, 8): #2등분부터 7둥분 봉까지 반복
                stockDfIndex = candleData[candleAmount].index[(candleData[candleAmount])['체결시간'].astype(str).str.contains(str(nextDayDate))].tolist() #index를 통해 불러온 날짜의 다음날 날짜 주가 데이터 index 리스트
                nextDayDataFrame = candleData[candleAmount].loc[stockDfIndex[0]:stockDfIndex[candleAmount-1]] #index를 통해 불러온 날짜의 다음날 날짜 주가 데이터 dataFrame
                nextDayDataFrame = nextDayDataFrame.reset_index()
                for i in range(0, candleAmount): #등분 개수만큼 반복
                    if i != (candleAmount-1):
                        calcNum = round(((abs(nextDayDataFrame.loc[i+1]['시가']) / abs(nextDayDataFrame.loc[i]['시가'])) - 1) * 100, 2) #마지막 봉이 아닐 시의 주가 등락 퍼센트
                    else:
                        calcNum = round(((abs(nextDayDataFrame.loc[i]['현재가']) / abs(nextDayDataFrame.loc[i]['시가'])) - 1) * 100, 2) #마지막 봉 일시의 주가 등락 퍼센트
                    newDayDataFrame.insert(19+tempInt, "nextStockUpDown_"+ str(candleAmount) + "_" + str(i+1), [calcNum], True) #계산한 주가 등락 퍼센트 dataFrame에 추가
                    tempInt = tempInt + 1
                    

            #nextDayDataFrame['nextStockUpDown'] = calcNum

            newStockDf = newStockDf.append(newDayDataFrame, ignore_index=True) #계산한 값들 dataFrame에 저장
        except (IndexError) as e:
            print(e)

        
        beforeTicker = ticker #현재 작업한 티커 이름 저장

        #터미널에 현재 작업 현황 메세지 출력
        progress = (round((dfIndex.index(index) + 1) / len(dfIndex), 4) * 100)
        clearConsole()
        print("\nKOSPI 시장의 " + dataKind + "을(를) 진행할 차트 사진 리스트 로딩이 완료되었습니다. | 일별(시간봉) 차트 사진 개수: " + str(len(dfIndex)))
        print("\n\n[ " + ("=" * int(progress / 2)) + ("-" * (50 - int(progress / 2))) + " ] | 현재 불러온 차트의 주식 티커: " + index[0:index.find('_')] + " | 현재 불러온 사진의 날짜: " + date + " | 현재 진행률: " + str(round(progress, 4)) + "%")
    
    newStockDf.to_csv(stockDataPath + dataKind + "_dataFrame.csv") #작업을 통해 획득한 최종 dataFrame을 csv 파일 형태로 저장