import argparse
import json

#function to convert MMM(Apr) to MM(04)
def findMonth(month):
	monthValues = {'Jan':'1', 'Feb':'2', 'Mar':'3', 'Apr':'4', 'May':'5', 'Jun':'6', 'Jul':'7', 'Aug':'8', 'Sep':'9', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
	return monthValues.get(month).zfill(2)

#function to find the string inbetween first and last words
def findBetween(s, first, last):
	start = s.index( first ) + len( first )
	end = s.index( last, start )
	return s[start:end]

#function to convert dict to json with indentation
def dict_to_json(dict):
	jsonObj = json.dumps(dict,indent=4)
	return jsonObj

#function to print the values of failed password and reverse mapping attempts
def printValues(failedAttemptDict, reverseMappingAttemptDict):
	print('\n# of Failed Password attempts: \n')
	print(dict_to_json(failedAttemptDict))
	print('\n\n# of Reverse Mapping attempts: \n')
	print(dict_to_json(reverseMappingAttemptDict))

#function to store the values in dictionary on a hierarchy and also to increase the count of repeated values
def pythonParser(dictValue, timestamp, identity, ipAddress, count):
	if(dictValue.get(timestamp) == None):
		dictValue[timestamp]={}
		dictValue[timestamp][identity]={}
		dictValue[timestamp][identity]['Total'] = count
		dictValue[timestamp][identity]['IPLIST'] = {}
		dictValue[timestamp][identity]['IPLIST'][ipAddress] = count
	else:
		if(dictValue[timestamp].get(identity) == None):
			dictValue[timestamp][identity]={}
			dictValue[timestamp][identity]['Total'] = count
			dictValue[timestamp][identity]['IPLIST'] = {}
			dictValue[timestamp][identity]['IPLIST'][ipAddress] = count
		else:
			if(dictValue[timestamp][identity]['IPLIST'].get(ipAddress) == None):
				dictValue[timestamp][identity]['Total'] = dictValue[timestamp][identity]['Total'] + count
				dictValue[timestamp][identity]['IPLIST'][ipAddress] = count
			else:
				dictValue[timestamp][identity]['Total'] = dictValue[timestamp][identity]['Total'] + count
				dictValue[timestamp][identity]['IPLIST'][ipAddress] = dictValue[timestamp][identity]['IPLIST'][ipAddress] + count


#function to process the arguments and preprocess the log file 
def parseValues(args):
	totalLines = sum(1 for line in open(args['file']))
	lcount = 0
	with open(args['file']) as file:
		for line in file:
			if(args['top'] != None):
				if(lcount == args['top']):
					break
			if('reverse mapping' in line):
				splittedLine = line.split()
				timestamp = 'YYYY'+'-'+findMonth(splittedLine[0])+'-'+(splittedLine[1].zfill(2))
				datagroup = splittedLine[10]
				ipAddress = splittedLine[11].strip('[').strip(']')
				pythonParser(reverseMapping, timestamp, datagroup, ipAddress, 1)
			elif('Failed password' in line):
				count = 1
				splittedLine = line.split()
				timestamp = 'YYYY'+'-'+findMonth(splittedLine[0])+'-'+(splittedLine[1].zfill(2))
				user = findBetween(line, 'Failed password for ', ' from')
				ipAddress = findBetween(line, 'from ', ' port')
				#HANDLED ADDITIONAL CASE
				#if message repeated for n times, then n is added in count too
				if('message repeated' in line):
					count = int(findBetween(line, 'message repeated ', ' times'))
				pythonParser(failedPasswords, timestamp, user, ipAddress,count)
			lcount = lcount + 1
	print('Parsed '+str(lcount)+' lines of '+str(totalLines)+' lines')
	if(args['date'] == None):
		printValues(failedPasswords,reverseMapping)
	else:
		splitDate = args['date'].split(',')
		tempFailedPasswords = {}
		tempReverseMapping = {}
		for date in splitDate:
			tempReverseMapping[date] = reverseMapping.get(date)
			tempFailedPasswords[date] = failedPasswords.get(date)
		printValues(tempFailedPasswords, tempReverseMapping)

#Command line argument parser
#REQUIRED ARGUMENT 
#======================================================================================
#-f filepath or --file filepath 
#======================================================================================
#
#OPTIONAL ARGUMENTS
#======================================================================================
#-d dateValue or --date dateValue (i.e -d YYYY-MM-DD)
#For multiple date values use -d datevalue1,datevalue2,....datevalueN.
#DO NOT ENTER datevalues with SPACE
#--------------------------------------------------------------------------------------
#-t number or --top number (i.e -t 100, fetches results from input-file's top 100 lines)
#======================================================================================

ap = argparse.ArgumentParser()
ap.add_argument('-f', '--file', required=True, help='Path of log file to parse')
ap.add_argument('-d', '--date', help='Enter multiple values seperated by comma')
ap.add_argument('-t', '--top', type= int, help='Finds result from top n lines')
args = vars(ap.parse_args())
failedPasswords = {}
reverseMapping = {}
parseValues(args)
