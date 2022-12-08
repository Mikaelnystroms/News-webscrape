import os
import smtplib
from datetime import date
from email.message import EmailMessage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pyshorteners

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)
type_tiny = pyshorteners.Shortener()
today = date.today()

driver.get("https://www.news.google.com")
accept_cookies = driver.find_element(By.TAG_NAME, "button")
accept_cookies.click()

SERVER = smtplib.SMTP("send.one.com", 587)
USERNAME = "mikael@nystroms.eu"
PASSWORD = os.eniron.get("PASSWORD")
SEND_TO = "mikaelnystromm@gmail.com"

search_bar = driver.find_element(
    By.XPATH,
    '//*[@id="gb"]/div[2]/div[2]/div/form/div[1]/div/div/div/div/div[1]/input[2]',
)
search_bar.send_keys(input("what news do you want?"), Keys.ENTER)
driver.get(driver.current_url)
# print titles of articles
articles = driver.find_elements(By.TAG_NAME, "h3")
message = []
with open("../../Documents/Python/HI/blocketsok/news.txt", "w") as f:
    f.write(f"Today's date: {today.isoformat()} \n")
for article in articles:
    num = articles.index(article) + 1
    link = article.find_element(By.TAG_NAME, "a").get_attribute("href")
    shortlink = type_tiny.tinyurl.short(link)
    textandlink = f"{num}.{article.text} \n Link \n {shortlink} \n"
    print(textandlink)
    message.append(textandlink)
    with open("../../Documents/Python/HI/blocketsok/news.txt", "a") as file:
        file.write(f"{textandlink} \n ")
    if num >= 10:
        SERVER.starttls()
        SERVER.login(USERNAME, PASSWORD)
        msg = EmailMessage()
        with open("../../Documents/Python/HI/blocketsok/news.txt", "r") as file:
            msg.set_content(file.read())
        msg["Subject"] = "Nyheter"
        msg["From"] = USERNAME
        msg["To"] = SEND_TO
        SERVER.send_message(msg)
        driver.quit()
        break
