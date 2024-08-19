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

from bs4 import BeautifulSoup

from lib_parser import *
from parse_rule import *

from parser_utils import *
from datetime import date
from lib_assets import *
from urllib import request

class DurhamLibrary:
    def __init__(self):
        super().__init__()
        self.checkouts = []
        self.holds = []
        self.parsers = {"holds": {"DVD": DurhamHoldParser(
            DurhamDVDHoldRule(title=2, item_format=2, status_with_subtitle=8, status_without_subtitle=7,
                              item_date_with_subtitle=10, item_date_without_subtitle=9, branch_with_subtitle=9,
                              branch_without_subtitle=8)),
                                  "CD_and_Book": DurhamHoldParser(
                                      DurhamBookAndCDHoldRule(title=2, item_format=2, contributors_with_subtitle=6,
                                                              contributors_without_subtitle=5, status_with_subtitle=14,
                                                              status_without_subtitle=13, item_date_with_subtitle=20,
                                                              item_date_without_subtitle=19, branch_with_subtitle=18,
                                                              branch_without_subtitle=17))},
                        "checkouts": {"DVD": DurhamCheckoutParser(
                            DurhamDVDCheckoutRule(title=2, item_format=2, status_with_subtitle=7,
                                                  status_without_subtitle=6, item_date_with_subtitle=9,
                                                  item_date_without_subtitle=7)),
                                      "CD_and_Book": DurhamCheckoutParser(
                                          DurhamBookAndCDCheckoutRule(title=2, item_format=2,
                                                                      contributors_with_subtitle=4,
                                                                      contributors_without_subtitle=3,
                                                                      status_with_subtitle=8, status_without_subtitle=7,
                                                                      item_date_with_subtitle=9,
                                                                      item_date_without_subtitle=8))}}

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

                hold_item = Item(date_retrieved=date.today(), title=title, contributors=contributors,
                                 item_format=item_format, is_hold=True, item_date=item_date, status=status,
                                 branch=branch, system='durham')
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
                hold_item = Item(date_retrieved=date.today(), title=title, contributors=contributors,
                                 item_format=item_format, is_hold=False, item_date=item_date, status=status, branch='',
                                 system='durham')
                if hold_item.title:
                    res.append(hold_item)
        return res


class PPL(DurhamLibrary):
    """Class for Pickering Public Library
    Attributes:
        - N/A
    """

    def __init__(self):
        super().__init__()
        # EC.title_is("On Hold | Pickering Public Library | BiblioCommons")
        self.name = "Pickering Public Library"

    @staticmethod
    def hold_data(page_source):
        """
        Logs into the holds page and returns a list of lists of textual data for each hold item

        Parameters
        ----------
        Returns
        -------
        str[][]
        """
        res = []
        soup = BeautifulSoup(page_source, "html.parser")
        holds = soup.select("div.cp-batch-actions-list-item")
        for item in holds:
            plain_text = item.get_text('\n')
            # print(plain_text)
            lines = plain_text.split('\n')
            # print(lines)
            res.append(lines)
        return res

    @staticmethod
    def checkout_data(page_source):
        """
        Logs into the checkouts page and returns a list of lists of textual data for each checkout item

        Parameters
        ----------
        page_source: plain text html of a checkout page

        Returns
        -------
        str[][]
        """
        res = []
        soup = BeautifulSoup(page_source, "html.parser")
        checkouts = soup.select("div.cp-batch-actions-list-item")

        for item in checkouts:
            plain_text = item.get_text('\n')
            # print(plain_text)
            lines = plain_text.split('\n')
            # print(lines)
            res.append(lines)
        return res

    def items_on_hold(self):
        """
        Scrapes and returns the items on hold for the user

        Parameters
        ----------
        Returns
        -------
        Item[]
        """
        page_source = request.urlopen('https://pickering.bibliocommons.com/v2/holds').read()
        hold_data = self.hold_data(page_source)
        return self.parse_hold_data(hold_data)

    def items_checked_out(self):
        """
        Scrapes and returns the items checked out for the user
        
        Parameters
        ----------
        Returns
        -------
        Item[]
        """
        page_source = request.urlopen('https://pickering.bibliocommons.com/v2/checkedout').read()
        checkout_data = self.checkout_data(page_source)
        return self.parse_checkout_data(checkout_data)

    @staticmethod
    def _hours(page_source, full_branch_name):
        """
        Scrapes the website for the hours of this branch
        
        Parameters
        ----------
        page_source: str
            plain text html of hours page
        ful_branch_name: str
            The full branch name of which hours will be retrieved
        Returns
        -------
        str
        """
        soup = BeautifulSoup(page_source, "html.parser")
        if full_branch_name == "Central Library Hours\n":
            container = soup.find(class_="c-hours-and-info__hours-wrapper")
        elif full_branch_name == 'George Ashe Library Hours\n':
            pass
        elif full_branch_name == 'Claremont Library Hours\n':
            pass
        lines = container.text.split('\n')
        return full_branch_name + '\n'.join(lines[1:])

    def hours(self, branch, page_source=None):
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
        full_branch_name = ""
        page_source = ""
        if "Central" in branch:
            page_source = request.urlopen('https://pickeringlibrary.ca/locations/3/').read()
            full_branch_name = 'Central Library Hours\n'
        elif "George Ashe" in branch:
            page_source = request.urlopen('https://pickeringlibrary.ca/locations/4/').read()
            full_branch_name = 'George Ashe Library Hours\n'

        elif "Claremont" in branch:
            page_source = request.urlopen('https://pickeringlibrary.ca/locations/5/').read()
            full_branch_name = 'Claremont Library Hours\n'
        else:
            raise Exception(f"Hours for {branch} cannot be found because the branch does not exist")
        return PPL._hours(page_source, full_branch_name)

