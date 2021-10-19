
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 09:53:15 2021

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
import logging
with open('countries.txt') as f:
    countries = f.readlines()
header = ["Name","email","website","phoneNumber","Fax","Address","Contact Person"]
with open('wlw_companies.csv', 'w', encoding='UTF8', newline='') as f:
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
        #lnks2 = self.driver.find_elements_by_tag_name("a href")
        #self.driver.find_elements_by_xpath('.//div[@class = "pagination-buttons"]')[0].text
        # traverse list
        """
        for lnk in lnks:
           # get_attribute() to get all href
           href = "href"
           print(lnk.get_attribute(href))
        """
        return lnks
class go_into_link:
    def __init__(self,country, name, driver, link):
        self.name = name
        self.driver = driver
        self.link = link
        self.country = country
    def go_inside(self):
        if self.name=="link_3d":#fablabs
            print("-------------------------------")
            print(self.link.get_attribute("href"))
            print("-------------------------------")
            self.driver.get(self.link.get_attribute("href"))
            #text = self.driver.find_element_by_xpath("/html/body").text#self.driver.find_element_by_name('body').text
            
            # check if the labs is related to 3d printing
            try:
                text = self.driver.find_elements_by_xpath('.//ul[@class = "capabilities"]')[0].text
            except IndexError as error:
                return
            emails_list = []
            name = self.link.get_attribute("href").split("/")[-1]
            website = self.link.get_attribute("href")
            #Telephone number
            try:
                phone_no = self.driver.find_elements_by_xpath('.//span[@itemprop = "telephone"]')[0].text
            except IndexError as error:
                phone_no = ""
            # email
            try:
                emails = self.driver.find_elements_by_xpath('.//span[@itemprop = "email"]')[0].text
            except IndexError as error:
                emails = ""
            #name
            try:
                first_name = self.driver.find_elements_by_xpath('.//span[@class = "first_name"]')[0].text
                last_name = self.driver.find_elements_by_xpath('.//span[@class = "last_name"]')[0].text
                name_employee = first_name + last_name
            except IndexError as error:
                name_employee = ""
            # write to makespace_fablabs.csv file
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
        elif self.name=="3dprintingbusinessdirectory":
            print("-------------------------------")
            print(self.link.get_attribute("href"))
            print("-------------------------------")
            self.driver.get(self.link.get_attribute("href"))
            #
            try:
                AllValues_label = self.driver.find_elements_by_xpath('.//td[@class = "detail-label"]')
            except IndexError as error:
                AllValues_label = ""
            try:
                AllValues = self.driver.find_elements_by_xpath('.//td[@class = "detail"]')
            except IndexError as error:
                AllValues = ""
            Name,zipcode,Address,Phone,Website,Email,Fax = "","","","","","",""
            for cnt,i in enumerate(AllValues_label):
                if i.text=="Name":
                    Name = AllValues[cnt].text
                elif i.text=="ZIP code":
                    zipcode = AllValues[cnt].text
                elif i.text=="Full Address":
                    Address = AllValues[cnt].text
                elif i.text=="Phone":
                    Phone = AllValues[cnt].text
                elif i.text=="Website":
                    Website = AllValues[cnt].text
                elif i.text=="E-mail":
                    Email = AllValues[cnt].text
                elif i.text=="Fax":
                    Fax = AllValues[cnt].text
                else:
                    pass
            data = [Name,Email,Website,Phone,Fax,Address,zipcode]
            #header = ["Name","Email","website","phoneNumber","Fax","Address","zipcode"]
            print(data)
            with open('3dprintingbusinessdirectory.csv', 'a+', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)
        elif self.name=="wlw":
            #pri#nt("-------------------------------")
            #print(self.link.get_attribute("href"))
            #print("-------------------------------")
            self.driver.get(self.link.get_attribute("href"))
            #print("---------------------------------------------------------")
            try:
                firm_name = self.driver.find_elements_by_xpath('.//h1[@class = "business-card__title"]')[0].text
            except IndexError as error:
                firm_name = ""
            try:
                website_firm = self.driver.find_elements_by_xpath('.//a[@id = "location-and-contact__website"]')[0].get_attribute("href")
            except IndexError as error:
                website_firm = ""
            try:
                phone_no_firm = self.driver.find_elements_by_xpath('.//a[@class = "vis-phone__number"]')[0].get_attribute("href")[4:]
                #<a href="tel:+49 6145546080" class="vis-phone__number"><span>+49 6145546080</span></a>
                """
                print(self.driver.find_elements_by_xpath('.//span[@id = "location-and-contact__website"]'))
                phone_no_webelement = self.driver.find_elements_by_xpath('.//div[@id = "location-and-contact__phone"]')[0].click()
                try:
                    #https://stackoverflow.com/questions/69290354/python-selenium-get-values-from-p-and-span
                    all_phone_no_firm = self.driver.find_elements_by_xpath('.//div[@class = "popper"]/*/span')
                    phone_no_firm = [i.text for i in all_phone_no_firm if i.text!='']
                        
                except IndexError as error:
                    phone_no_firm = ""
                """
            except IndexError as error:
                phone_no_firm = ""
            try:
                fax_no_firm = self.driver.find_elements_by_xpath('.//a[@class = "vis-phone__number"]')[-1].get_attribute("href")[4:]
                #<a href="tel:+49 6145546080" class="vis-phone__number"><span>+49 6145546080</span></a>
                """
                print(self.driver.find_elements_by_xpath('.//span[@id = "location-and-contact__website"]'))
                phone_no_webelement = self.driver.find_elements_by_xpath('.//div[@id = "location-and-contact__phone"]')[0].click()
                try:
                    #https://stackoverflow.com/questions/69290354/python-selenium-get-values-from-p-and-span
                    all_phone_no_firm = self.driver.find_elements_by_xpath('.//div[@class = "popper"]/*/span')
                    phone_no_firm = [i.text for i in all_phone_no_firm if i.text!='']
                        
                except IndexError as error:
                    phone_no_firm = ""
                """
            except IndexError as error:
                fax_no_firm = ""
            try:
                firm_address = '-'.join(self.driver.find_elements_by_xpath('.//address[@class = "location-and-contact__address"]')[0].text.split('\n'))
            except IndexError as error:
                firm_address = ""
            try:
                #direct-contact__person
                contact_person = '-'.join(self.driver.find_elements_by_xpath('.//div[@class = "direct-contact__person"]')[0].text.split('\n'))
            except IndexError as error:
                contact_person = ""
            try:
                #direct-contact__person
                email_firm = self.driver.find_elements_by_xpath('.//a[@id = "location-and-contact__email"]')[0].text
            except IndexError as error:
                email_firm = ""
            data = [firm_name,email_firm,website_firm,phone_no_firm,fax_no_firm,firm_address,contact_person]
            #header = ["Name","Email","website","phoneNumber","Fax","Address","zipcode"]
            #print(data)
            with open('wlw_companies.csv', 'a+', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)
            #return firm_name, website_firm, phone_no_firm, fax_no_firm, firm_address, contact_person
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
        elif self.name=="3dprintingbusinessdirectory":
            company_links = []
            page_links = []
            remain_links = []
            for link in self.links:
                if ("/company/" in link.get_attribute("href") and "linkedin" not in link.get_attribute("href")) :
                    company_links.append(link)
                elif "/?pageds=" in link.get_attribute("href"):
                    page_links.append(link)
                else:
                    remain_links.append(link)
            return company_links, page_links, remain_links

        elif self.name == "wlw":
            company_links = []
            page_links = []
            remain_links = []
            for link in self.links:
                #print(link.get_attribute("href"))
                if ("/firma/" in link.get_attribute("href") and "linkedin" not in link.get_attribute("href")) :
                    company_links.append(link)
                elif "/?pageds=" in link.get_attribute("href"):
                    page_links.append(link)
                else:
                    remain_links.append(link)
            return company_links, page_links, remain_links
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

