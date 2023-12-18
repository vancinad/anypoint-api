import requests
import os

host = 'https://anypoint.mulesoft.com'
api_login = '/accounts/login'
api_userData = '/accounts/api/me'
api_environments = '/accounts/api/cs/organizations/{orgId}/environments'
api_apis = '/apimanager/api/v1/organizations/{orgId}/environments/{envId}/apis'
api_logout = '/accounts/api/logout'

print(os.environ)

# get user id
user = os.environ.get('ANYPOINT_USERNAME',"")
if user == "":
    user = input("Enter Anypoint User Name:")
else:
    print('Using ANYPOINT_USERNAME "{}'.format(user))

# get password
pw = os.environ.get('ANYPOINT_PASSWORD',"")
if pw == "":
    pw = input("Enter password:")
else:
    print('Using ANYPOINT_PASSWORD "***"')

#login
r = requests.post(host+api_login,json={'username':user,'password':pw})
print("login returned {}".format(r.status_code))

#get user info
if r.status_code == 200:
    auth = r.json()['token_type'] + " " + r.json()['access_token']
    headers = {'Authorization':auth}
    r = requests.get(host+api_userData, headers=headers)
    print("user data request returned {}".format(r.status_code))

    orgId=r.json()['user']['organization']['id']

    #get environments
    url=host+api_environments.format(orgId=orgId)
    r = requests.get(url,headers=headers)
    print("get environments returned {}".format(r.status_code))

if r.status_code == 200:
    #find 'Production' environment id
    envList = r.json()['data']
    for env in envList:
        if env['name'] == 'Production':
            envId = env['id']
            break
    print("'Production' environment id='"+envId+"'")

    #get API names, IDs
    url=host+api_apis.format(orgId=orgId,envId=envId)
    r = requests.get(url,headers=headers)
    print("get apis returned {}".format(r.status_code))

if r.status_code == 200:
    apiList = r.json()['assets']
    print("API List:")
    for x in apiList:
        print("id:'{}' name:'{}'".format(x['id'],x['exchangeAssetName']))
#    pprint.pp(r.json())
        
    r = requests.get(host+api_logout, headers=headers)
    print("logout returned {}".format(r.status_code))
