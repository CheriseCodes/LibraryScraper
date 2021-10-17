from __future__ import print_function
from hashlib import new

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import re
import requests
import os # import os.path
from twilio.rest import Client
from libscrape.libparser import DurhamHoldParser, DurhamCheckoutParser
from libscrape.utils import save_output_as_html
from datetime import date

class Item:
    '''
    A library item
    ...
    Attributes
    ----------
    data_recieved: datetime.date
        The date the data for this library item was retreived from the website
    title: str
    contributors: str
    format: str
    is_hold: bool
    item_date: str
    status: str
    branch: str
    system: str
    
    Methods
    -------
    text_to_string()
        Formates the string version of the item that is suitable for presenting directly to the client
    '''
    def __init__(self, *args):
        if len(args) == 9:
            self.date_retrieved = args[0] # the date the data was retrieved from the website
            self.title = args[1]
            self.format = args[3]
            self.is_hold = args[4] # HOLD=0, CHECKOUT=1
            self.status = args[6] # the status of the item depending on _type
            self.item_date = args[5] # the pick up date or due date depending on _type
            self.branch = args[7]
            self.system = args[8]
            if self.system == 'toronto':
                contrib_lst = args[2].rsplit(',',1)
                contributors = contrib_lst[0]
                self.contributors = 'by ' + contributors
            else:
                self.contributors = args[2]
        else:
            self.date_retrieved = ''             
            self.title = ''
            self.format = ''
            self.is_hold = ''
            self.status = ''
            self.item_date = ''
            self.branch = ''
            self.system = '' 
            self.contributors = ''

    def __str__(self):
        return f"date_retrieved={self.date_retrieved},title={self.title},contributors={self.contributors},format={self.format},is_hold={self.is_hold},status={self.status},item_date={self.item_date},branch={self.branch}"

    def text_string(self):
        if self.title == '':
            return ''

        if self.contributors == "":
            return self.title +  " ("+ self.format + ") | " + (self.status!='')*(self.status + " | ") + self.item_date + self.is_hold*(' | ' + self.branch)
        else:
            return self.title +  " ("+ self.format + ") " + self.contributors + ' | ' +  (self.status!='')*(self.status + " | ") + self.item_date + self.is_hold*(' | ' + self.branch)
    def generate_mock(self):
        f = open("mock.txt", "a")
        new_mock = "Item(date.today(),'" + self.title + "','" + self.contributors + \
            "','" + self.format + "'," + str(self.is_hold) + ",'" + self.item_date + "','" + \
                self.status + "','" + self.branch + "','" + self.system + "')\n"
        f.write(new_mock)
        f.close()

