from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import re
import os
from twilio.rest import Client

from datetime import date

# TODO: move to its own file
def save_output_as_html(text):
    f = open('sample.html','w',encoding='utf-8')
    f.write(text)
    f.close()

class Item:
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
        return "date_retrieved={},title={},contributors={},format={},is_hold={},status={},item_date={},branch={}".format(self.date_retrieved,self.title,self.contributors,self.format,self.is_hold,self.status,self.item_date,self.branch)
        
    def text_string(self):
        if self.title == '':
            return ''

        if self.contributors == "":
            return self.title +  " ("+ self.format + ") | " + (self.status!='')*(self.status + " | ") + self.item_date + self.is_hold*(' | ' + self.branch)
        else:
            return self.title +  " ("+ self.format + ") " + self.contributors + ' | ' +  (self.status!='')*(self.status + " | ") + self.item_date + self.is_hold*(' | ' + self.branch)

class DurhamLibrary:
    def __init__(self, region=''):
        super().__init__()
        self.checkouts = []
        self.holds = []
        self.region = region
    def item_data_has_subtitle(self,item_format, is_hold, data):
        if ("CD" in item_format):
            if is_hold:
                return not(data[3][:2] == 'by')
            else:  
                if (data[3][:2] == 'by'):
                    return len(data) > 15
                else:
                    return len(data) > 14
        
        if ("Book" == item_format):
            if is_hold:
                return not(data[3][:2] == 'by')
            else:
                return len(data) > 15
        
        if ("DVD" in item_format):
            if is_hold:
                return not(data[3][:2] == 'by') and not(data[3][:6] == 'DVD - ')
            else:
                return len(data) > 14

    def create_cd_item_on_hold(self, date_today, data):
        title, item_format = data[2].rsplit(", ",1)
        status = ''
        if self.item_data_has_subtitle(item_format, True, data):
            # if hold it not ready
            if "Not ready" in data[9]:
                status = "Not Ready"
                item_date = data[11].replace("Expires on ","")
            else:
                status = "Ready"
                item_date = data[11].replace("Pick up by ", "")

            branch = data[10].replace("Pick up at ","")
            contributors = data[4]
        else:
            # if hold it not ready
            if "Not ready" in data[8]:
                status = "Not Ready"
                item_date = data[10].replace("Expires on ","")
            else:
                status = "Ready"
                item_date = data[10].replace("Pick up by ", "")

            branch = data[9].replace("Pick up at ","")
            contributors = data[3]
        return Item(date_today,title,contributors,item_format,True,item_date,status,branch,'durham')
    
    def create_cd_item_checked_out(self, date_today, data):
        title, item_format = data[2].rsplit(", ",1)
        status = ''
        if self.item_data_has_subtitle(item_format, False, data):
            # if hold it not ready
            if "Due soon" in data[8]:
                status = "Due Soon"
            elif "Due later" in data[8]:
                status = "Due Later"
            else:
                status = "Overdue"
            item_date = data[9].replace("Due by ", "")
            contributors = data[4]
        else:
            # if CD has contributors listed
            if data[3][:2] == 'by':
                if "Due soon" in data[7]:
                    status = "Due Soon"
                elif "Due later" in data[7]:
                    status = "Due Later"
                else:
                    status = "Overdue"
                
                item_date = data[8].replace("Due by ", "")
                contributors = data[3]
            else:
                if "Due soon" in data[6]:
                    status = "Due Soon"
                elif "Due later" in data[6]:
                    status = "Due Later"
                else:
                    status = "Overdue"
                
                item_date = data[7].replace("Due by ", "")
                contributors = ''
        branch = ''
        return Item(date_today,title,contributors,item_format,False,item_date,status,branch,'durham')

    def create_dvd_item_on_hold(self, date_today, data):
        title, item_format = data[2].rsplit(", ",1)
        status = ''
        # case one: there is no subtitle
        if self.item_data_has_subtitle(item_format, True, data):
            # if hold it not ready
            if "Not ready" in data[8]:
                status = "Not Ready"
                item_date = data[10].replace("Expires on ","")
            else:
                status = "Ready"
                item_date = data[10].replace("Pick up by ", "")

            branch = data[9].replace("Pick up at ","")
            contributors = ''
        else:
            # if hold it not ready
            if "Not ready" in data[7]:
                status = "Not Ready"
                item_date = data[9].replace("Expires on ","")
            else:
                status = "Ready"
                item_date = data[9].replace("Pick up by ", "")

            branch = data[8].replace("Pick up at ","")
            contributors = ''
        return Item(date_today,title,contributors,item_format,True,item_date,status,branch,'durham')

    def create_dvd_item_checked_out(self, date_today, data):
        # Check if renewed
        status = ''
        title, item_format = data[2].rsplit(", ",1)
        # case one: there is no subtitle
        if self.item_data_has_subtitle(item_format, False, data):
            # if hold it not ready
            if "Due later" in data[7]:
                status = "Due Later"
            elif "Due soon" in data[7]:
                status = "Due Soon"
            else:
                status = "Overdue"
            item_date = data[8].replace("Due by ","")
        else:
            if "Due later" in data[6]:
                status = "Due Later"
            elif "Due soon" in data[6]:
                status = "Due Soon"
            else:
                status = "Overdue"
            item_date = data[7].replace("Due by ","")
        branch = ''
        contributors = ''
        return Item(date_today,title,contributors,item_format,False,item_date,status,branch,'durham')
    
    def create_book_item_on_hold(self, date_today, data):
        title, item_format = data[2].rsplit(", ",1)
        status = ''
        if self.item_data_has_subtitle(item_format, True, data):
            # if hold it not ready
            if "Not ready" in data[9]:
                status = "Not Ready"
                item_date = data[11].replace("Expires on ","")
            else:
                status = "Ready"
                item_date = data[11].replace("Pick up by ", "")

            branch = data[10].replace("Pick up at ","")
            contributors = data[4]
        else:
            # if hold it not ready
            if "Not ready" in data[8]:
                status = "Not Ready"
                item_date = data[10].replace("Expires on ","")
            else:
                status = "Ready"
                item_date = data[10].replace("Pick up by ", "")

            branch = data[9].replace("Pick up at ","")
            contributors = data[3]
        return Item(date_today,title,contributors,item_format,True,item_date,status,branch,'durham')
    
    def create_book_item_checked_out(self, date_today,data):
        # Check if renewed
        status = ''
        title, item_format = data[2].rsplit(", ",1)
        if self.item_data_has_subtitle(item_format, False, data):
            # if hold it not ready
            if "Due later" in data[8]:
                status = "Due Later"
            elif "Due soon" in data[8]:
                status = "Due Soon"
            else:
                status = "Overdue"
            item_date = data[9].replace("Due by ", "")
            branch = ''
            contributors = data[4]
        else:
            # if hold it not ready
            if "Due soon" in data[7]:
                status = "Not Ready"
            elif "Due later" in data[7]:
                status = "Due Later"
            else:
                status = "Overdue"
            item_date = data[8].replace("Due by ", "")
            branch = ''
            contributors = data[3]
        return Item(date_today,title,contributors,item_format,False,item_date,status,branch,'durham')

    def create_item_object_checked_out(self, date_today, data):
        _, item_format = data[2].rsplit(", ",1)
        if "DVD" in item_format:
            return self.create_dvd_item_checked_out(date_today, data)
        elif ("CD" in item_format):
            return self.create_cd_item_checked_out(date_today, data)
        elif ("Book" in item_format):
            return self.create_book_item_checked_out(date_today, data)
        else:
            return Item()

    def create_item_object_on_hold(self, date, data):
        _, item_format = data[2].rsplit(", ",1)
        if "DVD" in item_format:
            return self.create_dvd_item_on_hold(date, data)
           
        elif ("CD" in item_format):
            return self.create_cd_item_on_hold(date, data)
        elif ("Book" in item_format):
            return self.create_book_item_on_hold(date, data)
        else:
            return Item()

    def create_item_object(self, date, is_hold, data):
        if is_hold:
            return self.create_item_object_on_hold(date, data)
        else:
            return self.create_item_object_checked_out(date, data)

    def formulate_checkouts_text(self, checkouts):
        res = '\n'+self.region +' CHECKOUTS ({}):\n'.format(date.today())
        i = 1
        for item in checkouts:
            res += str(i) + '. ' + item.text_string() + '\n'
            i+=1
        return res
        
    def formulate_holds_text(self, checkouts):
        res = '\n'+self.region +' HOLDS ({}):\n'.format(date.today())
        i = 1
        for item in checkouts:
            res += str(i) + '. ' + item.text_string() + '\n'
            i+=1
        return res
        

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
        self._name = "Pickering Public Library"

    def hold_data(self,username,password):
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

        checkouts = self.driver.find_elements_by_css_selector("div.cp-batch-actions-list-item")

        for item in checkouts:
            lines = item.text.split('\n')
            res.append(lines)
        return res

    def items_on_hold(self,username,password):
        '''Scrapes and returns the items on hold for the user with the login credentials given'''
        # record datetime this data was scraped
        # scrape for items on hold only
        res =[]
        hold_data = self.hold_data(username,password)
        for lines in hold_data:
            hold_item = self.create_item_object(date.today(), True,lines)
            if hold_item.title:
                res.append(hold_item)
        return res

    def items_checked_out(self,username,password):
        '''Scrapes and returns the items checked out for the user with the login credentials given'''
        
        res = []
        checkout_data = self.checkout_data(username,password)
        for lines in checkout_data:
            checkout_item = self.create_item_object_checked_out(date.today(),lines)
            if checkout_item.title:
                res.append(checkout_item)
        return res

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
            raise NoSuchElementException("Hours for {} cannot be found because the branch does not exist".format(branch))


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
        self._name = "Whitby Public Library"

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
        res = []
        hold_data = self.hold_data(username,password)
        for lines in hold_data:
            hold_item = self.create_item_object(date.today(), True,lines)
            if hold_item.title:
                res.append(hold_item)
        return res

    def items_checked_out(self,username,password):
        '''Scrapes and returns the items checked out for the user with the login credentials given'''
        res = []
        checkout_data = self.checkout_data(username,password)
        for lines in checkout_data:
            check_out_item = self.create_item_object_checked_out(date.today(),lines)
            res.append(check_out_item)
        return res

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
            raise NoSuchElementException("Hours for {} cannot be found because the branch does not exist".format(branch))
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
