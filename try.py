from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from utils.scraping_utils import ScrapeUtil, get_more_details, convert_csv_file_to_list

# collected_links = ScrapeUtil.get_links(csv_files=['NV_hotel_links.csv', 'NY_hotel_links.csv'], output_file='test.csv')
#
# collected_links = ScrapeUtil.remove_duplicates(collected_links)


driver = ScrapeUtil.get_driver()
temp_list = convert_csv_file_to_list('NV_hotel_links.csv')
# print(temp_list[:10])



"""data to collect: name, contact_number, address, yp_rating, reviews, payment_method, language"""
driver.get(temp_list[1])

# name = ScrapeUtil.get_detail(By.XPATH, '//*[@id="main-header"]/article/div/h1', driver)
# contact_number = ScrapeUtil.get_detail(By.XPATH, '//*[@id="default-ctas"]/a[1]/strong', driver)
# address = ScrapeUtil.get_detail(By.XPATH, '//*[@id="default-ctas"]/a[3]/span', driver)
# yp_rating_count = ScrapeUtil.get_detail(By.XPATH, '//*[@id="main-header"]/article/section/div[2]/section/a[1]/span', driver)
# reviews_count = ScrapeUtil.get_detail(By.XPATH, '//*[@id="main-header"]/article/section/div[2]/section/a[2]/span', driver)
dl_location = driver.find_element(By.XPATH, '//*[@id="business-info"]/dl')
dt_contents = get_more_details(dl_location, By.TAG_NAME, 'dt')
print(dt_contents)
# print([name, contact_number, address, yp_rating_count, reviews_count])