class DurhamLibrary:
    def __init__(self, region):
        super().__init__()
        self.checkouts = []
        self.holds = []
        self.region = region

    def select_parser(self, format, parsers):
        parser = None
        generic_format = None
        if "DVD" in format:
            generic_format = "DVD"
            parser = parsers["DVD"]
        elif "CD" in format:
            generic_format = "CD"
            parser = parsers["CD_and_Book"]
        elif "Book" in format:
            generic_format = "Book"
            parser = parsers["CD_and_Book"]
        return (parser, generic_format)

    def parse_hold_data(self, hold_data):
        res = []
        parsers = { "DVD": DurhamHoldParser({"title":2,
                                    "format":2,
                                    "contributors_with_subtitle": None,
                                    "contributors_without_subtitle": None,
                                    "status_with_subtitle":8,
                                    "status_without_subtitle":7,
                                    "item_date_with_subtitle": 10,
                                    "item_date_without_subtitle": 9,
                                    "branch_with_subtitle":9,
                                    "branch_without_subtitle": 8}),
                    "CD_and_Book": DurhamHoldParser({"title":2,
                                    "format":2,
                                    "contributors_with_subtitle": 4,
                                    "contributors_without_subtitle": 3,
                                    "status_with_subtitle":9,
                                    "status_without_subtitle":8,
                                    "item_date_with_subtitle": 11,
                                    "item_date_without_subtitle": 10,
                                    "branch_with_subtitle": 10,
                                    "branch_without_subtitle":9})}

        for lines in hold_data:
            format = DurhamHoldParser.format(lines)
            parser, generic_format = self.select_parser(format,parsers)
            if parser:

                has_subtitle = DurhamHoldParser.has_subtitle(lines,generic_format)
                title, format, contributors, status, item_date, branch = parser.all(lines, generic_format, has_subtitle)

                hold_item = Item(date.today(),title,contributors,format,True,item_date,status,branch,'durham')
                if hold_item.title:
                    res.append(hold_item)
        
        return res

    def parse_checkout_data(self, checkout_data):
        res = []
        parsers = { "DVD": DurhamCheckoutParser({"title":2,
                                    "format":2,
                                    "contributors_with_subtitle": None,
                                    "contributors_without_subtitle": None,
                                    "status_with_subtitle":7,
                                    "status_without_subtitle":6,
                                    "item_date_with_subtitle": 8,
                                    "item_date_without_subtitle": 7
                                    }),
                    "CD_and_Book": DurhamCheckoutParser({"title":2,
                                    "format":2,
                                    "contributors_with_subtitle": 4,
                                    "contributors_without_subtitle": 3,
                                    "status_with_subtitle":8,
                                    "status_without_subtitle":7,
                                    "item_date_with_subtitle": 9,
                                    "item_date_without_subtitle": 8
                                    })}
        for lines in checkout_data:
            format = DurhamCheckoutParser.format(lines)
            parser, generic_format = self.select_parser(format,parsers)
            if parser:
                has_subtitle = DurhamCheckoutParser.has_subtitle(lines,generic_format)
                title, format, contributors, status, item_date = parser.all(lines, generic_format, has_subtitle)
                hold_item = Item(date.today(),title,contributors,format,False,item_date,status,'','durham')
                if hold_item.title:
                    res.append(hold_item)
        return res
    
    def formulate_text(self, checkouts, type):
        res = ''
        # case 1: plain text
        if type == 1:
            i = 1
            for item in checkouts:
                res += str(i) + '. ' + item.text_string() + '\n'
                i+=1
        # case 2: Google doc link
        elif type == 2:
            res += 'Click here to view your updated report: https://docs.google.com/document/d/' + \
                os.environ['LIB_SCRAPER_DOC_ID']

        return res

    def formulate_checkouts_text(self, checkouts, type):
        print(self.region)
        res = '\n'+self.region + f" CHECKOUTS ({date.today()}):\n"
        res += self.formulate_text(checkouts, type)
        return res

    def formulate_holds_text(self, checkouts, type):
        res = '\n'+self.region + f" HOLDS ({date.today()}):\n"
        res += self.formulate_text(checkouts, type)
        return res

    def append_doc(self, items, is_hold):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        SCOPES = ['https://www.googleapis.com/auth/documents']
        DOCUMENT_ID = os.environ['LIB_SCRAPER_DOC_ID']
        #creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.path.join(ROOT_DIR, 'credentials.json'), SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        service = build('docs', 'v1', credentials=creds)

        # formulate new content
        
        if is_hold:
            new_text = self.formulate_holds_text(items, 1)
        else:
            new_text = self.formulate_checkouts_text(items, 1)

        new_text += '\n'

        req = [{
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': new_text
            }
        },
        ]
        # Retrieve the documents contents from the Docs service.
        document = service.documents().get(documentId=DOCUMENT_ID).execute()

        print('The title of the document is: {}'.format(document.get('title')))

        service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': req}).execute()

    def send_checkouts_text(self, data):
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)
        res = self.formulate_checkouts_text(data)
        message = client.messages \
                        .create(
                            body=res,
                            from_=os.environ['TWILIO_FROM'],
                            to=os.environ['TWILIO_TO']
                )
        return message

    def send_holds_text(self, data):
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)
        res = self.formulate_holds_text(data)
        message = client.messages \
                        .create(
                            body=res,
                            from_=os.environ['TWILIO_FROM'],
                            to=os.environ['TWILIO_TO']
                )
        return message

