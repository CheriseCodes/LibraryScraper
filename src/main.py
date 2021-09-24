from selenium import webdriver
from libscrape.library import *
import os

if __name__=="__main__":
    #print(sys.argv[1])
    login_info = {"p":(os.environ['PPL_USER'], os.environ['PPL_PASS']), "w":(os.environ['WPL_USER'], os.environ['WPL_PASS']), "t":(os.environ['TPL_USER'],os.environ['TPL_PASS'])}
    driver = webdriver.Chrome("chromedriver")
    library_obj = TPL(driver)
    on_hold = library_obj.items_on_hold(login_info['t'][0],login_info['t'][1])
    if on_hold:
        for item in on_hold:
            print(item)

    driver.close()

