import xml.etree.ElementTree as ET
import os
import pandas as pd
# import matplotlib.pyplot as plt

directory_path = 'XML_files/emscharts'
file_name = 'YTD_emscharts_5_13_23.xml'
file_path = os.path.join(directory_path, file_name)

tree = ET.parse(file_path)
root = tree.getroot()

# [0] = DATE_DISPATCHED
# [1] = PRID
# [2] = END_EVENT
# [3] = AED_BY
# [4] = AED_USE
# [5] = CPR_PROVIDED_PRIOR_TO_EMS_ARRIVAL
# [6] = DATE_TIME_OF_CPR
# [7] = DATE_TIME_OF_DEFIB
# [8] = DEFIBRILLATOR_TYPE
# [9] = ETIOLOGY
# [10] = DATE_TIME_CPR_DISCONTINUED
# [11] = WHO_WITNESSED
# [12] = DEST__RHYTHM
# [13] = INITIAL_RHYTHM
# [14] = REASON_CPR_TERMINATED
# [15] = DATE_TIME_CIRCULATION_RESTORED
# [16] = DATE_OF_BIRTH
# [17] = GENDER
# [18] = FIRST_NAME
# [19] = LAST_NAME
# [20] = RACE
# [21] = DISPATCH_LOCATION
# [22] = RECEIVING_HOSPITAL
# [23] = INITIATE_IV___TYPE
# [24] = DISPOSITION__OUTCOME_

data = []

for element in root:
    data.append({
        element[0].tag: element[0].text,
        element[1].tag: element[1].text,
        element[2].tag: element[2].text,
        element[3].tag: element[3].text,
        element[4].tag: element[4].text,
        element[5].tag: element[5].text,
        element[6].tag: element[6].text,
        element[7].tag: element[7].text,
        element[8].tag: element[8].text,
        element[9].tag: element[9].text,
        element[10].tag: element[10].text,
        element[11].tag: element[11].text,
        element[12].tag: element[12].text,
        element[13].tag: element[13].text,
        element[14].tag: element[14].text,
        element[15].tag: element[15].text,
        element[16].tag: element[16].text,
        element[17].tag: element[17].text,
        element[18].tag: element[18].text,
        element[19].tag: element[19].text,
        element[20].tag: element[20].text,
        element[21].tag: element[21].text,
        element[22].tag: element[22].text,
        element[23].tag: element[23].text,
        element[24].tag: element[24].text
    })


# Create DataFrame from the extracted data
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
df = pd.DataFrame(data)


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
        if child[9].text == "Not Known":
            sum += 1
    print(f'The number of times the Etiology was listed as "Not Known" was {sum}.')


def count_rosc_cases(unique_cases: list):
    sum = 0
    for child in unique_cases:
        if child[2].text == "ROSC in the Field":
            sum += 1
    print(f"The number of times the End Event was ROSC in the Field was {sum}.")


def count_aed_use(unique_cases: list):
    sum = 0
    for child in unique_cases:
        if child[4].text:
            if child[4].text.startswith("Yes"):
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
    print(df)

    

if __name__ == "__main__":
    main()