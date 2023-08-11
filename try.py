import time

from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from utils.scraping_utils import ScrapeUtil, convert_csv_file_to_list, get_specific_detail, get_digits_only

# collected_links = ScrapeUtil.get_links(csv_files=['NV_hotel_links.csv', 'NY_hotel_links.csv'], output_file='test.csv')
#
# collected_links = ScrapeUtil.remove_duplicates(collected_links)


driver = ScrapeUtil.get_driver()
temp_list = convert_csv_file_to_list('NV_hotel_links.csv')
# print(temp_list[:10])



"""data to collect: name, contact_number, address, yp_rating, reviews, payment_method, language"""
time_start = time.time()
driver.get(temp_list[0])

name = ScrapeUtil.get_detail(By.XPATH, '//*[@id="main-header"]/article/div/h1', driver)
contact_number = ScrapeUtil.get_detail(By.XPATH, '//*[@id="default-ctas"]/a[1]/strong', driver)
address = ScrapeUtil.get_detail(By.XPATH, '//*[@id="default-ctas"]/a[3]/span', driver)
yp_rating_count = ScrapeUtil.get_detail(By.XPATH, '//*[@id="main-header"]/article/section/div[2]/section/a[1]/span', driver)
yp_rating_count = get_digits_only(yp_rating_count)
reviews_count = ScrapeUtil.get_detail(By.XPATH, '//*[@id="main-header"]/article/section/div[2]/section/a[2]/span', driver)
reviews_count = get_digits_only(reviews_count)

dl_location = driver.find_element(By.XPATH, '//*[@id="business-info"]/dl')
services_products = get_specific_detail('Services/Products', dl_location, By.TAG_NAME, 'dt', 'dd')
payment_methods = get_specific_detail('Payment method', dl_location, By.TAG_NAME, 'dt', 'dd')
languages = get_specific_detail('Languages', dl_location, By.TAG_NAME, 'dt', 'dd').split(',')
categories = get_specific_detail('Categories', dl_location, By.TAG_NAME, 'dt', 'dd').split(',')
print([name, contact_number, address, yp_rating_count, reviews_count, services_products, payment_methods, languages, categories])
print(f"Time taken: {time.time() - time_start:.2f} seconds")