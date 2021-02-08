# CBC_ServiceNow_Studio_App

## Instructions

### 1. Configure Github Creds in ServiceNow
 * In ServiceNow, search 'Credentials' - Navigate to 'Connections & Credentials' --> 'Credentials'
 * Select 'New'
 * Select 'Basic Auth Credentials'
  * _Oauth 2.0 is the recommended best practice - but I opted for Basic for ease of showcasing integration_
 * Input in the following:
  * Name for Creds (I tend to go with 'Github - (insert github username)'
  * Your github username
  * Your github password
 * Select 'Submit'
 
 ### 2. Import App via Source Control
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
 
### 3. Ensure it is enabled
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
 
