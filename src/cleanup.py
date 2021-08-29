from selenium.webdriver.support.expected_conditions import element_selection_state_to_be
import sys
from scrape import *
import subprocess
import os

# Based on: https://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python

try:
    #print(sys.argv[1])
    scrape_holds(sys.argv[1])
except KeyboardInterrupt:
    # TODO: currently does not kill the process
    if os.name == 'nt':
        subprocess.run(["powershell","-Command","Stop-Process -name chromedriver"])
    else:
        print("This is not a Windows system")

