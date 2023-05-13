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
ticker = sheet.acell('C2').value
print('Found ticker symbol: ' + ticker)

# Dictionary of xPaths
xpath_dict = {
"summary" : {
"price": '//*[@id="quote-header-info"]/div[3]/div[1]/div/fin-streamer[1]',
"market cap": '//*[@id="quote-summary"]/div[2]/table/tbody/tr[1]/td[2]',
"beta": '//*[@id="quote-summary"]/div[2]/table/tbody/tr[2]/td[2]',
"P/E ratio": '//*[@id="quote-summary"]/div[2]/table/tbody/tr[3]/td[2]',
"EPS": '//*[@id="quote-summary"]/div[2]/table/tbody/tr[4]/td[2]'
	}
,
"key-statistics" : {
"enterprise value": '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[2]/td[2]',
"trailing P/E": '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[3]/td[2]',
"forward P/E": '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[4]/td[2]',
"PEG": '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[5]/td[2]',
"price/sales": '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[6]/td[2]',
"price/book": '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[7]/td[2]',
"diluted EPS (ttm)": '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[4]/div/div/table/tbody/tr[7]/td[2]',
"Book value per share (mrq)": '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[5]/div/div/table/tbody/tr[6]/td[2]',
"cash&cash equivalents" : '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[5]/div/div/table/tbody/tr[1]/td[2]',
"total debt" : '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[5]/div/div/table/tbody/tr[3]/td[2]',
"operating cash flow (ttm)": '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[6]/div/div/table/tbody/tr[1]/td[2]',
"free cash flow (ttm)": '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[6]/div/div/table/tbody/tr[2]/td[2]',
"shares outstanding": '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[2]/div/div[2]/div/div/table/tbody/tr[3]/td[2]'
	}
,
"financials" : {
	"Pretax income": '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[8]/div[1]/div[2]/span',
	"Tax provision": '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[9]/div[1]/div[2]/span',
	"Net income": '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[18]/div[1]/div[2]/span',
	"Interest expense (ttm)" : '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[21]/div[1]/div[2]/span',
	}
,
"analysis" : {
	"Growth estimate (5yr)" : '//*[@id="Col1-0-AnalystLeafPage-Proxy"]/section/table[6]/tbody/tr[5]/td[2]'
	}
}


# Add ublock extension to driver to not load ads => much faster
options = webdriver.ChromeOptions();
options.add_extension('./extension_ublock.crx')

# Create webdriver
driver = webdriver.Chrome(options=options)

ans = [[], []]
consentButton = '//*[@id="consent-page"]/div/div/div/form/div[2]/div[2]/button[1]'
consent = False;

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

	ans.append([subpage, ""])
	# Fetch data
	for item in xpath_dict[subpage]:
		elem = driver.find_element(By.XPATH, xpath_dict[subpage][item])
		print(item + ' ' + elem.text)
		ans.append([item, elem.text])
	    #ans[0].append(item)
	    #ans[1].append(elem.text)

# Store data to google sheets
sheet.update('D39:E75', ans)

driver.close()