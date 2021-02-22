# CBC_ServiceNow

[![CBC_SN_v2_Setup+Demo](https://j.gifs.com/K1PPDJ.gif)](https://youtu.be/c30jxm0XqZ8)
​

## Introduction

_Click on GIF for full setup+demo video, or read the instructions below_

This is the v2 iteration of my attempts to create a ServiceNow app for the Carbon Black Cloud. With helpful input from the likes of Alex Van Brunt, Ryan Fortress, Jon Nelson, and Jacob Barosin - this iteration leverages 2 primary components;
  * A ServiceNow Studio Custom Application 
  * A Carbon Black Cloud python script & yaml config file
    * Which facilitates the transfer of data from the CBC REST API, to the aforementioned ServiceNow Custom App
  
## ServiceNow Component

_It is recommended that this portion be installed first - in order to allow for any applicable variable alerteration within the yaml config file._

The application itself, which you will import in, is comprised of several componets, all of which are pre-configured;
  * Table Creation:
    * Allowing for the CB-related fields to be seamlessly imported into ServiceNow
  * UI Alterations:
    * A "VMware Carbon Black Cloud" table is created, based of the "Incidents" table
    * Each "Incident" ticket itself, when clicked into, will have 2 additional tabs exposing CBC related Device and Alert info
      * 'Carbon Black Cloud - Device Info'
      * 'Carbon Black Cloud - Alert Info'
  * Inbound Webservice
    * This is the critical; as it acts as the means of faciliating the alert info gathered by the python script (which calls the CBC RESTapi), and proceeds to populate it into the fields created in the steps above
​
### ServiceNow App Setup Instructions
​
#### 1. Fork Github Repo
 * Since this is not yet an official ServiceNow app - you must import this app via Source Control in ServiceNow Studio (discussed below)
 * Select 'Fork' option in the top right of this repo to create fork within your own github account (this will allow to alter the app if desired)
   *  See [ServiceNow KB Article](https://developer.servicenow.com/dev.do#!/learn/learning-plans/orlando/servicenow_application_developer/app_store_learnv2_serviceportal_orlando_exercise_fork_repository_and_import_application_for_the_creating_custom_widgets_module) for full details
   
#### 2. Configure Github Creds in ServiceNow
 * In ServiceNow, search 'Credentials' - Navigate to 'Connections & Credentials' --> 'Credentials'
 * Select 'New'
 * Select 'Basic Auth Credentials'
   * _Oauth 2.0 is the recommended best practice - but I opted for Basic for ease of showcasing integration_
 * Input in the following:
   * Name for Creds (I tend to go with 'Github - (insert github username)'
   * Your github username
   * Your github password
 * Select 'Submit'
 
#### 3. Import App via Source Control
 * In ServiceNow, search 'Studio' --> Launch Studio
 * On the 'Select Application' pop-up window, select 'Import from Source Control'
 * Input in the following:
   * URL: url of forked repo 
     * (Should look like https://github.com/your_github_user/CBC_ServiceNow.git)
   * Branch: main
   * Credentials: Select creds created in step 2 above
 * Select 'Import'
 * Upon completion of import, select 'Select Application'
 * Select 'VMware Carbon Black Cloud' application you just imported
 * Importing app should be completed, with all associated tables, indexes, UI designs, and web services built in!
 
#### 4. Ensure it is enabled
* Navigate back to your ServiceNow home page
* Search 'VMware Carbon Black Cloud'
  * Select 'All' --> you should see what resembles the 'Incidents' table
  * Select an Incident name --> when looking at the additional details, you should see two new tabs;
    * Carbon Black Cloud - Device Info
    * Carbon Black Cloud - Alert Info
 * _(Optional)_ Favorite this app by clicking the star icon
 * _(Optional)_ Back on the main 'All' Screen, if you select the 'Gear' icon you can choose which fields you would like displayed on the main table, my current fields are as follows:
   * Number
   * Opened
   * Category
   * Alert Type
   * Severity
   * Short Description
   * Device Name
   * CBC Policy
   * App Name
   * App Reputation
   * CBC WatchList
   * CBC Report Name
   * CBC URL
​    
## Carbon Black Component
​
This script leverages the cbc-sdk (or legacy cbapi) 'notification_listener' to periodically check for any new Alert Notifications within the CBC console. Once an alert is generated, it is then dumped to a temp json file - which is then reopened for parsing out of key fields. These fields are extracted out of the json, and then formatted based on table index fields created within the ServiceNow App.

Once the body of the post is formatted, a simple request call is made to the ServiceNow Inbound Webservice created within the ServiceNow App, as mentioned above. Then, an Incident Ticket is created within ServiceNow, and the UI additions regarding ticket details are populated with the corresponding CBC alert and device data.


### CB Python Script Setup Instructions
​
#### 1. Configure CBC-SDK  
 * Instructions here: https://carbon-black-cloud-python-sdk.readthedocs.io/en/latest/installation/
 * Download associated [cbc_servicenow_v2.py]() & [servicenow.yaml]().
    * You can leverage legacy cbapi, but alternation to the python script is required (lines 21 & 24) 
​
#### 2. In the Carbon Black Cloud Console, create a CBC API Key
 * Navigate in CBC Console to **Settings > API Access > Add API Key**
   * Create API Key with `‘Access Level’` SIEM
   * Copy Keys Created for Configuration:
      * API ID (Connector ID)
      * API Secret Key (API Key)
​
#### 3. Create CBC Notification
 * Navigate in CBC Console to **Settings > Notifications > Add Notification**
 * Set-up desired notification
   * You must make a notfication based a desired **threshold** to get alerts from both CB Standard and Enterprise EDR in one notification
 * Under “How do you want to be notified?” Select SIEM connector made in step 1, under API Keys
​
#### 4. Configure API Credentials File
 * Please follow instructions as outlined here: https://carbon-black-cloud-python-sdk.readthedocs.io/en/latest/authentication/
   * It is _highly recommended_ that you leverage the 'file' option, with the name 'credentials.cbc'
   * Example:
      * [TH_alerts]
      * url = https://api-prod05.conferdeploy.net
      * token = BZNA2UIHODBABT53GBNZL/9NASABOL4
      * org_key = N4LF97SHZ
      * ssl_verify = True
​       
#### 5. Configure servicenow.yaml File
  * Edit servicenow.yaml file with the following:
    * (line 4) Add in cb-sdk profile created in step 4
    * (lines 11 & 12) Input in your ServiceNow Username and Password
    * (line 16) Update the sn_url to the URL of your ServiceNow org
      * Note: Do not change the app service name specified on the end of the URL, just the org name
 ​     
#### 6. Run Associated cbc_servicenow_v2.py Script
  * Assuming above configurations are followed, and the ServiceNow App has been imported, the script should run on a loop
  * This script will check every 60 seconds, by default (configurable), if there is a new CBC Alert available
  * If there is an alert, that alert will get fed into ServiceNow, in the form of an Incident Ticket     
​
## Deleting Application
​
If, for whatever reason, you want to delete the application, and reimport, the process is as follows:
 * In ServiceNow search: 'System Applications'
   * Select 'My Company Applications'
   * Click on the 'VMware Carbon Black' Application
     * Select 'Delete' in the top right & type 'delete' into the prompt
 * Once complete - navigate, in left hand panel, to 'My Application Import History'
   * Select the entry for the CB app & use dropdown to select 'delete' action
 * Once complete - search 'sys_repo_config.list' in the search bar
   * Repeat above steps for selecting & deleting the CB app entry
 * Follow steps above for re-import via studio if desired
