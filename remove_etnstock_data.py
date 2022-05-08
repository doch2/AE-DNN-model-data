# -*- coding: utf-8 -*-
#Anaconda Virtual Environment: 64bit

import pandas as pd
import os

def removeFile(filepath):
    if os.path.isfile(filepath):
        os.remove(filepath)

imageFolderPath = "stock_data/"
stockDataFolderPath = "stock_data/stockPriceData/korea_kospi/kiwoom/"

stockListWithoutEtn = pd.read_csv("stock_data/kospi_ticker_without_etn.csv")['종목코드']
for ticker in stockListWithoutEtn: #티커 정보 전처리 ex) 5930 -> 005930
    newTicker = str(ticker)
    if len(newTicker) < 6:
        newTicker = ('0' * (6 - len(newTicker))) + newTicker
    
    index = stockListWithoutEtn.index[stockListWithoutEtn == ticker].tolist()[0]

    stockListWithoutEtn.iloc[index] = newTicker


#순수 회사 주식이 아닌 나머지 주식의 CSV 데이터 삭제
dataKindList = os.listdir(stockDataFolderPath)
for dataKind in dataKindList:
    stockDataList = os.listdir(stockDataFolderPath + dataKind + "/")

    for ticker in stockDataList:
        if not ticker[0:ticker.find('.csv')] in stockListWithoutEtn.tolist():
            removeFile(stockDataFolderPath + dataKind + "/" + ticker)


#순수 회사 주식이 아닌 나머지 주식의 주가 캔들차트 사진 삭제
for dataKind in ['train', 'test']:
    for dateKind in ['10minute', '30minute', 'day', 'week', 'month']:
        chartPicList = os.listdir(imageFolderPath + "image_" + dataKind + "/" + dateKind + "Chart/" + dateKind + "Chart1/")

        for pictureName in chartPicList:
            if not pictureName[0:pictureName.find('_')] in stockListWithoutEtn.tolist():
                removeFile(imageFolderPath + "image_" + dataKind + "/" + dateKind + "Chart/" + dateKind + "Chart1/" + pictureName)