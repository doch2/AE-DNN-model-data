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

def getPriceDataFrame(stockHourData, stockDayData, time): #주가 dataFrame 불러오기
    hourPriceDataFrame = stockHourData[stockHourData['체결시간'].astype(str).str.contains(time)] #특정 날짜의 시간봉 주가 데이터
    hourDataAmount = hourPriceDataFrame['index'].count() #시간봉 데이터 개수

    dayDateIndex = stockDayData.index[stockDayData['일자'] == int(time)].tolist() #특정 날짜의 일봉 주가 데이터의 Index
    if len(dayDateIndex) < 1: #Index 개수가 1 이하, 즉 일봉 데이터가 주가 데이터에 존재하지 않은 경우 False값 반환
        return False, None, None, None
    dayPriceDataFrame = stockDayData.loc[(dayDateIndex[0] - weekChartCandleAmount + 1):dayDateIndex[0]] #특정 기간의 일봉 주가 데이터
    dayDataAmount = dayPriceDataFrame['index'].count() #일봉 데이터 개수

    weekFirstDayIndex = (dayDateIndex[0] - (monthChartCandleAmount * 5)) + 1 #특정 날짜로부터 n주 전 주의 첫번째 일봉 주가 데이터의 Index
    if weekFirstDayIndex < 0: #Index가 0 이하, 즉 데이터가 주가 데이터에 존재하지 않은 경우 False값 반환
        return False, None, None, None
    weekPriceDataFrame_dayCandle = stockDayData.loc[weekFirstDayIndex:dayDateIndex[0]] #n주전 주부터 현재 날짜의 주까지의 일봉 주가 데이터
    weekPriceDataFrame_dayCandle = weekPriceDataFrame_dayCandle.reset_index()

    weekPriceDataFrame = pd.DataFrame(columns=['현재가', '시가', '고가', '저가']) #주봉 주가 데이터
    for i in range(0, (5 * weekChartCandleAmount), 5):
        tempDataFrame = weekPriceDataFrame_dayCandle.loc[i:(i+5)-1] #5일씩 자른 DataFrame
        
        weekPriceDataFrame = weekPriceDataFrame.append({ #일봉 데이터를 주봉 형태로 처리하여 dataFrame에 저장
            '현재가': tempDataFrame['현재가'].loc[i+4],
            '시가': tempDataFrame['시가'].loc[i],
            '고가': max(tempDataFrame['고가']),
            '저가': min(tempDataFrame['고가'])
        }, ignore_index=True)


    if hourDataAmount < 7: #시간봉 개수가 7개가 아닐 경우 False값 반환
        return False, None, None, None
    elif dayDataAmount < weekChartCandleAmount: #일봉 차트 주가 데이터 개수가 지정한 값보다 작을 경우 False값 반환
        return False, None, None, None
    

    return True, hourPriceDataFrame, dayPriceDataFrame, weekPriceDataFrame #값이 모두 정상적이면 True값과 함께 전처리한 주가 dataFrame 전달

def getMarketHoliday(): #주식 시장의 휴장일을 리스트 형태로 반환.
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

def getWeekFirstDate(sourceDate): #그 주의 첫번째 날 찾기. ex) 입력으로 들어온 sourceDate가 5고 이날이 수요일이라면, 반환값은 03임.
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

def getWeekFridayDate(sourceDate): #그 주의 금요일 찾기. ex) 입력으로 들어온 sourceDate가 5고 이날이 수요일이라면, 반환값은 07임.
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

def getMarketFirstOpenDate(priceDate_notIncludeTime): #그 주에서 처음 주식 시장이 열린 날짜를 반환함.
    weekFirstOpenDate = getWeekFirstDate(priceDate_notIncludeTime)
    while True:
        if (weekFirstOpenDate[0:4] + "-" + weekFirstOpenDate[4:6] + "-" +weekFirstOpenDate[6:8]) in marketHolidayList:
            weekFirstOpenDate = str(int(weekFirstOpenDate) + 1)
        
        if not (weekFirstOpenDate[0:4] + "-" + weekFirstOpenDate[4:6] + "-" +weekFirstOpenDate[6:8]) in marketHolidayList:
            break
    
    return weekFirstOpenDate

def saveChartPicture(chartKind, folderKindPath, tempPriceDataFrame, ticker, time): #주가 데이터를 캔들차트 형태로 변환하여 이미지로 저장함
    plt.figure(figsize=(0.44, 0.28)) #사진 사이즈 설정
    ax = plt.subplot()
    plt.axis('off')

    mpl_finance.candlestick2_ohlc( #주가 데이터 바탕으로 캔들차트 생성
        ax, 
        abs(tempPriceDataFrame['시가']), 
        abs(tempPriceDataFrame['고가']), 
        abs(tempPriceDataFrame['저가']), 
        abs(tempPriceDataFrame['현재가']), 
        width=0.5, 
        colorup='r', 
        colordown='b'
    )
    

    plt.savefig(imageFolderPath + folderKindPath + chartKind + "Chart/" + chartKind + "Chart1/" + ticker + "_" + time + ".jpg") #캔들차트 이미지 저장
    
    plt.close()

