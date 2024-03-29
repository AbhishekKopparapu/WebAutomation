# -*- coding: utf-8 -*-
"""
This code is just a sample program. Don't try to run this code, it won't run because I didn't provide my actual Corrigo credentials and company name
for obvious reasons. 

Also for merging or loading data you need a masterfile "Noshows_DB" which is in my local, so you can expect errors if you run the code.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import date, timedelta
import pandas as pd
import os
from datetime import date

#Initiate Webdriver and Login to Corrigo
driver = webdriver.Firefox()
driver.get("https://wt79ap.corrigo.com/Login/Login.aspx?username=&company=&c=1")
assert "Login Page" in driver.title
elem = driver.find_element_by_xpath("//input[@id='username']")
elem.send_keys("*****")
elem = driver.find_element_by_xpath("//input[@id='password']")
elem.send_keys("****")
elem = driver.find_element_by_xpath("//input[@id='_companyText']")
elem.send_keys("****")
button = driver.find_element_by_xpath("//input[@id='_loginButton']")
button.click()

#Open Reports dropdown and click Shared Reports
driver.find_element_by_xpath("//td[@class='menuitem'][contains(text(),'Reports')]").click()
driver.implicitly_wait(3000)
driver.find_element_by_xpath("/html[1]/body[1]/div[2]/div[8]/table[1]/tbody[1]/tr[2]/td[1]").click()

#Open Reports by bringing the report link into view
elem = driver.find_element_by_xpath("/html[1]/body[1]/table[1]/tbody[1]/tr[1]/td[1]/form[1]/table[1]/tbody[1]/tr[2]/td[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/div[1]/div[1]/span[4]/table[1]/tbody[1]/tr[1]/td[1]/span[1]/table[1]/tbody[1]/tr[1]/td[2]/div[1]/a[1]")
coordinates = elem.location_once_scrolled_into_view # returns dict of X, Y coordinates
self.driver.execute_script('window.scrollTo({}, {});'.format(coordinates['x'], coordinates['y']))
elem.click()

#click on Desired Report
driver.find_element_by_xpath("//a[contains(text(),'Custodial No-Show Report (current month)')]").click()

#Input range of dates. I am using yesterday's date to today  daily reporting
driver.find_element_by_xpath("//input[@id='tabBuilder__ctl0___FIELD_woCreated_CONTROL___edDate_Start_t']").send_keys(date.today()-timedelta(days=1))
driver.find_element_by_xpath("//input[@id='tabBuilder__ctl0___FIELD_woCreated_CONTROL___edDate_End_t']").send_keys(date.today())

#Clicking on "Generate Report" opens new window, so to switch between the windows we need to get window handles
window_before = driver.window_handles[0]
driver.find_element_by_xpath("//td[contains(text(),'Generate Report')]").click()
window_after = driver.window_handles[1]

#Switching from one window to other
driver.switch_to_window(window_after)

#Downloading data as csv
driver.find_element_by_xpath("//a[@id='report_ctl05_ctl04_ctl00_ButtonLink']").click()
driver.find_element_by_xpath("//a[contains(text(),'CSV (comma delimited)')]").click()

#Checking if file download is successfully done
bol = os.path.exists("C:\\Users\\abhik\\Downloads\\Custodial No-Show Report (current month).csv")

os.chdir("C:\\Users\\abhik\\Downloads")

#Preparing data for analysis
if(bol):
    col_names = ["store#", "City", "State", "Task", "WO#", "Date created", "Item Asset", "Vendor", "WO Status","Date Completed", "Notes", "Notes Date"]    
    data = pd.read_csv(r'Custodial No-Show Report (current month).csv', names=col_names)
    data[['Date created','Date Completed', 'Notes Date']] = data[['Date created','Date Completed','Notes Date']].apply(pd.to_datetime)

#Concatenating today's data with existing data (ETL Incremental loading)
Noshows_DB = pd.read_csv("Noshows_DB")
frames = ['Noshows_DB','data']
Noshows_DB = pd.con(frames)

#This masterfile can be used in tableau for daily reporting



        

    
