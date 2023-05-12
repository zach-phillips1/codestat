import xml.etree.ElementTree as ET
import os

directory_path = 'XML_files/codestat'
file_name = 'YTD_02_28_23_CPR summary report.xml'
file_path = os.path.join(directory_path, file_name)

tree = ET.parse(file_path)
root = tree.getroot()


def print_cases():
    '''
    This function prints out the case list.
    Returns:
        No return, prints cases.
    '''
    # [0] = IncidentID
    # [1] = CaseStart
    # [2] = Device
    # [3] = CompressionsRatio
    # [4] = CompressionRate
    # [5] = VentilationRate
    # [6] = CompressionDepth
    # [7] = GoodCompressionsWithTargetDepth
    # [8] = LongestPause
    # [9] = NumberOfShocks
    # [10] = AnyROSC
    # [11] = CPREdited

    for child in root:
        print(child[0].tag, child[0].text)
        print(child[1].tag, child[1].text)
        print(child[3].tag, child[3].text)
        print(child[4].tag, child[4].text)
        print(child[8].tag, child[8].text)
        if child[9].text != None:
            print(child[9].tag, child[9].text)
        print(child[10].tag, child[10].text)
        print("------------------------")


def average_longest_pause(num_cases: int):
    '''
    This function gets the average longest pause in compressions.
    Args:
        num_cases (int): Total number of cases

    Returns:
        No return, prints result.
    '''

    average_longest_pause = 0.0

    sum_pauses = 0
    for child in root:
        sum_pauses += float(child[8].text)
    average_longest_pause = sum_pauses / num_cases
    print(f"The average longest pause is {average_longest_pause:.2f} seconds")


def get_average_compression_ratio(num_cases: int):
    '''
    This function gets the average compression ratio.
    Args:
        num_cases (int): The total number of cases

    Returns:
        No return, prints results
    '''

    average_compression_ratio = 0.0
    sum_compression_ratio = 0.0
    for child in root:
        sum_compression_ratio += float(child[3].text)
    average_compression_ratio = sum_compression_ratio / num_cases
    print(f"The average compression ratio is {average_compression_ratio:.2f}.")


def get_average_compression_rate(num_cases: int):
    '''
    This function gets the average compression rate
    Args:
        num_cases (int): The total number of cases

    Returns:
        No return, prints the results.
    '''
    average_compression_rate = 0.0
    sum_compression_rate = 0.0
    for child in root:
        sum_compression_rate += float(child[4].text)
    average_compression_rate = sum_compression_rate / num_cases
    print(f"The average compression rate is {average_compression_rate:.2f} per minute.")


def get_num_cases() -> int:
    '''
    This function counts the number of cases and prints it out.
    Returns:
        (int): Returns the sum of the cases.
    '''
    sum = 0
    for child in root:
        sum += 1
    print(f"The number of cases is {sum}")
    return sum


def max_longest_pause():
    '''
    Finds the case with the longest pause.
    Returns:
        No return, prints the case with the longest pause.
    '''
    max_pause = 0.0
    incident_num = ""
    for child in root:
        if float(child[8].text) > max_pause:
            max_pause = float(child[8].text)
            incident_num = child[0].text
    print(f"The longest pause was {max_pause:.2f} seconds with incident number {incident_num}.")


def count_rosc() -> int:
    '''
    Counts the number of cases that had ROSC.
    Returns:
        (int): The number of cases with ROSC.
    '''
    num_rosc = 0
    for child in root:
        if child[10].text == "Yes":
            num_rosc += 1
    return num_rosc


def num_jan_cases():
    '''
    Gets the number of cases in January
    Returns:
        No return, prints the result
    '''
    sum = 0
    for child in root:
        if child[1].text.startswith("1/"):
            sum += 1
    print(f"The number of cases in January was {sum}.")


def num_feb_cases():
    '''
    Gets the number of cases in February
    Returns:
        No return, prints the result
    '''
    sum = 0
    for child in root:
        if child[1].text.startswith("2/"):
            sum += 1
    print(f"The number of cases in February was {sum}.")


def num_mar_cases():
    '''
    Gets the number of cases in March
    Returns:
        No return, prints the result
    '''
    sum = 0
    for child in root:
        if child[1].text.startswith("3/"):
            sum += 1
    print(f"The number of cases in March was {sum}.")


def max_compression_rate():
    '''
    Finds the case with the fastest compression rate.
    Returns:
        No return, prints the case with the fastest compression rate.
    '''
    max_rate = 0.0
    incident_num = ""
    for child in root:
        if float(child[4].text) > max_rate:
            max_rate = float(child[4].text)
            incident_num = child[0].text
    print(f"The fastest compression rate was {max_rate:.2f} pet minute with incident number {incident_num}.")


def main():
    '''
    Main function
    Returns: No returns, main function

    '''
    print_cases()
    print()
    num_cases = get_num_cases()
    print(f"The number of cases with ROSC: {count_rosc()}")
    max_longest_pause()
    average_longest_pause(num_cases)
    get_average_compression_ratio(num_cases)
    get_average_compression_rate(num_cases)
    max_compression_rate()
    num_jan_cases()
    num_feb_cases()
    num_mar_cases()


if __name__ == "__main__":
    main()
