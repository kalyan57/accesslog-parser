import psycopg2 as psqldb

q = "select * from pentries;"
try:
	print "Trying to connect to PostgreSQL DB..."
	con = psqldb.connect(
			host='ec2-54-157-51-176.compute-1.amazonaws.com',
			port = '7778',
			database = 'ptest',
			user = 'pusr',
			password = '15Ermine$'
		)
except Exception as e:
	print "ERROR! Could not connect to MySQL DB: ", str(e)
else:
	crs = con.cursor()
	print "Reading data from PostgreSQL DB. Query: %s..." % q
	crs.execute(q)
	res = crs.fetchall()
	tmpl = "| %s | %s | %s | %s | %s | %s |"
	head = tmpl % ('id'.ljust(5), 'ip'.ljust(16), 'requests'.ljust(8), 
				'reputation'.ljust(10), 'created'.ljust(26), 'changed'.ljust(26))
	print head
	for row in res:
		print tmpl % (
			str(row[0]).ljust(5),
			str(row[1]).ljust(16),
			str(row[2]).ljust(8),
			str(row[3]).ljust(10),
			str(row[4]).ljust(26),
			str(row[5]).ljust(26)		
		)
		#print '| ', ' | '.join(str(item) for item in row), ' |'
	crs.close()
	con.close()