from selenium.webdriver.support.expected_conditions import element_selection_state_to_be
import sys
from library import *
import subprocess
import os

# Based on: https://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python

try:
    #print(sys.argv[1])
    driver = webdriver.Chrome("chromedriver")
    library_obj = TPL(driver)
    on_hold = library_obj.get_items_on_hold()
    if on_hold:
        for item in on_hold:
            print(item)

    driver.close()
    if os.name == 'nt':
        subprocess.run(["powershell","-Command","Stop-Process -name chromedriver"])
    else:
        print("This is not a Windows system")
except KeyboardInterrupt:
    if os.name == 'nt':
        subprocess.run(["powershell","-Command","Stop-Process -name chromedriver"])
    else:
        print("This is not a Windows system")

