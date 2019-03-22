from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pprint
import json




class Actions(ActionChains):
    def wait(self, time_s: float):
        self._actions.append(lambda: sleep(time_s))
        return self


def scrap_flights(destination, departure_date, returning_date):
    url = "https://www.google.com.au/flights/explore"
    
    origin_name = 'Sydney' # Change this to your city 
    destination_name = str(destination) #'Tokyo'

    checkInDate = departure_date #'27/08/2019' #Format %d/%m/%Y
    checkOutDate = returning_date #'29/08/2019' #Format %d/%m/%Y

    driver = webdriver.Chrome('/Users/senvanle/python-projects/travel-project/chromedriver')
    action = ActionChains(driver)
    driver.get(url)

    time_out = 20

    sleep(10)

    origin_menu = driver.find_elements_by_xpath('//div[@data-flt-ve="destination_airport"]')
    sleep(2)
   
    Actions(driver) \
        .move_to_element(origin_menu[7]).click(origin_menu[7]) \
        .wait(2) \
        .send_keys(destination_name) \
        .wait(2) \
        .send_keys(Keys.ENTER) \
        .perform()

    sleep(5)

    try:
        WebDriverWait(driver, time_out).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='gws-flights-results__breadcrumb-step-heading']")))

    except TimeoutException:
        pass

    url = driver.current_url
    driver.quit()

    driver = webdriver.Chrome('/Users/senvanle/python-projects/travel-project/chromedriver')
    driver.get(url)

    sleep(6)

    results = driver.find_elements_by_xpath('//div[contains(@class, "gws-flights-results__itinerary-card-summary")]')

    html_list = [BeautifulSoup(html.get_attribute('innerHTML'), "html.parser") for html in results]

    driver.quit()
    #soup = BeautifulSoup(html, "html.parser")
    flight_details = []

    for e, soup in enumerate(html_list):
        
        try:
            details = {
            
                "flight_time": ' '.join(str(soup.select('div[class*="results__times"]')[0].text).split()[:-1]),
                "airline": ' '.join(str(soup.select('div[class*="results__carriers"]')[0].text).split()),
                "duration": ' '.join(str(soup.select('div[class*="results__duration"]')[0].text).split()),
                "airports": ' '.join(str(soup.select('div[class*="results__airports"]')[0].text).split()),
                "stops": ' '.join(str(soup.select('div[class*="results__stops"]')[0].text).split()),
                "layover": str(soup.select('div[class*="results__layover"]')[0].text).split(),
                "price": str(soup.select('div[class*="results__price"]')[0].text).split()[0]
            
            }

        except:
            continue


        flight_details.append(details)
        

    pprint.pprint(flight_details)
    return flight_details
    






