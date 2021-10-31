# PythonParser

Python parser: Write a python parser which takes auth.log file as input, (optional date) and return following summaries. Sample auth.log file is attached. 

Python parser.py –file /foo/auth.log [--date DATE ] 

# of “Failed password” and # of “reverse mapping” attempts distributed by IP addresses for a given date. 

# of failed password attempts: 
{ “2018-04-13” : { root : { “TOTAL” : 10, 
“IPLIST” : { “IP1“ : 4 , “IP2”: 6}, 
{ “BUSER” : { “TOTAL” : 18, 
“IPLIST” : { “IP3“ : 7 , “IP4”: 11} }} 
“YYYY-MM-DD” : { user: { total: value, IPLIST: {} } } 
} 

Above can be interpreted as there were 10 failed passwords attempts made for user root on “Date” and 4 came from IP1, and 6 came from IP2. If date is not given, then report all entries in the log file. 

For reverse mapping, instead of user, report getaddrinfo string. 
{ “DATE” : { “undefined.datagroup.ua” : {TOTAL: 1, IPLIST: {}} } 

Hints: Strings to look out for 
Reverse mapping#: “reverse mapping checking getaddrinfo for undefined.datagroup.ua [93.183.207.5] failed - POSSIBLE BREAK-IN ATTEMPT!” 
Failed password: “Failed password for root from 123.183.209.132 port 63858 ssh2” 
