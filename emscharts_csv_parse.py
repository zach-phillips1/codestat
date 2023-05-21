import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_path = 'XML_files/emscharts/YTD_5-21-23_emsCharts_CARES_Report.csv'

data = pd.read_csv(file_path)

df = pd.DataFrame(data)

print(df.head())