
'''

Script used to load users into ISE database. Used for lab testing. Development done on ISE version 2.2
Once users are loaded rest of scripts can be used to test changing passwords, etc.

'''




import openpyxl
import requests
import json
from startup import check_startup


workbook = 'user_file.xlsx'
sheet = 'Sheet1'


startup_vars = check_startup()
server = startup_vars['server']
token = startup_vars['token']


call = '/ers/config/internaluser'
user_filter = '?filter=name.EQ.{}'

headers = {
    "authorization": "Basic " + token,
    "accept": "application/json",
    "content-type": "application/json"
}


wb = openpyxl.load_workbook(workbook)
sheet = wb.get_sheet_by_name(sheet)
data_list = []
for row in range(2, sheet.max_row + 1):
    data = {}
    first = sheet['A' + str(row)].value
    last = sheet['B' + str(row)].value
    name = sheet['C' + str(row)].value
    email = sheet['D' + str(row)].value
    passwd = sheet['E' + str(row)].value
    data['first'] = first
    data['last'] = last
    data['name'] = name
    data['email'] = email
    data['passwd'] = passwd
    print(data)
    data_list.append(data)

print(data_list)


users=[]
for index in range(len(data_list)) :
    print(data_list[index]['email'])
    print(data_list[index]['name'])
    users.append(data_list[index]['name'])

print(users)

print(first, last, name, email)

for user in data_list :
    print('users is', users)
    index = data_list.index(user)
    print('index =', index)
    print('index type is:', type(index))
    name = data_list[index]['name']
    first = data_list[index]['first']
    last = data_list[index]['last']
    email = data_list[index]['email']
    passwd = data_list[index]['passwd']


# Run getGroupId.py to get the identityGroups and modify below req_body_json appropriately
    req_body_json = """  {{
        "InternalUser" : {{
            "name" : "{}",
            "description" : "{}",
            "enabled" : true,
            "email" : "{}",
            "password" : "{}",
            "firstName" : "{}",
            "identityGroups" : "10a42820-6d90-11e5-978e-005056bf2f0a,10df3550-6d90-11e5-978e-005056bf2f0a",
            "lastName" : "{}",
            "changePassword" : false,
            "expiryDateEnabled" : false,
            "enablePassword" : "{}",
            "customAttributes" : {{
            }},
            "passwordIDStore" : "Internal Users"
        }}
    }}
    """.format(name, email, email, passwd, first,last, passwd)


    url = 'https://' + server + ':9060' + call
    data = json.dumps(req_body_json)
    print(url)
    print('Headers is: ', headers)
    print('url is: ', url)
    print('req_body_json', req_body_json)
    print('body is:', data )

    resp = requests.post(url, data=req_body_json, headers=headers, verify=False)
    #response_json = resp.json()  # Get the json-encoded content from response
    print("Status: ", resp.status_code)  # This is the http request status
    print("Status text: ", resp.text)
    print("Response: ", resp.headers['Location'])


for user in users :
    url = 'https://' + server + ':9060' + call + user_filter.format(user)
    print(url)
    print('Headers is: ', headers)
    print('url is: ', url)

    resp = requests.get(url, headers=headers, verify=False)
    response_json = resp.json()  # Get the json-encoded content from response
    print("Status: ", resp.status_code)  # This is the http request status
    print(json.dumps(response_json,
                     indent=4))  # Convert "response_json" object to a JSON formatted string and print it out


