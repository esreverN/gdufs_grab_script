import json
file = 'course.json'
try:
	f = open(file,"r")
	df = open('course.dump','a+')
	json_str = f.read()
	# print json_str
	dict1 = json.loads(json_str)
	for row in dict1['aaData']:
		#temp = str(row['jx0404id'])+"\t"+str(row['kcmc'])+"\t"+str(row['skls'])+"\t"+str(row['sksj'])+"\t"+str(row['ctsm'])+"\n"
		#temp = row['jx0404id']+u"\t"+row['kcmc']+u"\t"+row['skls']+u"\t"+row['sksj']+u"\t"+row['ctsm']+"\n"
		#print temp
		if row['skls'] is None:
			row['skls'] = "unknown";
		print row['jx0404id'],row['kcmc'],row['skls'],row['sksj'],row['ctsm']
finally:
	if f:
		f.close()
