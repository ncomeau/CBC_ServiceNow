# CBC_ServiceNow

[![CBC_SN_v2_Setup+Demo](https://j.gifs.com/K1PPDJ.gif)](https://youtu.be/GmKztot8LsU)
​

## Introduction

_Click on GIF for full setup+demo video, or read the instructions below/on each branch_

This is the v2 iteration of my attempts to create a ServiceNow app for the Carbon Black Cloud. With helpful input from the likes of Ryan Fortress, Jon Nelson, and Jacob Barosin - this iteration leverages 2 primary components;
  * A ServiceNow Studio Custom Application 
  * A Carbon Black Cloud python script & yaml config file
    * Which facilitates the transfer of data from the CBC REST API, to the aforementioned ServiceNow Custom App
  
## ServiceNow Component

_You can find the full installation instructions within the README.md in the **cb_sn branch** of this repo. It is recommended that this portion be installed first - in order to allow for any applicable variable alerteration within the yaml config file._

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


### ServiceNow App Setup Instructions

#### 1. Configure Github Creds in ServiceNow
 * In ServiceNow, search 'Credentials' - Navigate to 'Connections & Credentials' --> 'Credentials'
 * Select 'New'
 * Select 'Basic Auth Credentials'
  * _Oauth 2.0 is the recommended best practice - but I opted for Basic for ease of showcasing integration_
 * Input in the following:
  * Name for Creds (I tend to go with 'Github - (insert github username)'
  * Your github username
  * Your github password
 * Select 'Submit'
 
#### 2. Import App via Source Control
 * In ServiceNow, search 'Studio' --> Launch Studio
 * On the 'Select Application' pop-up window, select 'Import from Source Control'
 * Input in the following:
  * URL: https://github.com/ncomeau/CBC_ServiceNow
  * Branch: cb_sn
  * Credentials: Select creds created in step 1 above
 * Select 'Import'
 * Upon completion of import, select 'Select Application'
 * Select 'VMware Carbon Black Cloud' application you just imported
 * Importing app should be completed, with all associated tables, indexes, UI designs, and web services built in!
 
#### 3. Ensure it is enabled
* Navigate back to your ServiceNow home page
* Search 'VMware Carbon Black Cloud'
 * Select 'All' --> you should see what resembles the 'Incidents' table
 * Select an Incident name --> when looking at the additional details, you should see two new tabs;
  * Carbon Black Cloud - Device Info
  * Carbon Black Cloud - Alert Info
 * (Optional) Favorite this app by clicking the star icon
 * (Optional) Back on the main 'All' Screen, if you select the 'gear' icon you can choose which fields you would like displayed on the main table, my current fields are as follows:
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
    
### Carbon Black Python Script & Yaml Config File

_You can find the full installation instructions within the README.md in the **cb_python branch** of this repo._

This script leverages the cbc-sdk (or legacy cbapi) 'notification_listener' to periodically check for any new Alert Notifications within the CBC console. Once an alert is generated, it is then dumped to a temp json file - which is then reopened for parsing out of key fields. These fields are extracted out of the json, and then formatted based on table index fields created within the ServiceNow App.

Once the body of the post is formatted, a simple request call is made to the ServiceNow Inbound Webservice created within the ServiceNow App, as mentioned above. Then, an Incident Ticket is created within ServiceNow, and the UI additions regarding ticket details are populated with the corresponding CBC alert and device data.
