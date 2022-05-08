#Anaconda Virtual Environment: 64bit

import PIL.Image as pilimg
import numpy as np
from keras.models import load_model
import pandas as pd
import os
import datetime
import requests
import cupy as cp



def removeFile(filepath): #파일 삭제
    if os.path.isfile(filepath):
        os.remove(filepath)

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

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
        # print(response.json()) 
        holidays = holidays + [x['calnd_dd_dy'] for x in resultJson['block1']] 
    
    return holidays
marketHolidayList = getMarketHoliday()

def getMarketFirstOpenDate(priceDate_notIncludeTime): #그 주에서 처음 주식 시장이 열린 날짜를 반환함.
    weekFirstOpenDate = getWeekFirstDate(priceDate_notIncludeTime)
    while True:
        if (weekFirstOpenDate[0:4] + "-" + weekFirstOpenDate[4:6] + "-" +weekFirstOpenDate[6:8]) in marketHolidayList:
            weekFirstOpenDate = str(int(weekFirstOpenDate) + 1)
        
        if not (weekFirstOpenDate[0:4] + "-" + weekFirstOpenDate[4:6] + "-" +weekFirstOpenDate[6:8]) in marketHolidayList:
            break
    
    return weekFirstOpenDate

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

def convertImgToArray(path): #사진 파일을 모델에 값으로 넣을 수 있는 배열 형태로 반환함
    im = cp.array(pilimg.open("{}".format(path)))
    im = cp.reshape(im.get(),(1,28,44,3))/255
    return im


#일, 주, 월 캔들차트 오토인코더의 인코더 부분 모델 불러오기
encoder_day = load_model('models/encoder_day_28_44_4.h5')
encoder_week = load_model('models/encoder_week_28_44_4.h5')
encoder_month = load_model('models/encoder_month_28_44_4.h5')

imageFolderPath = "stock_data/"


for imageKind in ["train", "test"]: #train롸 test 이미지를 구분하여 dataFrame을 생성함
    removeFile(imageFolderPath + imageKind + "_dataFrame.csv") #기존 dataFrame 삭제

    imageList = os.listdir(imageFolderPath + "image_" + imageKind + "/dayChart/dayChart1/") #이미지 리스트 불러오기
    imageList.sort() #이미지 리스트 정렬(티커, 날짜 오름차순)
    result = pd.DataFrame(columns=[ #Result dataFrame Object 생성
        'stockIndex', 'input1', 'input2', 'input3', 'input4', 'input5', 'input6', 'input7', 'input8', 'input9', 'input10', 'input11', 'input12'
    ])

    #터미널에 메세지 출력
    clearConsole()
    print("\nKOSPI 시장의 " + imageKind + "을(를) 진행할 차트 사진 리스트 로딩이 완료되었습니다. | 일별(시간봉) 차트 사진 개수: " + str(len(imageList)))
    
    #배열들 저장할 변수 생성
    dayImgArray = []
    weekImgArray = []
    monthImgArray = []
    nextDayImgArray = []
    successImageList = []

    for imageName in imageList: #폴더 안에 저장된 이미지들 for문 돌려서 분석
        imageDate = imageName[imageName.find('_')+1:imageName.find('.jpg')] #이미지로 저장된 캔들차트의 날짜

        smallImageList = [s for s in imageList if imageName[0:imageName.find('_')] in s]  #현재 저장 진행중인 주식의 이미지 리스트

        try:
            #일, 주, 월별 차트 이미지 경로 불러오기
            dayImagePath = imageFolderPath + "image_" + imageKind + "/dayChart/dayChart1/" + imageName
            weekImagePath = imageFolderPath + "image_" + imageKind + "/weekChart/weekChart1/" + imageName
            monthImagePath = imageFolderPath + "image_" + imageKind + "/monthChart/monthChart1/" + imageName

            #이미지들을 배열로 변환하여 변수에 저장
            dayImgArray.append(convertImgToArray(dayImagePath)[0])
            weekImgArray.append(convertImgToArray(weekImagePath)[0])
            monthImgArray.append(convertImgToArray(monthImagePath)[0])

            #배열 변환이 완료된 이미지의 이름 저장
            successImageList.append(imageName[0:imageName.find('.jpg')])
        except (FileNotFoundError, IndexError) as e: #파일이 없거나(예시: 일, 주별 차트는 있는데 월별 차트가 없음 등), 정상적으로 이미지 인식이 안됐을 시
            print(e)

        #터미널에 현재 작업 현황 메세지 출력
        progress = (round((imageList.index(imageName) + 1) / len(imageList), 4) * 100) #작업 완료 비율 계산
        clearConsole()
        print("\nKOSPI 시장의 " + imageKind + "을(를) 진행할 차트 사진 리스트 로딩이 완료되었습니다. | 일별(시간봉) 차트 사진 개수: " + str(len(imageList)))
        print("\n\n[ " + ("=" * int(progress / 2)) + ("-" * (50 - int(progress / 2))) + " ] | 현재 불러온 차트의 주식 티커: " + imageName[0:imageName.find('_')] + " | 현재 불러온 사진의 날짜: " + imageDate + " | 현재 진행률: " + str(round(progress, 4)) + "%", end='\r')
    
    #터미널에 현재 작업 현황 메세지 출력
    clearConsole()
    print("\nKOSPI 시장의 " + imageKind + "을(를) 진행할 차트 사진 리스트 로딩이 완료되었습니다. | 일별(시간봉) 차트 사진 개수: " + str(len(imageList)))
    print("\n\n마무리 작업 중입니다..", end='\r')

    #배열 형태로 저장된 캔들차트 이미지 데이터들을 오토인코더 모델에 입력값으로 집어넣어 key-hyp값 획득한 후, 변수에 저장
    day_val = encoder_day.predict((np.array(dayImgArray)))
    week_val = encoder_week.predict((np.array(weekImgArray)))
    month_val = encoder_month.predict((np.array(monthImgArray)))
    
    #획득한 key-hyp값을 dataFrame에 저장. (저장된 데이터값들: 이미지 이름, 일, 월, 주별 캔들차트 이미지의 key-hyp 값)
    for i in range(len(day_val)):
        result.loc[i] = ([successImageList[i]] + (np.concatenate((day_val[i][0:4], week_val[i][0:4], month_val[i][0:4]), axis=None)).tolist())

    #작업을 통해 획득한 최종 dataFrame을 csv 파일 형태로 저장
    result.to_csv(imageFolderPath + imageKind + "_dataFrame.csv")
