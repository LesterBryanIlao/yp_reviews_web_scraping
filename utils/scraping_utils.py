import csv
import time
from configparser import ConfigParser
from typing import Any

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import word2num
class ScrapeUtil:
	@staticmethod
	def get_links(csv_files: list, output_file: str) -> list:
		temp_list = []
		for file in csv_files:
			ScrapeUtil._validate_csv_file(file)
			links = ScrapeUtil._extract_links(file)
			temp_list.extend(links)

		ScrapeUtil._write_links_to_csv(temp_list, output_file)

		return temp_list

	@staticmethod
	def _validate_csv_file(file: str) -> None:
		if not file.endswith('.csv'):
			raise ValueError("All files must be of type .csv")

	@staticmethod
	def _extract_links(file: str) -> list:
		links = []
		with open(file, 'r', newline='') as f:
			reader = csv.reader(f, delimiter=',')
			for row in reader:
				ScrapeUtil._validate_link_format(row[0])
				links.append(row[0])
		return links

	@staticmethod
	def _validate_link_format(link: str) -> None:
		if not link.startswith('http'):
			raise ValueError("All links must start with 'http'")

	@staticmethod
	def _write_links_to_csv(links: list, output_file: str) -> None:
		with open(output_file, 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')
			for link in links:
				writer.writerow([link])

	@staticmethod
	def remove_duplicates(links: list) -> list:
		return list(set(links))

	@staticmethod
	def get_detail(mode: By, xpath: str, driver: webdriver) -> str or None:
		detail = None
		try:
			detail = driver.find_element(mode, xpath).text
		except NoSuchElementException or AttributeError:
			return None
		return detail

	@staticmethod
	def get_driver() -> webdriver:
		parser = ConfigParser()
		parser.read('project.config')

		web_driver_path = parser.get('webdriver', 'driver_file_path')

		service = Service(web_driver_path)

		chrome_options = Options()
		chrome_options.add_argument("--headless")

		driver = webdriver.Chrome(service=service, options=chrome_options)
		# driver = webdriver.Chrome(service=service)

		return driver


WAIT_TIME = 20


def collect_links(url) -> list:
	"""Collects all the links from the given url."""
	driver = ScrapeUtil.get_driver()

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


def get_parent(mode: By, attribute: str, driver: webdriver) -> WebElement | None:
	"""Gets the parent element from the given driver.

	Args:
	mode: The mode to search by.
	attribute: The attribute to search for.
	driver: The driver to search from.

	Returns:
	The parent element from the given driver.
	"""
	try:
		parent = driver.find_element(mode, attribute)
		return parent
	except NoSuchElementException:
		return None


def get_more_details(parent: WebElement, mode: By, attribute: str) -> list[str]:
	"""Gets the details from the given parent element.

	Args:
		parent: The parent element to search from.
		mode: The mode to search by.

	Returns:
		The details from the given parent element.
		:param mode:
		:param parent:
		:param attribute:
	"""

	if parent is None:
		return None

	try:
		details = parent.find_elements(mode, attribute)

		return [] if len(details) == 0 else [_.text for _ in details]
	except (NoSuchElementException, AttributeError):
		print("No details found")
		return []


def get_specific_detail(detail: str, parent: WebElement, mode: By, title_attribute: str, detail_attribute: str) -> str:
    """Gets the specific detail from the given parent element.

    Args:
        detail: The detail to search for.
        parent: The parent element to search from.
        mode: The mode to search by.
        title_attribute: The attribute to match for titles.
        detail_attribute: The attribute to match for details.

    Returns:
        The detail from the given parent element, or None if not found.
    """
    if not detail:
        return None

    try:
        titles = get_more_details(parent, mode, title_attribute)
        details = get_more_details(parent, mode, detail_attribute)

        contents_dict = dict(zip(titles, details))

        return contents_dict.get(detail)  # Using .get() method to retrieve value or return None if not found
    except NoSuchElementException:
        return None

def get_digits_only(text: str) -> int:
	"""Gets the digits from the given text.

	Args:
		text: The text to search for digits.

	Returns:
		The digits from the given text.
	"""
	return int(''.join([_ for _ in text if _.isdigit()]))


def get_clean_text(text: str) -> str:
	"""Gets the clean text from the given text.

	Args:
		text: The text to clean.

	Returns:
		The clean text from the given text.
	"""
	return text.replace('\n', ' ').replace('\t', '').strip()

