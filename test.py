# import regular expressions module
import re 
# import web modules for getting IP reputation
import urllib
import urllib2

# arguments parser and usage help generator
import argparse

##########==CONFIGURATION==###########
# Config for MySQL DB
mconf = {
	'host': 'ec2-54-157-51-176.compute-1.amazonaws.com',
	'port': '7777',
	'database': 'test',
	'user': 'musr', 
	'password': '15Ermines'
	}
#Config for PostgreSQL DB
pconf = {
	'host': 'ec2-54-157-51-176.compute-1.amazonaws.com',
	'port': '7778',
	'database': 'ptest',
	'user': 'pusr', 
	'password': '15Ermine$', 
	}

# get arguments	
parser = argparse.ArgumentParser()
parser.add_argument('in_file', help = "input log file to parse to")
parser.add_argument('out_file', help = "output CSV file to save results of parsing")
args = parser.parse_args()



# function pulls out IP address from the string (one per string!)
def getip(s):
	ip = re.compile('(([2][5][0-5]\.)|([2][0-4][0-9]\.)|([0-1]?[0-9]?[0-9]\.)){3}'
					+'(([2][5][0-5])|([2][0-4][0-9])|([0-1]?[0-9]?[0-9]))')
	
	match = ip.search(s)
	if match:
		return match.group()
	else:
		return ''

# function for getting reputation of the IP from on-line service		
def getrep(ip):
	url = "https://ip.pentestit.ru"
	data = urllib.urlencode({'ip': ip})
	results = urllib2.urlopen(url, data)
	page = results.read()
	return page[page.index('REPUTATION: ') + 12]

# opens access log file
def openlog(fname):
	return open(fname)
	
# processes file data string-by-string
def read_n_proc(f):
	# empty result dictionary of ip: ipdata in the beginning
	result = {}
	for line in f:
		ip = getip(line)
		if result.get(ip, None) == None:
			# if there is no ipdata for current ip yet, add it
			result[ip] = ipdata(ip) # create new instance of ipdata object for current IP
		else:
			# otherwise, if ipdata for IP already exists, increase requests number(reqnum)
			result[ip].increqnum()
	return result
		

# object for collecting and storing data for specific IP
class ipdata(object):
	
	def __init__(self, ip):
		self.ip = ip
		# object instance for IP is created on first occurrence, first request
		self.reqnum = 1
		print "instance of ipdata obj is created for ip %s, reqnum = %d" % (self.ip, self.reqnum)
	
	def increqnum(self):
		# increments reqnum of the specific IP on every occurrence in file
		self.reqnum += 1
		print "Reqnum for ip %s is increased to %d" % (self.ip, self.reqnum)
	
	def checkrep(self):
		# requests reputation for ip
		print "Trying to get reputation of IP %s" % self.ip
		self.rep = getrep(self.ip)

# Endeavours to import MySQL-connector module
def import_mysql_connector_module():
	try :
		import mysql.connector as mariadb
	except Exception as e:
		print "ERROR! Can't import MySQL connector module: ", str(e)
		return None
	else:
		return mariadb	


# Connects MySQL DB, returns connection or None
def connect_mysql(conf):
	mdb = import_mysql_connector_module() 
	if mdb != None:
		try:
			print "Trying to connect to MySQL DB..."
			mcon = mdb.connect(**conf)
		except Exception as e:
			print "ERROR! Can't connect to MySQL DB, Error: ", str(e)
			print "config:"
			for a,b in conf.items():
				print a, ': ', b
			return None
		else:
			print "MySQL Database is connected successfully! GZ!"
			return mcon
	else:
		return None

# Takes collected data and saves it to MySQL DB		
def dump_to_mysql(d):
	m_con = connect_mysql(mconf)
	if m_con == None:
		print "MySQL DB is not accessible, can't write there"
	else:
		print "Trying to write data to the MySQL DB"
		for item in d.values():
			i = ("insert into entries(ip,requests,reputation)" 
				"values('%s', %s, %s)" % (item.ip, item.reqnum, item.rep))
			# print "query: ", i
			cursor = m_con.cursor()
			cursor.execute(i)
		# should I commit all the changes at once?
		# or would it be better to commit every single insert?
		try:
			m_con.commit()
		except Exception as e:
			print "ERROR! Could not commit transaction: ", str(e)
		else:
			print "All data has been written to MySQL DB successfully!"
		
		cursor.close()
		m_con.close()
			
		
# Endeavours to import PostgreSQL-connector module
def import_psql_connector_module():
	try :
		import psycopg2 as pmodule
	except Exception as e:
		print "ERROR! Can't import PostgreSQL connector module: ", str(e)
		return None
	else:
		return pmodule			

# Connects MySQL DB, returns connection or None
def connect_psql(conf):
	psqldb = import_psql_connector_module() 
	if psqldb != None:
		try:
			print "Trying to connect to PostgreSQL DB..."
			pcon = psqldb.connect(**conf)
		except Exception as Err:
			print "ERROR! Can't connect to PostgreSQL DB, Error: ", str(err)
			return None
		else:
			print "PostgreSQL Database is connected successfully! GZ!"
			return pcon
	else:
		return None
		
# Takes collected data and saves it to MySQL DB		
def dump_to_psql(d):
	p_con = connect_psql(pconf)
	if p_con == None:
		print "PostgreSQLSQL DB is not accessible, can't write there"
	else:
		print "Trying to write data to the PostgreSQLSQL DB"
		for item in d.values():
			i = ("insert into pentries(ip,requests,reputation)" 
				"values('%s', %s, %s)" % (item.ip, item.reqnum, item.rep))
			# print "query: ", i
			cursor = p_con.cursor()
			cursor.execute(i)
		# should I commit all the changes at once?
		# or would it be better to commit every single insert?
		try:
			p_con.commit()
		except Exception as e:
			print "ERROR! Could not commit transaction: ", str(e)
		else:
			print "All data has been written to PostgreSQL DB successfully!"
		
		cursor.close()
		p_con.close()		
		


#:::::::::::::: SCRIPT ::::::::::::::#
# parse log	
data = read_n_proc(openlog(args.in_file))
# prepare output CSV file
csv = open(args.out_file, 'w')

# go throughout collected data and request reputation of each IP, writing data to CSV by the way
for ipaddr in data.values():
	# request IP reputation
	ipaddr.checkrep()
	# write string to CSV
	str = "%s,%s,%s\n" % (ipaddr.ip, ipaddr.reqnum, ipaddr.rep)
	csv.write(str)
# close CSV file
csv.close()
# write all the collected data to MySQL
dump_to_mysql(data)
# write all the collected data to PostgreSQL
dump_to_psql(data)
