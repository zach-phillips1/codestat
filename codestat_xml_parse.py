import tkinter as tk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET
import os
import time
import logging

# directory_path = 'XML_files/codestat/'
# file_name = 'CPR_Summary_YTD_9-26.xml'
# file_path = os.path.join(directory_path, file_name)


def open_file():
    filepath = filedialog.askopenfilename(
        filetypes=[("XML Files", "*.xml"), ("All Files", "*.*")]
    )
    if not filepath:
        return

    try:
        process_file(filepath)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open or process file: {e}")


def process_file(file_path):

    tree = ET.parse(file_path)
    root = tree.getroot()

    # TODO: Find some way to make the export prettier.

    current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
    logging.basicConfig(
        filename=f"logs/CodeStat_data{current_time}.log",  # Specify the name of your log file
        level=logging.INFO,  # Set the logging level (you can adjust this)
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    print_cases(root)
    num_cases = len(root)
    logging.info(f"The number of cases with ROSC: {count_rosc(root)}")
    max_longest_pause(root)
    average_longest_pause(num_cases, root)
    get_average_compression_ratio(num_cases, root)
    get_lowest_compression_ratio(num_cases, root)
    get_average_compression_rate(num_cases, root)
    max_compression_rate(root)


def print_cases(root):
    """
    This function prints out the case list.
    Returns:
        No return, prints cases.
    """
    # [0] = IncidentID
    # [1] = CaseStart
    # [2] = Device
    # [3] = CPRRatio
    # [4] = CompressionsRatio
    # [5] = CompressionRate
    # [6] = CompressionDepth
    # [7] = GoodCompressionsWithTargetDepth
    # [8] = LongestPause
    # [9] = NumberOfShocks
    # [10] = AnyROSC
    # [11] = CPREdited

    for child in reversed(root):
        logging.info(f"{child[0].tag}, {child[0].text}")
        logging.info(f"{child[1].tag}, {child[1].text}")
        logging.info(f"{child[3].tag}, {child[3].text}")
        logging.info(f"{child[4].tag}, {child[4].text}")
        if child[8].text != None:
            logging.info(f"{child[8].tag}, {child[8].text}")
        if child[9].text != None:
            logging.info(f"{child[9].tag}, {child[9].text}")
        logging.info(f"{child[10].tag}, {child[10].text}")
        logging.info("------------------------")


def average_longest_pause(num_cases: int, root):
    """
    This function gets the average longest pause in compressions.
    Args:
        num_cases (int): Total number of cases

    Returns:
        No return, prints result.
    """

    average_longest_pause = 0.0

    sum_pauses = 0
    for child in root:
        if child[8].text != None:
            sum_pauses += float(child[8].text)
    average_longest_pause = sum_pauses / num_cases
    logging.info(f"The average longest pause is {average_longest_pause:.2f} seconds")


def get_average_compression_ratio(num_cases: int, root):
    """
    This function gets the average compression ratio.
    Args:
        num_cases (int): The total number of cases

    Returns:
        No return, prints results
    """

    average_compression_ratio = 0.0
    sum_compression_ratio = 0.0
    for child in root:
        if child[3].text != None:
            sum_compression_ratio += float(child[3].text)
    average_compression_ratio = sum_compression_ratio / num_cases
    logging.info(f"The average compression ratio is {average_compression_ratio:.2f}.")


def get_lowest_compression_ratio(num_cases: int, root):
    """
    This function gets the case with the lowest compression ratio
    Args:
        num_cases (int): The total number of cases

    Returns:
        No return, prints results
    """
    lowest_compression_ratio = 100.0
    case_number = ""
    for child in root:
        if child[4].text != None and child[0].text != "23-03998":
            if float(child[4].text) < lowest_compression_ratio:
                lowest_compression_ratio = float(child[4].text)
                case_number = child[0].text

    logging.info(
        f"The case with the lowest compression ratio was {case_number} with a ratio of {lowest_compression_ratio}"
    )


def get_average_compression_rate(num_cases: int, root):
    """
    This function gets the average compression rate
    Args:
        num_cases (int): The total number of cases

    Returns:
        No return, prints the results.
    """
    average_compression_rate = 0.0
    sum_compression_rate = 0.0
    for child in root:
        if child[5].text != None:
            sum_compression_rate += float(child[5].text)
    average_compression_rate = sum_compression_rate / num_cases
    logging.info(
        f"The average compression rate is {average_compression_rate:.2f} per minute."
    )


# TODO: Remove this and use len(root)
# def get_num_cases() -> int:
# '''
# This function counts the number of cases and prints it out.
# Returns:
#     (int): Returns the sum of the cases.
# '''
# sum = 0
# for child in root:
#     sum += 1
# logging.info(f"The number of cases is {sum}")
# return sum


def max_longest_pause(root):
    """
    Finds the case with the longest pause.
    Returns:
        No return, prints the case with the longest pause.
    """
    max_pause = 0.0
    incident_num = ""
    for child in root:
        if child[8].text != None:
            if float(child[8].text) > max_pause:
                max_pause = float(child[8].text)
                incident_num = child[0].text
    logging.info(
        f"The longest pause was {max_pause:.2f} seconds with incident number {incident_num}."
    )


def count_rosc(root) -> int:
    """
    Counts the number of cases that had ROSC.
    Returns:
        (int): The number of cases with ROSC.
    """
    num_rosc = 0
    for child in root:
        if child[10].text == "Yes":
            num_rosc += 1
    return num_rosc


def num_jan_cases(root):
    """
    Gets the number of cases in January
    Returns:
        No return, prints the result
    """
    sum = 0
    for child in root:
        if child[1].text != None:
            if child[1].text.startswith("1/"):
                sum += 1
    logging.info(f"The number of cases in January was {sum}.")


def num_feb_cases(root):
    """
    Gets the number of cases in February
    Returns:
        No return, prints the result
    """
    sum = 0
    for child in root:
        if child[1].text != None:
            if child[1].text.startswith("2/"):
                sum += 1
    logging.info(f"The number of cases in February was {sum}.")


def num_mar_cases(root):
    """
    Gets the number of cases in March
    Returns:
        No return, prints the result
    """
    sum = 0
    for child in root:
        if child[1].text != None:
            if child[1].text.startswith("3/"):
                sum += 1
    logging.info(f"The number of cases in March was {sum}.")


def max_compression_rate(root):
    """
    Finds the case with the fastest compression rate.
    Returns:
        No return, prints the case with the fastest compression rate.
    """
    max_rate = 0.0
    incident_num = ""
    for child in root:
        if child[5].text != None:
            if float(child[5].text) > max_rate:
                max_rate = float(child[5].text)
                incident_num = child[0].text
    logging.info(
        f"The fastest compression rate was {max_rate:.2f} per minute with incident number {incident_num}."
    )


root = tk.Tk()
root.title("CPR Statistics Analyzer")

open_button = tk.Button(root, text="Open XML File", command=open_file)
open_button.pack(pady=10)

root.mainloop()
