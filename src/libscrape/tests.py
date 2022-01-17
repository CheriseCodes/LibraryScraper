"""
Unit test suite for every class and method in library.py
"""
from cmath import exp
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

        self.with_ui = False

        self.mock_durham_checkouts = [
            Item(date_retrieved="2022-01-13", title='Bach', contributors='by Grimaud, Hélène', item_format='Music CD',
                 is_hold=False, item_date='Oct. 20, 2021', status='Due Later', branch='',
                 system='durham'),
            Item(date_retrieved="2022-01-13", title='Nature', item_format='DVD', is_hold=False,
                 item_date='Oct. 20, 2021', status='Due Later', branch='', system='durham'),
            Item(date_retrieved="2022-01-13", title='The Defining Decade', contributors='by Jay, Meg',
                 item_format='Book', is_hold=False, item_date='Nov. 03, 2021', status='Due Later', branch='',
                 system='durham'),
            Item(date_retrieved="2022-01-13", title='Studying Soil', item_format='Book', is_hold=False,
                 status='Overdue', system='durham'),
            Item(date_retrieved="2022-01-13", title='What I Talk About When I Talk About Running',
                 contributors='by Murakami, Haruki', item_format='Book', is_hold=False,
                 item_date='Nov. 03, 2021', status='Due Later', system='durham')]

        self.mock_durham_holds = [
            Item(date_retrieved="2022-01-13", title='Lynyrd Skynyrd: Gold', contributors='by Lynyrd Skynyrd',
                 item_format='Music CD', is_hold=True, item_date=' Oct. 15, 2021', status='Ready',
                 branch='Central Library', system='durham'),
            Item(date_retrieved="2022-01-13", title="6 Traits of the World's Most Productive Companies",
                 item_format='DVD', is_hold=True, item_date='May 19, 2022',
                 status='Not Ready', branch='Central Library', system='durham')]

        self.mock_toronto_checkouts = [Item(date_retrieved="2022-01-13",
                                            title='Test-driven development with React : apply test-driven development'
                                                  + ' in your applications', contributors='by Qiu, Juntao',
                                            item_format='Book', is_hold=False, item_date='Yesterday',
                                            status='Overdue', branch='', system='toronto'),
                                       Item(date_retrieved="2022-01-13",
                                            title='Learning React : modern patterns for developing React apps',
                                            contributors='by Banks, Alex (Software engineer)', item_format='Book',
                                            is_hold=False, item_date='Sat 16 Oct',
                                            status='Due Tomorrow', branch='', system='toronto'),
                                       Item(date_retrieved="2022-01-13", title='The rope', contributors='by Barr',
                                            item_format='Compact Disc Set', is_hold=False,
                                            item_date='Sat 16 Oct', status='Due Tomorrow', branch='', system='toronto'),
                                       Item(date_retrieved="2022-01-13", title='The object-oriented thought process',
                                            contributors='by Weisfeld, Matt A.',
                                            item_format='Book', is_hold=False, item_date='Wed 20 Oct',
                                            status='Due Later', branch='', system='toronto'),
                                       Item(date_retrieved="2022-01-13",
                                            title='Test-driven development with Python : obey the testing goat: using' +
                                                  'Django, Selenium, and JavaScript', contributors='by Percival, Harry',
                                            item_format='Book', is_hold=False,
                                            item_date='Tue 2 Nov', status='Due Later', branch='', system='toronto')]

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
        library_obj.login(self.login_info['w'][0], self.login_info['w'][1],
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
        res_title = library_obj.driver.title
        library_obj.driver.close()
        self.assertEqual(res_title, "My WPL | Whitby Public Library | BiblioCommons")

    def test_ppl_login(self):
        driver = self.create_webdriver()
        library_obj = PPL(driver)
        library_obj.login(self.login_info['p'][0], self.login_info['p'][1],
                          url="https://pickering.bibliocommons.com/user/login?destination=%2Fdashboard%2Fuser" +
                              "_dashboard%3F&_ga=2.48438821.225519067.1641940790-1406162599.1640825023")
        sleep(8)
        res_title = library_obj.driver.title
        library_obj.driver.close()
        self.assertEqual(res_title, "My PPL | Pickering Public Library | BiblioCommons")

    def test_tpl_login(self):
        driver = self.create_webdriver()
        library_obj = TPL(driver)
        library_obj.login(self.login_info['t'][0], self.login_info['t'][1])
        sleep(3)
        res_title = library_obj.driver.title
        library_obj.driver.close()
        self.assertEqual(res_title, "Account Summary : Toronto Public Library")

    def test_wpl_attains_hold_data(self):
        holds_page = "/sample_pages/wpl-holds-Jan-05-2022.html"
        # holds_page = "/sample_pages/wpl-holds-Jan-13-2022.html"
        f = open(curr_path + holds_page, "r")
        page_source = f.read()
        hold_data = WPL.hold_data(page_source)
        f.close()
        # print(hold_data)
        exp_result = [
            ['Select. Item 1. Fullmetal Alchemist.', 'Fullmetal Alchemist', 'Fullmetal Alchemist, Book', '1', 'by ',
             'Arakawa, Hiromu', 'Book', ' - ', '2005', 'Book, 2005. Language: English', '\xa0', 'View details',
             'View details for Fullmetal Alchemist, Book, ', 'Not ready', '#1', ' on 2 copies', 'Pick up at ',
             'Central Library', 'Expires on ', 'Dec. 21, 2023', 'Pause hold', 'Cancel hold', 'For Later', 'Add ',
             'Fullmetal Alchemist', 'Book', ' ', 'by ', 'Arakawa, Hiromu', ' to your for later shelf', 'Add ',
             'Fullmetal Alchemist', 'Book', ' ', 'by ', 'Arakawa, Hiromu', ' to a different shelf', 'Placed on ',
             'Dec. 21, 2021']]
        self.assertListEqual(hold_data, exp_result)

    def test_ppl_attains_hold_data(self):
        f = open(curr_path + "/sample_pages/ppl-holds-Jan-12-2022.html", "r")
        hold_data = PPL.hold_data(f.read())
        f.close()
        # print(hold_data)
        exp_result = [
            ['Select. Item 1. France.', 'France', 'France, DVD', 'DVD', ' - ', '2002', 'DVD, 2002. Language: English',
             '\xa0', 'View details', 'View details for France, DVD, ', 'Not ready', '#1', ' on 1 copies', 'Pick up at ',
             'Central Library', 'Expires on ', 'Oct. 09, 2022', 'Pause hold', 'Cancel hold', 'For Later', 'Add ',
             'France', 'DVD', ' ', ' to your for later shelf', 'Add ', 'France', 'DVD', ' ', ' to a different shelf',
             'Placed on ', 'Jan. 12, 2022'],
            ['Select. Item 2. Rated R.', 'Rated R', 'Rated R, Music CD', 'by ', 'Rihanna', 'Music CD', ' - ', '2009',
             'Music CD, 2009. Language: English', '\xa0', 'View details', 'View details for Rated R, Music CD, ',
             'Not ready', '#1', ' on 1 copies', 'Pick up at ', 'Central Library', 'Expires on ', 'Oct. 09, 2022',
             'Pause hold', 'Cancel hold', 'For Later', 'Add ', 'Rated R', 'Music CD', ' ', 'by ', 'Rihanna',
             ' to your for later shelf', 'Add ', 'Rated R', 'Music CD', ' ', 'by ', 'Rihanna', ' to a different shelf',
             'Placed on ', 'Jan. 12, 2022'],
            ['Select. Item 3. Neon Genesis Evangelion.', 'Neon Genesis Evangelion', 'Neon Genesis Evangelion, Book',
             'Volume One', 'by ', 'Sadamoto, Yoshiyuki', 'Book', ' - ', '2004', 'Book, 2004. Language: English', '\xa0',
             'View details', 'View details for Neon Genesis Evangelion, Book, ', 'Not ready', '#1', ' on 1 copies',
             'Pick up at ', 'Central Library', 'Expires on ', 'Oct. 09, 2022', 'Pause hold', 'Cancel hold', 'For Later',
             'Placed on ', 'Jan. 12, 2022']]
        self.assertListEqual(hold_data, exp_result)
        # save_output_as_txt(str(hold_data), "ppl_hold_data")

    def test_tpl_attains_hold_data(self):
        f = open(curr_path + "/sample_pages/tpl-holds-Dec-30-2021.html", "r")
        hold_data = TPL.hold_data(f.read())
        f.close()
        # print(hold_data)
        exp_res = [[' ', ' ', 'Modern Java in action : lambda, streams, functional and reactive programming',
                    'Urma, Raoul-Gabriel, author.', 'Book', 'North York Central Library', 'Pick up by', 'Thu 6 Jan',
                    '(', '7 Days Left', ')', 'Cancel']]
        self.assertListEqual(hold_data, exp_res)

    def test_wpl_attains_checkout_data(self):
        f = open(curr_path + "/sample_pages/wpl-checkouts-Jan-05-2022.html", "r")
        page_source = f.read()
        checkout_data = WPL.checkout_data(page_source)
        f.close()
        exp_res = [['Select. Item 1. My Life in Full.', 'My Life in Full', 'My Life in Full, Book',
                    'Work, Family, and Our Future', 'by ', 'Nooyi, Indra K.', 'Book', ' - ', '2021',
                    'Book, 2021. Language: English', 'You have not rated this title. Rate this title', 'Rate this',
                    'Due later', '6 days  remaining ', 'Due by ', 'Jan. 11, 2022', '2 people waiting', 'Renew',
                    'In Progress', 'Add ', 'My Life in Full', 'Book', ' ', 'by ', 'Nooyi, Indra K.',
                    ' to your in progress shelf', 'Add ', 'My Life in Full', 'Book', ' ', 'by ', 'Nooyi, Indra K.',
                    ' to a different shelf']]
        self.assertListEqual(checkout_data, exp_res)
        # save_output_as_txt(str(checkout_data), "wpl_checkout_data")

    def test_ppl_attains_checkout_data(self):
        f = open(curr_path + "/sample_pages/ppl-checkouts-Jan-05-2022.html", "r")
        page_source = f.read()
        checkout_data = PPL.checkout_data(page_source)
        f.close()
        exp_res = [
            ['Select. Item 1. This Is Glenn Gould - Story of A Genius.', 'This Is Glenn Gould - Story of A Genius',
             'This Is Glenn Gould - Story of A Genius, Music CD', 'by ', 'Bach, Johann Sebastian', 'Music CD', ' - ',
             '2012', 'Music CD, 2012. Language: English', 'You have not rated this title. Rate this title', 'Rate this',
             'Due later', '21 days  remaining ', 'Due by ', 'Jan. 26, 2022', 'Renewed', ' ', '5 times', 'Renew',
             'In Progress', 'Add ', 'This Is Glenn Gould - Story of A Genius', 'Music CD', ' ', 'by ',
             'Bach, Johann Sebastian', ' to your in progress shelf', 'Add ', 'This Is Glenn Gould - Story of A Genius',
             'Music CD', ' ', 'by ', 'Bach, Johann Sebastian', ' to a different shelf']]
        self.assertListEqual(checkout_data, exp_res)
        # save_output_as_txt(str(checkout_data), "ppl_checkout_data")

    def test_tpl_attains_checkout_data(self):
        f = open(curr_path + "/sample_pages/tpl-checkouts-Jan-05-2022.html", "r")
        page_source = f.read()
        checkout_data = TPL.checkout_data(page_source)
        f.close()
        exp_res = [[' ',
                    'The bully-proof workplace : essential strategies, tips, and scripts for dealing with the office'
                    + ' sociopath', ' ',
                    'The bully-proof workplace : essential strategies, tips, and scripts for dealing with the office'
                    + ' sociopath',
                    'Dean, Peter J., 1946- author.', 'Book', '37131 187 370 002', 'Tue 11 Jan', '0', 'Renew'],
                   [' ', 'How to win : 36 ancient strategies for success', ' ',
                    'How to win : 36 ancient strategies for success', 'Wong, Eva, author.', 'Book', '37131 214 228 918',
                    'Mon 24 Jan', '1', 'Renew'],
                   [' ', 'Programming AWS lambda : build and deploy serverless applications with Java', ' ',
                    'Programming AWS lambda : build and deploy serverless applications with Java',
                    'Chapin, John, author.', 'Book', '37131 201 530 110', 'Mon 24 Jan', '1', 'Renew'],
                   [' ', 'Learning Amazon Web Services (AWS) : a hands-on guide to the fundamentals of AWS cloud', ' ',
                    'Learning Amazon Web Services (AWS) : a hands-on guide to the fundamentals of AWS cloud',
                    'Wilkins, Mark, author.', 'Book', '37131 115 211 575', 'Mon 24 Jan', '1', 'Renew'],
                   [' ', 'Hinduism', ' ', 'Hinduism', 'Sen, Kshitimohan, author.', 'Book', '37131 212 560 387',
                    'Tue 25 Jan', '2', 'Renew'],
                   [' ', 'Spring boot : up and running : building Cloud Native Java and Kotlin applications', ' ',
                    'Spring boot : up and running : building Cloud Native Java and Kotlin applications',
                    'Heckler, Mark, author.', 'Book', '37131 218 066 579', 'Tue 25 Jan', '0', 'Renew'],
                   [' ', 'Modern Java in action : lambda, streams, functional and reactive programming', ' ',
                    'Modern Java in action : lambda, streams, functional and reactive programming',
                    'Urma, Raoul-Gabriel, author.', 'Book', '37131 193 289 261', 'Tue 25 Jan', '0', 'Renew']]
        self.assertListEqual(checkout_data, exp_res)

    def test_durham_parses_hold_data_into_item(self):
        # check that a list exclusively contains items of a specific type
        hold_data = [['Select. Item 2. Why Do We Fight?.', 'Why Do We Fight?', 'Why Do We Fight?, Book',
                      'Conflict, War, and Peace', 'by ', 'Walker, Niki', 'Book', ' - ', '2013',
                      'Book, 2013. Language: English', '\xa0', 'View details',
                      'View details for Why Do We Fight?, Book, ', 'Not ready', '#1', ' on 1 copies', 'Pick up at ',
                      'Central Library', 'Expires on ', 'Jan. 13, 2024', 'Pause hold', 'Cancel hold', 'For Later',
                      'Placed on ', 'Jan. 13, 2022'],
                     ['Select. Item 1. Fullmetal Alchemist.', 'Fullmetal Alchemist', 'Fullmetal Alchemist, Book', '1',
                      'by ', 'Arakawa, Hiromu', 'Book', ' - ', '2005', 'Book, 2005. Language: English', '\xa0',
                      'View details', 'View details for Fullmetal Alchemist, Book, ', 'Not ready', '#1', ' on 2 copies',
                      'Pick up at ', 'Central Library', 'Expires on ', 'Dec. 21, 2023', 'Pause hold', 'Cancel hold',
                      'For Later', 'Add ', 'Fullmetal Alchemist', 'Book', ' ', 'by ', 'Arakawa, Hiromu',
                      ' to your for later shelf', 'Add ', 'Fullmetal Alchemist', 'Book', ' ', 'by ', 'Arakawa, Hiromu',
                      ' to a different shelf', 'Placed on ', 'Dec. 21, 2021']]
        library_obj = DurhamLibrary()
        # print(hold_data)
        hold_items = library_obj.parse_hold_data(hold_data)
        exp_items = [
            Item(date_retrieved="2022-01-13", title="Why Do We Fight?", contributors="Walker, Niki", item_format="Book",
                 is_hold=True, status="Not Ready", item_date="Jan. 13, 2024", branch="Central Library",
                 system="durham"),
            Item(date_retrieved="2022-01-13", title="Fullmetal Alchemist", contributors="Arakawa, Hiromu",
                 item_format="Book", is_hold=True, status="Not Ready", item_date="Dec. 21, 2023",
                 branch="Central Library", system="durham")]
        for i in range(len(exp_items)):
            # print(hold_items[i])
            # print(exp_items[i])
            # print(exp_items[i] == hold_items[i])
            self.assertTrue(hold_items[i] == exp_items[i])

    def test_toronto_parses_hold_data_into_item(self):
        # TODO: Correct indexes for TPL
        hold_data = [' ', ' ', 'Modern Java in action : lambda, streams, functional and reactive programming',
                     'Urma, Raoul-Gabriel, author.', 'Book', 'North York Central Library', 'Pick up by', 'Thu 6 Jan',
                     '(', '7 Days Left', ')', 'Cancel']
        exp_item = Item(date_retrieved="2022-01-13",
                        title="Modern Java in action : lambda, streams, functional and reactive programming",
                        contributors="Urma, Raoul-Gabriel", item_format="Book",
                        is_hold=True, status="Ready", item_date="Thu 6 Jan", branch="North York Central Library",
                        system="toronto")

        hold_item = TPL.parse_hold_data(hold_data)
        # print("hold_item:", hold_item)
        # print("exp_item:", exp_item)
        self.assertTrue(exp_item == hold_item)

    def test_toronto_parses_checkout_data_into_item(self):
        checkout_data = [' ', 'Programming AWS lambda : build and deploy serverless applications with Java', ' ',
                         'Programming AWS lambda : build and deploy serverless applications with Java',
                         'Chapin, John, author.', 'Book', '37131 201 530 110', 'Mon 24 Jan', '1', 'Renew']
        checkout_item = TPL.parse_checkout_data(checkout_data)
        exp_item = Item(date_retrieved="2022-01-13",
                        title='Programming AWS lambda : build and deploy serverless applications with Java',
                        contributors="Chapin, John", item_format="Book",
                        is_hold=False, status="Due Later", item_date="Mon 24 Jan", system="toronto")
        # print("exp_item:",exp_item)
        # print("checkout_item:",checkout_item)
        self.assertTrue(exp_item == checkout_item)

    def test_wpl_scrapes_hours_given_branch(self):
        branch = "Central"
        f = open(curr_path + "/sample_pages/wpl-hours-Jan-13-2022.html", "r")
        page_source = f.read()
        hours = WPL._hours(page_source, branch)
        f.close()
        # print(hours)
        exp_hours = """
        Central Library
        405 Dundas Street West, Whitby, ON, L1N 6A1
        905-668-6531
        Monday–Thursday 9:30 a.m.–9:00 p.m.
        Friday 9:30 a.m.–6:00 p.m.
        Saturday 9:00 a.m.–5:00 p.m.
        Sunday Closed
        """
        exp_hours = list(filter(lambda item: item != '', [x.strip() for x in exp_hours.split('\n')]))
        hours = hours.split('\n')
        # print(exp_hours)
        # print(hours)
        self.assertListEqual(hours, exp_hours)

    def test_ppl_scrapes_hours_given_branch(self):
        full_branch_name = "Central Library Hours\n"
        f = open(curr_path + "/sample_pages/ppl-cn-hours-Jan-13-2022.html", "r")
        page_source = f.read()
        hours = PPL._hours(page_source, full_branch_name)
        f.close()
        exp_hours = "Central Library Hours\n\nOpen today until 9:00pm\n\nMonday \n9:30AM - 9:00PM\n\nTuesday " \
                    + "\n9:30AM - 9:00PM\n\nWednesday \n9:30AM - 9:00PM\n\nThursday \n9:30AM - 9:00PM\n\nFriday " \
                    + "\n9:30AM - 9:00PM\n\nSaturday \n9:30AM - 4:30PM\n\nSunday \nClosed\n\n\n"
        exp_hours = [x.strip() for x in exp_hours.split('\n')]
        hours = [y.strip() for y in hours.split('\n')]
        # print(hours)
        # print(exp_hours)
        self.assertTrue(exp_hours == hours)

    def test_tpl_scrapes_hours_given_branch(self):
        branch = "Malvern"
        f = open(curr_path + "/sample_pages/tpl-hours-Jan-13-2022.html", "r")
        page_source = f.read()
        hours = TPL._hours(branch, page_source)
        f.close()
        exp_hours = """Malvern
        30 Sewells Road
        Toronto,
        ON 
        M1B 3G5
        416-396-8969
        View on map
        Wheelchair Accessible
        Free Wifi
        Hours
        Monday
        9:00 am
        to
        8:30 pm
        Tuesday
        9:00 am
        to
        8:30 pm
        Wednesday
        9:00 am
        to
        8:30 pm
        Thursday
        9:00 am
        to
        8:30 pm
        Friday
        9:00 am
        to
        8:30 pm
        Saturday
        9:00 am
        to
        5:00 pm
        Sunday
        1:30 pm
        to
        5:00 pm"""
        exp_hours = [x.strip() for x in exp_hours.split('\n')]
        hours = [y.strip() for y in hours.split('\n')]
        # print(exp_hours)
        # print(hours)
        self.assertEqual(hours, exp_hours)

    def test_messenger_formulates_checkouts_as_plain_text(self):
        # checkouts = library_obj.items_checked_out(self.login_info['p'][0], self.login_info['p'][1])
        messenger = Messenger("Pickering Public Library")
        text = messenger.formulate_checkouts_text(self.mock_durham_checkouts, "plain")
        exp_text = f"""Pickering Public Library CHECKOUTS ({date.today()}):
        1. Bach (Music CD) by Grimaud, Hélène | Due Later | Oct. 20, 2021
        2. Nature (DVD)  | Due Later | Oct. 20, 2021
        3. The Defining Decade (Book) by Jay, Meg | Due Later | Nov. 03, 2021
        4. Studying Soil (Book)  | Overdue | 
        5. What I Talk About When I Talk About Running (Book) by Murakami, Haruki | Due Later | Nov. 03, 2021
        """
        exp_text = [x.strip() for x in
                    list(filter(lambda item: item != '' and not (item.isspace()), exp_text.split('\n')))]
        text = [y.strip() for y in list(filter(lambda item: (item != '') and not (item.isspace()), text.split('\n')))]
        # print(text)
        # print(exp_text)
        self.assertEqual(text, exp_text)
