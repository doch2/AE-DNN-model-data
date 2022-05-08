#Anaconda Virtual Environment: 64bit

from pykrx import stock
import time
import os
import shutil

def remove_all_file(filepath): #폴더 내 모든 파일 삭제
    if os.path.exists(filepath):
        shutil.rmtree(filepath, ignore_errors=True)
        os.makedirs(filepath)
    else:
        os.makedirs(filepath)

def createFolder(directory): #새로운 폴더 생성
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        else:
            clearConsole()
            print("\n현재 사진 폴더를 삭제중입니다. | 폴더 이름: " + directory)
            remove_all_file(directory) #만약 기존에 폴더가 있을 경우, 폴더 안에 있는 모든 파일 삭제 진행.
    except OSError:
        print ('Error: Creating directory. ' +  directory)

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')


stockDataFolderPath = "stock_data/stockPriceData/korea_kospi/kiwoom/"
marketCapFolderPath = "stock_data/stockPriceData/korea_kospi/marketCap/"

createFolder(marketCapFolderPath)


tickerList = os.listdir(stockDataFolderPath + "hourCandle")
startDate = "20210608" #시가총액 데이터를 불러올 날짜 지장 - 이 날짜부터
endDate = "20211210" #시가총액 데이터를 불러올 날짜 지장 - 이 날짜까지


for ticker in tickerList:
    tickerName = ticker[0:ticker.find('.csv')] #주식 티커 불러오기
    marketCap_Df = stock.get_market_cap(startDate, endDate, tickerName) #시가총액 데이터 불러오기

    marketCap_Df.to_csv(marketCapFolderPath + tickerName + ".csv") #불러온 데이터 csv 파일 형태로 저장

    #터미널에 현재 작업 현황 메세지 출력
    progress = (round((tickerList.index(ticker) + 1) / len(tickerList), 4) * 100)
    clearConsole()
    print("\nKOSPI 시장의 티커 로딩이 완료되었습니다. | 티커 개수: " + str(len(tickerList)))
    print("\n\n[ " + ("=" * int(progress / 2)) + ("-" * (50 - int(progress / 2))) + " ] | 현재 불러온 티커: " + tickerName + "(" + stock.get_market_ticker_name(tickerName) + ")" + " | 현재 진행률: " + str(round(progress, 4)) + "%", end='\r')

    time.sleep(0.4) #과도한 요청으로 인한 API 차단을 막기 위한 일시정지