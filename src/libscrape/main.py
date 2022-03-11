#!/Users/cherise/Desktop/Code/Projects/LibraryScraper/env/bin/python3
from library import TPL, WPL, PPL
from selenium import webdriver
from lib_assets import Messenger
from dotenv import load_dotenv
import os

def send_tpl_checkouts_and_holds_sms(phone_number, username, password):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    tpl = TPL(driver)
    messenger = Messenger(tpl.name)
    messenger.send_checkouts_text(phone_number, tpl.items_checked_out(username, password), "plain")
    messenger.send_holds_text(phone_number, tpl.items_on_hold(username, password), "plain")
    tpl.driver.close()

def send_wpl_checkouts_and_holds_sms(phone_number, username, password):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    wpl = WPL(driver)
    messenger = Messenger(wpl.name)
    messenger.send_checkouts_text(phone_number, wpl.items_checked_out(username, password), "plain")
    messenger.send_holds_text(phone_number, wpl.items_on_hold(username, password), "plain")
    wpl.driver.close()

def send_ppl_checkouts_and_holds_sms(phone_number, username, password):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    ppl = PPL(driver)
    messenger = Messenger(ppl.name)
    messenger.send_checkouts_text(phone_number, ppl.items_checked_out(username, password), "plain")
    messenger.send_holds_text(phone_number, ppl.items_on_hold(username, password), "plain")
    ppl.driver.close()

if __name__ == "__main__":
    load_dotenv()
    receiving_phone_number = os.environ['PHONE_TO']
    username = os.environ['PPL_USER']
    password = os.environ['PPL_PASS']
    send_ppl_checkouts_and_holds_sms(receiving_phone_number, username, password)
    username = os.environ['WPL_USER']
    password = os.environ['WPL_PASS']
    send_wpl_checkouts_and_holds_sms(receiving_phone_number, username, password)
    username = os.environ['TPL_USER']
    password = os.environ['TPL_PASS']
    send_tpl_checkouts_and_holds_sms(receiving_phone_number, username, password)