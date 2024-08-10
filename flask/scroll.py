from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC  
import time
from selenium.webdriver.common.action_chains import ActionChains



def create_driver():

    # the webdriver with connect with the web and the chromeoptions can setting the web
    chrome_options=webdriver.ChromeOptions()
    # make the web fun at the back
    chrome_options.add_argument("--headless")
    # make sure they read all the screen
    chrome_options.add_argument("--window-size=1920,1080")
    # webdriver.Chrome was one class for the selenium
    # the Service was the Service class for manage // hromeDriverManager().install() download and return the pass
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver
def open_url(driver,url):
    driver.get(url)
    # wait the driver run success and the maximum waiting time was the 20 second 
    # untill will always waiting ultile the (condition) because true
    # the condition was until the class=hfpxzc succesful see the line 27
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'hfpxzc')))

    except Exception as e:
        return 1

def scroll_to_end(driver,page):
    page = page
    scroll_count = 0

    try:
        #  use the Xpath to find the scroll container
        scroll_container = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]')
        print("\033[1;31mFound scroll container\033[0m")
    except Exception as e:
        return 2

    while True:
        try:
            # the execute_script can make use use the javascript command in the screen
            #  set the scrolltop to = the height
            #  the function was the scroll
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_container)

            time.sleep(3)  # 等待页面加载
            # action was a class of selen
            #  move to the scroll container element 
            ActionChains(driver).move_to_element(scroll_container).perform()

        except Exception as e:
            return 1

        scroll_count += 1
        if scroll_count >= page:
            break



def get_company_names(driver):
    i=0
    name={}
    name_company=driver.find_elements(By.CLASS_NAME,'hfpxzc')
    #  the driver.find_elements will return a list and through the class_name to looking for hfpxzc
    elements = driver.find_elements(By.CSS_SELECTOR, '.lcr4fd.S9kvJb')
    if elements and name_company:
        # the zip can combined two element 
        for element,company in zip(elements,name_company):
            # get the value of aria-label for each element
            i+=1
            company=company.get_attribute('aria-label')
            href= element.get_attribute('href')
            if href and company:
                name[company] = href
    else:
        print("No company")
    return name
def url_fun(basic,address,z):
        basic=basic
        z=z
        url = f'{basic}{address},{z}z?entry=ttu'
        return url
def main():
    pass

if __name__ == "__main__":
    main()
