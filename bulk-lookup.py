import csv
import os
from twilio.rest import Client

## The following code takes a CSV file with each row as a phone number as input and 
## returns a CSV file with carrier data for each phone number.
filename = 'Input.CSV'

account_sid = 'TWILIO_ACCOUNT_SID'
auth_token = 'TWILIO_AUTH_TOKEN'
client = Client(account_sid, auth_token)

carrierdata =[]
with open(filename, 'r') as readfile:
    datareader = csv.reader(readfile)
    for row in datareader:
        try:
            ## This free Lookup call puts the phone number in E.164 format
            phone_number = client.lookups.v2.phone_numbers(row).fetch().phone_number
            ## This call finds carrier data for the phone number and costs $0.008 per request
            data = client.lookups \
                        .v2 \
                        .phone_numbers(phone_number) \
                        .fetch(fields='line_type_intelligence')
            print(row, data.line_type_intelligence)
            carrierdata.append([phone_number, data.line_type_intelligence])
        except:
            carrierdata.append([row, "ERROR"])
    readfile.close()

carrierResults = open('LookupResults.csv', 'w')
writer = csv.writer(carrierResults)
writer.writerows(carrierdata)

        