import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from webElements import *


# use creds to create a client to interact with the Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet (client must have access to the sheets)
sheet = client.open("Amateur Investor Chronicles").worksheet(
    "Intrinsic value calculation"
)

# Extract ticker from a cell in google sheets and print its value
ticker = sheet.acell("B2").value
print("Found ticker symbol: " + ticker)

# Function to check corectness of the xpath. Compares key with string obtained by scraping first column in the row of this xpath.
def checkCorectness(key, xpath, driver):
    ## replace last int
    left_xpath = re.sub(r'(\d+)\b', '1', xpath[::-1], 1)[::-1]
    # replace span 
    left_xpath = re.sub('span', 'div[1]/span', left_xpath)
    found_string =  driver.find_element(By.XPATH, left_xpath).text
    print("FOUND STRING:" + found_string)
    return found_string.startswith(key.split('_')[0])

# Function to convert from yahoo finance format to float
def convertToNumber(input):
    if not any(char.isdigit() for char in input): # is string
        return input
    elif input[-1] == "T":
        return 1000000000000 * float(input[:-1])
    elif input[-1] == "B":
        return 1000000000 * float(input[:-1])
    elif input[-1] == "M":
        return 1000000 * float(input[:-1])
    elif input[-1] == "K":
        return 1000 * float(input[:-1])
    elif input[-1] == "%":
        return 0.01 * float(input[:-1])
    elif "," in input:
        return 1000 * float(input[:].replace(",", ""))
    else:
        return float(input)

# Add ublock extension to driver to not load ads => much faster
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_extension("./extension_ublock.crx")

# Create webdriver
driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(10)

# Deal with cookies
consentButton = '//*[@id="consent-page"]/div/div/div/form/div[2]/div[2]/button[1]'
consent = False
expandAllButton = '//*[@id="Col1-1-Financials-Proxy"]/section/div[2]/button/div/span'
sectorField = '//*[@id="Col2-12-QuoteModule-Proxy"]/div/div/div/div/p[2]/span[2]'

results = []
currentSubpage = ""
for yahooElement in elements:
    if (yahooElement.subpage != currentSubpage):
        currentSubpage = yahooElement.subpage
        driver.get( "https://finance.yahoo.com/quote/" + ticker + "/" + yahooElement.subpage + "?p=" + ticker ) # get current subpage

        if not consent: # accept cookies
            wait = WebDriverWait(driver, 1)
            wait.until(EC.element_to_be_clickable((By.XPATH, consentButton)))
            driver.find_element(By.XPATH, consentButton).click()
            consent = True
            driver.implicitly_wait(10) # the part with sectors and industry takes a while to load (for some reason wait.until did not work for me for those elements)
        else:
            driver.implicitly_wait(0) # reset not to wait if any elements are not loaded

        if yahooElement.subpage == "financials" or yahooElement.subpage == "balance-sheet" or yahooElement.subpage == "cash-flow": 
            driver.find_element(By.XPATH, expandAllButton).click()
        results.append([yahooElement.subpage, ""])

    if (yahooElement.checkXpath != ""): # if there is a manual check for this xpath first check
        checkResult = yahooElement.checkCorrectnes(driver);
        if (not checkResult[0]):
            results.append([yahooElement.name, checkResult[1]])
            continue

    try:
        elem = driver.find_element(By.XPATH, yahooElement.xpath)
        results.append([yahooElement.name, convertToNumber(elem.text)])
    except NoSuchElementException:
        print(yahooElement.name + " " + "Not found (no check)")
        results.append([yahooElement.name, "Not found (no check)"])
    

# Store data to google sheets
for elem in results:
    print(elem)
sheet.update("A6:B54", results)

driver.close()
