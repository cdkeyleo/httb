"""
httb.py
Developed on Python 2.7.9, by Tao
Required Python module:
  requests
Install requests
  pip install requests
"""
import requests
import multiprocessing
from functools import partial
import sys
from datetime import datetime

# send http get request
# url: the target url to get
# x: unused argument, to be compatible with multipleprocessing pool.map
# return response time
def httpGet(url, x):
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0'} # change default User-Agent to avoid firewall deny
  try:
    r = requests.get(url, headers=headers)
  except Exception, e: # if error happens, return -1
    print '\nError.',
    return -1
  else:
    if r.status_code == 200: # if server response OK, return response time
      print '.', # print test progress
      return r.elapsed.total_seconds()
    else: # if server return response other than OK, return -1
      print '\nError.',
      return -1

# get url in argument, and format it
# args: the list containing arguments
# position: the position of url in arguments list
def urlInArgument(args, position):
  url = 'http://www.ausmore.com.au' # define a default url to return
  try: # get the argument for url, if user doesn't give a url argument, benchmark the default url
    url = args[position]
    if not url.startswith('http'): # if the url doesn't start with http://, add the string of http:// at the beginning
      url = 'http://' + url
  except Exception, e:
    print 'No URL given. Testing with default URL...\n'
  return url

# remove failed result from array
def refine(array):
  refined = []
  for x in array:
    if x < 0: # failed request is marked as -1
      pass
    else:
      refined.append(x)
  return refined

# calculate variance of a list
def variance(array):
  result = 0
  average = sum(array) / len(array)
  for x in array:
    result += (x - average) * (x - average)
  return result / len(array)

def usage():
  print 'NAME'
  print '\thttb.py - benchmark HTTP server with concurrent requests'
  print 'SYNOPSIS'
  print '\tpython httb.py {target_url} {numOfConns} {numOfRequests}'
  print 'OPTIONS'
  print '\t{numOfConns} is number of concurrent connections, default is 1, limited to 100'
  print '\t{numOfRequests} is number of requests to send, default is 5, limited to 1000'
  print 'Example'
  print '\tpython httb.py www.server.com/page 10 100'



if __name__ == '__main__': # only run when the script called by python interpreter
  try:
    if sys.argv[1] == ('-h' or '-help' or '--h'): # if user asks to print help
      usage()
      exit()
  except Exception, e: # if no arguments given, continue with default arguments
    pass

  numOfConns = 1 # define default value of numOfConns
  numOfRequests = 5 # define default value of numOfRequests
  url = urlInArgument(sys.argv, 1) # get url in arguments

  try: # try to get numOfConns argument
    numOfConns = int(sys.argv[2]) if int(sys.argv[2]) <= 100 else 100 # maximum value of numOfConns is 100
  except Exception, e:
    print 'Number of concurrent connections is not given. Testing with default', numOfConns, 'concurrent connections.'

  try: # try to get numOfRequests argument
    numOfRequests = int(sys.argv[3]) if int(sys.argv[3]) <= 1000 else 1000 # maximum value of numOfRequests is 1000
  except Exception, e:
    print 'Number of requests is not given. Testing with default', numOfRequests, 'requests.\n'

  print 'Sending', numOfRequests, 'request to:', url, 'in', numOfConns, 'concurrent connections', # start testing
  pool = multiprocessing.Pool(numOfConns) # create numOfConns workers for the job
  partial_get = partial(httpGet, url) # use functools.partial to pass multiple arguments to multipleprocessing pool.map
  start = datetime.now() # record test start time
  results = pool.map(partial_get, range(numOfRequests)) # numOfConns workers perform the httpGet method for numOfRequests times
  pool.close()
  pool.join()
  end = datetime.now() # record test end time
  successResults = refine(results) # remove failed results
  print '\n'
  print 'The test is finished in:', (end-start).total_seconds(), 'seconds'
  print 'Numbe of successful requests:', len(successResults)
  print 'Numbe of failed requests:', len(results) - len(successResults)
  if len(successResults) == 0: # exit now if all requests failed
    exit()
  print 'Average response time:', sum(successResults) / len(successResults) ,'seconds'
  print 'Shortest response time:', min(successResults) ,'seconds'
  print 'Longest response time:', max(successResults) ,'seconds'
  print 'Variance of response time:', variance(successResults)


