from selenium.webdriver.chrome.webdriver import WebDriver

from utils.scraping_utils import ScrapeUtil
from main import get_driver
# collected_links = ScrapeUtil.get_links(csv_files=['NV_hotel_links.csv', 'NY_hotel_links.csv'], output_file='test.csv')
#
# collected_links = ScrapeUtil.remove_duplicates(collected_links)


driver = get_driver()
print(isinstance(driver, WebDriver))