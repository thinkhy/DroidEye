#coding=utf-8
import requests
import json
import time
import random
import sys
import re
import string
import traceback

gol_lastId = '0'
# 设置请求头部信息
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
'Accept':'application/vnd.github.mercy-preview+json',
'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accept-Encoding':'gzip',
'Connection':'close',
'Referer':'http://www.baidu.com/link?url=_andhfsjjjKRgEWkj7i9cFmYYGsisrnm2A-TN3XZDQXxvGsM9k9ZZSnikW2Yds4s&amp;amp;wd=&amp;amp;eqid=c3435a7d00146bd600000003582bfd1f'
}

def getChangeUrl(url):
    try:
        characters = string.ascii_letters  + string.digits
        secret =  "".join(random.choice(characters) for x in range(random.randint(8, 16)))
        headers['Referer'] = 'http://www.baidu.com/link?url=_andhfsjjjKRgEWkj7i9cFmYYGsisrnm2A-TN3XZDQXxvGsM9k9ZZSnikW2Yds4s&amp;amp;wd=&amp;amp;eqid=%s'%(secret)
        print("header:", headers['Referer'])
        #添加代理IP
        secure_random = random.SystemRandom()
        proxy = secure_random.choice(proxy_list)
        print("choose proxy: ", proxy)
        session = requests.session()
        session.proxies = {'http':proxy,
                            'https':proxy
                            }
#         r=session.get(url,headers=headers)
        r=requests.get(url,headers=headers)
    except Exception as e:
        print traceback.format_exc()
    return r


def getUser(lastId):
    res_dict = {}
    url='https://api.github.com/users?since=%s'%(lastId)
    r=getChangeUrl(url)
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
    login_list=[]
    url='https://api.github.com/users/'+login+'/repos'
    r=getChangeUrl(url)
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
    print login,name
    url='https://api.github.com/repos/'+login+'/'+name+'/issues'
    r=getChangeUrl(url)
    if r.status_code == 200:
        if  r.content:
            res_issues_list=json.loads(r.content)
            for j in range(len(res_issues_list)):
#                     print  res_issues_list[j]['user']['id'],login,res_issues_list[j]['id'],res_issues_list[j]['title'] , res_issues_list[j]['body'] , res_issues_list[j]['comments_url']
                    content_list=getReposCommentss(res_issues_list[j]['comments_url'])
                    # print content_list
                    res_dict = {}
                    if not content_list:
                        res_dict['user_id']=res_issues_list[j]['user']['id']
                        res_dict['login_name']=login
                        res_dict['res_name']=name
                        res_dict['issues_id']=res_issues_list[j]['id']
                        res_dict['issues_title']=res_issues_list[j]['title']
                        res_dict['issues_body']=res_issues_list[j]['body']
                        res_dict['issues_comments_url']=res_issues_list[j]['comments_url']
                        jstxt=json.dumps(res_dict)
                        print jstxt
                        txt_name=gol_lastId+'_'+login+'_'+name+'.txt'
                        # file=open('/Users/chenxiangyu/local/'+txt_name,'a')
                        file=open('/home/cxy/python/'+txt_name,'a')
                        file.write(jstxt+'\n');
                        file.close()
                    else:
                        print len(content_list)
                        for k in range(len(content_list)):
                            res_dict['user_id']=res_issues_list[j]['user']['id']
                            res_dict['login_name']=login
                            res_dict['res_name']=name
                            res_dict['issues_id']=res_issues_list[j]['id']
                            res_dict['issues_title']=res_issues_list[j]['title']
                            res_dict['issues_body']=res_issues_list[j]['body']
                            res_dict['issues_comments_url']=res_issues_list[j]['comments_url']
                            res_dict['issues_comments_body']=content_list[k]
                            jstxt=json.dumps(res_dict)
                            print jstxt
                            txt_name=gol_lastId+'_'+login+'_'+name+'.txt'
                            # file=open('/Users/chenxiangyu/local/'+txt_name,'a')
                            file=open('/home/cxy/python/'+txt_name,'a')
                            file.write(jstxt+'\n');
                            file.close()

        else:
            print 'result  is empty '
            return
    else:
        print ('result status_code is %s'%r.status_code)

'''
根据url获取包结构
'''
def getReposCommentss(comments_url):
    content_list=[]
    r=getChangeUrl(comments_url)
    if r.status_code == 200:
        if  r.content:
            res_content_list=json.loads(r.content)
            for i in range(len(res_content_list)):
                content_list.append(res_content_list[i]['body'])
            return content_list
        else:
            print 'result  is empty '
            return content_list
    else:
        print ('result status_code is %s'%r.status_code)
        return content_list

'''
根据url获取包结构
'''
def getReposContents(contents_url):
    content_list=[]
    r=getChangeUrl(contents_url)
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
获取HTTPS代理
"""
proxy_list = ['http://1:1@198.56.194.123:8080']
# getIssues('chenpdsu','msms')

count = 0
try:
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
                    time.sleep(15)

            time.sleep(15)

        time.sleep(15)
        count+=1
except Exception as e:
    print(traceback.format_exc())
