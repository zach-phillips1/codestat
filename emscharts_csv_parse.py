import pandas as pd

file_path = 'XML_files/emscharts/YTD_6-1-23_emsCharts_CARES_Report.csv'
output_file_path = 'XML_files/emscharts/YTD_5-23-23_emsCharts_CARES_Report_output.csv'
data = pd.read_csv(file_path)

df = pd.DataFrame(data)
pd.options.display.width = 10



df['Stage'] = ''


unique_PRID = df['PRID'].unique()
print(f"There were {unique_PRID.size} number of unique cases")

print(df.size)
#print(df)
#print(df.columns)

df.to_csv(output_file_path, index=False)
