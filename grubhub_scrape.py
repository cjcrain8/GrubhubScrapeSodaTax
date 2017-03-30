 #!/user/bin/python

"""

##################################################
##												##
## 	GRUBHUB SCRAPE: MIN WAGE AND CAL POST		##
## 					PROJECTS					##
##	Chelsea Crain								##
##	12/07/16									##
##												##
## 	This program goes through the list of 		##
## 		neighborhoods and scrapes  				##
##		main pages and menu pages of all 		##
##		all restaurants located in those areas.	##
##												##
##################################################


"""

from __future__ import print_function, division
from lxml import html
import csv, sys
from itertools import izip_longest
from os.path import join, dirname, realpath
import pandas as pd
from os import path
from datetime import date
import os
import time 
import time, os, re, codecs, math, random, csv, datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import sys
import uuid

delay = 15

general_path = "E:\\Grubhub_SodaTax\Grubhub_Scrapes" 



def get_done_lists(area, scrape_name):

	path = general_path + "\\Scrape_" + scrape_name
	if not os.path.isdir(path):
		os.makedirs(path)
	done_zips_name = os.path.join(path, "done_zips_" + area + ".csv")
	done_list_name = os.path.join(path, "done_list_" + area + ".csv")
	
	try:
		df = pd.read_csv(done_list_name)
		done_list = df['done'].tolist()
	except:
		file = open(done_list_name, 'w')
		file.write("done" + "," + "\n")
		file.close()
		df = pd.read_csv(done_list_name)
		done_list = df['done'].tolist()
		
	try:
		df = pd.read_csv(done_zips_name)
		done_zips = df['done'].tolist()
	except:
		file = open(done_zips_name, 'w')
		file.write("done" + "," + " service notes" + "\n")
		file.close()
		df = pd.read_csv(done_zips_name)
		done_zips = df['done'].tolist()
		
	return done_list, done_zips, path, done_zips_name, done_list_name
	
def count_letters(zip):

	letters = len(zip) - zip.count(' ')
	
	if letters < 5:
		zip = "0" + str(zip)
	else:	
		zip = str(zip)
		
	print(zip)
	
	return zip

def get_driver():

	url = "https://www.grubhub.com"
	opts = Options()
	opts.add_experimental_option("prefs", {"profile.default_content_settings.cookies": 2})
	
	driver = webdriver.Chrome('C:\Program Files (x86)'
				'\Google\Chrome\Application\chromedriver.exe', chrome_options=opts)
	
	driver.get(url)
	
	
	return driver

def search_for_restaurants(driver, zip):
		
	try:
		driver.find_element_by_link_text('Thanks, but no thanks.').click()
	except:
		search_bar = driver.find_element_by_xpath('//*[@type="search"]')
		for x in range(0,50):
			search_bar.send_keys(Keys.BACKSPACE)
		search_bar.send_keys(zip)
		search_bar.send_keys(Keys.ENTER)
	
	time.sleep(3)
	
	try:
		driver.find_element_by_xpath('.//*[@class="icon-close"]').click()
	except:
		print("no 'enjoy $ off' option found")
		
	try:

		driver.find_element_by_xpath('.//*[@class="s-btn s-btn-tertiary"]').click()
	except:
		print("no 'later delivery' option found")
	
	
	print("waiting for s-tag")
	time.sleep(4)
	
	try:
		driver.find_element_by_link_text('Thanks, but no thanks.').click()
	except:
		no_thanks = "na"
			
	

		WebDriverWait(driver, delay).until(
			EC.presence_of_element_located(
			(By.CLASS_NAME, 'icon-close')
			))
		driver.find_element_by_class_name('icon-close').click()
		print("clicked out of 'open now'")
		WebDriverWait(driver, delay).until(
			EC.presence_of_element_located(
			(By.CLASS_NAME, "restaurantCard-primaryInfo-item")
			))
		print("found it")
		
	
		WebDriverWait(driver, delay).until(
			EC.presence_of_element_located(
			(By.CLASS_NAME, "restaurantCard-primaryInfo-item")
			))
			
		try:
			driver.find_element_by_link_text('Thanks, but no thanks.').click()
		except:
			no_thanks = "na"
			
		return True
		
	except:

		return False
		

