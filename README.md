# log_cleaner

Use this script to cleanup old CAST log files. 

## Prerequisites
The script is written in Python. Ensure that you have Python __3.6__ or above installed. 

## Initial setup
Update the log_cleaner.properties file before use.

The file has the following settings that you would need to update:
1. Log retention period
Specifies the duration for which the logs files are to be retained. Duration is specified in number of days. Logs files older than the specfied retention period are deleted.
'''
[criteria]
log_retention_days=180
'''

2. Log folder
This is the log folder to delete the files/sub-folders from. 

'''
[general]
log_folder=C:\scratch\logs
'''
Note that the sciprt creates its own log file at the same location. The log file will be named log_cleaner.YYYYmmDDHHMMSS.log.

## Usage:
open a __cmd__ prompt.
If the .py extension is recognized as a python script, simply type, '''log_cleaner.py log_cleaner.properties'''. Else, your should invoke python and pass the script and properties file names as an argument, as in, '''python log_cleaner.py log_cleaner.properties'''
