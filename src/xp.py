#!/usr/bin/env python
import sys, sqlite3, os, commands, subprocess

import utils

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

def list_components(args, extra_args):
	# List all saved path
	c.execute("SELECT * from ComponentByKey ORDER BY component_key")
	for row in c:
		number_files_cmd = 'find ' + row[1] + '/' + row[2] + ' -type f | wc -l'
		number_files=subprocess.check_output(number_files_cmd, shell=True)
		number_files=number_files.strip()
		print str(row[3]) + ":" + str(row[1] + ' [' + number_files + ' files]')

def get_auto_list(args, extra_args):
	# Auto List all saved path for Autocomplete use
	c.execute("SELECT * from ComponentByKey")
	strList = ''
	for row in c:
		strList = strList + ' ' +  str(row[3])
	print strList

def get_list_args(args, extra_args):
	print list_args

def save_component(args, extra_args):
	# Save current path
	if len(args) == 2:
		component_path = os.getcwd()
		component_key = args[0]
		component_relative_path = args[1]

		save_data = (component_path,
					 component_key,
					 component_relative_path)

		c.execute("INSERT INTO ComponentByKey " +\
			"(root_path,component_key,relative_path) VALUES " +\
			"(:root_path,:component_key,:relative_path)",
			save_data)
		conn.commit()
		print 'Saved component in database'

def add_component(args, extra_args):
	# Open saved path
	if len(args) == 1:
		get_query = "SELECT * FROM ComponentByKey WHERE component_key LIKE ?"
		get_data = (args[0],)
		c.execute(get_query, get_data)
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

def remove_component(args, extra_args):
	# Remove a saved path
	if len(args) == 1:
		print 'deleting', args[0]
		c.execute("DELETE FROM ComponentByKey WHERE component_key = ?", (args[0],))
		conn.commit()

def get_info_about_component(args, extra_args):
	# Open saved path
	if len(args) == 1:
		c.execute("SELECT * FROM ComponentByKey WHERE component_key LIKE ?", (args[0],))
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

commands_parse = {
    '-s'          : save_component,
    '-a'          : add_component,
    '-r'          : remove_component,
    '-i'          : get_info_about_component,
    '-l'		  : list_components,
    '--list'	  : list_components,
    '--info'      : get_info_about_component,
    '--remove'    : remove_component,
    '--auto-list' : get_auto_list,
    '--list-args' : get_list_args,
}

def parse_arguments():

    args = {}

    last_key = ''

    for i in xrange(1, len(sys.argv)):
        a = sys.argv[i]
        if a[0] == '-' and not utils.is_float(a):
            last_key = a
            args[a] = []
        elif last_key != '':
            arg_values = args[last_key]
            arg_values.append(a)
            args[last_key] = arg_values

    return args

def parse_commands(args):
    # print('DEBUG: Parsing args: ' + str(args))
    for a in args:
        if a in commands_parse:
            commands_parse[a](args[a], args)

args = parse_arguments()
parse_commands(args)

# We can also close the cursor if we are done with it
c.close()

