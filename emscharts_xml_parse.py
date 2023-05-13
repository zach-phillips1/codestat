import xml.etree.ElementTree as ET
import os

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


def count_total_cases():
    sum = 0
    for child in root:
        sum += 1
    print(f"YTD (5/13/23): There have been {sum} total cases")


def main():
    count_total_cases()


if __name__ == "__main__":
    main()