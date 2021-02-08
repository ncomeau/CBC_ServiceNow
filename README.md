# CBC_ServiceNow_Python_Script

## Instructions
​
### 1. Configure Cb-SDK  
 * Instructions here: https://carbon-black-cloud-python-sdk.readthedocs.io/en/latest/installation/
 * Download associated [cbc_servicenow_v2.py] & [servicenow.yaml]().
​
### 2. In the Carbon Black Cloud Console, create a CBC API Key
 * Navigate in CBC Console to **Settings > API Access > Add API Key**
   * Create API Key with `‘Access Level’` SIEM
   * Copy Keys Created for Configuration:
      * API ID (Connector ID)
      * API Secret Key (API Key)
​
### 3. Create CBC Notification
 * Navigate in CBC Console to **Settings > Notifications > Add Notification**
 * Set-up desired notification
   * You must make **both** an alert for Cb Standard and Cb Enterprise EDR, if you want to be alerted on both products
 * Under “How do you want to be notified?” Select SIEM connector made in step 1, under API Keys
​
### 4. Configure API Credentials File
 * Please follow instructions as outlined here: https://carbon-black-cloud-python-sdk.readthedocs.io/en/latest/authentication/
   * It is _highly recommended_ that you leverage the 'file' open, with the name 'credentials.cbc'
   * Example:
      * [TH_alerts]
      * url = https://api-prod05.conferdeploy.net
      * token = BZNA2UIHODBABT53GBNZL/9NASABOL4
      * org_key = N4LF97SHZ
      * ssl_verify = True
       
### 5. Configure servicenow.yaml File
  * Edit servicenow.yaml file with the following:
    * (line 4) Add in cb-sdk profile created in step 4
    * (lines 11 & 12) Input in your ServiceNow Username and Password
    * (line 16) Update the sn_url to the URL of your ServiceNow org
      * Note: Do not change the app service name specified on the end of the URL, just the org name
      
### 6. Run Associated cbc_servicenow_v2.py Script
  * Assuming above configurations are followed, and the ServiceNow App has been imported, the script should run on a loop
  * This script will check every 60 seconds, by default (configurable), if there is a new CBC Alert available
  * If there is an alert, that alert will get fed into ServiceNow, in the form of an Incident Ticket
       
​
