import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

import datetime

# 파일 불러오기
data = pd.read_csv('match_data.csv')

# 데이터 변환
pos = ['top1','jg1','mid1','adc1','sup1','top2','jg2','mid2','adc2', 'sup2']

data1 = data.loc[:,["date","top1","top2"]]
data2 = data.loc[:,["date","jg1","jg2"]]
data3 = data.loc[:,["date","mid1","mid2"]]
data4 = data.loc[:,["date","adc1","adc2"]]
data5 = data.loc[:,["date","sup1","sup2"]]

data1 = data1.rename(columns={'top1':'player1', 'top2':'player2'})
data2 = data2.rename(columns={'jg1':'player1', 'jg2':'player2'})
data3 = data3.rename(columns={'mid1':'player1', 'mid2':'player2'})
data4 = data4.rename(columns={'adc1':'player1', 'adc2':'player2'})
data5 = data5.rename(columns={'sup1':'player1', 'sup2':'player2'})

newdata = pd.concat([data1, data2, data3, data4, data5], ignore_index=True)  # 데이터 연결
newdata = newdata.drop_duplicates(ignore_index = True)   # 데이터 중복되는 행 삭제
newdata['date'] = newdata['date'].apply(lambda x : datetime.datetime(int(x.split('.')[0]),int(x.split('.')[1]),int(x.split('.')[2])))  # 시간데이터로 변경
newdata['daybefore'] = newdata['date'].apply(lambda x : x-datetime.timedelta(1))   # 하루 전 날짜 구하기
newdata['daybefore'] = pd.to_datetime(newdata['daybefore']).dt.date
newdata['player1'] = newdata['player1'].apply(lambda x: x.split()[1])   # 팀이름 제거
newdata['player2'] = newdata['player2'].apply(lambda x: x.split()[1])

print(newdata)


# 크롤링 - 선수 대 선수 승률 데이터
browser = webdriver.Chrome('c:/chromedriver/chromedriver.exe')  # chromedriver 다운받고, 다운 받은 경로 써주어야함
winrate = []

for i in range(len(newdata)):
    if i % 50 == 0: print(i) # 확인용

    search_url = "https://lol.inven.co.kr/dataninfo/match/playerList.php?iskin=lol&category=&category2=&shipcode=&shipgroup=&playerName="\
                 + newdata.loc[i,"player1"] + "&champ=0&targetName=" + newdata.loc[i,"player2"] + "&startDate=&endDate=" + str(newdata.loc[i,"daybefore"])
    browser.get(search_url)

    browser.implicitly_wait(1)

    table = browser.find_element(By.CLASS_NAME, "listTable")
    win = table.find_elements(By.TAG_NAME, "td")

    #print(win[4].text)
    if len(win) > 4:
        winrate.append(win[4].text)
    else:
        winrate.append("")

browser.close()


# 데이터프레임에 컬럼 추가
newdata['winrate'] = winrate


# dataframe을 csv파일로 내보내기
newdata.to_csv("winrate.csv", encoding = "utf-8-sig")