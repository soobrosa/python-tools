# -*- coding: utf-8 -*-
# June 11, 2012 --- soobrosa

import sys, csv, operator
from collections import defaultdict 

if len(sys.argv) == 1:
	print "No input filename provided, using default input file."
	print
	input = 'pg0b6_ipdm_relay_rr.tsv'
else:
	input = sys.argv[1] # input filename can be provided

rows = defaultdict(int) # dictionary to count different row masks
rows_example = {} # dictionary of examples of row masks
columns = [] # will be a list of dictionaries to count different values in columns
total_rows = 0

f = open(input, "rb")
headers = f.readline().strip().split('\t') # grab headers
for header in headers:
	columns.append(defaultdict(int)) # make a dictionary for each column

for row in f:
	row_mask = ''
	row = row.strip().split('\t')
	column_index = 0
	total_rows += 1
	for column in row:
		columns[column_index][column] += 1 # count each different cell value in its column
		column_index += 1
		if column <> '': # row_mask contains 1 if cell value is not empty
			row_mask += '1'
		else:
			row_mask += '0'
	rows[row_mask] += 1 # count each different row_mask
	if row_mask not in rows_example:
		rows_example[row_mask] = row # save an example if it's a new pattern
f.close()

print 'Most common row patterns.'
for item in sorted(rows, key=rows.get, reverse=True): # in descending order
	print '%s found %s times' % (item, rows[item]) # enlist mask + occurence
	current_header = []
	for i in range(0, len(item)):
		if item[i] == '1':
			current_header.append(headers[i]) # enlist occuring headers
		else:
			current_header.append('('+headers[i]+')') # non-occuring are within brackets
	print 'Mask consists of headers:'
	print ','.join(current_header)
	print 'Example row:'
	print rows_example[item]
	print ''

print 'Column analysis.'
for i in range (0, len(columns)): # in descending order
	sys.stdout.write(headers[i] + ' column values ')
	item_count = len(columns[i])
	answers = ['', 'are univocal.', 'are binary.', 'are binary (sort of).'] # comment on small number of values
	if item_count < 4:
		sys.stdout.write(answers[item_count])
	if item_count < 10: # list them only if less than 10 different values
		print # just for the new line
		for item in sorted(columns[i], key=columns[i].get, reverse=True): # in descending order
			if item == '':
				item_name = 'Empty' # translate empty string to 'Empty'
			else:
				item_name = item
			print '%s found %s times (%.2f percent)' % (item_name, columns[i][item], float(columns[i][item])/total_rows*100)
	else:
		print 'are too sparse (%d different values are given).' % item_count
		is_first = True
		for item in sorted(columns[i], key=columns[i].get, reverse=True): # tell about whether most common is empty string
			if is_first:
				is_first = False
				if item == '':
					print 'However empty is the most common and found %s times (%.2f percent)' % (columns[i][item], float(columns[i][item])/total_rows*100)
	print ''