imageFolderPath = "stock_data/"
stockDataFolderPath = "stock_data/stockPriceData/korea_kospi/kiwoom/"

weekChartCandleAmount = 5 #주별, 즉 일봉차트 캔들 개수
monthChartCandleAmount = 5 #월별, 즉 주봉차트 캔들 개수

marketHolidayList = getMarketHoliday()

tickerList = os.listdir(stockDataFolderPath + "hourCandle")
tickerAmount = len(tickerList)

def work(ticker): #주가 데이터를 이미지로 변화하는 핵심 함수 - multiprocessing 활용을 위해 함수로 분리해놓음
    ticker = ticker[0:ticker.find('.csv')] #주식 티커 추출

    #터미널에 현재 작업 현황 메세지 출력
    clearConsole()
    print("\nKOSPI 시장의 주식 캔들차트 이미지를 저장중입니다. | 티커 개수: " + str(len(tickerList)))
    print("\n\n현재 저장중인 주식 티커: " + ticker + "\n", end='\r')

    #저장되어 있는 주가 데이터 불러오기
    stockHourData = (pd.read_csv(stockDataFolderPath + "hourCandle/" + ticker + ".csv"))[::-1]
    stockDayData = (pd.read_csv(stockDataFolderPath + "dayCandle/" + ticker + ".csv"))[::-1]

    stockHourData = stockHourData.reset_index()
    stockDayData = stockDayData.reset_index()


    tempDate = str(stockHourData['체결시간'][0])[:8] #지정된 종목의 첫번째로 저장된 데이터의 날짜
    for priceDate in stockHourData['체결시간']: #저장된 데이터 날짜만큼 반복
        priceDate_notIncludeTime = str(priceDate)[:8] #현재 작업하고 있는 주가 데이터의 날짜 ex)20210608

        if priceDate_notIncludeTime != tempDate: #이미 사진으로 저장된 날짜의 주가가 아닐경우
            #현재 작업하고 있는 주식 종목의 작업 현황 퍼센테이지. ex) 70이라면 저장된 주가 데이터의 70%가 이미지화 되었다는 뜻
            savePicturePercentage = stockHourData.index[stockHourData['체결시간'].astype(str).str.contains(priceDate_notIncludeTime)].tolist()[0] / stockHourData['index'].count()
            savePicturePercentage = round(round(savePicturePercentage, 2) * 100, 0)

            folderKindPath = "image_train/"
            if savePicturePercentage > 80: #만약 작업이 80%가 넘었다면, test dataset에다가 저장
                folderKindPath = "image_test/"
            

            #시간,일,주봉 데이터가 정상적으로 존재하는지 확인하고, 만약 존재한다면 캔들차트 이미지로 저장할 주가 데이터를 전처리하여 반환함. 그 후 saveChartPicture 함수를 활용해 실제 컴퓨터에 이미지 형태로 캔들차트를 저장함.
            isCorrectPriceData, hourPriceDataFrame, dayPriceDataFrame, weekPriceDataFrame = getPriceDataFrame(stockHourData, stockDayData, priceDate_notIncludeTime)
            if isCorrectPriceData:
                saveChartPicture("day", folderKindPath, hourPriceDataFrame, ticker, priceDate_notIncludeTime)
                saveChartPicture("week", folderKindPath, dayPriceDataFrame, ticker, priceDate_notIncludeTime)
                saveChartPicture("month", folderKindPath, weekPriceDataFrame, ticker, priceDate_notIncludeTime)

            tempDate = priceDate_notIncludeTime

if __name__ == "__main__":
    #train과 test dataset으로 나누어 이미지 폴더 생성
    for imageKind in ["train", "test"]:
        createFolder(imageFolderPath + 'image_' + imageKind + '/' + 'dayChart/dayChart1')
        createFolder(imageFolderPath + 'image_' + imageKind + '/' + 'weekChart/weekChart1')
        createFolder(imageFolderPath + 'image_' + imageKind + '/' + 'monthChart/monthChart1')

    try:
        p = Pool(7) #7개 Thread 생성
        p.map_async(work, tickerList).get(timeout=1000000) #7개의 Thread에 분할하여 이미지 저장 다중작업 실행
    except KeyboardInterrupt as e:
        p.close()
        p.terminate()