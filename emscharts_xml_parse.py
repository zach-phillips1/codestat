import xml.etree.ElementTree as ET
import os
import pandas as pd
# import matplotlib.pyplot as plt

directory_path = 'XML_files/emscharts'
file_name = 'YTD_6-6-23_emsCharts_CARES_Report.xml'
file_path = os.path.join(directory_path, file_name)

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





def count_total_cases():
    '''
    This function counts the total amount of cases in the XML file.
    '''
    sum = 0
    for child in root:
        sum += 1
    print(f"YTD (5/13/23): There have been {sum} total cases")


def count_unique_cases():
    '''
    This function counts the number of unique cases based on the PRID.
    '''
    unique_cases = []
    sum = 0
    for child in root:
        if child[1].text not in unique_cases:
            unique_cases.append(child[1].text)
            sum += 1

    print(f"YTD (5/13/23): There have been {sum} unique cases")
    

def create_unique_case_list() -> list:
    unique_cases = []
    unique_cases_by_PRID = []
    for child in root:
        if child[1].text not in unique_cases_by_PRID:
            unique_cases_by_PRID.append(child[1].text)
            unique_cases.append(child)
    
    return unique_cases


def etiology_unknown_count(unique_cases: list):
    sum = 0
    for child in unique_cases:
        if child[13].text == "Not Known":
            sum += 1
    print(f'The number of times the Etiology was listed as "Not Known" was {sum}.')


def count_rosc_cases(unique_cases: list):
    sum = 0
    for child in unique_cases:
        if child[14].text == "ROSC in the Field":
            sum += 1
    print(f"The number of times the End Event was ROSC in the Field was {sum}.")


def count_aed_use(unique_cases: list):
    sum = 0
    for child in unique_cases:
        if child[16].text:
            if child[16].text.startswith("Yes"):
                sum += 1
    print(f"The number of times an AED was used was {sum}.")



def main():
    count_total_cases()
    count_unique_cases()
    unique_cases = create_unique_case_list()
    # This will give the dispatch data/time for the first item in the list
    # print(unique_cases[0][0].text)
    etiology_unknown_count(unique_cases)
    count_rosc_cases(unique_cases)
    count_aed_use(unique_cases)
    

   

if __name__ == "__main__":
    main()