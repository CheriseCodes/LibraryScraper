"""
Library that containing classes for scraping and processing data from
three library systems: Toronto Public Library, Whitby Public Library,
and Pickering Public Library
Available classes:
- DurhamLibrary: Base class for all libraries in Durham Region
- PPL: Pickering Public Library
- WPL: Whitby Public Library
- TPL: Toronto Public Library
"""

from __future__ import print_function

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from libscrape.lib_parser import *
from libscrape.parse_rule import *

from libscrape.parser_utils import *
from datetime import date
from libscrape.lib_assets import *


class DurhamLibrary:
    def __init__(self, region):
        super().__init__()
        self.checkouts = []
        self.holds = []
        self.region = region
        self.parsers = {"holds": {"DVD": DurhamHoldParser(DurhamDVDHoldRule(2, 2, 8, 7, 10, 9, 9, 8)),
                                  "CD_and_Book": DurhamHoldParser(
                                      DurhamBookAndCDHoldRule(2, 2, 4, 3, 9, 8, 11, 10, 10, 9))},
                        "checkouts": {"DVD": DurhamCheckoutParser(DurhamDVDCheckoutRule(2, 2, 7, 6, 9, 7)),
                                      "CD_and_Book": DurhamCheckoutParser(
                                          DurhamBookAndCDCheckoutRule(2, 2, 4, 3, 8, 7, 9, 8))}}

    @staticmethod
    def select_parser(item_format, parsers):
        """
        Returns the correct parser given the item_format of the item data that is to be parsed
        ----------
        item_format: str
            The item_format of the library items
        parsers: dict
            Dictionary of parsers such that the key is the item_format and the value is the expected parser
        Returns
        -------
        dict
        """
        parser = None
        generic_format = None
        if "DVD" in item_format:
            generic_format = "DVD"
            parser = parsers["DVD"]
        elif "CD" in item_format:
            generic_format = "CD"
            parser = parsers["CD_and_Book"]
        elif "Book" in item_format:
            generic_format = "Book"
            parser = parsers["CD_and_Book"]
        return parser, generic_format

    def parse_hold_data(self, hold_data):
        """
        Parses the hold data and returns a list of corresponding Item objects

        Parameters
        ----------
        hold_data: str[][]
            A list of lists of strings which represent data from the holds page split by the newline character
        Returns
        -------
        Item[]
        """
        res = []
        for lines in hold_data:
            item_format = DurhamHoldParser.format(lines)
            parser, generic_format = self.select_parser(item_format, self.parsers["holds"])
            if parser:

                has_subtitle = DurhamHoldParser.has_subtitle(lines, generic_format)
                title, item_format, contributors, status, item_date, branch = parser.all(lines, generic_format,
                                                                                         has_subtitle)

                hold_item = Item(date.today(), title, contributors, item_format, True, item_date, status,
                                 branch, 'durham')
                if hold_item.title:
                    res.append(hold_item)

        return res

    def parse_checkout_data(self, checkout_data):
        """
        Parses the checkout data and returns a list of corresponding Item objects
        
        Parameters
        ----------
        checkout_data: str[][]
            A list of lists of strings which represent data from the checkouts page split by the newline character
        Returns
        -------
        Item[]
        """
        res = []
        for lines in checkout_data:
            item_format = DurhamCheckoutParser.format(lines)
            parser, generic_format = self.select_parser(item_format, self.parsers["checkouts"])
            if parser:
                has_subtitle = DurhamCheckoutParser.has_subtitle(lines, generic_format)
                title, item_format, contributors, status, item_date = parser.all(lines, generic_format, has_subtitle)
                hold_item = Item(date.today(), title, contributors, item_format, False, item_date, status, '', 'durham')
                if hold_item.title:
                    res.append(hold_item)
        return res


