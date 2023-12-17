import requests
import pprint

host = 'https://anypoint.mulesoft.com'
api_login = '/accounts/login'
api_userData = '/accounts/api/me'
api_logout = '/accounts/api/logout'

# get user id
user = input("Enter Anypoint User Name:")

# get password
pw = input("Enter password:")

r = requests.post(host+api_login,json={'username':user,'password':pw})
print("login returned {}".format(r.status_code))

if r.status_code == 200:
    auth = r.json()['token_type'] + " " + r.json()['access_token']
    headers = {'Authorization':auth}
    r = requests.get(host+api_userData, headers=headers)
    print("user data request returned {}".format(r.status_code))

if r.status_code == 200:
    pprint.pp(r.json())
    r = requests.get(host+api_logout, headers=headers)
    print("logout returned {}".format(r.status_code))
