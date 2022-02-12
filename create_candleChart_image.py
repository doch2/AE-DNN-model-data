#Anaconda Virtual Environment: 64bit

from numpy.lib.npyio import save
import pandas as pd
import matplotlib.pyplot as plt
import mpl_finance
import os
import shutil
import datetime
import requests
from multiprocessing import Pool

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

def getPriceDataFrame(stockHourData, stockDayData, time):
    hourPriceDataFrame = stockHourData[stockHourData['체결시간'].astype(str).str.contains(time)]
    hourDataAmount = hourPriceDataFrame['index'].count()

    dayDateIndex = stockDayData.index[stockDayData['일자'] == int(time)].tolist()
    if len(dayDateIndex) < 1:
        return False, None, None, None
    dayPriceDataFrame = stockDayData.loc[(dayDateIndex[0] - weekChartCandleAmount + 1):dayDateIndex[0]]
    dayDataAmount = dayPriceDataFrame['index'].count()

    weekFirstDayIndex = (dayDateIndex[0] - (monthChartCandleAmount * 5)) + 1
    if weekFirstDayIndex < 0:
        return False, None, None, None
    weekPriceDataFrame_dayCandle = stockDayData.loc[weekFirstDayIndex:dayDateIndex[0]]
    weekPriceDataFrame_dayCandle = weekPriceDataFrame_dayCandle.reset_index()

    weekPriceDataFrame = pd.DataFrame(columns=['현재가', '시가', '고가', '저가'])
    for i in range(0, (5 * weekChartCandleAmount), 5):
        tempDataFrame = weekPriceDataFrame_dayCandle.loc[i:(i+5)-1] #5일씩 자른 DataFrame
        
        weekPriceDataFrame = weekPriceDataFrame.append({
            '현재가': tempDataFrame['현재가'].loc[i+4],
            '시가': tempDataFrame['시가'].loc[i],
            '고가': max(tempDataFrame['고가']),
            '저가': min(tempDataFrame['고가'])
    }, ignore_index=True)


    if hourDataAmount < 7: #시간봉 개수가 7개가 아닐경우
        return False, None, None, None
    elif dayDataAmount < weekChartCandleAmount:
        return False, None, None, None
    

    return True, hourPriceDataFrame, dayPriceDataFrame, weekPriceDataFrame

def getMarketHoliday():
    holidays = []

    for year in range(datetime.date.today().year - 7, datetime.date.today().year + 1):
        url = "https://open.krx.co.kr/contents/OPN/99/OPN99000001.jspx" 
        year = year # 휴장일 검색 연도 
        data = {
            "search_bas_yy": year,
            "gridTp": "KRX", 
            "pagePath": "/contents/MKD/01/0110/01100305/MKD01100305.jsp", 
            "code": 'VwN0qWxNxoQd3GptLiFi7VpQSV4Ewa+d2Su7DXPyhf9QzGrcwc/rwEcTS38k4e2df5Yx0Mfnbi2PWDHmer4lQzKMoOk5t9O8/DabZgelyz9UBc82a6GP7G4MABRDdIaJ7T+v79W6ON5hsRRGRUrUj69+eqY/BlbgIhBGzjGwqsT+CtNJN0ckkY/7efqYEaL7', 
            'pageFirstCall': 'Y'
        } 
        content_type = 'application/x-www-form-urlencoded; charset=UTF-8' 
        response = requests.post(url=url, data=data, headers={'Content-Type': content_type}) 
        resultJson = response.json() 

        holidays = holidays + [x['calnd_dd_dy'] for x in resultJson['block1']] 
    
    return holidays

def getWeekFirstDate(sourceDate): 
    temporaryDate = datetime.datetime(int(sourceDate[0:4]), int(sourceDate[4:6]), int(sourceDate[6:8])) 
    weekDayCount = temporaryDate.weekday() 
    targetDate = temporaryDate + datetime.timedelta(days = -weekDayCount)

    month = str(targetDate.month)
    if int(month) < 10:
        month = "0" + month
    
    day = str(targetDate.day)
    if int(day) < 10:
        day = "0" + day
    

    return str(targetDate.year) + month + day

def getWeekFridayDate(sourceDate): 
    temporaryDate = datetime.datetime(int(sourceDate[0:4]), int(sourceDate[4:6]), int(sourceDate[6:8])) 
    weekDayCount = temporaryDate.weekday() 
    targetDate = temporaryDate + datetime.timedelta(days = -weekDayCount) + datetime.timedelta(days = 4)

    month = str(targetDate.month)
    if int(month) < 10:
        month = "0" + month
    
    day = str(targetDate.day)
    if int(day) < 10:
        day = "0" + day
    
    return str(targetDate.year) + month + day