driver.get("https://www.wlw.de/")
#assert("Coronavirus" in driver.title)
"""
########################################################################################################################
"""
"""
#for country in countries:
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
"""

#elem = driver.find_element_by_id('search-box')
elem = driver.find_elements_by_xpath('.//input[@name = "q"]')
#elem  = driver.find_elements_by_id("header__login-icon")
elem[0].send_keys("gmbh")

#print(elem)
#elem.clear()
elem[0].send_keys(Keys.RETURN)



#print(company_links)
flag=True
cnt=1
next_page_link = ""
visited_links = []
visited_loaded_pages = []
while flag:
    print(len(visited_links))
    print("----------------------------------------------------------")
    print(cnt)
    if cnt==1:
        cnt+=1
        pass
    else:
       try:
           try:
               visited_loaded_pages.append(driver.find_elements_by_xpath('.//a[@class = "button arrow arrow-next"]')[0].get_attribute("href"))
               driver.find_elements_by_xpath('.//a[@class = "button arrow arrow-next"]')[0].click()
               next_page_link = driver.find_elements_by_xpath('.//a[@class = "button arrow arrow-next"]')[0]
               #driver.get(next_page_link.get_attribute("href"))
               
           except exceptions.ElementClickInterceptedException:
               print("Click Failed")
               
               try:
                   try:
                       driver.find_elements_by_xpath('.//a[@class = "button arrow arrow-next"]')[-1].click()
                       next_page_link = driver.find_elements_by_xpath('.//a[@class = "button arrow arrow-next"]')[-1]
                       driver.get(next_page_link.get_attribute("href"))
                       visited_loaded_pages.append(next_page_link.get_attribute("href"))
                   except exceptions.ElementClickInterceptedException:
                       print("Click Failed")
                       flag = False
                       continue
               except IndexError as error:
                   flag = False
                   continue
               
               flag = False
               continue
       except IndexError as error:
           try:
               try:
                   next_page_link = driver.find_elements_by_xpath('.//a[@data-test = "pagination"]')[0].get_attribute("href")
                   #driver.get(next_page_link)
                   if next_page_link not in visited_loaded_pages and cnt<2:
                       driver.get(next_page_link)
                   else:
                       next_page_link = driver.find_elements_by_xpath('.//a[@data-test = "pagination"]')[-1].get_attribute("href")
                       driver.get(next_page_link)
                   visited_loaded_pages.append(next_page_link)
               except exceptions.ElementClickInterceptedException:
                   print("Click Failed")
                   flag = False
                   continue
           except IndexError as error:
               flag = False
               continue
           except AttributeError as error:
               flag = False
               continue

    find_links_obj = find_http_links("wlw",cnt,driver)
    links = find_links_obj.traverse_links()
    #print(links)
    split_links_obj = split_links("wlw", driver, links)
    company_links, page_links, remain_links = split_links_obj.split_links_method()
    print("len of company links: {0}".format(len(company_links)))
    driver_link = webdriver.Chrome(ChromeDriverManager().install())
    for lnk in company_links:
        if lnk.get_attribute("href") not in visited_links:
            visited_links.append(lnk.get_attribute("href"))
            go_inside_obj = go_into_link("None","wlw",driver_link,lnk)#link_3d =  fablabs
            go_inside_obj.go_inside()
    driver_link.close()
