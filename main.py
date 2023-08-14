from pgsql_conn import YPDatabaseConnection
from utils.scraping_utils import *

driver = ScrapeUtil.get_driver()
temp_list = ScrapeUtil.remove_duplicates(convert_csv_file_to_list('test.csv'))
print(len(temp_list))
total_success = 0
for url in temp_list:
	try:
		driver.get(url)

		hotel_name = ScrapeUtil.get_detail(By.XPATH, '//*[@id="main-header"]/article/div/h1', driver)

		contact_number = ScrapeUtil.get_detail(By.XPATH, '//*[@id="default-ctas"]/a[1]/strong', driver)

		address = ScrapeUtil.get_detail(By.XPATH, '//*[@id="default-ctas"]/a[3]/span', driver)
		address = get_clean_text(address)

		yp_rating = get_rating(By.CLASS_NAME, 'yp-ratings', driver)
		yp_rating = clean_rating(yp_rating, 'yp')
		yp_review_count = get_review_count(By.CLASS_NAME, 'yp-ratings', driver)
		yp_review_count = clean_review_count(yp_review_count)

		ta_rating = get_rating(By.CLASS_NAME, 'ta-rating-wrapper', driver)
		ta_rating = clean_rating(ta_rating, 'ta')
		ta_review_count = get_review_count(By.CLASS_NAME, 'ta-rating-wrapper', driver)
		ta_review_count = clean_review_count(ta_review_count)

		dl_location = driver.find_element(By.XPATH, '//*[@id="business-info"]/dl')
		services_products = get_specific_detail('Services/Products', dl_location, By.TAG_NAME, 'dt', 'dd')
		payment_methods = get_specific_detail('Payment method', dl_location, By.TAG_NAME, 'dt', 'dd')
		languages = get_specific_detail('Languages', dl_location, By.TAG_NAME, 'dt', 'dd')
		categories = get_specific_detail('Categories', dl_location, By.TAG_NAME, 'dt', 'dd')

		collected_details = (
			hotel_name, contact_number, address, yp_rating, yp_review_count, ta_rating, ta_review_count, services_products,
			payment_methods, languages, categories, url)

		collected_details = [str(value) if value is not None else "Null" for value in collected_details if
		                     not (isinstance(value, (int, float)) and value == "Null")]

		yp_db_conn = YPDatabaseConnection()
		yp_db_conn.insert_into_table('yellow_page_reviews', collected_details)
		total_success += 1
	except Exception as e:
		print(e)
		continue

print(f"Total successful scraped links: {total_success}")