class WPL(DurhamLibrary):
    """Class for Whitby Public Library
    Attributes:
        - N/A
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Whitby Public Library"

    @staticmethod
    def checkout_data(page_source):
        """
        Logs into the checkouts page and returns a list of lists of textual data for each checkout item

        Parameters
        ----------
        Returns
        -------
        str[][]
        """
        res = []
        soup = BeautifulSoup(page_source, "html.parser")
        checkouts = soup.find_all("div", class_="cp-batch-actions-list-item")
        for item in checkouts:
            plain_text = item.get_text('\n')
            # print(plain_text)
            lines = plain_text.split('\n')
            # print(lines)
            res.append(lines)

        return res

    @staticmethod
    def hold_data(page_source):
        """
        Logs into the holds page and returns a list of lists of textual data for each hold item

        Parameters
        ----------
        Returns
        -------
        str[][]
        """
        res = []
        soup = BeautifulSoup(page_source, "html.parser")
        holds = soup.find_all("div", class_='cp-batch-actions-list-item')

        for item in holds:
            plain_text = item.get_text('\n')
            # print(plain_text)
            lines = plain_text.split('\n')
            # print(lines)
            res.append(lines)
        # print(res)
        return res

    def items_on_hold(self):
        """
        Scrapes and returns the items on hold for the user

        Parameters
        ----------
        Returns
        -------
        Item[]
        """
        page_source = request.urlopen('https://whitby.bibliocommons.com/v2/holds').read()
        hold_data = self.hold_data(page_source)
        return self.parse_hold_data(hold_data)

    def items_checked_out(self):
        """
        Scrapes and returns the items on checked for the user

        Parameters
        ----------
        Returns
        -------
        Item[]
        """
        page_source = request.urlopen('https://whitby.bibliocommons.com/v2/checkedout').read()
        checkout_data = self.checkout_data(page_source)
        return self.parse_checkout_data(checkout_data)

    @staticmethod
    def _hours(page_source, branch):
        """
        Scrapes the website for the hours of this branch
        
        Parameters
        ----------
        page_source: str
            Plain text html of hours page
        branch: str
            The branch of which hours will be retrieved
        
        Returns
        -------
        str
        """
        soup = BeautifulSoup(page_source, 'html.parser')
        hours = soup.select(".content.clearfix")
        # print(hours)
        lines = [x.get_text() for x in hours]
        lines = lines[0].split('\n')
        lines = [y.strip() for y in lines]
        # print(list(hours))
        # print(len(lines),lines)
        if branch == "Central":
            return '\n'.join(lines[2:9])
        elif branch == "Rossland":
            return '\n'.join(lines[17:23])
        elif branch == "Brooklin":
            return '\n'.join(lines[10:17])
        else:
            return ''

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
        page_source = request.urlopen('https://www.whitbylibrary.ca/hours').read()
        return WPL._hours(page_source, branch)

class TPL:
    """Class for Toronto Public Library
    Attributes:
        - N/A
    """

    def __init__(self):
        self.name = "Toronto Public Library"

    @staticmethod
    def parse_hold_data(hold_data):
        parser = TorontoHoldParser(TorontoHoldParseRule(title=2, item_format=4, contributors=3, item_date=7, branch=5))
        title, item_format, contributors, item_date, status, branch = parser.all(hold_data)
        print("in library.py:",title, item_format, contributors, item_date, status, branch)
        return Item(date_retrieved=date.today(), title=title, contributors=contributors, item_format=item_format,
                    is_hold=True, item_date=item_date, status=status, branch=branch, system='toronto')

    @staticmethod
    def parse_checkout_data(checkout_data):
        parser = TorontoCheckoutParser(
            TorontoCheckoutParseRule(title=1, item_format=5, contributors=4, status=8, item_date=7))
        title, item_format, contributors, item_date, status = parser.all(checkout_data)
        # print(title, item_format, contributors, item_date, status)
        return Item(date_retrieved=date.today(), title=title, contributors=contributors, item_format=item_format,
                    is_hold=False, item_date=item_date, status=status, system='toronto')

    @staticmethod
    def create_item_object(date_retrieved, is_hold, data):
        if is_hold:
            return Item(date_retrieved=date_retrieved, title=data[0], item_format=data[1], contributors=data[2],
                        is_hold=is_hold, item_date=data[5], status='Ready', branch=data[3], system='toronto')
        else:
            status = re.search('(?i)due', data[-2])
            if status:
                status = data[-2]
            else:
                status = "Due Later"

            return Item(date_retrieved=date_retrieved, title=data[0], item_format=data[1], contributors=data[2],
                        is_hold=is_hold, item_date=data[4], status=status, branch='', system='toronto')

    @staticmethod
    def hold_data(page_source):
        """
        Logs into the holds page and returns a list of lists of textual data for each hold item

        Parameters
        ----------
        Returns
        -------
        str[][]
        """
        res = []
        soup = BeautifulSoup(page_source, "html.parser")
        on_hold = soup.select("#PageContent > div.holds-redux.ready-for-pickup > div > div > table > tbody")
        for item in on_hold:
            plain_text = item.get_text('\n')
            lines = plain_text.split('\n')
            res.append(lines)
        return res

    @staticmethod
    def checkout_data(page_source):
        """
        Logs into the checkouts page and returns a list of lists of textual data for each checkout item

        Parameters
        ----------
        Returns
        -------
        str[][]
        """
        res = []
        soup = BeautifulSoup(page_source, "html.parser")
        checkouts = soup.find_all(class_="item-wrapper")
        for item in checkouts:
            plain_text = item.get_text('\n')
            # print(plain_text)
            lines = plain_text.split('\n')
            # print(lines)
            res.append(lines)
        # save_output_as_txt(str(res), 'tpl-checkouts-raw')
        return res

    def items_on_hold(self):
        """
        Scrapes and returns the items on hold for the user

        Parameters
        ----------
        Returns
        -------
        Item[]
        """
        # By.CSS_SELECTOR, "#PageContent > div.holds-redux.ready-for-pickup"))
        hold_data = TPL.hold_data()
        #print(hold_data)
        res = []
        if hold_data:
            for lines in hold_data:
                hold_item = TPL.parse_hold_data(lines)
                res.append(hold_item)
        return res

    def items_checked_out(self):
        """
        Scrapes and returns the items on checked for the user

        Parameters
        ----------
        Returns
        -------
        Item[]
        """
        # By.CLASS_NAME, "item-wrapper"))
        checkout_data = self.checkout_data()
        # print(checkout_data)
        res = []
        for lines in checkout_data:
            checkout_item = self.parse_checkout_data(lines)
            # print(checkout_item)
            res.append(checkout_item)

        # print(res)
        return res

    @staticmethod
    def _hours(branch, page_source):
        soup = BeautifulSoup(page_source, "html.parser")
        first_letter = branch[0]
        alpha_selector = "alphaIndex-" + first_letter
        end_of_branches = False
        curr_selector = "a[name=" + alpha_selector + "]"
        branch_element = ""
        while not end_of_branches:
            curr_selector = curr_selector + "+.row"
            try:
                branch_element = soup.select(curr_selector)
                # print(type(branch_element), len(branch_element))
                lines = None

                for item in branch_element:
                    lines = item.get_text()

                # print("lines:\n",lines)
                if branch in lines:
                    lines = lines.split('\n')
                    lines = list(filter(lambda item: not (item.isspace()) and (item != ''), lines))
                    lines = [x.lstrip() for x in lines]
                    # print(lines)
                    return '\n'.join(lines)
            except Exception as e:
                end_of_branches = True

        if end_of_branches:
            raise Exception(f"Hours for {branch} cannot be found because the branch does not exist")
        return ""

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
        page_source = request.urlopen('https://www.torontopubliclibrary.ca/branches/').read()
        return TPL._hours(page_source, branch)