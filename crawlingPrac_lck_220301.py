from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

browser = webdriver.Chrome('c:/chromedriver/chromedriver.exe')  # chromedriver 다운받고, 다운 받은 경로 써주어야함

datelist = []
titlelist = []
stagelist = []
team1list = []
team2list = []
winlist = []

# 크롤링
for page in range(1,3):
    search_url = "https://lol.inven.co.kr/dataninfo/match/teamList.php?pg=" + str(page) + "&iskin=lol&category=LCK2021"
    browser.get(search_url)

    browser.implicitly_wait(2)

    game = browser.find_elements(By.CLASS_NAME, "listFrame")

    for i in range(20):
        date = game[i].find_element(By.CLASS_NAME, "date").text
        title = game[i].find_element(By.CLASS_NAME, "title").text
        stage = game[i].find_element(By.CLASS_NAME, "stage").text
        teamname = game[i].find_elements(By.CLASS_NAME, "teamname")
        team1 = teamname[0].text
        team2 = teamname[1].text
        win = game[i].find_element(By.CLASS_NAME, "color1.tx5").text

        #print(date, title, stage, team1, team2, win)
        datelist.append(date)
        titlelist.append(title)
        stagelist.append(stage)
        team1list.append(team1)
        team2list.append(team2)
        winlist.append(win)

browser.close()


# dataframe으로 변환
data = {"date" : datelist,"title":titlelist, "stage":stagelist, "team1":team1list, "team2":team2list, win:winlist}
df = pd.DataFrame(data)
print(df.head(5))


# dataframe을 csv파일로 내보내기
df.to_csv("test.csv", encoding = "utf-8-sig")