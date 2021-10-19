# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 16:27:03 2021

@author: Jaideep Bommidi
"""

#import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
#import ChromeDriverManager
from selenium.common import exceptions  
import time
from webdriver_manager.chrome import ChromeDriverManager
import csv
import pandas as pd
with open('countries.txt') as f:
    countries = f.readlines()
header = ["Name","email","website","phoneNumber","country","NameOfEmployee"]
with open('makespace_fablabs.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
#https://www.tutorialspoint.com/fetch-all-href-link-using-selenium-in-python
#https://www.tutorialspoint.com/python/python_classes_objects.htm
class find_http_links:
    def __init__(self,name, count, driver):
        self.name = name
        self.count = count
        self.driver = driver
    def traverse_links(self):
        # identify elements with tagname <a>
        lnks=self.driver.find_elements_by_tag_name("a")
        # traverse list
        for lnk in lnks:
           # get_attribute() to get all href
           href = "href"
           #print(lnk.get_attribute(href))
        return lnks
class go_into_link:
    def __init__(self,country, name, driver, link):
        self.name = name
        self.driver =  driver
        self.link = link
        self.country = country
    def go_inside(self):
        print("-------------------------------")
        print(self.link.get_attribute("href"))
        print("-------------------------------")
        self.driver.get(self.link.get_attribute("href"))
        #text = self.driver.find_element_by_xpath("/html/body").text#self.driver.find_element_by_name('body').text
        try:
            text = self.driver.find_elements_by_xpath('.//ul[@class = "capabilities"]')[0].text
        except IndexError as error:
            return
        emails_list = []
        name = self.link.get_attribute("href").split("/")[-1]
        website = self.link.get_attribute("href")
        try:
            phone_no = self.driver.find_elements_by_xpath('.//span[@itemprop = "telephone"]')[0].text
        except IndexError as error:
            phone_no = ""
        try:
            emails = self.driver.find_elements_by_xpath('.//span[@itemprop = "email"]')[0].text
        except IndexError as error:
            emails = ""
        try:
            first_name = self.driver.find_elements_by_xpath('.//span[@class = "first_name"]')[0].text
            last_name = self.driver.find_elements_by_xpath('.//span[@class = "last_name"]')[0].text
            name_employee = first_name + last_name
        except IndexError as error:
            name_employee = ""
        if("3D" in text or "3d" in text):
            """
            #https://stackoverflow.com/questions/31397410/selenium-python-how-do-i-find-every-email-on-a-webpage
            emails = self.driver.find_elements_by_tag_name("a")
            
            for x in range(0,len(emails)):
                code = emails[x].get_attribute("href")
                email = code[4:len(code)-17]
                print(code)
                if "@" in email:
                    emails_list.append(email)
            """
            data = [name,emails,website,phone_no,self.country,name_employee]
            print(data)
            with open('makespace_fablabs.csv', 'a+', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)
        
class split_links:
    def __init__(self,name,driver, links):
        self.name = name
        self.driver = driver
        self.links = links
    def split_links_method(self):
        if self.name== "fablabs":
            labs_links = []
            page_links = []
            remain_links = []
            for link in self.links:
                if "/labs/" in link.get_attribute("href"):
                    labs_links.append(link)
                elif "/search?page=" in link.get_attribute("href"):
                    page_links.append(link)
                else:
                    remain_links.append(link)
            return labs_links, page_links, remain_links
        else:
            return [],[],[]
"""
########################################################################################################################
"""
chrome_driver_binary=r"D:\Anaconda3\envs\tensorflow1/chromedriver.exe"
options = webdriver.ChromeOptions()
options.binary_location = r"C:\Program Files\Google\Chrome\Application/chrome.exe"

"""
https://stackoverflow.com/questions/60296873/sessionnotcreatedexception-message-session-not-created-this-version-of-chrome/62127806
"""
driver = webdriver.Chrome(ChromeDriverManager().install())

#driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_driver_binary, chrome_options=options)

driver.get("https://fablabs.io/")
#assert("Coronavirus" in driver.title)
"""
########################################################################################################################
"""
for country in countries:
    elem = driver.find_element_by_id('search-box')
    elem.clear()
    elem.send_keys(country)
    try:
        elem.send_keys(Keys.RETURN)
    except exceptions.StaleElementReferenceException:
        print(country)
        pass
    
    try:
        content = driver.find_element_by_class_name('labs')
    except exceptions.NoSuchElementException:
        print("labs: "+country)
        continue
    flag=True
    cnt=0
    while flag:
        if cnt==0:
            cnt=1
            pass
        else:
           try:
               try:
                   #http://makeseleniumeasy.com/2020/05/25/elementclickinterceptedexception-element-click-intercepted-not-clickable-at-point-other-element-would-receive-the-click/
                   ele = driver.find_elements_by_xpath('.//a[@rel = "next"]')[0]
                   ele.send_keys(Keys.RETURN)
               except exceptions.ElementClickInterceptedException:
                   flag = False
                   continue
           except IndexError as error:
               flag = False
               continue
        find_links_obj = find_http_links("makerspace",1,driver)
        links = find_links_obj.traverse_links()
        split_links_obj = split_links("fablabs", driver, links)
        labs_links, page_links, remain_links = split_links_obj.split_links_method()
        visited_links = []
        driver_link = webdriver.Chrome(ChromeDriverManager().install())
        for lnk in labs_links:
            if lnk.get_attribute("href") not in visited_links:
                visited_links.append(lnk.get_attribute("href"))
                go_inside_obj = go_into_link(country,"link_3d",driver_link,lnk)
                go_inside_obj.go_inside()
        driver_link.close()
    #assert("No results found." not in driver.page_source)
driver.close()