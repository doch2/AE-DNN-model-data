#Anaconda Virtual Environment: 64bit

from pykrx import stock
import time
import os
import shutil

def remove_all_file(filepath):
    if os.path.exists(filepath):
        shutil.rmtree(filepath, ignore_errors=True)
        os.makedirs(filepath)
    else:
        os.makedirs(filepath)

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        else:
            clearConsole()
            print("\n현재 사진 폴더를 삭제중입니다. | 폴더 이름: " + directory)
            remove_all_file(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')


stockDataFolderPath = "stock_data/stockPriceData/korea_kospi/kiwoom/"
marketCapFolderPath = "stock_data/stockPriceData/korea_kospi/marketCap/"

createFolder(marketCapFolderPath)


tickerList = os.listdir(stockDataFolderPath + "hourCandle")
startDate = "20210608"
endDate = "20211210"


for ticker in tickerList:
    tickerName = ticker[0:ticker.find('.csv')]
    marketCap_Df = stock.get_market_cap(startDate, endDate, tickerName)

    marketCap_Df.to_csv(marketCapFolderPath + tickerName + ".csv")

    progress = (round((tickerList.index(ticker) + 1) / len(tickerList), 4) * 100)
    clearConsole()
    print("\nKOSPI 시장의 티커 로딩이 완료되었습니다. | 티커 개수: " + str(len(tickerList)))
    print("\n\n[ " + ("=" * int(progress / 2)) + ("-" * (50 - int(progress / 2))) + " ] | 현재 불러온 티커: " + tickerName + "(" + stock.get_market_ticker_name(tickerName) + ")" + " | 현재 진행률: " + str(round(progress, 4)) + "%", end='\r')

    time.sleep(0.4)