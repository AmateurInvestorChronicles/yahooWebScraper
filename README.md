# yahooWebScraper

This script copies data from yahoo finance webpage into google sheets.
I give some overview in the following youtube videos:
https://www.youtube.com/watch?v=NembUhEsk7w
https://www.youtube.com/watch?v=VLKLrQPOs_4

### Instructions

#### 1. Install python and selenium

Download python from https://www.python.org/downloads/ and install it.
Folow the instructions in https://selenium-python.readthedocs.io/installation.html to install selenium.

#### 2. Install gspread and oauth2client (optional, see below)

`pip install gspread oauth2client`

This is needed to read&write to Google sheets.

#### 3. Configure the service account for your spreadsheet

Follow the **Google Setup** in https://www.makeuseof.com/tag/read-write-google-sheets-python/.
Name the key file `client_secret.json` and put it in this folder.

#### 4. Modify the script for your own needs

Change names of worksheets, sheet cell numbers, selenium driver, xpaths, etc.  

### Running without connection to google sheets 

For me, the most difficult part was configuring the service account
for google sheets, but that is optional. If `gspread` or `oauth2client` is not installed,
the script asks for yahoo ticker manually and still displays the results.
So if you don't mind copy-pasting the content to google sheets yourself, this is the easy option.
