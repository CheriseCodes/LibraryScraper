"""
Functional test suite for the core functionality of the LibraryScraper app
"""

import unittest
import os
from libscrape.library import WPL, PPL, TPL
from selenium import webdriver


# TODO: Client for each case? (TPL, TPL+PPL, TPL+WPL, TPL+WPL+PPL, PPL,...)

class Client(unittest.TestCase):
    def setUp(self) -> None:
        self.login_info = {"p": (os.environ['PPL_USER'], os.environ['PPL_PASS']), "w": (os.environ['WPL_USER'],
                                                                                        os.environ['WPL_PASS']),
                           "t": (os.environ['TPL_USER'], os.environ['TPL_PASS'])}

    def receive_wpl_holds_as_a_text(self):
        pass

    def receive_wpl_checkouts_as_a_text(self):
        pass

    def receive_tpl_holds_as_a_text(self):
        pass

    def receive_tpl_checkouts_as_a_text(self):
        pass

    def receive_ppl_holds_as_a_text(self):
        pass

    def receive_ppl_checkouts_as_a_text(self):
        pass

    def receive_location_info_as_a_google_maps_link(self):
        # Get latitude and longitude: https://developers.google.com/maps/documentation/geocoding/overview
        # convert to Google maps url: https://stackoverflow.com/questions/5086220/google-maps-api-send-email
        # -with-directions
        pass
