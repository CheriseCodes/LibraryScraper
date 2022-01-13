"""
Unit test suite for every class and method in library.py
"""
from time import sleep
from typing import List
import unittest
from library import WPL, PPL, TPL, DurhamLibrary, Item
from parser_utils import *
from selenium import webdriver
from datetime import date
import os

from lib_assets import Messenger

from parser_utils import save_output_as_html

curr_path = os.path.dirname(__file__)

class Library(unittest.TestCase):
    def setUp(self):
        self.login_info = {"p": (os.environ['PPL_USER'], os.environ['PPL_PASS']),
                           "w": (os.environ['WPL_USER'], os.environ['WPL_PASS']),
                           "t": (os.environ['TPL_USER'], os.environ['TPL_PASS'])}

        self.with_ui = True

        self.mock_durham_checkouts = [
            Item(date.today(), 'Bach', 'by Grimaud, Hélène', 'Music CD', False, 'Oct. 20, 2021', 'Due Later', '',
                 'durham'),
            Item(date.today(), 'Nature', '', 'DVD', False, 'Oct. 20, 2021', 'Due Later', '', 'durham'),
            Item(date.today(), 'The Defining Decade', 'by Jay, Meg', 'Book', False, 'Nov. 03, 2021', 'Due Later', '',
                 'durham'),
            Item(date.today(), 'Studying Soil', 'Book - 2013', 'Book', False, 'Renewed 1 time', 'Overdue', '',
                 'durham'),
            Item(date.today(), 'What I Talk About When I Talk About Running', 'by Murakami, Haruki', 'Book', False,
                 'Nov. 03, 2021', 'Due Later', '', 'durham')]

        self.mock_durham_holds = [
            Item(date.today(), 'Lynyrd Skynyrd: Gold', 'by Lynyrd Skynyrd', 'Music CD', True, ' Oct. 15, 2021', 'Ready',
                 'Pick up at Central Library', 'durham'),
            Item(date.today(), "6 Traits of the World's Most Productive Companies", '', 'DVD', True, 'May 19, 2022',
                 'Not Ready', 'Pick up at Central Library', 'durham')]

        self.mock_toronto_checkouts = [Item(date.today(),
                                            'Test-driven development with React : apply test-driven development in' +
                                            'your applications', 'by Qiu, Juntao', 'Book', False, 'Yesterday',
                                            'Overdue', '', 'toronto'),
                                       Item(date.today(), 'Learning React : modern patterns for developing React apps',
                                            'by Banks, Alex (Software engineer)', 'Book', False, 'Sat 16 Oct',
                                            'Due Tomorrow', '', 'toronto'),
                                       Item(date.today(), 'The rope', 'by Barr', 'Compact Disc Set', False,
                                            'Sat 16 Oct', 'Due Tomorrow', '', 'toronto'),
                                       Item(date.today(), 'The object-oriented thought process', 'by Weisfeld, Matt A.',
                                            'Book', False, 'Wed 20 Oct', 'Due Later', '', 'toronto'), Item(date.today(),
                                            'Test-driven development with Python : obey the testing goat: using'+
                                            'Django, Selenium, and JavaScript', 'by Percival, Harry', 'Book', False,
                                            'Tue 2 Nov', 'Due Later', '','toronto')]

        self.mock_toronto_holds = []

        # TODO: Create mock checkout and hold page for each branch

    def create_webdriver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--log-level=3')
        if not self.with_ui:
            options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        return driver

    def save_current_tpl_checkouts_page(self):
        driver = self.create_webdriver()
        library_obj = TPL(driver)
        library_obj.login(self.login_info['t'][0], self.login_info['t'][1],
                          url="https://account.torontopubliclibrary.ca/signin?redirect=%2Fcheckouts")
        sleep(3)
        save_output_as_html(library_obj.driver.page_source, "tpl-checkouts")
        driver.close()

    def save_current_tpl_holds_page(self):
        driver = self.create_webdriver()
        library_obj = TPL(driver)
        library_obj.login(self.login_info['t'][0], self.login_info['t'][1],
                          url="https://https://account.torontopubliclibrary.ca/signin?redirect=%2Fholds")
        sleep(3)
        save_output_as_html(library_obj.driver.page_source, "tpl-holds")
        driver.close()

    def save_current_wpl_holds_page(self):
        driver = self.create_webdriver()
        library_obj = WPL(driver)
        library_obj.login(self.login_info['w'][0],self.login_info['w'][1],
                          url="https://whitby.bibliocommons.com/v2/holds")
        sleep(3)
        save_output_as_html(library_obj.driver.page_source, "wpl-holds")
        driver.close()

    def save_current_wpl_checkouts_page(self):
        driver = self.create_webdriver()
        library_obj = WPL(driver)
        library_obj.login(self.login_info['w'][0], self.login_info['w'][1],
                          url="https://whitby.bibliocommons.com/v2/checkedout")
        sleep(10)
        save_output_as_html(library_obj.driver.page_source, "wpl-checkouts")
        driver.close()

    def save_current_ppl_holds_page(self):
        driver = self.create_webdriver()
        library_obj = PPL(driver)
        library_obj.login(self.login_info['p'][0], self.login_info['p'][1],
                          url="https://pickering.bibliocommons.com/user/login?destination=%2Fv2%2Fholds")
        sleep(10)
        save_output_as_html(library_obj.driver.page_source, "ppl-holds")
        driver.close()

    def save_current_ppl_checkouts_page(self):
        driver = self.create_webdriver()
        library_obj = PPL(driver)
        library_obj.login(self.login_info['p'][0], self.login_info['p'][1],
                          url="https://pickering.bibliocommons.com/user/login?destination=%2Fcheckedout")
        sleep(10)
        save_output_as_html(library_obj.driver.page_source, "ppl-checkouts")
        driver.close()

    def test_wpl_login(self):
        driver = self.create_webdriver()
        library_obj = WPL(driver)
        library_obj.login(self.login_info['w'][0], self.login_info['w'][1])
        sleep(8)
        res_title=library_obj.driver.title
        library_obj.driver.close()
        self.assertEquals(res_title, "My WPL | Whitby Public Library | BiblioCommons")

    def test_ppl_login(self):
        driver = self.create_webdriver()
        library_obj = PPL(driver)
        library_obj.login(self.login_info['p'][0], self.login_info['p'][1])
        sleep(8)
        res_title = library_obj.driver.title
        library_obj.driver.close()
        self.assertEquals(res_title, "My PPL | Whitby Public Library | BiblioCommons")

    def test_tpl_login(self):
        driver = self.create_webdriver()
        library_obj = TPL(driver)
        library_obj.login(self.login_info['t'][0], self.login_info['t'][1])
        sleep(3)
        res_title = library_obj.driver.title
        library_obj.driver.close()
        self.assertEquals(res_title, "Account Summary : Toronto Public Library")

    def test_wpl_attains_hold_data(self):
        f = open(curr_path + "/sample_pages/wpl-holds-Jan-05-2022.html", "r")
        page_source = f.read()
        hold_data = WPL.hold_data(page_source)
        f.close()
        print(hold_data)
        exp_result = [['Select. Item 1. Fullmetal Alchemist.', 'Fullmetal Alchemist', 'Fullmetal Alchemist, Book', '1', 'by ', 'Arakawa, Hiromu', 'Book', ' - ', '2005', 'Book, 2005. Language: English', '\xa0', 'View details', 'View details for Fullmetal Alchemist, Book, ', 'Not ready', '#1', ' on 2 copies', 'Pick up at ', 'Central Library', 'Expires on ', 'Dec. 21, 2023', 'Pause hold', 'Cancel hold', 'For Later', 'Add ', 'Fullmetal Alchemist', 'Book', ' ', 'by ', 'Arakawa, Hiromu', ' to your for later shelf', 'Add ', 'Fullmetal Alchemist', 'Book', ' ', 'by ', 'Arakawa, Hiromu', ' to a different shelf', 'Placed on ', 'Dec. 21, 2021']]
        self.assertListEqual(hold_data, exp_result)

    def test_ppl_attains_hold_data(self):
        f = open(curr_path + "/sample_pages/ppl-holds-Jan-12-2022.html", "r")
        hold_data = PPL.hold_data(f.read())
        f.close()
        #print(hold_data)
        exp_result = [['Select. Item 1. France.', 'France', 'France, DVD', 'DVD', ' - ', '2002', 'DVD, 2002. Language: English', '\xa0', 'View details', 'View details for France, DVD, ', 'Not ready', '#1', ' on 1 copies', 'Pick up at ', 'Central Library', 'Expires on ', 'Oct. 09, 2022', 'Pause hold', 'Cancel hold', 'For Later', 'Add ', 'France', 'DVD', ' ', ' to your for later shelf', 'Add ', 'France', 'DVD', ' ', ' to a different shelf', 'Placed on ', 'Jan. 12, 2022'], ['Select. Item 2. Rated R.', 'Rated R', 'Rated R, Music CD', 'by ', 'Rihanna', 'Music CD', ' - ', '2009', 'Music CD, 2009. Language: English', '\xa0', 'View details', 'View details for Rated R, Music CD, ', 'Not ready', '#1', ' on 1 copies', 'Pick up at ', 'Central Library', 'Expires on ', 'Oct. 09, 2022', 'Pause hold', 'Cancel hold', 'For Later', 'Add ', 'Rated R', 'Music CD', ' ', 'by ', 'Rihanna', ' to your for later shelf', 'Add ', 'Rated R', 'Music CD', ' ', 'by ', 'Rihanna', ' to a different shelf', 'Placed on ', 'Jan. 12, 2022'], ['Select. Item 3. Neon Genesis Evangelion.', 'Neon Genesis Evangelion', 'Neon Genesis Evangelion, Book', 'Volume One', 'by ', 'Sadamoto, Yoshiyuki', 'Book', ' - ', '2004', 'Book, 2004. Language: English', '\xa0', 'View details', 'View details for Neon Genesis Evangelion, Book, ', 'Not ready', '#1', ' on 1 copies', 'Pick up at ', 'Central Library', 'Expires on ', 'Oct. 09, 2022', 'Pause hold', 'Cancel hold', 'For Later', 'Placed on ', 'Jan. 12, 2022']]
        self.assertListEqual(hold_data,exp_result)
        #save_output_as_txt(str(hold_data), "ppl_hold_data")

    def test_tpl_attains_hold_data(self):
        f = open(curr_path + "/sample_pages/tpl-holds-Dec-30-2021.html", "r")
        hold_data = TPL.hold_data(f.read())
        f.close()
        #print(hold_data)
        exp_res = [[' ', ' ', 'Modern Java in action : lambda, streams, functional and reactive programming', 'Urma, Raoul-Gabriel, author.', 'Book', 'North York Central Library', 'Pick up by', 'Thu 6 Jan', '(', '7 Days Left', ')', 'Cancel']]
        self.assertListEqual(hold_data, exp_res)

    def test_wpl_attains_checkout_data(self):
        f = open(curr_path + "/sample_pages/wpl-checkouts-Jan-05-2022.html", "r")
        page_source = f.read()
        checkout_data = WPL.checkout_data(page_source)
        f.close()
        exp_res = [['Select. Item 1. My Life in Full.', 'My Life in Full', 'My Life in Full, Book', 'Work, Family, and Our Future', 'by ', 'Nooyi, Indra K.', 'Book', ' - ', '2021', 'Book, 2021. Language: English', 'You have not rated this title. Rate this title', 'Rate this', 'Due later', '6 days  remaining ', 'Due by ', 'Jan. 11, 2022', '2 people waiting', 'Renew', 'In Progress', 'Add ', 'My Life in Full', 'Book', ' ', 'by ', 'Nooyi, Indra K.', ' to your in progress shelf', 'Add ', 'My Life in Full', 'Book', ' ', 'by ', 'Nooyi, Indra K.', ' to a different shelf']]
        self.assertListEqual(checkout_data, exp_res)
        #save_output_as_txt(str(checkout_data), "wpl_checkout_data")

    def test_ppl_attains_checkout_data(self):
        f = open(curr_path + "/sample_pages/ppl-checkouts-Jan-05-2022.html", "r")
        page_source = f.read()
        checkout_data = PPL.checkout_data(page_source)
        f.close()
        exp_res = [['Select. Item 1. This Is Glenn Gould - Story of A Genius.', 'This Is Glenn Gould - Story of A Genius', 'This Is Glenn Gould - Story of A Genius, Music CD', 'by ', 'Bach, Johann Sebastian', 'Music CD', ' - ', '2012', 'Music CD, 2012. Language: English', 'You have not rated this title. Rate this title', 'Rate this', 'Due later', '21 days  remaining ', 'Due by ', 'Jan. 26, 2022', 'Renewed', ' ', '5 times', 'Renew', 'In Progress', 'Add ', 'This Is Glenn Gould - Story of A Genius', 'Music CD', ' ', 'by ', 'Bach, Johann Sebastian', ' to your in progress shelf', 'Add ', 'This Is Glenn Gould - Story of A Genius', 'Music CD', ' ', 'by ', 'Bach, Johann Sebastian', ' to a different shelf']]
        self.assertListEqual(checkout_data, exp_res)
        #save_output_as_txt(str(checkout_data), "ppl_checkout_data")

    def test_tpl_attains_checkout_data(self):
        f = open(curr_path + "/sample_pages/tpl-checkouts-Jan-05-2022.html", "r")
        page_source = f.read()
        checkout_data = TPL.checkout_data(page_source)
        f.close()
        exp_res = [[' ', 'The bully-proof workplace : essential strategies, tips, and scripts for dealing with the office sociopath', ' ', 'The bully-proof workplace : essential strategies, tips, and scripts for dealing with the office sociopath', 'Dean, Peter J., 1946- author.', 'Book', '37131 187 370 002', 'Tue 11 Jan', '0', 'Renew'], [' ', 'How to win : 36 ancient strategies for success', ' ', 'How to win : 36 ancient strategies for success', 'Wong, Eva, author.', 'Book', '37131 214 228 918', 'Mon 24 Jan', '1', 'Renew'], [' ', 'Programming AWS lambda : build and deploy serverless applications with Java', ' ', 'Programming AWS lambda : build and deploy serverless applications with Java', 'Chapin, John, author.', 'Book', '37131 201 530 110', 'Mon 24 Jan', '1', 'Renew'], [' ', 'Learning Amazon Web Services (AWS) : a hands-on guide to the fundamentals of AWS cloud', ' ', 'Learning Amazon Web Services (AWS) : a hands-on guide to the fundamentals of AWS cloud', 'Wilkins, Mark, author.', 'Book', '37131 115 211 575', 'Mon 24 Jan', '1', 'Renew'], [' ', 'Hinduism', ' ', 'Hinduism', 'Sen, Kshitimohan, author.', 'Book', '37131 212 560 387', 'Tue 25 Jan', '2', 'Renew'], [' ', 'Spring boot : up and running : building Cloud Native Java and Kotlin applications', ' ', 'Spring boot : up and running : building Cloud Native Java and Kotlin applications', 'Heckler, Mark, author.', 'Book', '37131 218 066 579', 'Tue 25 Jan', '0', 'Renew'], [' ', 'Modern Java in action : lambda, streams, functional and reactive programming', ' ', 'Modern Java in action : lambda, streams, functional and reactive programming', 'Urma, Raoul-Gabriel, author.', 'Book', '37131 193 289 261', 'Tue 25 Jan', '0', 'Renew']]
        self.assertListEqual(checkout_data, exp_res)
        print(checkout_data)
    def test_durham_parses_hold_data_into_item(self):
        # check that a list exclusively contains items of a specific type
        hold_data = [['Select. Item 1. Fullmetal Alchemist.', 'Fullmetal Alchemist', 'Fullmetal Alchemist, Book', '1', 'by ', 'Arakawa, Hiromu', 'Book', ' - ', '2005', 'Book, 2005. Language: English', '\xa0', 'View details', 'View details for Fullmetal Alchemist, Book, ', 'Not ready', '#1', ' on 2 copies', 'Pick up at ', 'Central Library', 'Expires on ', 'Dec. 21, 2023', 'Pause hold', 'Cancel hold', 'For Later', 'Add ', 'Fullmetal Alchemist', 'Book', ' ', 'by ', 'Arakawa, Hiromu', ' to your for later shelf', 'Add ', 'Fullmetal Alchemist', 'Book', ' ', 'by ', 'Arakawa, Hiromu', ' to a different shelf', 'Placed on ', 'Dec. 21, 2021']]
        library_obj = DurhamLibrary("Whitby Public Library")
        hold_items = library_obj.parse_hold_data(hold_data)
        # TODO: create a useful assertion
        # TODO: fix associated bug

    def test_wpl_scrapes_holds_page(self):
        f = open(curr_path + "/sample_pages/wpl-holds-Jan-05-2022.html", "r")
        page_source = f.read()
        hold_data = WPL.hold_data(page_source)
        f.close()
        print(hold_data)

    def test_wpl_scrapes_checkouts_page(self):
        f = open(curr_path + "/sample_pages/wpl-checkouts-Jan-05-2022.html", "r")
        page_source = f.read()
        checkout_data = WPL.checkout_data(page_source)
        f.close()
        print(checkout_data)

    def test_wpl_scrapes_hours_given_branch(self):

        branch = "Rossland"
        driver = self.create_webdriver()
        library_obj = WPL(driver)
        hours = library_obj.hours(branch)
        library_obj.driver.close()
        if branch == "Central":
            pass
            # self.assertRegex(hours, branch + " Library")
        else:
            pass
            # self.assertRegex(hours, branch + " Branch")

    def test_ppl_scrapes_holds_page(self):
        f = open(curr_path + "/sample_pages/ppl-holds-Jan-05-2022.html", "r")
        page_source = f.read()
        hold_data = PPL.hold_data(page_source)
        f.close()
        print(hold_data)

    def test_ppl_scrapes_checkouts_page(self):
        f = open(curr_path + "/sample_pages/ppl-checkouts-Jan-05-2022.html", "r")
        page_source = f.read()
        checkouts_data = PPL.hold_data(page_source)
        f.close()
        print(checkouts_data)

    def test_ppl_scrapes_hours_given_branch(self):
        driver = self.create_webdriver()
        branch = "Claremont Library"
        library_obj = PPL(driver)
        hours = library_obj.hours(branch)
        #xprint(hours)
        self.assertRegex(hours, branch)
        library_obj.driver.close()

    def test_tpl_scrapes_holds_page(self):
        f = open(curr_path + "/sample_pages/tpl-holds-Dec-30-2021.html", "r")
        page_source = f.read()
        holds = TPL.hold_data(page_source)
        f.close()

    def test_tpl_scrapes_checkouts_page(self):
        f = open(curr_path + "/sample_pages/tpl-holds-Dec-30-2021.html", "r")
        page_source = f.read()
        checkouts = TPL.checkout_data(page_source)
        f.close()

    def test_tpl_scrapes_hours_given_branch(self):
        branch = "Highland Creek"
        driver = self.create_webdriver()
        library_obj = TPL(driver)
        hours = library_obj.hours(branch)
        self.assertRegex(hours, branch)
        library_obj.driver.close()

    def test_messenger_sends_checkouts_as_plain_text(self):
        #checkouts = library_obj.items_checked_out(self.login_info['p'][0], self.login_info['p'][1])
        messenger = Messenger("Pickering Public Library")
        response = messenger.send_checkouts_text(self.mock_durham_checkouts, 1)

    def test_messenger_sends_checkouts_as_google_doc(self):
        messenger = Messenger("Pickering Public Library")
        response = messenger.formulate_checkouts_text(self.mock_durham_checkouts, 2)

    def test_durham_library_formulates_text_message_in_plain_text(self):
        driver = self.create_webdriver()
        library_obj = PPL(driver)
        checkouts = library_obj.items_checked_out(self.login_info['p'][0], self.login_info['p'][1])
        messenger = Messenger(ppl)
        res = messenger.formulate_checkouts_text(checkouts, 1)
        self.assertIsNotNone(res)  # TODO: Assert with regex
        library_obj.driver.close()

    def test_durham_update_doc(self):
        driver = self.create_webdriver()
        library_obj = WPL(driver)
        checkouts = library_obj.items_checked_out(self.login_info['w'][0], self.login_info['w'][1])
        library_obj.driver.close()
        messenger = Messenger(library_obj)
        messenger.append_doc(checkouts, is_hold=False)

    def test_generate_mock(self):
        driver = self.create_webdriver()
        library_obj = TPL(driver)
        checkouts = library_obj.items_checked_out(self.login_info['t'][0], self.login_info['t'][1])
        for item in checkouts:
            item.generate_mock()
        library_obj.driver.close()
