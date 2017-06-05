'''
github 被封信息
{
  "message": "API rate limit exceeded for 119.57.68.162. (But here's the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.)",
  "documentation_url": "https://developer.github.com/v3/#rate-limiting"
}

'''
import requests
import json
import time
gol_lastId = '0'
headers = {'Accept':'application/vnd.github.mercy-preview+json'}
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
        print ('result status_code is %s'%r.status_code)

'''
根据用户名查询repos
'''
def getResposByLogin(login):
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
        print ('result status_code is '%r.status_code)
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
