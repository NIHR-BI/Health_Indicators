import pydrive

 

# Create a PyDrive client

client = pydrive.auth.GoogleAuth()

client.authenticate()

 

# Get the file to upload

file_path = 'C:/Users/busaji/Documents/Projects/ObesitySWR/Health_Indicators/dat/obesity-in-adults-chart-data.csv'

 

# Create a Google Drive file object

file = pydrive.DriveFile(file_path)

 

# Upload the file to Google Drive

file.upload()