def getMarketFirstOpenDate(priceDate_notIncludeTime):
    weekFirstOpenDate = getWeekFirstDate(priceDate_notIncludeTime)
    while True:
        if (weekFirstOpenDate[0:4] + "-" + weekFirstOpenDate[4:6] + "-" +weekFirstOpenDate[6:8]) in marketHolidayList:
            weekFirstOpenDate = str(int(weekFirstOpenDate) + 1)
        
        if not (weekFirstOpenDate[0:4] + "-" + weekFirstOpenDate[4:6] + "-" +weekFirstOpenDate[6:8]) in marketHolidayList:
            break
    
    return weekFirstOpenDate

def saveChartPicture(chartKind, folderKindPath, tempPriceDataFrame, ticker, time):
    plt.figure(figsize=(0.44, 0.28))
    ax = plt.subplot()
    plt.axis('off')

    mpl_finance.candlestick2_ohlc(
        ax, 
        abs(tempPriceDataFrame['시가']), 
        abs(tempPriceDataFrame['고가']), 
        abs(tempPriceDataFrame['저가']), 
        abs(tempPriceDataFrame['현재가']), 
        width=0.5, 
        colorup='r', 
        colordown='b'
    )
    

    plt.savefig(imageFolderPath + folderKindPath + chartKind + "Chart/" + chartKind + "Chart1/" + ticker + "_" + time + ".jpg")
    
    plt.close()

imageFolderPath = "stock_data/"
stockDataFolderPath = "stock_data/stockPriceData/korea_kospi/kiwoom/"

weekChartCandleAmount = 5 #주별, 즉 일봉차트 캔들 개수
monthChartCandleAmount = 5 #월별, 즉 주봉차트 캔들 개수

marketHolidayList = getMarketHoliday()

tickerList = os.listdir(stockDataFolderPath + "hourCandle")
tickerAmount = len(tickerList)

def work(ticker):
    ticker = ticker[0:ticker.find('.csv')]

    clearConsole()
    print("\nKOSPI 시장의 주식 캔들차트 이미지를 저장중입니다. | 티커 개수: " + str(len(tickerList)))
    print("\n\n현재 저장중인 주식 티커: " + ticker + "\n", end='\r')

    stockHourData = (pd.read_csv(stockDataFolderPath + "hourCandle/" + ticker + ".csv"))[::-1]
    stockDayData = (pd.read_csv(stockDataFolderPath + "dayCandle/" + ticker + ".csv"))[::-1]

    stockHourData = stockHourData.reset_index()
    stockDayData = stockDayData.reset_index()


    tempDate = str(stockHourData['체결시간'][0])[:8]
    for priceDate in stockHourData['체결시간']:
        priceDate_notIncludeTime = str(priceDate)[:8]

        if priceDate_notIncludeTime != tempDate: #이미 사진으로 저장된 날짜의 주가가 아닐경우
            savePicturePercentage = stockHourData.index[stockHourData['체결시간'].astype(str).str.contains(priceDate_notIncludeTime)].tolist()[0] / stockHourData['index'].count()
            savePicturePercentage = round(round(savePicturePercentage, 2) * 100, 0)

            folderKindPath = "image_train/"
            if savePicturePercentage > 80:
                folderKindPath = "image_test/"
            

            isCorrectPriceData, hourPriceDataFrame, dayPriceDataFrame, weekPriceDataFrame = getPriceDataFrame(stockHourData, stockDayData, priceDate_notIncludeTime)
            if isCorrectPriceData:
                saveChartPicture("day", folderKindPath, hourPriceDataFrame, ticker, priceDate_notIncludeTime)
                saveChartPicture("week", folderKindPath, dayPriceDataFrame, ticker, priceDate_notIncludeTime)
                saveChartPicture("month", folderKindPath, weekPriceDataFrame, ticker, priceDate_notIncludeTime)

            tempDate = priceDate_notIncludeTime

if __name__ == "__main__":
    for imageKind in ["train", "test"]:
        createFolder(imageFolderPath + 'image_' + imageKind + '/' + 'dayChart/dayChart1')
        createFolder(imageFolderPath + 'image_' + imageKind + '/' + 'weekChart/weekChart1')
        createFolder(imageFolderPath + 'image_' + imageKind + '/' + 'monthChart/monthChart1')

    try:
        p = Pool(7)
        p.map_async(work, tickerList).get(timeout=1000000)
    except KeyboardInterrupt as e:
        p.close()
        p.terminate()