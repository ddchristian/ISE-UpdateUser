
# Update User Passwords in Identity Services Engine (ISE) 


This project is intended to update the user passwords for the ISE Local Users changing it to random passwords.

The user database can be copied to an excel sheet. An excel sheet is used to read the user id's make the call to the ISE server to change the password and then write the changed password back to the excel sheet.

An ISE Administrator with the "ERS-Admin" or "ERS-Operator" group assignment is required to use the API. 

From the ISE console choose Administration > Settings > ERS Settings.

The initial project was done using Python 3.6.2.

 
--- 

## Repo Information
* *README.md*
	* This document
* *requirements.txt*
	* Some of the library dependencies used
* *startup.cfg*
	* A configparser file used to store and retrieve ISE IP Address and ISE base 64 encoded token.
* *startup.py*
	* Used to set the read IP Address and token into the environment and perform basic connectivity testing
	* os.environ variables are called followed by configuration in startup.cfg file. If none of those are available user is prompted for the variables.
* *getToken.py*
	* Generates base64 encoded token.
	* Can be used to generate the token from the userid and password.
	* Can be used to manually update the token in startup.cfg
* *excel.xlsx*
	* Various Excel sheets with the expected file format to read user data and write data to.
* *addUsers.py*
	* Script used to load users into ISE database. Used for lab testing. Development done on ISE version 2.2. 
Once users are loaded the rest of scripts can be used to test changing passwords, etc.
* *getGroupId.py*
	* Used to get the group id the user belongs to. This is needed in the json request body in the addUsers.py script.
* *updateUser.py*
	* This is the main script written to iterate XML data.
Supported with ISE 1.3 and above. With ISE 1.3 XML is the only option payload option.
* *updateUser_json.py*
	* This is what the script would look like if the payload is json. ISE 1.3 only supports XML so this is useful
only to test modifying user passwords on systems that support json.
Used for lab testing. Development was done on ISE version 2.2



## Placing Environment Variables in the OS
In some environments (especially during development) it may be desireable to set some variables outside of the scripting environment.

Add the following commands from the same window (shell) that you call the Python intepreter from.

### ***MAC OSx***
```
export ISE_SERVER=198.18.16.1
export ISE_TOKEN=aXFlX2FwzSqqf8FGSXNzRVBy
```

### ***Windows***
```
set ISE_SERVER=198.18.16.1
set ISE_TOKEN=aXFlX2FwzSqqf8FGSXNzRVBy
```



	
 