class PPL(DurhamLibrary):
    """Class for Pickering Public Library
    Attributes:
        - driver: an instance of a Selenium Chrome web driver
    """

    def __init__(self, driver):
        super().__init__("Pickering Public Library")
        self.driver = driver

    def hold_data(self, username, password):
        """
        Logs into the holds page and returns a list of lists of textual data for each hold item

        Parameters
        ----------
        username: str
            The username of the account that will be signed into
        password: str
            The password of the account that will be signed into
        Returns
        -------
        str[][]
        """
        res = []

        self.login(username, password, url="https://pickering.bibliocommons.com/user/login?destination=%2Fv2%2Fholds")

        WebDriverWait(driver=self.driver, timeout=10).until(
            EC.title_is("On Hold | Pickering Public Library | BiblioCommons")
        )
        holds = self.driver.find_elements_by_css_selector("div.cp-batch-actions-list-item")

        for item in holds:
            lines = item.text.split('\n')
            res.append(lines)
        return res

    def checkout_data(self, username, password):
        """
        Logs into the checkouts page and returns a list of lists of textual data for each checkout item

        Parameters
        ----------
        username: str
            The username of the account that will be signed into
        password: str
            The password of the account that will be signed into
        Returns
        -------
        str[][]
        """
        res = []

        self.login(username, password, url="https://pickering.bibliocommons.com/user/login?destination=%2Fcheckedout")

        WebDriverWait(driver=self.driver, timeout=10).until(
            EC.title_is("Checked Out | Pickering Public Library | BiblioCommons")
        )

        #save_output_as_html(self.driver.page_source, "ppl-checkouts")

        checkouts = self.driver.find_elements_by_css_selector("div.cp-batch-actions-list-item")

        for item in checkouts:
            lines = item.text.split('\n')
            res.append(lines)
        return res

    def items_on_hold(self, username, password):
        """
        Scrapes and returns the items on hold for the user with the login credentials given

        Parameters
        ----------
        username: str
            The username of the account that will be signed into
        password: str
            The password of the account that will be signed into
        Returns
        -------
        Item[]
        """
        # record datetime this data was scraped
        # scrape for items on hold only
        hold_data = self.hold_data(username, password)
        return self.parse_hold_data(hold_data)

    def items_checked_out(self, username, password):
        """
        Scrapes and returns the items checked out for the user with the login credentials given
        
        Parameters
        ----------
        username: str
            The username of the account that will be signed into
        password: str
            The password of the account that will be signed into
        Returns
        -------
        Item[]
        """
        checkout_data = self.checkout_data(username, password)
        return self.parse_checkout_data(checkout_data)

    def hours(self, branch):
        """
        Scrapes the website for the hours of this branch
        
        Parameters
        ----------
        branch: str
            The branch of which hours will be retrieved
        Returns
        -------
        str
        """
        if "Central" in branch:
            self.driver.get("https://pickeringlibrary.ca/locations/PC/")
            container = self.driver.find_element(By.CLASS_NAME, "location-summary-wrapper")
            lines = container.text.split('\n')
            return 'Central Library Hours\n' + '\n'.join(lines[1:])
        elif "George Ashe" in branch:
            self.driver.get("https://pickeringlibrary.ca/locations/PC/")
            container = self.driver.find_element(By.CLASS_NAME, "location-summary-wrapper")
            lines = container.text.split('\n')
            return 'George Ashe Library Hours\n' + '\n'.join(lines[1:])

        elif "Claremont" in branch:
            self.driver.get("https://pickeringlibrary.ca/locations/CL/")
            container = self.driver.find_element(By.CLASS_NAME, "location-summary-wrapper")
            lines = container.text.split('\n')
            return 'Claremont Library Hours\n' + '\n'.join(lines[1:])
        else:
            raise NoSuchElementException(f"Hours for {branch} cannot be found because the branch does not exist")

        return ""

    def login(self, username, password,
              url="https://pickering.bibliocommons.com/user/login?destination=https%3A%2F%2Fpickeringlibrary.ca"):
        """
        Applies login credentials to the url given

        Parameters
        ----------
        username: str
            The username of the account that will be signed into
        password: str
            The password of the account that will be signed into
        url: str
            The url which the login credentials will be applied to
        """
        self.driver.get(url)
        try:
            user_login = WebDriverWait(driver=self.driver, timeout=10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[testid=field_username]"))
            )
            pass_login = WebDriverWait(driver=self.driver, timeout=10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[testid=field_userpin]"))
            )
            submit_login = WebDriverWait(driver=self.driver, timeout=10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[testid=button_login]"))
            )
            user_login.send_keys(username)
            pass_login.send_keys(password)
            submit_login.click()
        except TimeoutException as e:
            if not ('Pickering Public Library' in self.driver.title):
                raise (e)


