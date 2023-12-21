# Crozer Cardiac Arrest Data Repository
This repository is dedicated to the Crozer Cardiac arrest data project. It includes scripts for processing and analyzing CARES report data from emsCharts and performing data analysis on CodeStat XML exports.

# CARES_input
CARES_input is a script designed to utilize the CARES report from emsCharts.

## Usage
Download the CARES Report:

Obtain the CARES report from emsCharts in XML format.
Place the downloaded report in the XML_files/emscharts/ directory.
The current naming convention for the report is emsCharts_{start_date}_{end_date}.xml.
## Running the Script:

### When running the script from the command line interface (CLI), provide the following arguments:
USERNAME: Your username.
PASSWORD: Your password.
emsCharts Report start date: Format "Month-Day".
emsCharts Report end date: Format "Month-Day".
Features
Web Scraping: Utilizes Selenium for web scraping.
XML Processing: Uses ElementTree for XML data processing.
Logging: Generates a log file located in logs/CARES_input{date_time}.log.
Comments: Most sections of the script are commented to describe their purpose.
Note
The CARES form often has numerous validation errors, and most reports require manual adjustments.
codestat_xml_parse
codestat_xml_parse is used for performing data analysis on CodeStat XML exports.

### TODO
 Improve the formatting of the README.md file.
 Additional items to be added.