from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


class yahooElement(object):
    def __init__(self, subpage, name, xpath, checkName="", checkXpath=""):
        self.subpage = subpage # subpage/tab on the yahoo finance page
        self.name = name # name of the value
        self.xpath = xpath
        self.checkName = checkName # if this is initialized, the name of element at checkXpath will be compared to this string
        self.checkXpath = checkXpath

    def checkCorrectnes(self, driver):
        try:
            webElem = driver.find_element(By.XPATH, self.checkXpath)
            if (webElem.text.startswith(self.checkName)):
                return True,""
            else:
                return False,"Found row with: " + webElem.text
        except NoSuchElementException:
            return False, "No such element."

# list of elements we want to fetch
elements = [
    yahooElement("profile", "Company name", '//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/h3'),
    yahooElement("profile", "Sector", '//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[2]/span[2]'),
    yahooElement("profile", "Industry", '//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[2]/span[4]'),
    yahooElement("profile", "Full Time Employees", '//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[2]/span[6]/span'),

    yahooElement("summary", "Price",  '//*[@id="quote-header-info"]/div[3]/div[1]/div/fin-streamer[1]'),
    yahooElement("summary", "Market cap",  '//*[@id="quote-summary"]/div[2]/table/tbody/tr[1]/td[2]'),
    yahooElement("summary", "Beta",  '//*[@id="quote-summary"]/div[2]/table/tbody/tr[2]/td[2]'),
    yahooElement("summary", "P/E ratio",  '//*[@id="quote-summary"]/div[2]/table/tbody/tr[3]/td[2]'),
    yahooElement("summary", "Earnings per share",  '//*[@id="quote-summary"]/div[2]/table/tbody/tr[4]/td[2]'),

    yahooElement("key-statistics", "Enterprise value", '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[2]/td[2]'),
    yahooElement("key-statistics", "Trailing P/E", '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[3]/td[2]'),
    yahooElement("key-statistics", "Forward P/E", '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[4]/td[2]'),
    yahooElement("key-statistics", "PEG", '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[5]/td[2]'),
    yahooElement("key-statistics", "Price/Sales", '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[6]/td[2]'),
    yahooElement("key-statistics", "Price/Book", '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[7]/td[2]'),
    yahooElement("key-statistics", "Diluted EPS (ttm)", '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[4]/div/div/table/tbody/tr[7]/td[2]'),
    yahooElement("key-statistics", "Book Value Per Share (mrq)", '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[5]/div/div/table/tbody/tr[6]/td[2]'),
    yahooElement("key-statistics", "Total Cash (mrq)", '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[5]/div/div/table/tbody/tr[1]/td[2]'),
    yahooElement("key-statistics", "Total Debt (mrq)", '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[5]/div/div/table/tbody/tr[3]/td[2]'),
    yahooElement("key-statistics", "Operating Cash Flow (ttm)", '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[6]/div/div/table/tbody/tr[1]/td[2]'),
    yahooElement("key-statistics", "Levered Free Cash Flow (ttm)", '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[6]/div/div/table/tbody/tr[2]/td[2]'),
    yahooElement("key-statistics", "Shares Outstanding", '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[2]/div/div[2]/div/div/table/tbody/tr[3]/td[2]'),
    yahooElement("key-statistics", "Forward Annual Dividend Rate", '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[2]/div/div[3]/div/div/table/tbody/tr[1]/td[2]'),
    yahooElement("key-statistics", "Forward Annual Dividend Yield", '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[2]/div/div[3]/div/div/table/tbody/tr[2]/td[2]'),

    yahooElement("financials", "Pretax Income", '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[8]/div[1]/div[2]/span',
                               "Pretax Income", '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[8]/div[1]/div[1]/div[1]/span'),
    yahooElement("financials", "Tax Provision", '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[9]/div[1]/div[2]/span', 
                                "Tax Provision", '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[9]/div[1]/div[1]/div[1]/span'),
    yahooElement("financials", "Net Income", '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[18]/div[1]/div[2]/span',
                               "Net Income", '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[18]/div[1]/div[1]/div[1]/span'),
    yahooElement("financials", "Interest Expense", '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[21]/div[1]/div[2]/span',
                               "Interest Expense", '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[21]/div[1]/div[1]/div[1]/span'),

    yahooElement("balance-sheet", "Total Assets", '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[1]/div[2]/span'),
    yahooElement("balance-sheet", "Current Assets", '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/span',
                                  "Current Assets", '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/span'),
    yahooElement("balance-sheet", "Total Liabilities", '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[2]/div[1]/div[2]/span'),
    yahooElement("balance-sheet", "Current Liabilities", '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div[2]/span',
                                  "Current Liabilities", '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/span'),
    yahooElement("balance-sheet", "Common Stock", '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[3]/div[2]/div/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/span',
                                  "Common Stock", '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[3]/div[2]/div/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/span'),

    yahooElement("cash-flow", "Cash Dividends_(year-1)", '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[3]/div[2]/div/div[2]/div[3]/div[1]/div[3]/span',
                                  "Cash Dividends Paid", '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[3]/div[2]/div/div[2]/div[3]/div[1]/div[1]/div[1]/span'),
    yahooElement("cash-flow", "Cash Dividends_(year-2)", '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[3]/div[2]/div/div[2]/div[3]/div[1]/div[4]/span'),
    yahooElement("cash-flow", "Cash Dividends_(year-3)", '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[3]/div[2]/div/div[2]/div[3]/div[1]/div[5]/span'),
    yahooElement("cash-flow", "Cash Dividends_(year-4)", '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[3]/div[2]/div/div[2]/div[3]/div[1]/div[6]/span'),
    yahooElement("cash-flow", "Operating Cash Flow_(year-1)", '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[1]/div[3]/span',
                                       "Operating Cash Flow", '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div[1]/span'),
    yahooElement("cash-flow", "Operating Cash Flow_(year-2)", '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[1]/div[4]/span'),
    yahooElement("cash-flow", "Operating Cash Flow_(year-3)", '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[1]/div[5]/span'),
    yahooElement("cash-flow", "Operating Cash Flow_(year-4)", '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[1]/div[6]/span'),

    yahooElement("analysis", "Growth estimate (5yr)", '//*[@id="Col1-0-AnalystLeafPage-Proxy"]/section/table[6]/tbody/tr[5]/td[2]',
                                      "Next 5 Years", '//*[@id="Col1-0-AnalystLeafPage-Proxy"]/section/table[6]/tbody/tr[5]/td[1]/span')
]
