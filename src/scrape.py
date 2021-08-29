import bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.wait import IGNORED_EXCEPTIONS

usernames = ["not_so_casual_reader","casualreader","27131040634604"]
passwords = ["2103","7422","647458768"]

def login_wpl(driver):
    ignored_exceptions = (NoSuchElementException,StaleElementReferenceException)

    try:
        user_login = WebDriverWait(driver=driver, timeout=10, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,"input[testid=field_username]"))
        )
        pass_login = WebDriverWait(driver=driver, timeout=10, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,"input[testid=field_userpin]"))
        )
        submit_login = WebDriverWait(driver=driver, timeout=10, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,"input[testid=button_login]"))
        )
        if user_login and pass_login and submit_login:
            user_login.send_keys(usernames[0])
            pass_login.send_keys(passwords[0])
            submit_login.click()
    except TimeoutException as e:
        print("No login needed")

def login_tpl(driver):
    user_lgn = driver.find_element_by_id("userID")
    pass_lgn = driver.find_element_by_id("password")
    submit_lgn = driver.find_element_by_css_selector("#form_signin > div > button")
    user_lgn.send_keys(usernames[2])
    pass_lgn.send_keys(passwords[2])
    submit_lgn.click()
    #driver.execute_script('arguments[0].click()',submit_lgn)

def login_ppl(driver):
    #ignored_exceptions = (NoSuchElementException,StaleElementReferenceException)

    #try:
    user_login = WebDriverWait(driver=driver, timeout=10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,"input[testid=field_username]"))
    )
    #WebDriverWait(driver=driver, timeout=20)
    pass_login = WebDriverWait(driver=driver, timeout=10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,"input[testid=field_userpin]"))
    )
    #WebDriverWait(driver=driver, timeout=20)
    submit_login = WebDriverWait(driver=driver, timeout=10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,"input[testid=button_login]"))
    )
    #WebDriverWait(driver=driver, timeout=20)
    if user_login and pass_login and submit_login:
        user_login.send_keys(usernames[1])
        pass_login.send_keys(passwords[1])
        #driver.execute_script('arguments[0].click()',submit_login)
        submit_login.click()
    #except TimeoutException as e:
    #    print("No login needed")

def get_wpl_holds():
    driver = webdriver.Chrome("chromedriver")

    driver.get("https://whitby.bibliocommons.com/user/login?destination=%2Fholds")

    login_wpl(driver=driver)


    print("Waiting for page to load")
    ignored_exceptions = (NoSuchElementException,StaleElementReferenceException)
    
    # https://whitby.bibliocommons.com/holds
    #el_to_click = WebDriverWait(driver=driver, timeout=10, ignored_exceptions=ignored_exceptions).until(
    #    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,"holds"))
    #)
    #if el_to_click:
    #    print(el_to_click.text, el_to_click.get_attribute("href"))
    #    driver.execute_script("arguments[0].click()",el_to_click)
        

    # login_wpl(driver=driver)
    
    print("Navigated to hold page")
    WebDriverWait(driver=driver, timeout=10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#content > div > div > div.borrowing-content.col-12.col-xs-12.col-sm-12.col-md-12.col-lg-9.cp-layout-main-content > div > div > div > div.cp-borrowing-list > div.cp-holds-list > div > div.cp-item-list > div > div.batch-actions-list-item-details > div")))
    
    pickup = driver.find_elements_by_css_selector("#content > div > div > div.borrowing-content.col-12.col-xs-12.col-sm-12.col-md-12.col-lg-9.cp-layout-main-content > div > div > div > div.cp-borrowing-list > div.cp-holds-list > div > div.cp-item-list > div > div.batch-actions-list-item-details > div")
    print("Retrieved items ready for pickup")
    
    for item in pickup:
        i = 1
        print_line = False
        lines = item.text.split('\n')
        
        for line in lines:
            if (i==1) or (i==3) or (i==4):
                print_line = True
            if print_line:
                print(i, '. ', line)
            i+=1
            print_line = False

        if "ready" in item.get_attribute("class"):
            print("IS READY FOR PICK UP")
        else:
            print("IS NOT READY FOR PICKUP")

    driver.close()

def get_ppl_holds():
    driver = webdriver.Chrome("chromedriver")

    driver.get("https://pickering.bibliocommons.com/user/login?destination=%2Fv2%2Fholds")

    login_ppl(driver=driver)
    #login_ppl(driver=driver)

    #ignored_exceptions = (NoSuchElementException,StaleElementReferenceException)
    print("Navigated to:",driver.title)
    # https://whitby.bibliocommons.com/holds
    WebDriverWait(driver=driver, timeout=10).until(
        EC.title_is("On Hold | Pickering Public Library | BiblioCommons")
    )
    print("Navigated to:",driver.title)

    pickup = driver.find_elements_by_css_selector("div.cp-batch-actions-list-item")
    pickup_ready = driver.find_elements_by_css_selector("div.cp-batch-actions-list-item")

    #WebDriverWait(driver=driver, timeout=30)
    i = 1
    for item in pickup_ready:
        lines = item.text.split('\n')
        #print(i, ".",item.text)
        i+=1
        print(lines[1])
        print(lines[3])

        if ("ready" in item.get_attribute("class")):
            print("IS READY")
        else:
            print("IS NOT READY")
    
    driver.close()

def get_tpl_holds():
    driver = webdriver.Chrome("chromedriver")
    driver.get("https://account.torontopubliclibrary.ca/holds")

    login_tpl(driver=driver)

    WebDriverWait(driver=driver, timeout=10).until(
        EC.title_is("Holds : Toronto Public Library")
    )

    ignored_exceptions=(NoSuchElementException)
    #TODO: When poetry book is ready for pickup, distinguish between ready and not ready
    pickup = WebDriverWait(driver=driver, timeout=10, ignored_exceptions=ignored_exceptions).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.holds-redux.ready-for-pickup td div"))
    )

    if pickup:
        for i in range(0,len(pickup),5):
            print(i, pickup[i].text, "by", pickup[i+1].text, "IS READY FOR PICKUP",pickup[i+4].text) 



    return None
    
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
    return None

def scrape_holds(library):
    if library == "p":
        get_ppl_holds()
    elif library == "w":
        get_wpl_holds()
    elif library == "t":
        get_tpl_holds()
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
        get_ppl_holds()
        get_ppl_due_dates()
        get_ppl_hours()
    elif library == "w":
        get_wpl_holds()
    elif library == "t":
        get_tpl_holds()
    else:
        print(library, "is not a valid input. Enter w for Whitby Public Library. Enter p for Pickering Public Library. Enter t for Toronto Public Library.")