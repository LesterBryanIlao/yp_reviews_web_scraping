from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from utils.scraping_utils import ScrapeUtil
from main import get_driver, convert_csv_file_to_list
# collected_links = ScrapeUtil.get_links(csv_files=['NV_hotel_links.csv', 'NY_hotel_links.csv'], output_file='test.csv')
#
# collected_links = ScrapeUtil.remove_duplicates(collected_links)


driver = get_driver()
temp_list = convert_csv_file_to_list('NV_hotel_links.csv')
# print(temp_list[:10])

def get_detail(mode: By, xpath: str):
	detail = None
	try:
		detail = driver.find_element(mode, xpath).text
	except NoSuchElementException or AttributeError:
		return None
	return detail

"""data to collect: name, contact_number, address, yp_rating, reviews, payment_method, language"""
driver.get(temp_list[1])

name = get_detail(By.XPATH, '//*[@id="main-header"]/article/div/h1')
contact_number = get_detail(By.XPATH, '//*[@id="default-ctas"]/a[1]/strong')
address = get_detail(By.XPATH, '//*[@id="default-ctas"]/a[3]/span')
yp_rating_count = get_detail(By.XPATH, '//*[@id="main-header"]/article/section/div[2]/section/a[1]/span')
reviews_count = get_detail(By.XPATH, '//*[@id="main-header"]/article/section/div[2]/section/a[2]/span')
dl_location = '//*[@id="business-info"]/dl'
services_products_xpath = '//*[@id="business-info"]/dl/dt[4]'
services_products = get_detail(By.XPATH, '//*[@id="business-info"]/dl/dd[4]/text()')
print([name, contact_number, address, yp_rating_count, reviews_count])