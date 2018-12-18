"""
BBC News Article Web Scraper

This script is designed to do the following:
1. Open up the BBC World News webpage.
2. Go to the US & Canada Section of the page.
3. Select the Top Headline for the section.
4. Extract text from the headline for the Top article. 
"""

# Import libraries
import numpy as np 
import pandas as pd 
import re
import os
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from bs4 import BeautifulSoup 
from tabulate import tabulate 
import requests 
from datetime import datetime 
from shutil import which
# Create BBC Article Web Scraper class object
class BBCArticleColletor:

	def __init__(self,url):
		self.link = url

	def collect(self):
		try:
			# Search for available driver paths on system
			path = which('chromedriver.exe') 
			print(path)
		except:
			pass
		finally:
			# Load available driver
			driver = webdriver.Chrome(executable_path=path)
			driver.implicitly_wait(30)
			driver.get(self.link)
			
			# Select US & Canada Section for headline collection
			python_button =  driver.find_element_by_xpath("//a[@data-panel-id='js-navigation-panel-US___Canada']")
			#python_button = python_button[0]
			python_button.click()
			# Select Top Headline
			# Selenium hands page source to Beautiful Soup 
			soup = BeautifulSoup(driver.page_source, 'html.parser')
			#print(soup.prettify())
			#headlines = soup.find('a', {'class':'title-link'})
			def headlines():
				headlines = soup.find_all('a', {'class': 'faux-block-link__overlay-link'})

				article_titles = []
				for headline in headlines:
					article = headline.contents[0]
					article_titles.append(article)
				print(article_titles)	


			weblinks = soup.find_all('a', {'class': 'faux-block-link__overlay-link', 'href': True})

			pagelinks = []
			for link in weblinks[:7]:
				url = "https://www.bbc.com{}".format(link['href'])
				pagelinks.append(url)

			articles = []
			title = []
			thearticle = []
			for link in pagelinks:
				# Store text from each article
				paragraphtext = []
				# Get URL
				url = link 
				# Get page text
				page = requests.get(url)
				# Parse with BFS
				soup = BeautifulSoup(page.text, 'html.parser')
				# Get author name, if there's a named author
				atitle = soup.find('title')
				thetitle = atitle.get_text()
				# Get the main article page
				articletext = soup.find_all('p')
				# Print text
				for paragraph in articletext:
					# Get the text only
					text = paragraph.get_text()
					paragraphtext.append(text)
				# Combine all paragraphs into an article
				thearticle.append(paragraphtext)
				title.append(thetitle)

			myarticle = [' '.join(article) for article in thearticle]

			data = {'Title':title,
			'PageLink':pagelinks,
			'Article':myarticle,
			'Date':datetime.now()}

			oldnews = pd.read_excel('bbc\\news.xlsx')
			news = pd.DataFrame(data=data)
			cols=['Title','PageLink','Article','Date']
			news = news[cols]

			uscanews = oldnews.append(news)
			uscannews.drop_duplicates(subset='Title', inplace=True)

			filename= 'bbc\\news.xlsx'
			wks_name='Data'

			writer = pd.ExcelWriter(filename)
			uscannews.to_excel(writer, wks_name, index=False)

			writer.save()
	
	
if __name__=="__main__":
	print("The bbcwebscraper.py script has started!")
	url = "https://www.bbc.com/news/world/"
	access = BBCArticleColletor(url)
	access.collect()
else:
	print("The bbcwebscrape.py file has been imported!")