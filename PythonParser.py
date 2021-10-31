import argparse
import json

def parseValues(args):
	#Write your code here

ap = argparse.ArgumentParser()
ap.add_argument('-f', '--file', required=True, help='Path of log file to parse')
ap.add_argument('-d', '--date', help='Enter multiple values seperated by comma')
ap.add_argument('-t', '--top', type= int, help='Finds result from top n lines')
args = vars(ap.parse_args())
parseValues(args)
