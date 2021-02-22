import json
import requests
import yaml

#!!! It is recommended you use the new cb-sdk - if you are still using legacy cbapi, reference lines 16-24 !!!#
from cbc_sdk import CBCloudAPI
from cbapi.psc.defense import *


##### Call Yaml for configs #####

# Call yaml to pull in configs for proper hygiene
with open('servicenow.yaml') as f:
    y = yaml.load(f)

###### Creds From Yaml #######

# Input your cbapi profile from yaml - make sure the connector type is 'SIEM'

#!!! Use the below if using the new cb-sdk -- recommended !!!#
cb = CBCloudAPI(profile=y['creds']['cb']['cb_profile'])

#!!! Use the below profile, and comment out the above, if using the legacy cbapi !!!#
#cb = CbDefenseAPI(profile=y['creds']['cb']['cb_profile'])

# SN user and password
user = y['creds']['sn']['sn_user']
pwd = y['creds']['sn']['sn_pwd']

###### Variables ######

# SN inbound webservice api url
sn_url = y['creds']['sn']['sn_url']

# Set proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"}


###### Primary Function ######

def main():


    # Get alerts from the PSC via cbapi notification listener
    while True:


        for notification in cb.notification_listener():

            # Write alert output to file for parsing
            with open('alert.json', 'w+') as a1:
                notify = (json.dumps(notification, indent=4, sort_keys=True))
                a1.write('')
                a1.write(notify)
                print (notify)
                a1.close()


            # Parse alert output for sn app
            with open('alert.json') as a:
                data = json.load(a)

                # Determine if it is a CbD Alert if 'threatInfo' in alert
                if 'threatInfo' in data:

                    ### Compile info for SN Ticket ###

                    # Investigate URL
                    cb_url = data['url']

                    # Device Info
                    device = data['deviceInfo']['deviceName']
                    device_id = data['deviceInfo']['deviceId']
                    device_ex_ip = data['deviceInfo']['externalIpAddress']
                    device_in_ip = data['deviceInfo']['internalIpAddress']
                    device_policy = data['deviceInfo']['groupName']
                    device_user = data['deviceInfo']['email']
                    device_type = data['deviceInfo']['deviceType']


                    # App Info of Primary Actor in Alert
                    actor_hash = data['threatInfo']['threatCause']['actor']
                    actor_name = data['threatInfo']['threatCause']['actorName']
                    actor_rep = data['threatInfo']['threatCause']['reputation']

                    # Compile url for vt lookup
                    vt_url = 'https://www.virustotal.com/en/file/{}/analysis/'.format(actor_hash)

                    # Compile URL for Go Live
                    lr_url_base = 'https://defense-prod05.conferdeploy.net/live-response/{}'.format(device_id)

                    # Alert data
                    description = data['threatInfo']['summary']
                    email = "noreply@carbonblack.com"
                    incident_id = data['threatInfo']['incidentId']
                    ttps = []
                    for x in data['threatInfo']['indicators']:
                        if x['indicatorName'] not in ttps:
                            ttps.append(x['indicatorName'])

                    # Compile Incident Score based on Alert Severity - add in SN notation for low, med, high
                    incident_score = []
                    score = data['threatInfo']['score']

                    if score > 0:
                        if score <= 3:
                            incident_score.append(str(score) + ' - Low')

                    if score > 3:
                        if score <= 5:
                            incident_score.append(str(score) + ' - Medium')

                    if score > 5:
                        if score <=8:
                            incident_score.append(str(score) + ' - High')

                    if score > 8:
                        incident_score.append(str(score) + ' - Critical')

                    # Populate body of ticket with data from CB alert
                    body = {
                        "u_alert_type":"CB Analytics",
                        "u_app_hash":actor_hash,
                        "u_app_name":actor_name,
                        "u_app_reputation":actor_rep,
                        "u_caller":email,
                        "u_category":"SecOps",
                        "u_cbc_incident_id":incident_id,
                        "u_cbc_policy":device_policy,
                        "u_cbc_report_name":"N/A",
                        "u_cbc_url":cb_url,
                        "u_cbc_watchlist":"N/A",
                        "u_device_id":device_id,
                        "u_device_name":device,
                        "u_device_os":device_type,
                        "u_external_ip":device_ex_ip,
                        "u_internal_ip":device_in_ip,
                        "u_severity":incident_score[0],
                        "u_short_description":description,
                        "u_ttps":ttps,
                        "u_user":device_user,
                        "u_virus_total_lookup":vt_url,
                        "u_live_response":lr_url_base,
                        "u_description": "Please see the below Carbon Black Cloud for additional details, as well as the ability to pivot directly to the console"
                    }


                    # Send Ticket via Rest API to ServiceNow Instance
                    response = requests.post(sn_url, auth=(user, pwd), headers=headers ,json=body)

                    # Check for HTTP codes other than 200
                    if response.status_code != 200:
                        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())

                    # Clear TTP & Incident score dict, so that app can keep running without restart
                    incident_score.clear()
                    ttps.clear()


                else:

                    ### Compile info for SN ticket ###

                    # This section is for handling EEDR (or Threathunter [TH]) Alerts
                    TH_url = data['url']

                    # Device Info
                    device = data['deviceInfo']['deviceName']
                    device_id = data['deviceInfo']['deviceId']
                    device_ex_ip = data['deviceInfo']['externalIpAddress']
                    device_in_ip = data['deviceInfo']['internalIpAddress']
                    device_policy = data['deviceInfo']['groupName']
                    device_user = data['deviceInfo']['email']
                    device_type = data['deviceInfo']['deviceType']

                    # App Info of Primary Actor in Alert
                    actor_hash = data['threatHunterInfo']['threatCause']['actor']
                    actor_name = data['threatHunterInfo']['threatCause']['actorName']
                    actor_rep = data['threatHunterInfo']['threatCause']['reputation']


                    # TH specific alert data
                    TH_score = data['threatHunterInfo']['score']
                    TH_report = data['threatHunterInfo']['reportName']
                    TH_watchlist = data['threatHunterInfo']['watchLists'][0]['name']

                    # Compile url for vt lookup
                    vt_url = 'https://www.virustotal.com/en/file/{}/analysis/'.format(actor_hash)

                    # Compile URL for Go Live
                    lr_url_base = 'https://defense-prod05.conferdeploy.net/live-response/{}'.format(device_id)

                    # Alert data
                    TH_description =  data['threatHunterInfo']['threatCause']['reason']
                    email = "noreply@carbonblack.com"
                    incident_id = data['threatHunterInfo']['incidentId']

                    # Compile Incident Score based on Alert Severity - add in SN notation for low, med, high

                    incident_score = []

                    if TH_score > 0:
                        if TH_score <= 3:
                            incident_score.append(str(TH_score) + ' - Low')

                    if TH_score > 3:
                        if TH_score <= 5:
                            incident_score.append(str(TH_score) + ' - Medium')

                    if TH_score > 5:
                        if TH_score <=8:
                            incident_score.append(str(TH_score) + ' - High')

                    if TH_score > 8:
                        incident_score.append(str(TH_score) + ' - Critical')


                    # Populate body of ticket with data from CB alert
                    body = {
                        "u_alert_type":"Watchlists",
                        "u_app_hash":actor_hash,
                        "u_app_name":actor_name,
                        "u_app_reputation":actor_rep,
                        "u_caller":email,
                        "u_category":"SecOps",
                        "u_cbc_incident_id":incident_id,
                        "u_cbc_policy":device_policy,
                        "u_cbc_report_name":TH_report,
                        "u_cbc_url":TH_url,
                        "u_cbc_watchlist":TH_watchlist,
                        "u_device_id":device_id,
                        "u_device_name":device,
                        "u_device_os":device_type,
                        "u_external_ip":device_ex_ip,
                        "u_internal_ip":device_in_ip,
                        "u_severity":incident_score[0],
                        "u_short_description":TH_description,
                        "u_ttps":"N/A",
                        "u_user":device_user,
                        "u_virus_total_lookup":vt_url,
                        "u_live_response":lr_url_base,
                        "u_description": "Please see the below Carbon Black Cloud for additional details, as well as the ability to pivot directly to the console"
                    }


                    # Send Ticket via Rest API to ServiceNow Instance
                    response = requests.post(sn_url, auth=(user, pwd), headers=headers ,json=body)

                    # Check for HTTP codes other than 200
                    if response.status_code != 200:
                        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())

                    # Clear Incident score dict, so that app can keep running without restart
                    incident_score.clear()

# Run App
if __name__ == "__main__":
    main()




