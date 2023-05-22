import pandas as pd

file_path = 'XML_files/emscharts/YTD_5-21-23_emsCharts_CARES_Report.csv'

data = pd.read_csv(file_path)

df = pd.DataFrame(data)
pd.options.display.width = 10

print(df.head())

df = df.set_index("PRID")

print(df.head())