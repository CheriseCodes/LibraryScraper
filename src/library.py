import bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.wait import IGNORED_EXCEPTIONS
import copy
from datetime import date

login_info = {"p":("casualreader", "7422"), "w":("not_so_casual_reader", "2103"), "t":("27131040634604","647458768")}

class Item:
    def __init__(self, date_retrived, title, contributors, format, type, item_date, status):
        self.date_retrieved = date_retrived # the date the data was retrieved from the website
        self.title = title
        self.contributors = contributors
        self.format = format
        self.type = type # HOLD or CHECKOUT
        self.status = status # the status of the item depending on _type
        self.item_date = item_date # the pick up date or due date depending on _type

    def __str__(self):
        action = ""
        if self.type == "HOLD":
            action = "picked up"
        elif self.type == "CHECKOUT":
            action = "returned"

        if self.contributors == "":
            return self.title +  " ("+ self.format + ") to be " + action + " by " + self.item_date
        else:
            return self.title +  " ("+ self.format + ") by " +self.contributors + " to be " + action + " by " + self.item_date

class PPL:
    '''Class for Pickering Public Library'''
    def __init__(self, driver, branch="Central"):
        self._driver = driver
        self._name = "Pickering Public Library"
        self._branch = branch
        self._hours = self._get_hours()
        self._items_on_hold = self._get_items_on_hold()
        self._items_checked_out = self._get_items_checked_out()

    def _get_items(self):
        # record datetime this data was scraped
        # scrape the website for all items on hold and checked out
        self._get_items_checked_out()
        self._get_items_on_hold()
        pass

    def _get_items_on_hold(self):
        # record datetime this data was scraped
        # scrape for items on hold only

        res = []
        self._driver.get("https://pickering.bibliocommons.com/user/login?destination=%2Fv2%2Fholds")

        self._login()
        #login_ppl(driver=self._driver)

        #ignored_exceptions = (NoSuchElementException,StaleElementReferenceException)
        print("Navigated to:",self._driver.title)
        # https://whitby.bibliocommons.com/holds
        WebDriverWait(driver=self._driver, timeout=10).until(
            EC.title_is("On Hold | Pickering Public Library | BiblioCommons")
        )
        print("Navigated to:",self._driver.title)

        #pickup = self._driver.find_elements_by_css_selector("div.cp-batch-actions-list-item")
        pickup = self._driver.find_elements_by_css_selector("div.cp-batch-actions-list-item")

        #WebDriverWait(driver=self._driver, timeout=30)
        if pickup:
            date_retrieved = date.today()
        for item in pickup:
            i = 0
            lines = item.text.split('\n')
            for line in lines:
                print(i, ".",line)
                i+=1
            
            title_format = lines[2].split(", ")

            if "Not ready" in lines[7]:
                status = "not ready"
            else:
                status = "ready"
            
            if status == "not ready":
                print(lines[9].rindex("Expires on "))
                hold_date = lines[9].replace("Expires on ","")
            else:
                hold_date = lines[9].replace("Pick up by ", "")
    
            contributors = lines[6]
            #print(lines[3])
            #print(lines)
            hold_item = Item(date_retrieved,title_format[0],contributors,title_format[1],"HOLD",hold_date,status)
            
            res.append(hold_item)

        return res

    def _get_items_checked_out(self):
        # scrape
        return []

    def _get_hours(self):
        '''Scrapes the website for the hours of this branch'''
        return ""

    def get_items_checked_out(self):
        '''Return a copy of the items that were checked out'''
        return copy.deepcopy(self._items_checked_out)

    def get_items_on_hold(self):
        '''Return a copy of the items that are on hold'''
        return copy.deepcopy(self._items_on_hold)

    def get_hours(self):
        '''Return the hours this library is open'''
        return self._hours

    def _login(self):
        #ignored_exceptions = (NoSuchElementException,StaleElementReferenceException)
        #try:
        user_login = WebDriverWait(driver=self._driver, timeout=10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,"input[testid=field_username]"))
        )
        #WebDriverWait(driver=self._driver, timeout=20)
        pass_login = WebDriverWait(driver=self._driver, timeout=10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,"input[testid=field_userpin]"))
        )
        #WebDriverWait(driver=self._driver, timeout=20)
        submit_login = WebDriverWait(driver=self._driver, timeout=10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,"input[testid=button_login]"))
        )
        #WebDriverWait(driver=self._driver, timeout=20)
        if user_login and pass_login and submit_login:
            user_login.send_keys(login_info["p"][0])
            pass_login.send_keys(login_info["p"][1])
            #driver.execute_script('arguments[0].click()',submit_login)
            submit_login.click()
        #except TimeoutException as e:
        #    print("No login needed")

