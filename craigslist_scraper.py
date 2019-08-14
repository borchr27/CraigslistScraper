# Based off of a LucidProgramming Tutorial
# https://www.youtube.com/watch?v=x5o0XFozYnE
# Created/Modified by AV 4/16/19

# Environment: go to anaconda cloud then search for borchr27/stableenv

# chromedriver (needs to match your version of chrome use this link to download chrome drivers)
# chromedriver link: https://chromedriver.chromium.org/downloads

# bs4 v 4.6.3
# selenium v 3.141.0
# pandas v 0.23.4
# urllib3 v 1.23

"""
This program is used to scrape craigslist for a certain item with the specified parameters listed at the end of the code. 
In this case it is used to monitor cragislist for a Toyota in Ann Arbor MI for less than $7000. 
The program opens a browser directs itself to the inteded site, scrapes the data, then throws the Date, Price, Title, and Link into an excel file. 

"""
from datetime import date
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd

from bs4 import BeautifulSoup
import urllib.request

class CraigslistScraper(object):
    
    def __init__(self, location, max_price, auto_make_model):
        self.location = location 
        self.max_price = max_price
        self.auto_make_model = auto_make_model       
       
        self.url = f"https://{location}.craigslist.org/search/cto?max_price={max_price}&auto_make_model={auto_make_model}"
    
        self.driver = webdriver.Chrome("C:/Users/mitch/Google Drive/Coding/Craigslist Scraper/chromedriver_win32/chromedriver.exe")
        self.delay = 3 #3 seconds
        
        
    def load_craigslist_url(self):
        self.driver.get(self.url)
        try: 
            wait = WebDriverWait(self.driver, self.delay)
            wait.until(EC.presence_of_element_located((By.ID, "searchform")))
            print("Page is ready")
        except TimeoutException:
            print("Loading took too much time")
            
            
    def extract_post_information(self):
        all_posts = self.driver.find_elements_by_class_name("result-row")
        
        data = []
        
        for post in all_posts:
            title = post.text.split("$")
            # ['', '800\nApr 18 Toyota Camry 1996 for sale by owner ', '800 (Ypsilanti)']

            if title[0] == '':
                title = title[1]
            else:
                title = title[0]
            
            title = title.split("\n")
            if title[0] == '':
                price = ''
            else: price = title[0]
            
            title = title[-1]      
            title = title.split(" ")
            month = title[0]
            day = int(title[1])
            title = ' '.join(title[2:])
            #date = month + " " + day
            
            data.append([month, day, price, title])
        return data 
    
        
    def extract_post_urls(self):
        url_list = []
        html_page = urllib.request.urlopen(self.url)
        soup = BeautifulSoup(html_page, "lxml")
        for link in soup.findAll("a",{"class": "result-title hdrlnk"}): 
            #print(link)
            url_list.append(link["href"])
        return url_list

    def quit(self):
        self.driver.close()
    
    def pretty_data(self, data, url_list):
        #data processing, import datetime and pandas
        #section below takes in date, price, title, and URL then adds all results to spreadsheet
        #should also sort by date column
        df = pd.DataFrame(data, columns=['Month', 'Day', 'Price', 'Title'])
        df2 = pd.DataFrame(url_list)
        df['URLs'] = df2
        df = df.sort_values(by=['Month', 'Day'])
        df.to_excel('output.xlsx')

        print('Complete')
            
    #def test(self):
    #    print(self.url)

        
#function parameters        
location = 'annarbor' #input('Location (no spaces): ')
max_price = '7000' #input('Max Price ($): ')
auto_make_model = 'toyota' #input('Auto Make / Model: ')

scraper = CraigslistScraper(location, max_price, auto_make_model)
scraper.load_craigslist_url()
url_list = scraper.extract_post_urls()
data = scraper.extract_post_information() #titles, prices, dates, 

scraper.pretty_data(data, url_list)
scraper.quit()