def get_list(driver):

	current_page = 1
	try:
		WebDriverWait(driver, delay).until(
			EC.presence_of_element_located(
			(By.XPATH, '//*[contains(@ng-bind,"searchData.totalPages")]')
			))
		time.sleep(3)	
		pages_exist=True
	except:
		pages_exist=False
		
	if pages_exist:
		total_pages = int(driver.find_element_by_xpath('//*[contains(@ng-bind,"searchData.totalPages")]').text)

		print("total pages: %s" %total_pages)
		
		current_restaurant_index = 0
		total_restaurants = int(driver.find_element_by_xpath('//*[contains(@ng-bind,"searchData.totalResults")]').text)
		print("total results: %s" %total_restaurants)
		url_list = []
		while current_page <= total_pages:
				# check to make sure connected to internet 
			try:
				driver.find_element_by_link_text('Thanks, but no thanks.').click()
			except:
				no_thanks = "na"
				
			time.sleep(1)
			text = driver.find_element_by_xpath('html[@id="ng-app"]').text
			text = text.encode('utf-8').strip()
			if "An error occurred" in text: 
				sys.exit()
			try:
				driver.find_element_by_link_text('Thanks, but no thanks.').click()
			except:
				x=0
			print("page %s of %s" %(current_page, total_pages))
			time.sleep(random.randint(1,3))
			WebDriverWait(driver, delay).until(
				EC.presence_of_element_located(
				(By.CLASS_NAME, "restaurantCard-primaryInfo-item")
				))
			try:
				restaurants_on_page = len(driver.find_elements_by_xpath('//*[contains(@class,"restaurantCard-primaryInfo-item")]//a'))
			except:
				time.sleep(5)
				restaurants_on_page = len(driver.find_elements_by_xpath('//*[contains(@class,"restaurantCard-primaryInfo-item")]//a'))
			i = 0
			while i < (restaurants_on_page):
				# print(i)
				url = str(driver.find_elements_by_xpath('//*[contains(@class,"restaurantCard-primaryInfo-item")]//a')[i].get_attribute('href'))
				# print(url)
				url_list.append(url)	
				i+=1
				
			try:
				driver.find_element_by_link_text('Thanks, but no thanks.').click()
			except:
				x=0
				
			current_page+=1
			
			if current_page <= total_pages: # go to next page if not on last page
				next_page = driver.find_element_by_link_text(str(current_page)).click()
				WebDriverWait(driver, delay).until(
					EC.presence_of_element_located(
					(By.XPATH, '//*[contains(@ng-bind,"searchData.currentPage")]')
					))
				
			try:
				driver.find_element_by_link_text('Thanks, but no thanks.').click()
			except:
				x=0
				
			found = False
			while found == False:
				time.sleep(1)
				try:
					actual_current_page = int(driver.find_element_by_xpath('//*[contains(@ng-bind,"searchData.currentPage")]').text)
					found = True
				except:
					found = False
					
			if (current_page != actual_current_page) and (current_page <= total_pages):
				print("WEIRD SHIT IS GOING DOWM")
				time.sleep(50)
				sys.exit()
				break
			
	elif pages_exist==False:
		total_restaurants = int(driver.find_element_by_xpath('//*[contains(@ng-bind,"searchData.totalResults")]').text)
		url_list = []
		try:
			restaurants_on_page = len(driver.find_elements_by_xpath('//*[contains(@class,"restaurantCard-primaryInfo-item")]//a'))
		except:
			time.sleep(5)
			restaurants_on_page = len(driver.find_elements_by_xpath('//*[contains(@class,"restaurantCard-primaryInfo-item")]//a'))
		i=0
		while i < (restaurants_on_page):
			url = str(driver.find_elements_by_xpath('//*[contains(@class,"restaurantCard-primaryInfo-item")]//a')[i].get_attribute('href'))
			url_list.append(url)	
			i+=1
			
	return(url_list)

	
