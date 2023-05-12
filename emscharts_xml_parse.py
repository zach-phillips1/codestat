import xml.etree.ElementTree as ET
import os

directory_path = 'XML_files/emscharts'
file_name = 'YTD_emscharts_5_12_23'
file_path = os.path.join(directory_path, file_name)

tree = ET.parse(file_path)
root = tree.getroot()

