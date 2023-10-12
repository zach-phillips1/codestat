import xml.etree.ElementTree as ET
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException
import time
import logging

USER_NAME = "zphillips"
PASSWORD = "Summer2023!"


file_path = "XML_files/emscharts/emsCharts_6-7_10-11.xml"
logging.basicConfig(
    filename='logs/CARES_input.log',  # Specify the name of your log file
    level=logging.WARNING,  # Set the logging level (you can adjust this)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

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
    # A list that has things that need to be addressed.
    cases_that_need_looking = []
    unique_cases = create_unique_case_list()

    options = Options()
    options.add_argument("--start-maximized")  # Maximize the browser window
    options.add_argument("--disable-extensions")  # Disable browser extensions
    # Set up the Selenium webdriver
    PATH = "C:\chromedriver\chromedriver.exe"
    driver = webdriver.Chrome(options=options)

    driver.get("https://mycares.net")
    time.sleep(2)

    user_name_input = driver.find_element(By.NAME, "username")
    user_name_input.send_keys(USER_NAME)
    # time.sleep(2)

    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(PASSWORD)

    login_button = driver.find_element(
        By.CSS_SELECTOR, 'input[type="submit"][value="Login"]'
    )
    login_button.click()

    time.sleep(2)

    driver.get("https://mycares.net/secure/formCaresRev4.jsp")

    for case in unique_cases:
        # Extract the required data from the case element
        # [3] = REF__ADDRESS_LINE_1
        incident_address = case[3].text.upper()
        incident_address_input = driver.find_element(By.NAME, "IncidentAddress")
        incident_address_input.send_keys(incident_address)

        # [4] = REF__CITY
        incident_city = case[4].text.upper()
        incident_city_input = driver.find_element(By.NAME, "IncidentCity")
        incident_city_input.send_keys(incident_city)

        # [5] = REC__ZIP_CODE
        if not case[5].text:
            incident_zip = ""
        else:
            incident_zip = case[5].text
        incident_zip_input = driver.find_element(By.NAME, "IncidentZipCode")
        incident_zip_input.send_keys(incident_zip)

        # [6] = FIRST_NAME
        fname = case[6].text
        fname_input = driver.find_element(By.NAME, "FirstName")
        fname_input.send_keys(fname)

        # [7] = LAST_NAME
        lname = case[7].text
        lname_input = driver.find_element(By.NAME, "LastName")
        lname_input.send_keys(lname)

        # [8] = DATE_OF_BIRTH
        # Make sure that there is a DOB prior to trying to split.
        dob = case[8].text
        if dob:
            dob_date_only = dob.split(" ")[0]
        else:
            dob_date_only = ""
        dob_input = driver.find_element(By.NAME, "dateofbirth")
        dob_input.send_keys(dob_date_only, Keys.TAB)

        # [0] = DATE_DISPATCHED
        # Split the date and time
        date_of_arrest, dispatch_time = case[0].text.split()

        # Separate the hours and minutes
        dispatch_hours, dispatch_minutes = dispatch_time.split(":")

        date_of_arrest_input = driver.find_element(By.NAME, "todaysdate")
        date_of_arrest_input.send_keys(date_of_arrest)

        dispatch_hours_input = driver.find_element(By.NAME, "AmbDispatched_Hours")
        dispatch_hours_input.send_keys(dispatch_hours)

        dispatch_minutes_input = driver.find_element(By.NAME, "AmbDispatched_Minutes")
        dispatch_minutes_input.send_keys(dispatch_minutes)

        # [2] = DISPATCH_ID
        dispatch_ID = case[2].text
        dispatch_ID_input = driver.find_element(By.NAME, "CallNumberID")
        dispatch_ID_input.send_keys(dispatch_ID)

        # [27] = DATE_ENROUTE
        # Split the date and time
        date_of_enroute, enroute_time = case[27].text.split()

        # Separate the hours and minutes
        enroute_hours, enroute_minutes = enroute_time.split(":")

        enroute_hours_input = driver.find_element(By.NAME, "AmbEnRoute_Hours")
        enroute_hours_input.send_keys(enroute_hours)

        enroute_minutes_input = driver.find_element(By.NAME, "AmbEnRoute_Minutes")
        enroute_minutes_input.send_keys(enroute_minutes)

        # [28] = DATE_ARRIVED
        # Split the date and time
        date_of_arrive, arrive_time = case[28].text.split()

        # Separate the hours and minutes
        arrive_hours, arrive_minutes = arrive_time.split(":")

        arrive_hours_input = driver.find_element(By.NAME, "AmbArrivedAtScene_Hours")
        arrive_hours_input.send_keys(arrive_hours)

        arrive_minutes_input = driver.find_element(By.NAME, "AmbArrivedAtScene_Minutes")
        arrive_minutes_input.send_keys(arrive_minutes)

        # [29] = DATE_AT_PT
        # Split the date and time
        date_of_arrive_pt, arrive_pt_time = case[29].text.split()

        # Separate the hours and minutes
        arrive_pt_hours, arrive_pt_minutes = arrive_pt_time.split(":")

        arrive_pt_hours_input = driver.find_element(By.NAME, "EMSArrivedAtScene_Hours")
        arrive_pt_hours_input.send_keys(arrive_hours)

        arrive_pt_minutes_input = driver.find_element(
            By.NAME, "EMSArrivedAtScene_Minutes"
        )
        arrive_pt_minutes_input.send_keys(arrive_minutes)

        # [30] = DATE_LEAVE_REF
        if case[11].text:
            # Split the date and time
            date_of_transport, transport_time = case[30].text.split()

            # Separate the hours and minutes
            transport_hours, transport_minutes = transport_time.split(":")
        else:
            transport_hours = ""
            transport_minutes = ""

        transport_hours_input = driver.find_element(By.NAME, "AmbLeftScene_Hours")
        transport_hours_input.send_keys(transport_hours)

        transport_minutes_input = driver.find_element(By.NAME, "AmbLeftScene_Minutes")
        transport_minutes_input.send_keys(transport_minutes)

        # [31] = DATE_ARRIVE_REC
        if case[11].text:
            # Split the date and time
            date_of_transport_arrive, transport_arrive_time = case[31].text.split()

            # Separate the hours and minutes
            (
                transport_arrive_hours,
                transport_arrive_minutes,
            ) = transport_arrive_time.split(":")
        else:
            transport_arrive_hours = ""
            transport_arrive_minutes = ""

        transport_arrive_hours_input = driver.find_element(
            By.NAME, "AmbArrivedAtED_Hours"
        )
        transport_arrive_hours_input.send_keys(transport_arrive_hours)

        transport_arrive_minutes_input = driver.find_element(
            By.NAME, "AmbArrivedAtED_Minutes"
        )
        transport_arrive_minutes_input.send_keys(transport_arrive_minutes)

        # [9] = GENDER
        gender = case[9].text

        # Find the radio button elements by name and value
        radio_button_male = driver.find_element(
            By.CSS_SELECTOR, 'input[name="GenderID"][value="1"]'
        )
        radio_button_female = driver.find_element(
            By.CSS_SELECTOR, 'input[name="GenderID"][value="2"]'
        )

        if gender == "Male":
            radio_button_male.click()
        elif gender == "Female":
            radio_button_female.click()

        # [10] = RACE Handled in the Main
        # Race input
        # Define the race-to-checkbox-value mapping
        race_mapping = {
            "American-Indian/Alaska Native": "7",
            "Native Hawaiian/Pacific Islander": "4",
            "Asian": "1",
            "White": "6",
            "Black": "3",
            "Unknown": "8",
            "Hispanic/Latino": "9",
        }
        # Find the div element containing the checkboxes by its ID
        div_ethnicity = driver.find_element(By.ID, "EthnicityIDDiv")

        # Find all the checkbox elements within the div
        checkboxes = div_ethnicity.find_elements(
            By.CSS_SELECTOR, 'input[type="checkbox"][name="EthnicityID"]'
        )

        # Get the individual race values from case[10].text
        if case[10].text:
            race_values = case[10].text.split(",")

        # Handle the case where the race field is empty or missing
        if not case[10].text or case[10].text.strip() == "":
            # Do something when the race field is empty or missing
            pass

        # Handle the case where there is only one value
        elif len(race_values) == 1:
            race_value = race_values[0].strip()
            if race_value in race_mapping:
                checkbox_value = race_mapping[race_value]
                for checkbox in checkboxes:
                    if checkbox.get_attribute("value") == checkbox_value:
                        checkbox.click()
        # Handle the case where there are multiple values
        else:
            for race_value in race_values:
                race_value = race_value.strip()
                if race_value in race_mapping:
                    checkbox_value = race_mapping[race_value]
                    for checkbox in checkboxes:
                        if checkbox.get_attribute("value") == checkbox_value:
                            checkbox.click()

        # [11] = RECEIVING_HOSPITAL
        destination_hospital = case[11].text
        # Handles the Destination hospital
        # Locate drop down element
        destination_hospital_drop_down_element = driver.find_element(
            By.ID, "DestinationHospital"
        )
        # Create a Select object
        destination_hospital_drop_down = Select(destination_hospital_drop_down_element)
        # Map the hospitals from emsCharts to the value of CARES.
        hospital_mapping = {
            "Crozer-Chester Medical Center": 1010,
            "Main Line Health - Lankenau Medical Center": 1011,
            "Main Line Health - Bryn Mawr Hospital": 1165,
            "Mercy Fitzgerald Hospital": 973,
            "Taylor Hospital": 1571,
        }
        # Check if the hospital name exists in the hospital mapping
        if destination_hospital in hospital_mapping:
            # Get the corresponding CARES value for the hospital
            cares_hospital_value = hospital_mapping[destination_hospital]
            # Select the hospital in the dropdown by value
            destination_hospital_drop_down.select_by_value(str(cares_hospital_value))
        else:
            # Handle the case when the hospital name is not found in the mapping
            logging.warning(f"Hospital mapping not found for '{destination_hospital}'")

        # [12] = WHO_WITNESSED
        witnessed = case[12].text

        radio_button_unwitnessed = driver.find_element(
            By.CSS_SELECTOR, 'input[name="ArrestWitnessStatusID"][value="1"]'
        )
        radio_button_witness_bystander = driver.find_element(
            By.CSS_SELECTOR, 'input[name="ArrestWitnessStatusID"][value="2"]'
        )
        radio_button_witness_911 = driver.find_element(
            By.CSS_SELECTOR, 'input[name="ArrestWitnessStatusID"][value="3"]'
        )

        if witnessed == "Witnessed by Healthcare Provider":
            radio_button_witness_911.click()
        elif witnessed == "Witnessed by Bystander":
            radio_button_witness_bystander.click()
        else:
            radio_button_unwitnessed.click()

        # [13] = ETIOLOGY
        etiology = case[13].text

        button_etiology_cardiac = driver.find_element(
            By.CSS_SELECTOR, 'input[name="CardiacEtiology"][value="1"]'
        )
        button_etiology_trauma = driver.find_element(
            By.CSS_SELECTOR, 'input[name="CardiacEtiology"][value="2"]'
        )
        button_etiology_respiratory = driver.find_element(
            By.CSS_SELECTOR, 'input[name="CardiacEtiology"][value="3"]'
        )
        button_etiology_drowning = driver.find_element(
            By.CSS_SELECTOR, 'input[name="CardiacEtiology"][value="4"]'
        )
        button_etiology_electrocution = driver.find_element(
            By.CSS_SELECTOR, 'input[name="CardiacEtiology"][value="5"]'
        )
        button_etiology_exsanguination = driver.find_element(
            By.CSS_SELECTOR, 'input[name="CardiacEtiology"][value="8"]'
        )
        button_etiology_overdose = driver.find_element(
            By.CSS_SELECTOR, 'input[name="CardiacEtiology"][value="7"]'
        )
        button_etiology_other = driver.find_element(
            By.CSS_SELECTOR, 'input[name="CardiacEtiology"][value="6"]'
        )

        match etiology:
            case "Presumed Cardiac":
                button_etiology_cardiac.click()
            case "Not Known":
                button_etiology_cardiac.click()
            case "Traumatic Cause":
                button_etiology_trauma.click()
            case "Respiratory":
                button_etiology_respiratory
            case "Drug Overdose":
                button_etiology_overdose.click()
            case "Drowning":
                button_etiology_drowning.click()
                # There will need to be more, it might error out
            case "Exsanguination-Medical (Non-Traumatic)":
                button_etiology_exsanguination.click()
            case "Electrocution":
                button_etiology_electrocution.click()
            case "Other":
                button_etiology_other.click()
            case _:
                cases_that_need_looking.append(
                    f"Case {case[2].text} needs etiology checked."
                )

        # CARES 21
        button_resus_attempted = driver.find_element(
            By.CSS_SELECTOR, 'input[name="ResusAttemptEMS"][value="1"]'
        )
        button_resus_attempted.click()

        # [16] = AED_USE
        aed_use = case[16].text
        button_AED_use_with_defib = driver.find_element(
            By.CSS_SELECTOR, 'input[name="AEDUsedPriorEMS"][value="5"]'
        )
        button_AED_use_no_defib = driver.find_element(
            By.CSS_SELECTOR, 'input[name="AEDUsedPriorEMS"][value="6"]'
        )
        button_AED_not_used = driver.find_element(
            By.CSS_SELECTOR, 'input[name="AEDUsedPriorEMS"][value="3"]'
        )

        if aed_use == "Yes, Applied with Defibrillation":
            button_AED_use_with_defib.click()
        elif aed_use == "Yes, Applied without Defibrillation":
            button_AED_use_no_defib.click()
        else:
            button_AED_not_used.click()

        # [15] = AED_BY
        aed_by = case[15].text

        button_AED_applied_bystander = driver.find_element(
            By.CSS_SELECTOR, 'input[name="WhoFirstAppliedAED"][value="1"]'
        )
        button_AED_applied_family = driver.find_element(
            By.CSS_SELECTOR, 'input[name="WhoFirstAppliedAED"][value="2"]'
        )
        button_AED_applied_healthcare = driver.find_element(
            By.CSS_SELECTOR, 'input[name="WhoFirstAppliedAED"][value="6"]'
        )
        button_AED_applied_law_first = driver.find_element(
            By.CSS_SELECTOR, 'input[name="WhoFirstAppliedAED"][value="10"]'
        )
        button_AED_applied_non_law_first = driver.find_element(
            By.CSS_SELECTOR, 'input[name="WhoFirstAppliedAED"][value="11"]'
        )
        if aed_by:
            match aed_by:
                case "First Responder (Fire, Law, EMS)":
                    button_AED_applied_non_law_first.click()
                case "Healthcare Professional (Non-EMS)":
                    button_AED_applied_healthcare.click()
                case "Lay Person (Non-Family)":
                    button_AED_applied_bystander.click()
                case "Family Member":
                    button_AED_applied_family.click()

        # CARES 27 - Who first defibrillated the patient?
        # [20] = DEFIBRILLATOR_TYPE
        who_first_defib = case[20].text

        button_who_defib_NA = driver.find_element(
            By.CSS_SELECTOR, 'input[name="FirstDefibPatient"][value="8"]'
        )
        button_who_defib_bystander = driver.find_element(
            By.CSS_SELECTOR, 'input[name="FirstDefibPatient"][value="1"]'
        )
        button_who_defib_family = driver.find_element(
            By.CSS_SELECTOR, 'input[name="FirstDefibPatient"][value="2"]'
        )
        button_who_defib_healthcare = driver.find_element(
            By.CSS_SELECTOR, 'input[name="FirstDefibPatient"][value="5"]'
        )
        button_who_defib_law_first = driver.find_element(
            By.CSS_SELECTOR, 'input[name="FirstDefibPatient"][value="10"]'
        )
        button_who_defib_non_law_first = driver.find_element(
            By.CSS_SELECTOR, 'input[name="FirstDefibPatient"][value="11"]'
        )
        button_who_defib_EMS = driver.find_element(
            By.CSS_SELECTOR, 'input[name="FirstDefibPatient"][value="4"]'
        )

        # N/A
        # AED
        # Manual
        match who_first_defib:
            case "N/A":
                button_who_defib_NA.click()
            case "AED":
                button_who_defib_non_law_first.click()
            case "Manual":
                button_who_defib_EMS.click()

        # CARES 28 - Did 911 responder perform CPR | Always Yes
        button_responder_perform_cpr = driver.find_element(
            By.CSS_SELECTOR, 'input[name="911RespCPR"][value="1"]'
        )
        button_responder_perform_cpr.click()

        # [22] = INITIAL_RHYTHM | CARES 29
        initial_rhythm = case[22].text

        button_first_rhythm_VF = driver.find_element(
            By.CSS_SELECTOR, 'input[name="FirstRhythm"][value="0"]'
        )
        button_first_rhythm_PEA = driver.find_element(
            By.CSS_SELECTOR, 'input[name="FirstRhythm"][value="3"]'
        )
        button_first_rhythm_VT = driver.find_element(
            By.CSS_SELECTOR, 'input[name="FirstRhythm"][value="1"]'
        )
        button_first_rhythm_unknown_shockable = driver.find_element(
            By.CSS_SELECTOR, 'input[name="FirstRhythm"][value="6"]'
        )
        button_first_rhythm_asystole = driver.find_element(
            By.CSS_SELECTOR, 'input[name="FirstRhythm"][value="2"]'
        )
        button_first_rhythm_unknown_unshockable = driver.find_element(
            By.CSS_SELECTOR, 'input[name="FirstRhythm"][value="7"]'
        )

        # Asystole
        # Normal Sinus Rhythm (Need to remind people it's first arrest rhythm)
        # PEA
        # Ventricular Fibrillation
        # Unknown AED Shockable
        # Unknown AED Non-Shockable
        # Not Available
        # Bradycardia
        # Ventricular Tachycardia
        match initial_rhythm:
            case "Asystole":
                button_first_rhythm_asystole.click()
            case "PEA":
                button_first_rhythm_PEA.click()
            case "Ventricular Fibrillation":
                button_first_rhythm_VF.click()
            case "Ventricular Tachycardia":
                button_first_rhythm_VT.click()
            case "Unknown AED Shockable":
                button_first_rhythm_unknown_shockable.click()
            case "Unknown AED Non-Shockable":
                button_first_rhythm_unknown_unshockable.click()
            case _:
                cases_that_need_looking.append(
                    f"Case {case[2].text} needs initial rhythm checked."
                )

        # CARES 30 - Sustained ROSC

        # CARES 31 - TTM - Always No
        button_ttm_provided_no = driver.find_element(
            By.CSS_SELECTOR, 'input[name="Hypothermia_Provided"][value="2"]'
        )
        button_ttm_provided_no.click()

        # [14] = END_EVENT | CARES 32 - End Event
        # [23] = REASON_CPR_TERMINATED | Only way to catch DNR
        end_event = case[14].text
        if case[23].text == "DNR":
            end_event = "DNR"

        button_end_event_dnr = driver.find_element(
            By.CSS_SELECTOR, 'input[name="EndOfEvent"][value="4"]'
        )
        button_end_event_field_pronounced = driver.find_element(
            By.CSS_SELECTOR, 'input[name="EndOfEvent"][value="1"]'
        )
        button_end_event_ed_pronounced = driver.find_element(
            By.CSS_SELECTOR, 'input[name="EndOfEvent"][value="2"]'
        )
        button_end_event_ongoing_in_ed = driver.find_element(
            By.CSS_SELECTOR, 'input[name="EndOfEvent"][value="3"]'
        )

        match end_event:
            case "ROSC in the Field":
                button_end_event_ongoing_in_ed.click()
            case "Expired in the Field":
                button_end_event_field_pronounced.click()
            case "Expired in ED":
                button_end_event_ed_pronounced.click()
            case "Ongoing Resuscitation in ED":
                button_end_event_ongoing_in_ed.click()
            case "ROSC in the ED":
                button_end_event_ongoing_in_ed.click()
            case "DNR":
                button_end_event_dnr.click()

        # [17] = CPR_PROVIDED_PRIOR_TO_EMS_ARRIVAL

        # [18] = DATE_TIME_OF_CPR
        # Split the date and time
        if case[18].text:
            date_of_start_cpr, start_cpr_time = case[18].text.split()

            # Separate the hours and minutes
            start_cpr_hours, start_cpr_minutes = start_cpr_time.split(":")

            start_cpr_hours_input = driver.find_element(By.NAME, "CPRTime_Hours")
            start_cpr_hours_input.send_keys(start_cpr_hours)

            start_cpr_minutes_input = driver.find_element(By.NAME, "CPRTime_Minutes")
            start_cpr_minutes_input.send_keys(start_cpr_minutes)
        # [19] = DATE_TIME_OF_DEFIB
        # NAME = DefibTime_Hours
        # Split the date and time
        if case[19].text:
            date_of_first_defib, first_defib_time = case[19].text.split()

            # Separate the hours and minutes
            first_defib_hours, first_defib_minutes = first_defib_time.split(":")

            first_defib_hours_input = driver.find_element(By.NAME, "DefibTime_Hours")
            first_defib_hours_input.send_keys(first_defib_hours)

            first_defib_minutes_input = driver.find_element(
                By.NAME, "DefibTime_Minutes"
            )
            first_defib_minutes_input.send_keys(first_defib_minutes)

        # [24] = DATE_TIME_CIRCULATION_RESTORED
        # Split the date and time
        if case[24].text:
            date_of_first_rosc, first_rosc_time = case[24].text.split()

            # Separate the hours and minutes
            first_rosc_hours, first_rosc_minutes = first_rosc_time.split(":")

            first_rosc_hours_input = driver.find_element(By.NAME, "TimeSusRosc_Hours")
            first_rosc_hours_input.send_keys(first_rosc_hours)

            first_rosc_minutes_input = driver.find_element(
                By.NAME, "TimeSusRosc_Minutes"
            )
            first_rosc_minutes_input.send_keys(first_rosc_minutes)

        # [21] = DATE_TIME_CPR_DISCONTINUED
        if case[21].text:
            date_of_end_cpr, end_cpr_time = case[21].text.split()

            # Separate the hours and minutes
            end_cpr_hours, end_cpr_minutes = end_cpr_time.split(":")
            # time.sleep(300)
            if (
                end_event == "DNR"
                or end_event == "Expired in the Field"
                or end_event == "Expired in ED"
            ):
                end_cpr_hours_input = driver.find_element(
                    By.NAME, "TimeResusTerminate_Hours"
                )
                end_cpr_hours_input.send_keys(end_cpr_hours)

                end_cpr_minutes_input = driver.find_element(
                    By.NAME, "TimeResusTerminate_Minutes"
                )
                end_cpr_minutes_input.send_keys(end_cpr_minutes)

        # [25] = INITIATE_IV___TYPE
        # [26] = DISPOSITION__OUTCOME_

        # CARES 40 - Automated CPR feedback device used? Always No
        button_cpr_feedback_no = driver.find_element(
            By.CSS_SELECTOR, 'input[name="CPRFeedbackDevice"][value="2"]'
        )
        button_cpr_feedback_no.click()

        # CARES 42 - ITD used | Always No
        button_itd_used_no = driver.find_element(
            By.CSS_SELECTOR, 'input[name="ITD"][value="2"]'
        )
        button_itd_used_no.click()

        # SAVE
        button_save = driver.find_element(By.NAME, "SAVE")
        try:
            # Code that triggers the exception
            button_save.click()

            # Handle the alert if it appears
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert_text = alert.text

            if 'Did you confirm "Other" cardiac arrest etiology' in alert_text:
                # Click the OK button to confirm
                alert.accept()
        except WebDriverException as e:
            pass

        logging.info(f"Case {case[2].text} has been entered.")
        time.sleep(2)
        driver.get("https://mycares.net/secure/formCaresRev4.jsp")
        time.sleep(2)

    logging.warning(f"The following cases need to be reviewed {cases_that_need_looking}")
    input("Press Enter to close the Chrome window...")
    driver.quit()


if __name__ == "__main__":
    main()
