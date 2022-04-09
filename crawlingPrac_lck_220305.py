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
player1 = [[] for i in range(5)]
player2 = [[] for i in range(5)]



# 크롤링
for page in range(1,21):
    search_url = "https://lol.inven.co.kr/dataninfo/match/teamList.php?pg=" + str(page) + "&iskin=lol&category=LCK2021"
    browser.get(search_url)

    browser.implicitly_wait(2)

    game = browser.find_elements(By.CLASS_NAME, "listFrame")

    for i in range(len(game)):
        date = game[i].find_element(By.CLASS_NAME, "date").text
        title = game[i].find_element(By.CLASS_NAME, "title").text
        stage = game[i].find_element(By.CLASS_NAME, "stage").text
        teamname = game[i].find_elements(By.CLASS_NAME, "teamname")
        team1 = teamname[0].text
        team2 = teamname[1].text
        win = game[i].find_element(By.CLASS_NAME, "color1.tx5").text

        game[i].find_element(By.CLASS_NAME, "detail").click()
        dt = game[i].find_element(By.CLASS_NAME, "detailTable")
        p1 = dt.find_elements(By.CLASS_NAME, "playername.color1")
        p2 = dt.find_elements(By.CLASS_NAME, "playername.color2")

        if len(p1) == 0 : continue

        for j in range(5):
            player1[j].append(p1[j].text)
            player2[j].append(p2[j].text)


        #print(date, title, stage, team1, team2, win)
        datelist.append(date)
        titlelist.append(title)
        stagelist.append(stage)
        team1list.append(team1)
        team2list.append(team2)
        winlist.append(win)

browser.close()


# dataframe으로 변환
data = {"date" : datelist,"title":titlelist, "stage":stagelist, "team1":team1list, "team2":team2list, "win":winlist,
        "top1" : player1[0], "jg1" : player1[1], "mid1" : player1[2], "adc1" : player1[3], "sup1" : player1[4],
        "top2" : player2[0], "jg2" : player2[1], "mid2" : player2[2], "adc2" : player2[3], "sup2" : player2[4]}
df = pd.DataFrame(data)
print(df.head(5))


# dataframe을 csv파일로 내보내기
df.to_csv("match_data.csv", encoding = "utf-8-sig")


