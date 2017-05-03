#!/usr/local/bin/python3
#!/usr/bin/python3
################################################################################
# file:    crawler.py
# brief:   crawl stackoverflow pages tagged with "Android"
# date:    2017-04-26
# creator: thinkhy
# TODO:    2017-05-02: wait when hit rate limit
# changes:
# 	2017-04-25  init @thinkhy
# 	2017-04-26  add two arguments @thinkhy
# 	2017-04-30  read ip list from proxy1.in and proxy2.in, select a proxy randomly 
#################################################################################
import traceback
import requests
import time
import sys
import optparse
import re
import os
import os.path
import random 
import string
from retrying import retry
from bs4 import BeautifulSoup

url='https://stackoverflow.com/questions/tagged/android'
parms=('&sort=newest&pagesize=15')
page=('page=')

# 设置请求头部信息
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
'Accept':'text/html;q=0.9,*/*;q=0.8',
'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accept-Encoding':'gzip',
'Connection':'close',
'Referer':'http://www.baidu.com/link?url=_andhfsjjjKRgEWkj7i9cFmYYGsisrnm2A-TN3XZDQXxvGsM9k9ZZSnikW2Yds4s&amp;amp;wd=&amp;amp;eqid=c3435a7d00146bd600000003582bfd1f'
}

# process command line arguments
parser = optparse.OptionParser()
parser.add_option('-s', '--start', 
             action="store", dest="start", type=int,default="1",
             help='starting number for page list')		
parser.add_option('-e', '--end', 
             action="store", dest="end", type=int,default="1000",
             help='ending number for page list')		
parser.add_option('-p', '--proxy', 
             action="store", dest="proxy", type=str,default="",
             help='file containing proxy list')		
options, args = parser.parse_args()

start=options.start
end=options.end
proxy=options.proxy

print("[INFO] starting page: ", start)
print("[INFO] ending page: ", end)
proxy_mode=(len(proxy)>0)

if(proxy_mode > 0):
   # read ip list
   proxy_list = []
   with open("proxy1.in") as file:
     user='pd430'
     passwd='pd430'
     port=888
     for line in file:
       ip = line.strip()
       proxy="http://%s:%s@%s:%d"%(user,passwd,ip, port)
       print("proxy: ", proxy)
       proxy_list.append(proxy)

#@retry(stop_max_attempt_number=1)
def get_page(myurl):
     characters = string.ascii_letters  + string.digits
     secret =  "".join(random.choice(characters) for x in range(random.randint(8, 16)))
     headers['Referer'] = 'http://www.baidu.com/link?url=_andhfsjjjKRgEWkj7i9cFmYYGsisrnm2A-TN3XZDQXxvGsM9k9ZZSnikW2Yds4s&amp;amp;wd=&amp;amp;eqid=%s'%(secret)
     print("header:", headers['Referer'])

     if (proxy_mode == False):
        r = requests.get(url=myurl, headers=headers)
     else:
        secure_random = random.SystemRandom()
        proxy = secure_random.choice(proxy_list)
        print("choose proxy: ", proxy)
        session = requests.session()
        session.proxies = {'http':proxy,
                           'https':proxy
                          }
        r=session.get(url=myurl,headers=headers)
      
     html=str(r.content)
     if 'Method: rate limit' in html: 
         print("waiting for a minute to work around rate limit")
         time.sleep(10*60) # I'm banned, have a sleep
     
     return r

# crawl page info
html=""
pagenum=1
for i in range(start,end):
  try:
     i=str(i)
     print("[INFO] we are at page list #"+i+"...")
     a=(url+'?'+page+i+'&'+parms)
     time.sleep(1)
     r=get_page(a)
     html=r.content
     items=BeautifulSoup(html, 'html.parser')
     docs=items.find_all('a', href=True,attrs={'class':'question-hyperlink'})
     links=[]
     sn=""
     filename=""
     for a in docs:
         m=re.search('/questions/(\d+)/',a['href'])
         if m: 
             sn=m.group(1)
             filename="./%s.html"%(sn)		
             if os.path.isfile(filename): # filter existed file
                 print(filename + " is existed")
                 continue
         else:
             print("Invalid URL %s"%(a['href']))
             continue	

         link="http://stackoverflow.com" + a['href']
         print("[INFO] crawling list %s page %d: %s\n"%(i, pagenum,link))
         r=get_page(link)
         r=requests.get(url=link, headers=headers)
         html=r.content
         print("[INFO] writing to the file %s.html"%(sn))
         out=open(filename, "wb") 
         out.write(html)
         out.close()
         pagenum=pagenum+1
     
         # every 1 seconds
         time.sleep(2)
     

  except Exception as e:
      print(traceback.format_exc())  
      print(url)
      #raise

'''          
The page of BANNED!!!

Too many requests

This IP address (198.11.174.68) has performed an unusual high number of requests and has been temporarily rate limited. If you believe this to be in error, please contact us at team@stackexchange.com.

When contacting us, please include the following information in the email:

Method: rate limit

XID: 3655009981-SJC

IP: 198.11.174.68

X-Forwarded-For:

User-Agent: Mozilla/5.0 _Windows NT 6.1; WOW64_ AppleWebKit/537.36 _KHTML, like Gecko_ Chrome/45.0.2454.101 Safari/537.36

Reason: Request rate.

Time: Tue, 02 May 2017 07:09:39 GMT

URL: stackoverflow.com/questions/3471827/how-do-i-list-all-remote-branches-in-git-1-7      
'''




