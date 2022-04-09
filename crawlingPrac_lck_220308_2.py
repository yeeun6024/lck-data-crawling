import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

import datetime

# 파일 불러오기
data = pd.read_csv('match_data.csv')

# 데이터 변환
data = data.loc[:,["date", "team1","team2"]]
data = data.drop_duplicates(ignore_index = True)   # 데이터 중복되는 행 삭제
data['date'] = data['date'].apply(lambda x : datetime.datetime(int(x.split('.')[0]),int(x.split('.')[1]),int(x.split('.')[2])))  # 시간데이터로 변경
data['daybefore'] = data['date'].apply(lambda x : x-datetime.timedelta(1))   # 하루 전 날짜 구하기
data['daybefore'] = pd.to_datetime(data['daybefore']).dt.date

print(data)


# 크롤링 - 팀 대 팀 승률 데이터
browser = webdriver.Chrome('c:/chromedriver/chromedriver.exe')  # chromedriver 다운받고, 다운 받은 경로 써주어야함
winrate = []

for i in range(len(data)):
    if i % 50 == 0: print(i) # 확인용

    search_url = "https://lol.inven.co.kr/dataninfo/match/teamList.php?iskin=lol&category=&category2=&shipcode=&shipgroup=&teamName="+ data.loc[i,"team1"].replace(" ","+") +"&teamName2="+ data.loc[i,"team2"].replace(" ","+") +"&startDate=&endDate=" + str(data.loc[i,"daybefore"])
    browser.get(search_url)

    browser.implicitly_wait(1)

    table = browser.find_element(By.CLASS_NAME, "listTable")
    win = table.find_elements(By.TAG_NAME, "td")

    print(win[4].text)
    if len(win) > 4:
        winrate.append(win[4].text)
    else:
        winrate.append("")

browser.close()


# 데이터프레임에 컬럼 추가
data['winrate'] = winrate


# dataframe을 csv파일로 내보내기
data.to_csv("winrate_team.csv", encoding = "utf-8-sig")