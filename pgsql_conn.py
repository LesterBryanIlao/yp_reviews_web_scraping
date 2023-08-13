from configparser import ConfigParser


parser = ConfigParser()
parser.read('project.config')

class PgSqlConn:
	def __init__(self):
		self._host = parser.get('postgresql', 'host')
		self._port = parser.get('postgresql', 'port')
		self._database = parser.get('postgresql', 'database')
		self._user = parser.get('postgresql', 'user')
		self._password = parser.get('postgresql', 'password')

