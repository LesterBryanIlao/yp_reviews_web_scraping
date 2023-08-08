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

WAIT_TIME = 20


def collect_links(url) -> list:
	"""Collects all the links from the given url."""

	parser = ConfigParser()
	parser.read('project.config')

	web_driver_path = parser.get('webdriver', 'driver_file_path')

	service = Service(web_driver_path)

	chrome_options = Options()
	chrome_options.add_argument("--headless")

	# driver = webdriver.Chrome(service=service, options=chrome_options)
	driver = webdriver.Chrome(service=service)

	driver.get(url)
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
			except Exception as e:
				print(e)
				continue
		try:
			driver.refresh()
			next_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='next ajax-page']")))
			next_page_button.click()
		except Exception as e:
			print(e)
			break
	print("Execution time: {} seconds".format(time.time() - start_time))

	return hotels


def write_to_csv_file(data: list[str], output_file: str):
	"""Writes the given data to the given output file.

	Args:
    data: The data to write to the file.
    output_file: The path to the output file.
    """
	for _ in data:
		with open(output_file, 'a', newline='') as file:
			writer = csv.writer(file)
			writer.writerow([_])
def convert_csv_file_to_list(file_name: str) -> list[str]:
	"""Converts the given csv file to a list.

	Args:
	file_name: The path to the csv file.

	Returns:
	A list containing the data from the csv file.
	"""
	data = []
	with open(file_name, newline='') as file:
		reader = csv.reader(file)
		for row in reader:
			data.append(row[0])
	return data

# def get_data(url):


# if __name__ == '__main__':
# 	# website = "https://www.yellowpages.com/search?search_terms=hotel&geo_location_terms=New+York%2C+NY"
# 	website = "https://www.yellowpages.com/search?search_terms=hotel&geo_location_terms=Las+Vegas%2C+NV"
# 	output_file = f"{website[-2:]}_hotel_links.csv"
# 	write_to_csv_file(collect_links(website), output_file)

