# CraigslistScraper
Search craigslist using chrome, selenium, and chromedriver

Based off of a LucidProgramming Tutorial
https://www.youtube.com/watch?v=x5o0XFozYnE
Created/Modified by AV 4/16/19

Environment: go to anaconda cloud then search for borchr27/stableenv

chromedriver (needs to match your version of chrome use this link to download chrome drivers)
chromedriver link: https://chromedriver.chromium.org/downloads

bs4 v 4.6.3
selenium v 3.141.0
pandas v 0.23.4
urllib3 v 1.23

This program is used to scrape craigslist for a certain item with the specified parameters listed at the end of the code. 
In this case it is used to monitor cragislist for a Toyota in Ann Arbor MI for less than $7000. 
The program opens a browser directs itself to the inteded site, scrapes the data, then throws the Date, Price, Title, and Link into an excel file.
