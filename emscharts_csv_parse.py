import pandas as pd

file_path = 'XML_files/emscharts/YTD_5-23-23_emsCharts_CARES_Report.csv'

data = pd.read_csv(file_path)

df = pd.DataFrame(data)
pd.options.display.width = 10


unique_prid = df["PRID"].unique()

print(unique_prid.size)
print(df)