driver.close()
"""
flag=True
cnt=1
page_links = ""
while flag:
    if cnt==1:
        cnt+=1
        pass
    else:
       try:
           try:
               #http://makeseleniumeasy.com/2020/05/25/elementclickinterceptedexception-element-click-intercepted-not-clickable-at-point-other-element-would-receive-the-click/
               #page_links[0].get_attribute("href") = page_links[0].get_attribute("href")[:page_links[0].get_attribute("href").find("=")+1]+str(cnt)
               #ele =  page_links[0]
               next_page_link =page_links[0].get_attribute("href")[:page_links[0].get_attribute("href").find("=")+1]+str(cnt)
               driver.get(next_page_link)
               #page_links[cnt-1]
               #driver.find_elements_by_xpath('.//a[@rel = "next"]')[0]
               #ele.send_keys(Keys.RETURN)
               cnt+=1
           except exceptions.ElementClickInterceptedException:
               flag = False
               continue
       except IndexError as error:
           flag = False
           continue

    find_links_obj = find_http_links("3dprintingbusinessdirectory",1,driver)
    links = find_links_obj.traverse_links()
    split_links_obj = split_links("3dprintingbusinessdirectory", driver, links)
    company_links, page_links, remain_links = split_links_obj.split_links_method()
    visited_links = []
    driver_link = webdriver.Chrome(ChromeDriverManager().install())
    for lnk in company_links:
        if lnk.get_attribute("href") not in visited_links:
            visited_links.append(lnk.get_attribute("href"))
            go_inside_obj = go_into_link("None","3dprintingbusinessdirectory",driver_link,lnk)#link_3d =  fablabs
            go_inside_obj.go_inside()
    driver_link.close()
    #assert("No results found." not in driver.page_source)
"""
#driver.close()