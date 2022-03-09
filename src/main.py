from libscrape.library import TPL, WPL, PPL
from selenium import webdriver
from libscrape.lib_assets import Messenger
from dotenv import load_dotenv
import os

def send_tpl_checkouts_and_holds(phone_number, username, password):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    tpl = TPL(driver)
    messenger = Messenger(tpl.name)
    messenger.send_checkouts_text(phone_number, tpl.items_checked_out(username, password), "plain")
    messenger.send_holds_text(phone_number, tpl.items_on_hold(username, password), "plain")
    tpl.driver.close()

def send_wpl_checkouts_and_holds(phone_number, username, password):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    wpl = WPL(driver)
    messenger = Messenger(wpl.name)
    messenger.send_checkouts_text(phone_number, wpl.items_checked_out(username, password), "plain")
    messenger.send_holds_text(phone_number, wpl.items_on_hold(username, password), "plain")
    wpl.driver.close()

if __name__ == "__main__":
    load_dotenv()
    receiving_phone_number = os.environ['PHONE_TO']
    username = os.environ['WPL_USER']
    password = os.environ['WPL_PASS']
    send_wpl_checkouts_and_holds(receiving_phone_number, username, password)