class WPL:
    '''Class for Whitby Public Library'''
    def __init__(self, driver, branch="Central"):
        self._driver = driver
        self._name = "Whitby Public Library"
        self._branch = branch
        self._hours = ""
        self._items_on_hold = []
        self._items_checked_out = []

    def _get_items(self):
        # record datetime this data was scraped
        # scrape the website for all items on hold and checked out
        pass

    def _get_items_on_hold(self):
        # record datetime this data was scraped
        # scrape for items on hold only
        res = []
        self._driver.get("https://whitby.bibliocommons.com/user/login?destination=%2Fholds")

        self._login()

        print("Waiting for page to load")
        
        #ignored_exceptions = (NoSuchElementException,StaleElementReferenceException)
        
        # https://whitby.bibliocommons.com/holds
        #el_to_click = WebDriverWait(driver=self._driver, timeout=10, ignored_exceptions=ignored_exceptions).until(
        #    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,"holds"))
        #)
        #if el_to_click:
        #    print(el_to_click.text, el_to_click.get_attribute("href"))
        #    driver.execute_script("arguments[0].click()",el_to_click)
            

        # login_wpl(driver=self._driver)
        
        print("Navigated to hold page")
        WebDriverWait(driver=self._driver, timeout=10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#content > div > div > div.borrowing-content.col-12.col-xs-12.col-sm-12.col-md-12.col-lg-9.cp-layout-main-content > div > div > div > div.cp-borrowing-list > div.cp-holds-list > div > div.cp-item-list > div > div.batch-actions-list-item-details > div")))
        
        pickup = self._driver.find_elements_by_css_selector("#content > div > div > div.borrowing-content.col-12.col-xs-12.col-sm-12.col-md-12.col-lg-9.cp-layout-main-content > div > div > div > div.cp-borrowing-list > div.cp-holds-list > div > div.cp-item-list > div > div.batch-actions-list-item-details > div")
        print("Retrieved items ready for pickup")
        
        if pickup:
            date_retrieved = date.today()
        
        for item in pickup:
            i = 0
            lines = item.text.split('\n')
            
            for line in lines:
                print(i, ".", line)
            #    if (i==1) or (i==3) or (i==4):
            #        print_line = True
            #    if print_line:
            #        print(i, '. ', line)
            #    i+=1
            #    print_line = False

            # TODO: new_hold = Item(...date_retrieved...)
            # TODO: res.append(new_hold)
            if "ready" in item.get_attribute("class"):
                print("IS READY FOR PICK UP")
            else:
                print("IS NOT READY FOR PICKUP")

        return res

    def _get_items_checked_out(self):
        # scrape
        pass

    def _get_hours(self):
        '''Gets the hours for this branch'''
        pass

    def get_items_checked_out(self):
        '''Return a copy of the items that were checked out'''
        pass

    def get_items_on_hold(self):
        '''Return a copy of the items that are on hold'''
        pass

    def get_hours(self):
        '''Return the hours this library is open'''
        pass

    def _login(self):
        ignored_exceptions = (NoSuchElementException,StaleElementReferenceException)

        try:
            user_login = WebDriverWait(driver=self._driver, timeout=10, ignored_exceptions=ignored_exceptions).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,"input[testid=field_username]"))
            )
            pass_login = WebDriverWait(driver=self._driver, timeout=10, ignored_exceptions=ignored_exceptions).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,"input[testid=field_userpin]"))
            )
            submit_login = WebDriverWait(driver=self._driver, timeout=10, ignored_exceptions=ignored_exceptions).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,"input[testid=button_login]"))
            )
            if user_login and pass_login and submit_login:
                user_login.send_keys(login_info["w"][0])
                pass_login.send_keys(login_info["w"][1])
                submit_login.click()
        except TimeoutException as e:
            print("No login needed")

