This is the repo for Crozer Cardiac arrest data.

CARES_input utilizes the CARES report from emsCharts. 
    Download the CARES report from emsCharts in XML format and place in the "XML_files/emscharts/" directory.
        Current naming convention is "emsCharts_{start_date}_{end_date}.xml"
    Change "XML_FILE_PATH" to correct file
    Verify USER_NAME and PASSWORD is correct

    Uses Selenium for webscraping and ElementTree for scraping.
    Most sections have a comment to inform what each section is.

    Log file located in logs/CARES_input{date_time}.log