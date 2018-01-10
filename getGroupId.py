import requests
import json


startup_vars = check_startup()
server = startup_vars['server']
token = startup_vars['token']


call = '/ers/config/identitygroup'


headers = {
    "authorization" : "Basic " + token,
    "accept": "application/json",
    "content-type": "application/json"
}

url = 'https://' + server + ':9060' + call
print('Headers is: ', headers)
print('url is: ', url)

resp = requests.get(url, headers=headers, verify=False)
response_json = resp.json()  # Get the json-encoded content from response
print("Status: ", resp.status_code)  # This is the http request status
print("Status.Headers: ", resp.headers)
print(json.dumps(response_json,
                 indent=4))  # Convert "response_json" object to a JSON formatted string and print it out

groups = response_json['SearchResult']['resources']

for group in groups :
    print('id = ',groups[groups.index(group)]['id'])
    print('name = ', groups[groups.index(group)]['name'])
    print('description = ', groups[groups.index(group)]['description'])
    print('\n')