def prep_file(path, zip):

	zip_path = os.path.join(path, zip)
	if not os.path.exists(zip_path):
		os.makedirs(zip_path)
	
	id = str(uuid.uuid4())
	print(id)
	visible_text_file = open(os.path.join(zip_path, id + ".txt"), "w")
	html_file = open(os.path.join(zip_path, id ), "w")
	
	return  visible_text_file, html_file
					
def download_menu_info(driver, url, zip, path, area):

	driver.get(url)
	
	
	try:
		WebDriverWait(driver, delay).until(
			EC.presence_of_element_located(
			(By.CLASS_NAME, "menuItem-inner")
			))
	except:
			driver.find_element_by_link_text('here').click()
			WebDriverWait(driver, delay).until(
				EC.presence_of_element_located(
				(By.CLASS_NAME, "menuItem-inner")
				))

	visible_text_file, html_file = prep_file(path, zip)	
	
	visible_text = driver.find_element_by_xpath('.//html[@id]').text
	visible_text = visible_text.encode('utf-8').strip()
	if "An error occurred" in visible_text: # check to make sure connected to internet 
		sys.exit()
	visible_text_file.write(visible_text)
	visible_text_file.close()
	

	html_text = driver.page_source
	html_text = html_text.encode('utf-8').strip()
	html_file.write(html_text)
	html_file.close()	


def main(area, scrape_name):

	
	try:	
		done_list, done_zips, path, done_zips_name, done_list_name = get_done_lists(area, scrape_name)
		
		user_agent_list = os.path.join(general_path, "user_agents.csv")
		list_of_zips = os.path.join(general_path, "zips_"+ area + ".csv")
		df = pd.read_csv(list_of_zips)
		zip_list = df['zip'].tolist()
			
		print("Number of zips done: %s" %len(done_zips))
		print("Number of menus downloaded: %s" % len(done_list))

		driver = get_driver()

		for zip in zip_list:
			if (zip in done_zips) or (str(zip) in done_zips):
				print("already got this zip: %s" %zip)
				continue
			zip = str(zip)
			if len(zip) == 4:
				zip = "0" + zip	
			print("Starting on zip %s" %zip)
			
			## GET TO THE RIGHT SEARCH PAGE #######
			service = search_for_restaurants(driver, zip)
			print(service)
			## GO THROUGH ALL PAGES AND MAKE LIST OF ALL RESTAURANT URLS #####
			if service == True:
				url_list = get_list(driver)
				random.shuffle(url_list)
				# print(url_list)
				print("Starting to save menu info")
				
				## DOWNLOAD INFO FROM ALL RESTAURANT LINKS IN ZIP CODE LIST ####
				for url in url_list:
					if url in done_list:
						print("already got this one")
						service_status = ""
						continue
					else:
						print(url)
						download_menu_info(driver, url, zip, path, area)
					
					done_list_file = open(done_list_name, 'a')
					done_list_file.write(url + "\n")
					done_list_file.close()
					done_list.append(url)	
					service_status = ""
			
			## IF NO SERVICE THEN MAKE NOTE IN DONE LIST AND CONTINUE ####
			elif service == False:
				print("NO SERVICE HERE DUDE: %s" %zip)
				service_status = "no service"
				
			done_zip_file = open(done_zips_name, 'a')
			done_zip_file.write(zip + "," + service_status + "\n")
			done_zip_file.close()
			done_zips.append(zip)
			
			try:
				driver.find_element_by_link_text('Thanks, but no thanks.').click()
			except:
				print("")
			main_page = driver.find_element_by_class_name('mainNavBrand-logo').click()
			
			WebDriverWait(driver, delay).until(
				EC.presence_of_element_located(
				(By.XPATH, '//*[@type="search"]')
				))
				
		print("ALL DONE!!!!")
			
	except:
		sys.exit()
		
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
	