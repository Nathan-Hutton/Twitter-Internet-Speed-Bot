import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
import time
import os
from dotenv import load_dotenv


class InternetSpeedTwitterBot:
    load_dotenv('/Users/natha/PycharmProjects/info.env')

    def __init__(self):
        service = Service("C:\important\chromedriver.exe")
        self.driver = webdriver.Chrome(service=service)
        self.DOWN = 150
        self.UP = 10
        self.twitter_email = os.getenv('EMAIL')
        self.twitter_password = os.getenv('TWITTER_PASSWORD')
        self.phone_number = os.getenv('TWILIO_RECEIVER')

    def get_internet_speed(self):
        self.driver.get('https://www.speedtest.net/')
        go_button = self.driver.find_element(By.CLASS_NAME, 'start-text')
        go_button.click()
        time.sleep(50)
        download_speed = self.driver.find_element(By.CLASS_NAME, 'download-speed')
        upload_speed = self.driver.find_element(By.CLASS_NAME, 'upload-speed')
        return [float(download_speed.text), float(upload_speed.text)]

    def tweet_at_provider(self):
        speeds = self.get_internet_speed()
        if not speeds[0] < self.DOWN or speeds[1] < self.UP:
            return

        self.driver.get('https://twitter.com/home')
        time.sleep(4)
        email_box = self.driver.find_element(By.NAME, 'text')
        email_box.send_keys(self.twitter_email + Keys.ENTER)
        try:
            time.sleep(2)
            verification_box = self.driver.find_element(By.NAME, 'text')
            verification_box.send_keys(self.phone_number + Keys.ENTER)
            time.sleep(2)
        except selenium.common.exceptions.NoSuchElementException:
            pass
        finally:
            password_box = self.driver.find_element(By.NAME, 'password')
            password_box.send_keys(self.twitter_password + Keys.ENTER)
            time.sleep(4)

        tweet_box = self.driver.find_element(By.CLASS_NAME, 'public-DraftStyleDefault-ltr')
        tweet_box.send_keys(f'I am supposed to have {self.DOWN}/{self.UP} '
                            f'speeds but I only have {speeds[0]}/{speeds[1]}'
                            f' speeds')
        tweet_button = self.driver.find_element(By.CSS_SELECTOR, '.css-18t94o4.css-1dbjc4n.r-l5o3uw.r-42olwf.r-sdzlij.r-1phboty.r-rs99b7.r-19u6a5r.r-2yi16.r-1qi8awa.r-1ny4l3l.r-ymttw5.r-o7ynqc.r-6416eg.r-lrvibr')
        tweet_button.click()
