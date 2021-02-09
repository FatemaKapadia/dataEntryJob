from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time

chrome_web_driver = "D:\Program Files\Chromedriver\chromedriver.exe"
zillowURl = 'https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C' \
            '%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.69219435644531%2C%22east%22%3A-122' \
            '.17446364355469%2C%22south%22%3A37.703343724016136%2C%22north%22%3A37.847169233586946%7D%2C' \
            '%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A' \
            '%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse' \
            '%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B' \
            '%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C' \
            '%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22' \
            '%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D'

formURL = 'https://docs.google.com/forms/d/e/1FAIpQLSc9xupW_pnC7bbEk-iOG4cPr0qvlfATYCTKMBt12uStVD4nBg/viewform'
responsesURL = 'https://docs.google.com/forms/d/1HL2JAR6Dwj6xsGHbjzRtVU7WxOlpQ3iziokpzp9Svw0/edit#responses'

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 " \
             "Safari/537.36 "
accept_language = "en-US,en;q=0.9"
add = 'https://www.zillow.com'


class Action:

    def __init__(self):
        response = requests.get(zillowURl, headers={"User-Agent": user_agent, "Accept-Language": accept_language})
        yc_web = response.text
        self.soup = BeautifulSoup(yc_web, "html.parser")

    def find(self):
        information = self.soup.find_all(class_="list-card-info")
        self.all_info = {
            information.index(i): {"address": i.address.text, "price": i.find(class_="list-card-price").text,
                                   "link": i.a.get("href")} for i in information}
        for i in self.all_info:
            x = self.all_info.get(i)["link"]
            if x.split('/')[0] != 'https:':
                self.all_info[i]["link"] = add + x

    def fillForm(self):
        self.bot = webdriver.Chrome(executable_path=chrome_web_driver)
        self.bot.get(formURL)
        time.sleep(3)
        for i in self.all_info:
            q1 = self.bot.find_element_by_xpath(
                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            q1.send_keys(self.all_info.get(i)["address"])
            q2 = self.bot.find_element_by_xpath(
                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            q2.send_keys(self.all_info.get(i)["price"])
            q3 = self.bot.find_element_by_xpath(
                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
            q3.send_keys(self.all_info.get(i)["link"])
            submit = self.bot.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div')
            submit.click()
            time.sleep(5)
            next_response = self.bot.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
            next_response.click()
            time.sleep(3)

        self.bot.quit()
        self.bot.get(responsesURL)
        makeSpreadsheet = self.bot.find_element_by_xpath('//*[@id="ResponsesView"]/div/div[1]/div[1]/div[2]/div[1]/div/div')
        makeSpreadsheet.click()

        self.bot.quit()


perform = Action()
time.sleep(5)
perform.find()
time.sleep(10)
perform.fillForm()
