import csv
import os
from configparser import ConfigParser
from time import sleep
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



# def get_data(url):


# if __name__ == '__main__':
# 	# website = "https://www.yellowpages.com/search?search_terms=hotel&geo_location_terms=New+York%2C+NY"
# 	website = "https://www.yellowpages.com/search?search_terms=hotel&geo_location_terms=Las+Vegas%2C+NV"
# 	output_file = f"{website[-2:]}_hotel_links.csv"
# 	write_to_csv_file(collect_links(website), output_file)

