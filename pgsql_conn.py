from configparser import ConfigParser

import psycopg2


class YPDatabaseConnection:
	def __init__(self):
		self._parser = ConfigParser()
		self._parser.read('project.config')
		self._host = self._parser.get('pg_connection', 'host')
		self._port = self._parser.get('pg_connection', 'port')
		self._user = self._parser.get('pg_connection', 'user')
		self._dbname = self._parser.get('pg_connection', 'dbname')
		self._password = self._parser.get('pg_connection', 'password')
		self.conn = psycopg2.connect(host=self._host, port=self._port, user=self._user, dbname=self._dbname,
		                             password=self._password)

		if self.conn is None:
			print("Error connecting to the database")
		else:
			print("Connection established successfully")

	def get_all_from_table(self, table: str):
		cursor = self.conn.cursor()
		cursor.execute(f"SELECT * FROM {table};")
		results = cursor.fetchall()
		cursor.close()
		return results

	def insert_into_table(self, table: str, values: list):
		cursor = self.conn.cursor()
		columns = (
		"hotel_name", "contact_number", "address", "yp_rating", "yp_review_count", "ta_rating", "ta_review_count",
		"services_products", "payment_methods", "languages", "categories", "url")
		columns_placeholder = ', '.join(columns)

		values = [str(value) if value is not None else "Null" for value in values]
		values = [f"'{value}'" if value != "Null" else value for value in values]
		values_placeholder = ', '.join(values)

		query = f"INSERT INTO {table} ({columns_placeholder}) VALUES ({values_placeholder});"

		print(f'Adding data to database:{values}')
		cursor.execute(query)
		self.conn.commit()
		print("Successfully added data to database.\n")
		cursor.close()
