#!/usr/bin/env python
import sys, sqlite3, os, commands, subprocess

list_args = '--save -s --add -a --remove -r --info -i'

# Open Connection
xp_directory = os.environ['XP_DIR'] + '/db/'
conn = sqlite3.connect(xp_directory + 'xp.sqlite');

# Creating cursor
c = conn.cursor()

# Create table
c.execute('''
	CREATE TABLE IF NOT EXISTS ComponentByKey (
		id_componentbykey INTEGER,
		root_path TEXT,
		relative_path TEXT,
		component_key TEXT,
		PRIMARY KEY (id_componentbykey)
	)
''')

if len(sys.argv) == 4:
	if (sys.argv[1] == '--save' or sys.argv[1] == '-s'):
		# Save current path
		#print "Saving Current Path " + os.getcwd() + " string " + sys.argv[2]
		dict_path = {":root_path" : os.getcwd(), ":key": sys.argv[2], ":relative_path" : sys.argv[3]}
		#print dict_path
		c.execute("INSERT INTO ComponentByKey (root_path,component_key,relative_path) VALUES (:root_path,:component_key,:relative_path)", (os.getcwd(), sys.argv[2], sys.argv[3]))
		conn.commit()
		print 'Saved component in database'
if len(sys.argv) == 3:
	if (sys.argv[1] == '--add' or sys.argv[1] == '-a'): # Add component to current path
		# Open saved path
		c.execute("SELECT * FROM ComponentByKey WHERE component_key LIKE ?", (sys.argv[2],))
		row = c.fetchone()
		if row is None:
			print '.'
		else:
			# print row[0] # id_componentbykey
			# print row[1] # root_path
			# print row[2] # relative_path
			# print row[3] # component_key

			create_relative_path_cmd = 'mkdir -p ' + row[2]
			subprocess.check_output(create_relative_path_cmd, shell=True)
			copy_component_cmd = 'cp -r ' + row[1] + '/' + row[2]  + ' ' + row[2]
			subprocess.check_output(copy_component_cmd, shell=True)

			print 'Added component ' + row[3]

	elif (sys.argv[1] == "--remove" or sys.argv[1] == '-r'):
		# Remove a saved path
		print 'deleting', sys.argv[2]
		c.execute("DELETE FROM ComponentByKey WHERE component_key = ?", (sys.argv[2],))
		conn.commit()
	elif (sys.argv[1] == '--info' or sys.argv[1] == '-i'): # Add component to current path
		# Open saved path
		c.execute("SELECT * FROM ComponentByKey WHERE component_key LIKE ?", (sys.argv[2],))
		row = c.fetchone()
		if row is None:
			print '.'
		else:
			# print row[0] # id_componentbykey
			number_files_cmd = 'find ' + row[1] + '/' + row[2] + ' -type f | wc -l'
			number_files=subprocess.check_output(number_files_cmd, shell=True)
			number_files=number_files.strip()
			print "Component " + row[3] + " {" # component_key
			print "\tDirectory: " + row[1] # root_path
			print "\tRelative Path: " + row[2] # relative_path
			print '\tNumber of Files: ' + number_files
			print "}"

elif len(sys.argv) == 2:
	if (sys.argv[1] == '--list' or sys.argv[1] == '-l'):
		# List all saved path
		c.execute("SELECT * from ComponentByKey ORDER BY component_key")
		for row in c:
			number_files_cmd = 'find ' + row[1] + '/' + row[2] + ' -type f | wc -l'
			number_files=subprocess.check_output(number_files_cmd, shell=True)
			number_files=number_files.strip()
			print str(row[3]) + ":" + str(row[1] + ' [' + number_files + ' files]')
	elif (sys.argv[1] == '--auto-list'):
		# Auto List all saved path for Autocomplete use
		c.execute("SELECT * from ComponentByKey")
		strList = ''
		for row in c:
			strList = strList + ' ' +  str(row[3])
		print strList
	elif (sys.argv[1] == '--list-args'):
		print list_args


# We can also close the cursor if we are done with it
c.close()
