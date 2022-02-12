# -*- coding: utf-8 -*-
#Anaconda Virtual Environment: 32bit

from pykiwoom.kiwoom import *
import os
import shutil
import time
from datetime import datetime


def remove_all_file(filepath):
    if os.path.exists(filepath):
        shutil.rmtree(filepath, ignore_errors=True)
        os.makedirs(filepath)
    else:
        os.makedirs(filepath)

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')


remove_all_file('stock_data/stockPriceData/korea_kospi/kiwoom/10minuteCandle')
remove_all_file('stock_data/stockPriceData/korea_kospi/kiwoom/30minuteCandle')
remove_all_file('stock_data/stockPriceData/korea_kospi/kiwoom/halfDayCandle')
remove_all_file('stock_data/stockPriceData/korea_kospi/kiwoom/hourCandle')
remove_all_file('stock_data/stockPriceData/korea_kospi/kiwoom/dayCandle')
remove_all_file('stock_data/stockPriceData/korea_kospi/kiwoom/weekCandle')

for i in range (3, 7):
    remove_all_file("stock_data/stockPriceData/korea_kospi/kiwoom/day" + str(i) + "Candle/")

kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)
print("키움증권 로그인 완료")

tickerList = kiwoom.GetCodeListByMarket('0') #코스피 주가 티커 종목 리스트
print("KOSPI 시장의 티커 로딩이 완료되었습니다. | 티커 개수: " + str(len(tickerList)))

marketOpenTimeAmount = 400

for ticker in tickerList:
    stockName = kiwoom.GetMasterCodeName(ticker)
    

    df = kiwoom.block_request("opt10080", 종목코드=ticker, 틱범위=10, output="주식분봉차트조회요청", 수정주가구분=1, next=0)
    df.to_csv("stock_data/stockPriceData/korea_kospi/kiwoom/10minuteCandle/" + ticker + ".csv", index=False)
    
    df = kiwoom.block_request("opt10080", 종목코드=ticker, 틱범위=30, output="주식분봉차트조회요청", 수정주가구분=1, next=0)
    df.to_csv("stock_data/stockPriceData/korea_kospi/kiwoom/30minuteCandle/" + ticker + ".csv", index=False)

    df = kiwoom.block_request("opt10080", 종목코드=ticker, 틱범위=200, output="주식분봉차트조회요청", 수정주가구분=1, next=0)
    df.to_csv("stock_data/stockPriceData/korea_kospi/kiwoom/halfDayCandle/" + ticker + ".csv", index=False)

    for i in range (3, 7):
        df = kiwoom.block_request("opt10080", 종목코드=ticker, 틱범위=int(marketOpenTimeAmount / i), output="주식분봉차트조회요청", 수정주가구분=1, next=0)
        df.to_csv("stock_data/stockPriceData/korea_kospi/kiwoom/day" + str(i) + "Candle/" + ticker + ".csv", index=False)
    
    df = kiwoom.block_request("opt10080", 종목코드=ticker, 틱범위=60, output="주식분봉차트조회요청", 수정주가구분=1, next=0)
    df.to_csv("stock_data/stockPriceData/korea_kospi/kiwoom/hourCandle/" + ticker + ".csv", index=False)

    df = kiwoom.block_request("opt10081", 종목코드=ticker, output="주식일봉차트조회요청", 수정주가구분=1, next=0)
    df.to_csv("stock_data/stockPriceData/korea_kospi/kiwoom/dayCandle/" + ticker + ".csv", index=False)

    df = kiwoom.block_request("opt10082", 종목코드=ticker, 기준일자=int(datetime.today().strftime("%Y%m%d")), output="주식주봉차트조회요청", 수정주가구분=1, next=0)
    df.to_csv("stock_data/stockPriceData/korea_kospi/kiwoom/weekCandle/" + ticker + ".csv", index=False)


    progress = (round((tickerList.index(ticker) + 1) / len(tickerList), 4) * 100)
    clearConsole()
    print("\nKOSPI 시장의 티커 로딩이 완료되었습니다. | 티커 개수: " + str(len(tickerList)))
    print("\n\n[ " + ("=" * int(progress / 2)) + ("-" * (50 - int(progress / 2))) + " ] | 현재 불러온 티커: " + ticker + "(" + stockName + ")" + " | 현재 진행률: " + str(round(progress, 4)) + "%", end='\r')
    time.sleep(36) #1시간에 1000회 조회 제한으로 인한 딜레이 설정