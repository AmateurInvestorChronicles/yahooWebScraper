# yahooWebScraper

This script copies data from yahoo finance webpage into google sheets.
I give some overview in the following youtube videos:
https://www.youtube.com/watch?v=NembUhEsk7w
https://www.youtube.com/watch?v=VLKLrQPOs_4

### Instructions

#### 1. Install selenium

Folow the instructions in https://selenium-python.readthedocs.io/installation.html.

#### 2. Install gspread and oauth2client

`pip install gspread oauth2client`

This is needed to read&write to Google sheets.

#### 3. Configure the service account for your spreadsheet

Follow the **Google Setup** in https://www.makeuseof.com/tag/read-write-google-sheets-python/.
Name the key file `client_secret.json` and put it in this folder.

#### 4. Modify the script for your own needs

Change names of worksheets, sheet cell numbers, selenium driver, xpaths, etc.  