class PPL(DurhamLibrary):
    '''Class for Pickering Public Library'''
    def __init__(self,driver):
        super().__init__("Pickering Public Library")
        self.driver = driver

    def hold_data(self,username,password):
        '''
        Logs into the holds page and returns a list of lists of textual data for each hold item
        Parameters
        ----------
        username: str
            The username of the account that will be signed into
        password: str
            The password of the account that will be signed into
        Returns
        -------
        A list of list of strings in which every string is a separate line of data from the holds page
        '''
        res = []

        self.login(username,password,url="https://pickering.bibliocommons.com/user/login?destination=%2Fv2%2Fholds")
       
        WebDriverWait(driver=self.driver, timeout=10).until(
            EC.title_is("On Hold | Pickering Public Library | BiblioCommons")
        )
        holds = self.driver.find_elements_by_css_selector("div.cp-batch-actions-list-item")

        for item in holds:
            lines = item.text.split('\n')
            res.append(lines)
        return res

    def checkout_data(self,username,password):
        res = []

        self.login(username,password,url="https://pickering.bibliocommons.com/user/login?destination=%2Fcheckedout")

        WebDriverWait(driver=self.driver, timeout=10).until(
            EC.title_is("Checked Out | Pickering Public Library | BiblioCommons")
        )

        save_output_as_html(self.driver.page_source)

        checkouts = self.driver.find_elements_by_css_selector("div.cp-batch-actions-list-item")

        for item in checkouts:
            lines = item.text.split('\n')
            res.append(lines)
        return res

    def items_on_hold(self,username,password):
        '''Scrapes and returns the items on hold for the user with the login credentials given'''
        # record datetime this data was scraped
        # scrape for items on hold only
        hold_data = self.hold_data(username,password)
        return self.parse_hold_data(hold_data)

    def items_checked_out(self,username,password):
        '''Scrapes and returns the items checked out for the user with the login credentials given'''
        checkout_data = self.checkout_data(username,password)
        return self.parse_checkout_data(checkout_data)

    def hours(self, branch):
        '''Scrapes the website for the hours of this branch'''
        if "Central" in branch:
            self.driver.get("https://pickeringlibrary.ca/locations/PC/")
            container = self.driver.find_element(By.CLASS_NAME, "location-summary-wrapper")
            lines = container.text.split('\n')
            return 'Central Library Hours\n'+'\n'.join(lines[1:])
        elif "George Ashe" in branch:
            self.driver.get("https://pickeringlibrary.ca/locations/PC/")
            container = self.driver.find_element(By.CLASS_NAME, "location-summary-wrapper")
            lines = container.text.split('\n')
            return 'George Ashe Library Hours\n'+'\n'.join(lines[1:])

        elif "Claremont" in branch:
            self.driver.get("https://pickeringlibrary.ca/locations/CL/")
            container = self.driver.find_element(By.CLASS_NAME, "location-summary-wrapper")
            lines = container.text.split('\n')
            return 'Claremont Library Hours\n'+'\n'.join(lines[1:])
        else:
            raise NoSuchElementException(f"Hours for {branch} cannot be found because the branch does not exist")


        return ""

    def login(self,username,password,url="https://pickering.bibliocommons.com/user/login?destination=https%3A%2F%2Fpickeringlibrary.ca"):
        '''Applies login credentials to the url given'''
        self.driver.get(url)
        try:
            user_login = WebDriverWait(driver=self.driver, timeout=10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,"input[testid=field_username]"))
            )
            pass_login = WebDriverWait(driver=self.driver, timeout=10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,"input[testid=field_userpin]"))
            )
            submit_login = WebDriverWait(driver=self.driver, timeout=10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,"input[testid=button_login]"))
            )
            user_login.send_keys(username)
            pass_login.send_keys(password)
            submit_login.click()
        except TimeoutException as e:
            if not('Pickering Public Library' in self.driver.title):
                raise(e)

class WPL(DurhamLibrary):
    '''Class for Whitby Public Library'''
    def __init__(self,driver):
        super().__init__("Whitby Public Library")
        self.driver = driver
        print(self.region)

    def checkout_data(self,username,password):
        res = []
        self.login(username,password,url="https://whitby.bibliocommons.com/v2/checkedout")

        WebDriverWait(driver=self.driver, timeout=10).until(EC.presence_of_element_located((By.CLASS_NAME,'cp-item-list')))

        # locate the checkouts
        check_out_container = self.driver.find_element(By.CLASS_NAME,'cp-item-list')
        checkouts = check_out_container.find_elements(By.CLASS_NAME,'cp-batch-actions-list-item')

        for item in checkouts:
            lines = item.text.split('\n')
            res.append(lines)

        return res

    def hold_data(self,username,password):
        res = []
        self.login(username,password,url="https://whitby.bibliocommons.com/v2/holds")

        WebDriverWait(driver=self.driver, timeout=10).until(EC.presence_of_element_located((By.CLASS_NAME,'cp-item-list')))
        # locate the checkouts
        holds_container = self.driver.find_element(By.CLASS_NAME,'cp-item-list')
        holds = holds_container.find_elements(By.CLASS_NAME,'cp-batch-actions-list-item')

        for item in holds:
            lines = item.text.split('\n')
            res.append(lines)
        
        return res

    def items_on_hold(self,username,password):
        '''Scrapes and returns the items on hold for the user with the login credentials given'''
        # scrape for items on hold only
        hold_data = self.hold_data(username,password)
        return self.parse_hold_data(hold_data)

    def items_checked_out(self,username,password):
        '''Scrapes and returns the items checked out for the user with the login credentials given'''
        checkout_data = self.checkout_data(username,password)
        return self.parse_checkout_data(checkout_data)

    def hours(self,branch):
        '''Scrapes and returns the hours for the given branch'''
    
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

    def login(self, username,password,url='https://whitby.bibliocommons.com/user/login?destination=%2Fuser_dashboard'):
        '''Enters login info to the url given'''
        self.driver.get(url)
        # if this instance of the library is connected to a particular user, log them in
        try:
            user_login = WebDriverWait(driver=self.driver, timeout=10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,"input[testid=field_username]"))
            )
            pass_login = WebDriverWait(driver=self.driver, timeout=10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,"input[testid=field_userpin]"))
            )
            submit_login = WebDriverWait(driver=self.driver, timeout=10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,"input[testid=button_login]"))
            )
            if user_login and pass_login and submit_login:
                user_login.send_keys(username)
                pass_login.send_keys(password)
                submit_login.click()
        except (TimeoutException, NoSuchElementException) as e:
            if not('Whitby Public Library' in self.driver.title): 
                raise(e)