class WPL(DurhamLibrary):
    """Class for Whitby Public Library
    Attributes:
        - driver: an instance of a Selenium Chrome web driver
    """

    def __init__(self, driver):
        super().__init__("Whitby Public Library")
        self.driver = driver

    def checkout_data(self, username, password):
        """
        Logs into the checkouts page and returns a list of lists of textual data for each checkout item

        Parameters
        ----------
        username: str
            The username of the account that will be signed into
        password: str
            The password of the account that will be signed into
        Returns
        -------
        str[][]
        """
        res = []
        self.login(username, password, url="https://whitby.bibliocommons.com/v2/checkedout")

        WebDriverWait(driver=self.driver, timeout=10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'cp-item-list')))

        # locate the checkouts
        check_out_container = self.driver.find_element(By.CLASS_NAME, 'cp-item-list')
        checkouts = check_out_container.find_elements(By.CLASS_NAME, 'cp-batch-actions-list-item')

        for item in checkouts:
            lines = item.text.split('\n')
            res.append(lines)

        return res

    def hold_data(self, username, password):
        """
        Logs into the holds page and returns a list of lists of textual data for each hold item

        Parameters
        ----------
        username: str
            The username of the account that will be signed into
        password: str
            The password of the account that will be signed into
        Returns
        -------
        str[][]
        """
        res = []
        self.login(username, password, url="https://whitby.bibliocommons.com/v2/holds")

        WebDriverWait(driver=self.driver, timeout=10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'cp-item-list')))
        # locate the checkouts
        # save_output_as_html(self.driver.page_source, "wpl-hold-data-library-py")
        holds_container = self.driver.find_element(By.CLASS_NAME, 'cp-item-list')
        holds = holds_container.find_elements(By.CLASS_NAME, 'cp-batch-actions-list-item')

        for item in holds:
            lines = item.text.split('\n')
            res.append(lines)
        print(res)
        return res

    def items_on_hold(self, username, password):
        """
        Scrapes and returns the items on hold for the user with the login credentials given

        Parameters
        ----------
        username: str
            The username of the account that will be signed into
        password: str
            The password of the account that will be signed into
        Returns
        -------
        Item[]
        """
        # scrape for items on hold only
        hold_data = self.hold_data(username, password)
        return self.parse_hold_data(hold_data)

    def items_checked_out(self, username, password):
        """
        Scrapes and returns the items on checked for the user with the login credentials given

        Parameters
        ----------
        username: str
            The username of the account that will be signed into
        password: str
            The password of the account that will be signed into
        Returns
        -------
        Item[]
        """
        checkout_data = self.checkout_data(username, password)
        return self.parse_checkout_data(checkout_data)

    def hours(self, branch):
        """
        Scrapes the website for the hours of this branch
        
        Parameters
        ----------
        branch: str
            The branch of which hours will be retrieved
        Returns
        -------
        str
        """

        self.driver.get("https://www.whitbylibrary.ca/hours")

        hours = self.driver.find_element(By.CSS_SELECTOR, ".content.clearfix")
        i = 0
        lines = hours.text.split('\n')
        if branch == "Central":
            return '\n'.join(lines[0:6])
        elif branch == "Rossland":
            return '\n'.join(lines[12:17])
        elif branch == "Brooklin":
            return '\n'.join(lines[6:12])
        else:
            return ''

    def login(self, username, password,
              url='https://whitby.bibliocommons.com/user/login?destination=%2Fuser_dashboard'):
        """
        Applies login credentials to the url given

        Parameters
        ----------
        username: str
            The username of the account that will be signed into
        password: str
            The password of the account that will be signed into
        url: str
            The url which the login credentials will be applied to
        """
        self.driver.get(url)
        # if this instance of the library is connected to a particular user, log them in
        try:
            user_login = WebDriverWait(driver=self.driver, timeout=10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[testid=field_username]"))
            )
            pass_login = WebDriverWait(driver=self.driver, timeout=10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[testid=field_userpin]"))
            )
            submit_login = WebDriverWait(driver=self.driver, timeout=10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[testid=button_login]"))
            )
            if user_login and pass_login and submit_login:
                user_login.send_keys(username)
                pass_login.send_keys(password)
                submit_login.click()
        except (TimeoutException, NoSuchElementException) as e:
            if not ('Whitby Public Library' in self.driver.title):
                raise e


