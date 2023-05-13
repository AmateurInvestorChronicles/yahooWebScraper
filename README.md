# yahooWebScraper

This script copies data from yahoo finance webpage into google sheets.

### Instructions

#### 1. Install selenium

Folow the instructions in https://selenium-python.readthedocs.io/installation.html.

#### 2. Install gspread and oauth2client

`pip install gspread oauth2client`

This is needed to read&write to Google sheets.

#### 3. Configure the service account for your spreadsheet

Follow the **Google Setup** in https://www.makeuseof.com/tag/read-write-google-sheets-python/.

#### 4. Modify the script for your own needs

Change names of worksheets, selenium driver, xpaths, etc.  