from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet (client must have access to the sheets)
sheet = client.open("Amateur Investor Chronicles").worksheet('Intrinsic value calculation')

# Extract ticker from a cell in google sheets and print its value
ticker = sheet.acell('B2').value
print('Found ticker symbol: ' + ticker)

# Dictionary of xPaths
xpath_dict = {
"summary" : {
    "Price": '//*[@id="quote-header-info"]/div[3]/div[1]/div/fin-streamer[1]',
    "Market cap": '//*[@id="quote-summary"]/div[2]/table/tbody/tr[1]/td[2]',
    "Beta": '//*[@id="quote-summary"]/div[2]/table/tbody/tr[2]/td[2]',
    "P/E ratio": '//*[@id="quote-summary"]/div[2]/table/tbody/tr[3]/td[2]',
    "Earnings per share": '//*[@id="quote-summary"]/div[2]/table/tbody/tr[4]/td[2]'
	}
,
"key-statistics" : {
	"Enterprise value": '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[2]/td[2]',
    "Trailing P/E": '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[3]/td[2]',
    "Forward P/E": '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[4]/td[2]',
    "PEG": '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[5]/td[2]',
    "Price/sales": '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[6]/td[2]',
    "Price/book": '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[7]/td[2]',
    "Diluted EPS (ttm)": '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[4]/div/div/table/tbody/tr[7]/td[2]',
    "Book value per share (mrq)": '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[5]/div/div/table/tbody/tr[6]/td[2]',
    "Cash&cash equivalents" : '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[5]/div/div/table/tbody/tr[1]/td[2]',
    "Total debt" : '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[5]/div/div/table/tbody/tr[3]/td[2]',
    "Operating cash flow (ttm)": '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[6]/div/div/table/tbody/tr[1]/td[2]',
    "Free cash flow (ttm)": '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[6]/div/div/table/tbody/tr[2]/td[2]',
    "Shares outstanding": '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[2]/div/div[2]/div/div/table/tbody/tr[3]/td[2]',
	"Forward annual dividend rate": '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[2]/div/div[3]/div/div/table/tbody/tr[1]/td[2]',
	"Forward annual dividend yield": '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[2]/div/div[3]/div/div/table/tbody/tr[2]/td[2]'
	}
,
"financials" : {
	"Pretax income": '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[7]/div[1]/div[2]/span',
	"Tax provision": '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[8]/div[1]/div[2]/span',
	"Net income": '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[18]/div[1]/div[2]/span',
	"Interest expense (ttm)" : '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[20]/div[1]/div[2]/span',
	}
,
"cash-flow" : {
	"Cash dividends (yr-1)": '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[3]/div[2]/div/div[2]/div[3]/div[1]/div[3]/span',
	"Cash dividends (yr-2)": '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[3]/div[2]/div/div[2]/div[3]/div[1]/div[4]/span',
	"Cash dividends (yr-3)": '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[3]/div[2]/div/div[2]/div[3]/div[1]/div[5]/span',
	"Cash dividends (yr-4)": '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[3]/div[2]/div/div[2]/div[3]/div[1]/div[6]/span',
	}
,
"analysis" : {
	"Growth estimate (5yr)" : '//*[@id="Col1-0-AnalystLeafPage-Proxy"]/section/table[6]/tbody/tr[5]/td[2]'
	}
}

# Function to convert from yahoo finance format to float
def convertToNumber(input):
	if (input == 'N/A'):
		return input;
	elif (input[-1] == 'T'):
		return 1000000000000*float(input[:-1])
	elif (input[-1] == 'B'):
		return 1000000000*float(input[:-1])
	elif (input[-1] == 'M'):
		return 1000000*float(input[:-1])
	elif (input[-1] == 'K'):
		return 1000*float(input[:-1])
	elif (input[-1] == '%'):
		return 0.01*float(input[:-1])
	elif (',' in input):
		return 1000*float(input[:].replace(',', ''))
	else:
		return float(input)
	

# Add ublock extension to driver to not load ads => much faster
options = webdriver.ChromeOptions();
options.add_extension('./extension_ublock.crx')

# Create webdriver
driver = webdriver.Chrome(options=options)

# Deal with cookies
consentButton = '//*[@id="consent-page"]/div/div/div/form/div[2]/div[2]/button[1]'
consent = False;
expandAllButton = '//*[@id="Col1-1-Financials-Proxy"]/section/div[2]/button/div/span'

results = []

# Go over subpages
for subpage in xpath_dict:
	website = 'https://finance.yahoo.com/quote/'+ticker+'/'+subpage+'?p='+ticker
	driver.get(website)

	# Accept cookies
	if (not consent):
		wait = WebDriverWait(driver, 0)
		wait.until(EC.element_to_be_clickable((By.XPATH, consentButton)))
		driver.find_element(By.XPATH, consentButton).click()
		consent = True;

	# Potentially expand cash-flow statement
	if (subpage == 'financials' or subpage == 'cash-flow'):
		driver.find_element(By.XPATH, expandAllButton).click()

	results.append([subpage.title(), ""])
	# Fetch data
	for item in xpath_dict[subpage]:
		elem = driver.find_element(By.XPATH, xpath_dict[subpage][item])
		print(item + ' ' + elem.text)
		results.append([item, convertToNumber(elem.text)])

# Store data to google sheets
print(results)
sheet.update('A6:B55', results)

driver.close()

