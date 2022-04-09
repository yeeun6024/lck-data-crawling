'''from selenium import webdriver
from selenium.webdriver.common.by import By


search_url = "https://game.naver.com/esports/schedule/lck?date=2022-01"

browser = webdriver.Chrome('c:/chromedriver/chromedriver.exe')  # chromedriver 다운받고, 다운 받은 경로 써주어야함
browser.get(search_url)

browser.implicitly_wait(2)

date = browser.find_elements(By.CLASS_NAME, "card_date__1kdC3")
name = browser.find_elements(By.CLASS_NAME, "row_name__IDFHz")
score = browser.find_elements(By.CLASS_NAME, "row_score__2RmGQ")

for i in range(len(date)):
    k = 4 * i
    for j in range(0,4,2):
        print(date[i].text, name[k + j].text, score[k+j].text, ':', score[k+j+1].text, name[k + j + 1].text)

browser.close()'''


from selenium import webdriver
from selenium.webdriver.common.by import By


search_url = "https://game.naver.com/esports/schedule/lck_cl"

browser = webdriver.Chrome('c:/chromedriver/chromedriver.exe')  # chromedriver 다운받고, 다운 받은 경로 써주어야함
browser.get(search_url)

browser.implicitly_wait(2)

oneday = browser.find_elements(By.CLASS_NAME, "card_item__3Covz")

for i in range(len(oneday)):
    date = oneday[i].find_element(By.CLASS_NAME, "card_date__1kdC3").text
    games = oneday[i].find_elements(By.CLASS_NAME, "card_list__-eiJk")

    for j in range(len(games)):
        teams = games[j].find_elements(By.CLASS_NAME, "row_item__dbJjy")

        for k in range(len(teams)):
            team1 = teams[k].find_elements(By.CLASS_NAME, "row_name__IDFHz")[0].text
            team2 = teams[k].find_elements(By.CLASS_NAME, "row_name__IDFHz")[1].text
            print(date, team1, team2)

browser.close()