class TPL:
    '''Class for Toronto Public Library'''
    def __init__(self, driver):
        self.driver = driver
        self.name = "Toronto Public Library"

    def create_item_object(self, date, is_hold, data):
        if is_hold:
            return Item(date,data[0],data[1],data[2],is_hold,data[5],'Ready',data[3], 'toronto')
        else:
            status = re.search('(?i)due',data[-2])
            if status:
                status = data[-2]
            else:
                status = "Due Later"

            return Item(date, data[0],data[1],data[2],is_hold,data[4],status,'', 'toronto')

    def hold_data(self,username,password):
        res = []
        holds_url = "https://account.torontopubliclibrary.ca/signin?redirect=%2Fholds"
        self.login(username, password,url=holds_url)

        WebDriverWait(driver=self.driver, timeout=10).until(
            EC.title_is("Holds : Toronto Public Library")
        )

        on_hold = self.driver.find_elements(By.CSS_SELECTOR, "div.holds-redux.ready-for-pickup .item-wrapper")
        
        for item in on_hold:
            lines = item.text.split('\n')
            res.append(lines)
        return res

    def checkout_data(self,username,password):
        res = []
        checkout_url = "https://account.torontopubliclibrary.ca/signin?redirect=%2Fcheckouts"
        self.login(username, password,url=checkout_url)

        WebDriverWait(driver=self.driver, timeout=10).until(
            EC.title_is("Checkouts : Toronto Public Library")
        )

        checkouts = WebDriverWait(driver=self.driver, timeout=10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "item-wrapper")))
        
        for item in checkouts:
            lines = item.text.split('\n')
            res.append(lines)
        
        return res

    def items_on_hold(self,username,password):
        '''Scrapes and returns the items on hold for the user with the login credentials given'''
        hold_data = self.hold_data(username,password)
        res = []
        if hold_data:
            for lines in hold_data:
                hold_item = self.create_item_object(date.today(),True,lines)
                res.append(hold_item)
        return res


    def items_checked_out(self, username, password):
        '''Scrapes and returns the items checked out for the user with the login credentials given'''
        res = []
        checkout_data = self.checkout_data(username,password)
        for lines in checkout_data:
            checkout_item = self.create_item_object(date.today(),False,lines)
            res.append(checkout_item)
        return res

    def hours(self,branch):
        '''Scrapes the website for the hours for the given branch'''
        first_letter = branch[0]
        self.driver.get("https://www.torontopubliclibrary.ca/branches/")
        alpha_selector = "alphaIndex-" + first_letter
        end_of_branches = False
        curr_selector = "a[name=" + alpha_selector + "]"
        branch_element = ""
        while not(end_of_branches):
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

    def login(self,username,password,url='https://account.torontopubliclibrary.ca/login'):
        '''Enters login info to the url given'''
        self.driver.get(url)
        user_login = self.driver.find_element_by_id("userID")
        pass_login = self.driver.find_element_by_id("password")
        submit_login = self.driver.find_element_by_css_selector("#form_signin > div > button")
        user_login.send_keys(username)
        pass_login.send_keys(password)
        submit_login.click()

