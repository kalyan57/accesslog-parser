import mysql.connector as mariadb

q = "select * from entries"
try:
	print "Trying to connect to MySQL DB..."
	con = mariadb.connect(
			host='ec2-54-157-51-176.compute-1.amazonaws.com',
			port = '7777',
			database = 'test',
			user = 'musr',
			password = '15Ermines'
		)
except Exception as e:
	print "ERROR! Could not connect to MySQL DB: ", str(e)
else:
	crs = con.cursor()
	print "Reading data from MySQL DB. Query: %s..." % q
	crs.execute(q)
	res = crs.fetchall()
	tmpl = "| %s | %s | %s | %s | %s | %s |"
	head = tmpl % ('id'.ljust(5), 'ip'.ljust(16), 'requests'.ljust(8), 
				'reputation'.ljust(10), 'changed'.ljust(22), 'created'.ljust(22))
	print head
	for row in res:
		print tmpl % (
			str(row[0]).ljust(5),
			str(row[1]).ljust(16),
			str(row[2]).ljust(8),
			str(row[3]).ljust(10),
			str(row[4]).ljust(22),
			str(row[5]).ljust(22)		
		)
		#print '| ', ' | '.join(str(item) for item in row), ' |'
	crs.close()
	con.close()