#!/usr/bin/python3
################################################################################
# file:    crawler.py
# brief:   crawl stackoverflow pages tagged with "Android"
# date:    2017-04-26
# creator: thinkhy
# changes:
# 	2017-04-25  init @thinkhy
# 	2017-04-26  add two arguments @thinkhy
#################################################################################
import requests
import time
import sys
import optparse
import re
import os
import os.path
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
options, args = parser.parse_args()

start=options.start
end=options.end

print("[INFO] starting page: ", start)
print("[INFO] ending page: ", end)

# crawl page info
html=""
pagenum=1
for i in range(start,end):
     i=str(i)
     print("[INFO] we are at page list #"+i+"...")
     a=(url+'?'+page+i+'&'+parms)
     r=requests.get(url=a,headers=headers)

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
             continue	

         link="http://stackoverflow.com" + a['href']
         print("[INFO] crawling list %s page %d: %s"%(i, pagenum,link))
         r=requests.get(url=link,headers=headers)
         html=r.content
         print("[INFO] writing to the file %s.html"%(sn))
         out=open(filename, "wb") 
         out.write(html)
         out.close()
         pagenum=pagenum+1
     
         # every 1 seconds
         time.sleep(1)
      