class TPL:
    """Class for Toronto Public Library
    Attributes:
        - driver: an instance of a Selenium Chrome web driver
    """

    def __init__(self, driver):
        self.driver = driver
        self.name = "Toronto Public Library"

    @staticmethod
    def parse_hold_data(hold_data):
        parser = TorontoHoldParser(TorontoHoldParseRule(0, 2, 1, 5, 3))
        title, item_format, contributors, item_date, status, branch = parser.all(hold_data)
        return Item(date.today(), title, contributors, item_format, True, item_date, status, branch, 'toronto')

    @staticmethod
    def parse_checkout_data(checkout_data):
        parser = TorontoCheckoutParser(TorontoCheckoutParseRule(0, 2, 1, 4, -2))
        title, item_format, contributors, item_date, status = parser.all(checkout_data)
        #print(title, item_format, contributors, item_date, status)
        return Item(date.today(), title, contributors, item_format, False, item_date, status, '', 'toronto')

    @staticmethod
    def create_item_object(item_date, is_hold, data):
        if is_hold:
            return Item(item_date, data[0], data[1], data[2], is_hold, data[5], 'Ready', data[3], 'toronto')
        else:
            status = re.search('(?i)due', data[-2])
            if status:
                status = data[-2]
            else:
                status = "Due Later"

            return Item(item_date, data[0], data[1], data[2], is_hold, data[4], status, '', 'toronto')

    def hold_data(self, username, password):
        """
        Logs into the holds page and returns a list of lists of textual data for each hold item

        Parameters
        ----------
        username: str
            The username of the account that will be signed into
        password: str
            The password of the account that will be signed into
        Returns
        -------
        str[][]
        """
        res = []
        holds_url = "https://account.torontopubliclibrary.ca/signin?redirect=%2Fholds"
        self.login(username, password, url=holds_url)

        WebDriverWait(driver=self.driver, timeout=10).until(
            EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, "#PageContent > div.holds-redux"))
        )

        on_hold = self.driver.find_elements_by_css_selector("#PageContent > div.holds-redux.ready-for-pickup > div" +
                                                            " > div > table > tbody")
        # on_hold = self.driver.find_elements(By.CSS_SELECTOR, "#PageContent > div.holds-redux.ready-for-pickup
        # > div > div > table > tbody")
        # save_output_as_html(self.driver.page_source, "tpl-holds-raw")
        for item in on_hold:
            lines = item.text.split('\n')
            res.append(lines)

        #save_output_as_txt(str(res), "tpl-hold-data-raw")
        return res

    def checkout_data(self, username, password):
        """
        Logs into the checkouts page and returns a list of lists of textual data for each checkout item

        Parameters
        ----------
        username: str
            The username of the account that will be signed into
        password: str
            The password of the account that will be signed into
        Returns
        -------
        str[][]
        """
        res = []
        checkout_url = "https://account.torontopubliclibrary.ca/signin?redirect=%2Fcheckouts"
        self.login(username, password, url=checkout_url)

        checkouts = WebDriverWait(driver=self.driver, timeout=10).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, "item-wrapper"))
        )

        for item in checkouts:
            lines = item.text.split('\n')
            res.append(lines)
        #save_output_as_txt(str(res), 'tpl-checkouts-raw')
        return res

    def items_on_hold(self, username, password):
        """
        Scrapes and returns the items on hold for the user with the login credentials given

        Parameters
        ----------
        username: str
            The username of the account that will be signed into
        password: str
            The password of the account that will be signed into
        Returns
        -------
        Item[]
        """
        hold_data = self.hold_data(username, password)
        res = []
        if hold_data:
            for lines in hold_data:
                hold_item = self.parse_hold_data(lines)
                res.append(hold_item)
        return res

    def items_checked_out(self, username, password):
        """
        Scrapes and returns the items on checked for the user with the login credentials given

        Parameters
        ----------
        username: str
            The username of the account that will be signed into
        password: str
            The password of the account that will be signed into
        Returns
        -------
        Item[]
        """
        res = []
        checkout_data = self.checkout_data(username, password)
        print(checkout_data)
        for lines in checkout_data:
            checkout_item = self.parse_checkout_data(lines)
            print(checkout_item)
            res.append(checkout_item)

        print(res)
        return res

    def hours(self, branch):
        """
        Scrapes the website for the hours of this branch
        
        Parameters
        ----------
        branch: str
            The branch of which hours will be retrieved
        Returns
        -------
        str
        """
        first_letter = branch[0]
        self.driver.get("https://www.torontopubliclibrary.ca/branches/")
        alpha_selector = "alphaIndex-" + first_letter
        end_of_branches = False
        curr_selector = "a[name=" + alpha_selector + "]"
        branch_element = ""
        while not end_of_branches:
            curr_selector = curr_selector + "+.row"
            try:
                branch_element = self.driver.find_element(By.CSS_SELECTOR, curr_selector)
                lines = branch_element.text.split('\n')
                if branch in lines[0]:
                    lines = lines[0:4] + lines[5:]
                    return '\n'.join(lines)
            except NoSuchElementException as e:
                end_of_branches = True

        if end_of_branches:
            raise NoSuchElementException(f"Hours for {branch} cannot be found because the branch does not exist")
        return ""

    def login(self, username, password, url='https://account.torontopubliclibrary.ca/login'):
        """
        Applies login credentials to the url given

        Parameters
        ----------
        username: str
            The username of the account that will be signed into
        password: str
            The password of the account that will be signed into
        url: str
            The url which the login credentials will be applied to
        """
        self.driver.get(url)
        user_login = self.driver.find_element_by_id("userID")
        pass_login = self.driver.find_element_by_id("password")
        submit_login = self.driver.find_element_by_css_selector("#form_signin > div > button")
        user_login.send_keys(username)
        pass_login.send_keys(password)
        submit_login.click()
