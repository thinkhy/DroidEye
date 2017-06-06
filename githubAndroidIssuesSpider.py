'''
github 被封信息
{
  "message": "API rate limit exceeded for 119.57.68.162. (But here's the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.)",
  "documentation_url": "https://developer.github.com/v3/#rate-limiting"
}

'''
#coding=utf-8
import requests
import json
import time
import random
import sys
gol_lastId = '0'
headers = {'Accept':'application/vnd.github.mercy-preview+json'}
def getUser(lastId):
    res_dict = {}
    url='https://api.github.com/users?since=%s'%(lastId)
    #添加代理IP
#     secure_random = random.SystemRandom()
#     proxy = secure_random.choice(proxy_list)
#     print("choose proxy: ", proxy)
#     session = requests.session()
#     session.proxies = {'http':proxy,
#                         'https':proxy
#                         }
#     r=session.get(url)
    r = requests.get(url)
    if r.status_code == 200:
        if  r.content:
            res_list=json.loads(r.content)
            for i in range(len(res_list)):
                    res_dict[res_list[i]['id']]=res_list[i]['login']
                    if i==len(res_list)-1:
                        global gol_lastId
                        gol_lastId = res_list[i]['id']
            return res_dict
        else:
            print 'result  is empty '
            return
    else:
        print ('result status_code is %s'%r.status_code)

'''
根据用户名查询repos
'''
def getResposByLogin(login):
    print ('select user  is  %s '%login)
    login_list=[]
    r = requests.get('https://api.github.com/users/'+login+'/repos',headers=headers)
    if r.status_code == 200:
        if  r.content:
            res_login_list=json.loads(r.content)
            for j in range(len(res_login_list)):
                    if res_login_list[j]['has_issues'] is True:
                        if getCondition_Name(res_login_list[j]['name']):
                            login_list.append(res_login_list[j]['name'])
                        elif getCondition_List_Topics(list_topics = res_login_list[j]['topics']):
                            login_list.append(res_login_list[j]['name'])
                        elif getCondition_Contents_Url(res_login_list[j]['contents_url'].replace('/{+path}','')):
                            login_list.append(res_login_list[j]['name'])

            return login_list
        else:
            print 'result  is empty '
            return
    else:
        print ('result status_code is %s'%r.status_code)


'''
issues列表查询
对应的commits为comments_url
'''
def getIssues(login,name):
    print ('select user  %s respos  is %s'%(login,name))
    issues_list=[]
    r = requests.get('https://api.github.com/repos/'+login+'/'+name+'/issues')
    if r.status_code == 200:
        if  r.content:
            res_issues_list=json.loads(r.content)
            for j in range(len(res_issues_list)):
                    print 'select >>>>>>>>>>>>>success:'
                    print  res_issues_list[j]['title'] , res_issues_list[j]['body'] , res_issues_list[j]['comments_url']
        else:
            print 'result  is empty '
            return
    else:
        print ('result status_code is %s'%r.status_code)




'''
根据url获取包结构
'''
def getReposContents(contents_url):
    content_list=[]
    r = requests.get(contents_url)
    if r.status_code == 200:
        if  r.content:
            res_content_list=json.loads(r.content)
            for i in range(len(res_content_list)):
                content_list.append(res_content_list[i]['name'])
            return content_list
        else:
            print 'result  is empty '
            return content_list
    else:
        print ('result status_code is %s'%r.status_code)
        return content_list

'''
条件1：项目名称包含Android
'''
def getCondition_Name(name):
    if name.upper().find('ANDROID')==0:
        return True
    return False
'''
条件2：list_topics包含Android
'''
def getCondition_List_Topics(list_topics):
    for k in list_topics:
        if k.upper().find('ANDROID')==0:
            return True
    return False
'''
条件3：包结构包含build.gradle
'''
def getCondition_Contents_Url(contents_url):
    content_list=getReposContents(contents_url)
    if content_list:
        for i in content_list:
            if i=='build.gradle':
                return True
    return False

"""
http://www.ip181.com/获取HTTPS代理
"""
def get_ip181_proxies():
    proxy_list = []
    html_page = requests.get('http://www.ip181.com/').content.decode('utf-8','ignore')
    items = BeautifulSoup(html_page, 'html.parser')
    docs = items.find_all('td')
    for i in range(len(docs)):
        if docs[i].string:
            l=re.findall(r'\d+.\d+.\d+.\d+', docs[i].string)
            if l:
                proxy_list.append(l[0]+":"+docs[i+1].string)
    return proxy_list


"""
获取HTTPS代理
"""
proxy_list = []
def func1():
    global  proxy_list
    proxy_list=get_ip181_proxies()



count = 0
while (count < 9999999999):
    print count
    res_dict = getUser(gol_lastId)
    if not res_dict:
        break
    for k,v in res_dict.items():
        login_list = getResposByLogin(v)
        if login_list:
            for i in login_list:
                issues_list = getIssues(v,i)
                print issues_list
                time.sleep(5)

        time.sleep(5)

    time.sleep(5)
    count+=1

# func1()

# while 1:
#     try:
#         res_dict = getUser('0')
#         print len(res_dict)
#     except Exception as exc:
#         print(exc)
#     finally:
#         time.sleep(2)
