import csv
from configparser import ConfigParser
from time import sleep
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WAIT_TIME = 20

def scrape_hotel_links(website, output_file):
	"""Scrapes the hotel links from the given website and writes them to the given output file.

	Args:
    website: The URL of the website to scrape.
    output_file: The path to the output file.
    """
	parser = ConfigParser()
	parser.read('project.config')

	web_driver_path = parser.get('webdriver', 'driver_file_path')

	service = Service(web_driver_path)

	chrome_options = Options()
	chrome_options.add_argument("--headless")

	# driver = webdriver.Chrome(service=service, options=chrome_options)
	driver = webdriver.Chrome(service=service)
	driver.get(website)
	driver.implicitly_wait(WAIT_TIME)
	driver.maximize_window()

	start_time = time.time()
	hotels = []
	next_page_button = driver.find_element(By.XPATH, "//a[@class='next ajax-page']")

	while len(hotels) < 500 and next_page_button.is_displayed():
		wait = WebDriverWait(driver, WAIT_TIME)
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		temp_hotel_links = driver.find_elements(By.XPATH, "//a[@class='business-name']")
		for link in temp_hotel_links:
			try:
				true_link = link.get_attribute('href')
				print(f"Adding {true_link}")
				hotels.append(true_link)
				with open(output_file, 'a', newline='') as csvfile:
					writer = csv.writer(csvfile, delimiter=',')
					writer.writerow([true_link])
			except Exception as e:
				print(e)
				continue

		next_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='next ajax-page']")))
		next_page_button.click()



	# with open(output_file, 'w', newline='') as csvfile:
	# 	writer = csv.writer(csvfile, delimiter=',')
	# 	for hotel in hotels:
	# 		writer.writerow([hotel])

	end_time = time.time()
	print("Execution time: {} seconds".format(end_time - start_time))

if __name__ == '__main__':
	website = "https://www.yellowpages.com/search?search_terms=hotel&geo_location_terms=New+York%2C+NY"
	# website = "https://www.yellowpages.com/search?search_terms=hotel&geo_location_terms=Las+Vegas%2C+NV"
	output_file = f"{website[-2:]}_hotel_links.csv"
	scrape_hotel_links(website, output_file)
