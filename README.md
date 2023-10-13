This is the repo for Crozer Cardiac arrest data.

CARES_input utilizes the CARES report from emsCharts. 
    Download the CARES report from emsCharts in XML format and place in the "XML_files/emscharts/" directory.
        Current naming convention is "emsCharts_{start_date}_{end_date}.xml"
    
    When running the script from the CLI, arguements are as followed.
        [1] USERNAME
        [2] PASSWORD
        [3] emsCharts Report start date "Month-Day"
        [4] emsCharts Report end date "Month-Day"

    Uses Selenium for webscraping and ElementTree for XML processing.
    Most sections have a comment to inform what each section is.

    Log file located in logs/CARES_input{date_time}.log

codestat_xml_parse uses CodeStat XML exports to perform data analysis. 

# TODO: Figure out formating for README