class TPL:
    '''Class for Whitby Public Library'''
    def __init__(self, driver, branch="Highland Creek"):
        self._driver = driver
        self._name = "Toronto Public Library"
        self._branch = branch
        self._hours = ""
        self._items_on_hold = []
        self._items_checked_out = []

    def _get_items(self):
        # record datetime this data was scraped
        # scrape the website for all items on hold and checked out
        pass

    def _get_items_on_hold(self):
        res = []
        # record datetime this data was scraped
        # scrape for items on hold only
        self._driver.get("https://account.torontopubliclibrary.ca/holds")

        self._login()

        WebDriverWait(driver=self._driver, timeout=10).until(
            EC.title_is("Holds : Toronto Public Library")
        )

        ignored_exceptions=(NoSuchElementException)
        #TODO: When poetry book is ready for pickup, distinguish between ready and not ready
        pickup = WebDriverWait(driver=self._driver, timeout=10, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.holds-redux.ready-for-pickup td div"))
        )
        if pickup:
            date_retrieved = date.today()
        
        for item in pickup:
            i = 0
            lines = item.text.split('\n')
            
            for line in lines:
                print(i, ".", line)
           # for i in range(0,len(pickup),5):
           #     print(i, pickup[i].text, "by", pickup[i+1].text, "IS READY FOR PICKUP",pickup#[i+4].text) 
        return res

    def _get_items_checked_out(self):
        # scrape
        pass

    def _get_hours(self):
        '''Scrapes the website for the hours for this branch'''
        pass
    def get_items_checked_out(self):
        '''Return a copy of the items that were checked out'''
        pass

    def get_items_on_hold(self):
        '''Return a copy of the items that are on hold'''
        pass

    def get_hours(self):
        '''Return the hours this library is open'''
        pass

    def _login(self):
        user_lgn = self._driver.find_element_by_id("userID")
        pass_lgn = self._driver.find_element_by_id("password")
        submit_lgn = self._driver.find_element_by_css_selector("#form_signin > div > button")
        user_lgn.send_keys(login_info["t"][0])
        pass_lgn.send_keys(login_info["t"][1])
        submit_lgn.click()
    
    
def get_tpl_due_dates():
    return None

def get_ppl_due_dates():
    return None

def get_wpl_due_dates():
    return None


def get_tpl_hours():
    return None

def get_wpl_hours():
    return None

def get_ppl_hours():
    return None

def scrape_due_dates(library):
    pass

def scrape_holds(library):
    if library == "p":
        #get_ppl_holds()
        pass
    elif library == "w":
        #get_wpl_holds()
        pass
    elif library == "t":
        #get_tpl_holds()
        pass
    else:
        print(library, "is not a valid input. Enter w for Whitby Public Library. Enter p for Pickering Public Library. Enter t for Toronto Public Library.")

def scrape_hours(library):
    if library == "p":
        get_ppl_hours()
    elif library == "w":
        get_wpl_hours()
    elif library == "t":
        get_tpl_hours()
    else:
        print(library, "is not a valid input. Enter w for Whitby Public Library. Enter p for Pickering Public Library. Enter t for Toronto Public Library.")
    return None

def scrape_due_dates(library):
    if library == "p":
        get_ppl_due_dates()
    elif library == "w":
        get_wpl_due_dates()
    elif library == "t":
        get_tpl_due_dates()
    else:
        print(library, "is not a valid input. Enter w for Whitby Public Library. Enter p for Pickering Public Library. Enter t for Toronto Public Library.")
    return None

def scrape_all(library):
    if library == "p":
        #get_ppl_holds()
        get_ppl_due_dates()
        get_ppl_hours()
    elif library == "w":
        pass
        #get_wpl_holds()
    elif library == "t":
        pass
        #get_tpl_holds()
    else:
        print(library, "is not a valid input. Enter w for Whitby Public Library. Enter p for Pickering Public Library. Enter t for Toronto Public Library.")