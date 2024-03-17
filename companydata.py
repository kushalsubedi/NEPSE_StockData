# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from bs4 import BeautifulSoup
# from selenium.webdriver.common.by import By
# import time
# import csv

# StockSymbol = input("Enter the stock symbol: ")
# time.sleep(2)
# driver = webdriver.Chrome()
# url = f"https://merolagani.com/CompanyDetail.aspx?symbol={StockSymbol}#0"
# driver.get(url)
# print (" ......... Fetching Data From Merolagani ............ ")

# button = driver.find_element(By.XPATH,
#     '//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_lnkHistoryTab"]'
# )
# button.click()

# time.sleep(2)

# page_source = driver.page_source
# soup = BeautifulSoup(page_source, 'html.parser')
# table = soup.find_all('table', class_='table table-bordered table-striped table-hover')

# headers = [i.text.replace('\n', '') for i in table[0].find_all('th')]
# print(headers)

# data = [[i.text for i in row.find_all('td')] for row in table[0].find_all('tr')]

# driver.quit()

# print(" ......... Generating CSV File OF Company Data ............ ")
# time.sleep(2)

# try:
#     with open(f'{StockSymbol}.csv', 'w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(headers)
#         writer.writerows(data)
#         print("Done")
# except Exception as e:
#     print(e)
#     print("Error in generating CSV file")
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import csv

StockSymbol = input("Enter the stock symbol: ").upper()
time.sleep(2)
driver = webdriver.Chrome()
url = f"https://merolagani.com/CompanyDetail.aspx?symbol={StockSymbol}#0"
driver.get(url)
print(" ......... Fetching Data From Merolagani ............ ")

# Clicking on the History tab to get to the table
button = driver.find_element(By.XPATH,
                             '//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_lnkHistoryTab"]'
                             )
button.click()
time.sleep(2)

all_data = []
page_count=0
while page_count<3:
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//table[@class="table table-bordered table-striped table-hover"]')))
    except TimeoutException:
        print("Table not found on the page.")
        break

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    table = soup.find_all('table', class_='table table-bordered table-striped table-hover')

    headers = [i.text.replace('\n', '') for i in table[0].find_all('th')]
    if not headers:
        print("Headers not found on the page.")
        break

    data = [[i.text for i in row.find_all('td')] for row in table[0].find_all('tr')]

    all_data.extend(data)
    page_count+=1

    try:
        next_button = driver.find_element(By.XPATH, '//a[contains(@title, "Next Page")]')
        next_button.click()
        time.sleep(2)
    except NoSuchElementException:
        print("No more next button found, exiting loop.")
        break

driver.quit()

print(" ......... Generating CSV File OF Company Data ............ ")
time.sleep(2)
headers = ['#','LTP','%Change','High','Low','Open','QTY','Turnover']
try:
    with open(f'{StockSymbol}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(all_data)
        print("Done")
except Exception as e:
    print(e)
    print("Error in generating CSV file")