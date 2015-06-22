# httb
a lightweighted HTTP server response benchmark tools. It is capable of sending concurrent HTTP Get requests.

# Usage
NAME
        httb.py - benchmark HTTP server with concurrent requests
SYNOPSIS
        python httb.py {target_url} {numOfConns} {numOfRequests}
OPTIONS
        {numOfConns} is number of concurrent connections, default is 1, limited to 100
        {numOfRequests} is number of requests to send, default is 5, limited to 1000
Example
        python httb.py www.server.com/page 10 100

# Prerequest
Developed on Python 2.7.9
Required Python modules:
  requests
Install modules:
  pip install requests