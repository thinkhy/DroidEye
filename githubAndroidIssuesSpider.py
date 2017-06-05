import requests
import json
import time
gol_lastId = '0'
def getUser(lastId):
    res_dict = {}
    url='https://api.github.com/users?since=%s'%(lastId)
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
        print ('result status_code is '%r.status_code)

'''
根据用户名查询repos
'''
def getResposByLogin(login):
    login_list=[]
    print 'https://api.github.com/users/'+login+'/repos'
    r = requests.get('https://api.github.com/users/'+login+'/repos')
    if r.status_code == 200:
        if  r.content:
            res_login_list=json.loads(r.content)
#             print len(res_login_list),type(res_login_list)
            for j in range(len(res_login_list)):
                    if res_login_list[j]['language'] == 'Java' and res_login_list[j]['has_issues'] is True:
                        login_list.append(res_login_list[j]['name'])
            return login_list
        else:
            print 'result  is empty '
            return
    else:
        print ('result status_code is '%r.status_code)


'''
issues列表查询
对应的commits为comments_url
'''
def getIssues(login,name):
    issues_list=[]
    r = requests.get('https://api.github.com/repos/'+login+'/'+name+'/issues')
    if r.status_code == 200:
        if  r.content:
            res_issues_list=json.loads(r.content)
            for j in range(len(res_issues_list)):
                    print  res_issues_list[j]['title'] , res_issues_list[j]['body'] , res_issues_list[j]['comments_url']
        else:
            print 'result  is empty '
            return
    else:
        print ('result status_code is '%r.status_code)


count = 0
while (count < 9999999999):
    res_dict = getUser(gol_lastId)
    if not res_dict:
        break
    for k,v in res_dict.items():
        login_list = getResposByLogin(v)
        if login_list:
            for i in login_list:
                issues_list = getIssues(v,i)
                print issues_list
                time.sleep(1)

        time.sleep(1)

    time.sleep(1)
    count+=1
