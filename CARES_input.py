import xml.etree.ElementTree as ET
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
from selenium.webdriver.common.by import By
import time


file_path = 'XML_files/emscharts/emsCharts_4-12_6-6.xml'

# Parse the XML file
tree = ET.parse(file_path)
root = tree.getroot()

# [0] = DATE_DISPATCHED
# [1] = PRID
# [2] = DISPATCH_ID
# [3] = REF__ADDRESS_LINE_1
# [4] = REF__CITY
# [5] = REC__ZIP_CODE
# [6] = FIRST_NAME
# [7] = LAST_NAME
# [8] = DATE_OF_BIRTH
# [9] = GENDER
# [10] = RACE
# [11] = RECEIVING_HOSPITAL
# [12] = WHO_WITNESSED
# [13] = ETIOLOGY
# [14] = END_EVENT
# [15] = AED_BY
# [16] = AED_USE
# [17] = CPR_PROVIDED_PRIOR_TO_EMS_ARRIVAL
# [18] = DATE_TIME_OF_CPR
# [19] = DATE_TIME_OF_DEFIB
# [20] = DEFIBRILLATOR_TYPE
# [21] = DATE_TIME_CPR_DISCONTINUED
# [22] = INITIAL_RHYTHM
# [23] = REASON_CPR_TERMINATED
# [24] = DATE_TIME_CIRCULATION_RESTORED
# [25] = INITIATE_IV___TYPE
# [26] = DISPOSITION__OUTCOME_
# [27] = DATE_ENROUTE
# [28] = DATE_ARRIVED
# [29] = DATE_AT_PT
# [30] = DATE_LEAVE_REF
# [31] = DATE_ARRIVE_REC


def create_unique_case_list() -> list:
    unique_cases = []
    unique_cases_by_PRID = []
    for child in root:
        if child[1].text not in unique_cases_by_PRID:
            unique_cases_by_PRID.append(child[1].text)
            unique_cases.append(child)
    
    return unique_cases

def main():
    unique_cases = create_unique_case_list()

    # Set up the Selenium webdriver
    PATH = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
    driver = webdriver.Chrome(PATH, chrome_options=chrome_options)

    
    driver.get('https://mycares.net')
    time.sleep(2)

    USER_NAME = 'zphillips'
    user_name_input = driver.find_element(By.NAME, 'username')
    user_name_input.send_keys(USER_NAME)
    # time.sleep(2)
    PASSWORD = 'Winter2023!'
    password_input = driver.find_element(By.NAME, 'password')
    password_input.send_keys(PASSWORD)

    login_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="Login"]')
    login_button.click()

    time.sleep(3)

    driver.get('https://mycares.net/secure/formCaresRev4.jsp')

    for case in unique_cases:
        # Extract the required data from the case element
        # [3] = REF__ADDRESS_LINE_1
        incident_address = case[3].text
        # [4] = REF__CITY
        incident_city = case[4].text
        # [5] = REC__ZIP_CODE
        incident_zip = case[5].text
        # [6] = FIRST_NAME
        fname = case[6].text
        # [7] = LAST_NAME
        lname = case[7].text
        # [8] = DATE_OF_BIRTH
        # TODO: Make sure that there is a DOB prior to trying to split.
        dob = case[8].text
        dob_date_only = dob.split(' ')[0]
        # [0] = DATE_DISPATCHED
        # [1] = PRID
        # [2] = DISPATCH_ID
        
       
        
        
        
        
        # [9] = GENDER
        # [10] = RACE
        # [11] = RECEIVING_HOSPITAL
        # [12] = WHO_WITNESSED
        # [13] = ETIOLOGY
        # [14] = END_EVENT
        # [15] = AED_BY
        # [16] = AED_USE
        # [17] = CPR_PROVIDED_PRIOR_TO_EMS_ARRIVAL
        # [18] = DATE_TIME_OF_CPR
        # [19] = DATE_TIME_OF_DEFIB
        # [20] = DEFIBRILLATOR_TYPE
        # [21] = DATE_TIME_CPR_DISCONTINUED
        # [22] = INITIAL_RHYTHM
        # [23] = REASON_CPR_TERMINATED
        # [24] = DATE_TIME_CIRCULATION_RESTORED
        # [25] = INITIATE_IV___TYPE
        # [26] = DISPOSITION__OUTCOME_
        # [27] = DATE_ENROUTE
        # [28] = DATE_ARRIVED
        # [29] = DATE_AT_PT
        # [30] = DATE_LEAVE_REF
        # [31] = DATE_ARRIVE_REC
        # Locate the input fields and input the data using Selenium
        incident_address_input = driver.find_element(By.NAME, 'IncidentAddress')
        incident_address_input.send_keys(incident_address)

        incident_city_input = driver.find_element(By.NAME, 'IncidentCity')
        incident_city_input.send_keys(incident_city)

        incident_zip_input = driver.find_element(By.NAME, 'IncidentZipCode')
        incident_zip_input.send_keys(incident_zip)

        fname_input = driver.find_element(By.NAME, 'FirstName')
        fname_input.send_keys(fname)

        lname_input = driver.find_element(By.NAME, 'LastName')
        lname_input.send_keys(lname)

        dob_input = driver.find_element(By.NAME, 'dateofbirth')
        dob_input.send_keys(dob_date_only)








        

if __name__ == "__main__":
    main()

      