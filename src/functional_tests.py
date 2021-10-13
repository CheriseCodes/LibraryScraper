import unittest
import os
from libscrape.library import WPL, PPL, TPL
from selenium import webdriver

# TODO: Client for each case? (TPL, TPL+PPL, TPL+WPL, TPL+WPL+PPL, PPL,...)

class Client(unittest.TestCase):
    def setUp(self) -> None:
        self.login_info = {"p":(os.environ['PPL_USER'], os.environ['PPL_PASS']), "w":(os.environ['WPL_USER'], os.environ['WPL_PASS']), "t":(os.environ['TPL_USER'],os.environ['TPL_PASS'])}

    def recieve_wpl_holds_as_a_text(self):
        '''driver = webdriver.Chrome("chromedriver")
        wpl = WPL(driver)
        holds = wpl.items_on_hold()
        response = wpl.send_text(holds)
        self.assertDictContainsSubset({'key':'value'}, response)
        driver.close()'''
        pass

    def recieve_wpl_checkouts_as_a_text(self):
        pass

    def recieve_tpl_holds_as_a_text(self):
        pass

    def recieve_tpl_checkouts_as_a_text(self):
        pass

    def recieve_ppl_holds_as_a_text(self):
        pass

    def recieve_ppl_checkouts_as_a_text(self):
        pass

    def recieve_location_info_as_a_google_maps_link(self):

        # Get latitude and longitude: https://developers.google.com/maps/documentation/geocoding/overview
        # convert to Google maps url: https://stackoverflow.com/questions/5086220/google-maps-api-send-email-with-directions
        pass



