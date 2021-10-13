from typing import List
import unittest
from libscrape.library import WPL, PPL, TPL, DurhamLibrary, Item
from selenium import webdriver
from datetime import date
import os

class Library(unittest.TestCase):
    def setUp(self):
        self.login_info = {"p":(os.environ['PPL_USER'], os.environ['PPL_PASS']), "w":(os.environ['WPL_USER'], os.environ['WPL_PASS']), "t":(os.environ['TPL_USER'],os.environ['TPL_PASS'])}
        self.test_with_ui = False

    def create_webdriver(self):
        if self.test_with_ui:
            driver = webdriver.Chrome('chromedriver')
        else:
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            driver = webdriver.Chrome(options=options)
        return driver

    def test_wpl_login(self):
        driver = self.create_webdriver()
        wpl = WPL(driver)
        wpl.login(self.login_info['w'][0],self.login_info['w'][1])
        cookies = wpl.driver.get_cookies()
        found_new_user_cookie = False
        for cookie in cookies:
            #print(cookie,'\n\n')
            if cookie['name'] == '_live_bcui_session_id':
                found_new_user_cookie = True

        driver.close()
        self.assertTrue(found_new_user_cookie)

    def test_ppl_login(self):
        driver = self.create_webdriver()
        ppl = PPL(driver)
        ppl.login(self.login_info['p'][0],self.login_info['p'][1])
       # cookies = self.ppl.driver.get_cookies()
       # for cookie in cookies:
       #     print(cookie,'\n\n')
       #     ppl.login('abc','123')
       # self.assertFalse('Log In' in ppl.driver.title)
        cookies = ppl.driver.get_cookies()
        found_new_user_cookie = False
        for cookie in cookies:
        #    print(cookie)
            if cookie['name'] == '_live_bcui_session_id':
                found_new_user_cookie = True

        driver.close()
        self.assertTrue(found_new_user_cookie)

    def test_tpl_login(self):
        driver = self.create_webdriver()
        tpl = TPL(driver)
        tpl.login(self.login_info['t'][0],self.login_info['t'][1])
        cookies = tpl.driver.get_cookies()
        found_new_user_cookie = False
        for cookie in cookies:
            if cookie['name'] == 'new-account':
                found_new_user_cookie = True
        driver.close()
        self.assertTrue(found_new_user_cookie)
        
    def test_wpl_holds_returns_items(self):
        # check that a list exclusively contains items of a specific type
        driver = self.create_webdriver()
        wpl = WPL(driver)
        holds = wpl.items_on_hold(self.login_info['w'][0],self.login_info['w'][1])
        driver.close()
        #print(holds)
        for item in holds:
            self.assertTrue(type(item) == Item, f"type(item) is {type(item)}")


    def test_wpl_scrapes_items_on_hold(self):
        # check that a list exclusively contains items of a specific type
        driver = self.create_webdriver()
        wpl = WPL(driver)
        holds = wpl.items_on_hold(self.login_info['w'][0],self.login_info['w'][1])
        driver.close()
        #print(holds)
        for item in holds:
            self.assertTrue(item.is_hold, "Item is not on hold")
    
    def test_wpl_scrapes_items_checked_out(self):
        driver = self.create_webdriver()
        wpl = WPL(driver)
        check_outs = wpl.items_checked_out(self.login_info['w'][0],self.login_info['w'][1])
        driver.close()
        for item in check_outs:
            print(item.text_string())
            self.assertTrue(type(item) == Item, f"type(item) is {type(item)}")

    def test_wpl_scrapes_hours_given_branch(self):
        
        branch = "Rossland"
        driver = self.create_webdriver()
        wpl = WPL(driver)
        hours = wpl.hours(branch)
        if branch == "Central":
            self.assertRegex(hours, branch + " Library")
        else:
            self.assertRegex(hours, branch + " Branch")
        driver.close()

    def test_ppl_scrapes_items_on_hold(self):
        driver = self.create_webdriver()
        ppl = PPL(driver)
        on_hold = ppl.items_on_hold(self.login_info['p'][0],self.login_info['p'][1])
        for item in on_hold:
            print(item.text_string())
            self.assertTrue(type(item) == Item, f"type(item) is {type(item)}")
        driver.close()

    def test_ppl_scrapes_items_checked_out(self):
        driver = self.create_webdriver()
        ppl = PPL(driver)
        check_outs = ppl.items_checked_out(self.login_info['p'][0],self.login_info['p'][1])
        #print(check_outs)
        driver.close()
        for item in check_outs:
            print(item.text_string())
            self.assertTrue(type(item) == Item, f"type(item) is {type(item)}")

    def test_ppl_scrapes_hours_given_branch(self):
        driver = self.create_webdriver()
        branch = "Claremont Library"
        ppl = PPL(driver)
        hours = ppl.hours(branch)
        print(hours)
        self.assertRegex(hours, branch)
        driver.close()

    def test_tpl_scrapes_items_on_hold(self):
        driver = self.create_webdriver()
        tpl = TPL(driver)
        holds = tpl.items_on_hold(self.login_info['t'][0], self.login_info['t'][1])
        driver.close()
        for item in holds:
            print(item.text_string())
            self.assertTrue(type(item) == Item, f"type(item) is {type(item)}")
        
    
    def test_tpl_scrapes_items_checked_out(self):
        driver = self.create_webdriver()
        tpl = TPL(driver)
        checkouts = tpl.items_checked_out(self.login_info['t'][0], self.login_info['t'][1])
        driver.close()
        for item in checkouts:
            print(item.text_string())
            self.assertTrue(type(item) == Item, f"type(item) is {type(item)}")
        

    def test_tpl_scrapes_hours_given_branch(self):
        
        branch = "Highland Creek"
        driver = self.create_webdriver()
        tpl = TPL(driver)
        hours = tpl.hours(branch)
        self.assertRegex(hours, branch)
        driver.close()


    def drafttest_durham_library_sends_text_message(self):
        driver = self.create_webdriver()
        ppl = PPL(driver)
        checkouts = ppl.items_checked_out(self.login_info['p'][0],self.login_info['p'][1])
        response = ppl.send_checkouts_text(checkouts)
        print(response)
        self.assertIsNotNone(response)
        driver.close()
        pass

    def test_durham_library_formulates_text_message(self):
        driver = self.create_webdriver()
        ppl = PPL(driver)
        checkouts = ppl.items_checked_out(self.login_info['p'][0],self.login_info['p'][1])
        res = ppl.formulate_checkouts_text(checkouts)
        print(res)
        self.assertIsNotNone(res) # TODO: Assert with regex
        driver.close()