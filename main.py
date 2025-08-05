from smtplib import SMTP_SSL
import json
from datetime import date, datetime,timedelta
from time import sleep
import os.path

date_format = "%m/%d/%Y"

# log file 
# TODO

# TODO need to rewrite the 

def readConfigFile():
    # config file
    with open("config.json", 'r') as f:
        config = json.load(f)
        
    # globals 
    global password
    global from_addr
    global to_addrs
    global is_test
    global subject
    global msg
    global smtp_server
    global reminder_interval
    global mileage_due
    global date_due
    global current_mileage
    global last_sent_path
    global today

    ### begin json parsing and adding to globals
    password = config["password"]
    from_addr = config["from"]
    to_addrs = config["to"]
    is_test = config["isTest"]
    subject = config["subject"]
    smtp_server = config["smtpServer"]
    reminder_interval = config["reminderIntervalDays"]
    mileage_due = config["mileageDue"]
    date_due = datetime.strptime(config["dateDue"], date_format).date()
    msg = f"Hello,\n\nYour next service is scheduled when your vehicle has {mileage_due} miles, or before {date_due}. Schedule a service appointment 1 month prior.\n\n--Rob"
    current_mileage = config["currentMileage"]
    last_sent_path = config["lastSentPath"]
    today = date.today()
    ### end

    f.close()

def connectToServer():
    server = SMTP_SSL(smtp_server)
    server.login(from_addr, password)
    server.set_debuglevel(1)

    return server



def main():
    readConfigFile()
    while today < date_due:
        print("waking up...")

        if is_test:
            print("TEST VERSION")
            to_addrs = from_addr
        # if last_sent file is still there, read from the file. if not, create and send the email again today
        if not os.path.isfile(last_sent_path):
            createLastSentFile(today)
        
        # get last sent date
        with open(last_sent_path, 'r') as read_file:
            last_sent_on = datetime.strptime(read_file.readlines()[-1].split(" ")[-1].strip(), "%Y-%m-%d").date()
        
        day_before_next_email_date =  last_sent_on + timedelta(days=reminder_interval - 1) # last sent + reminder_interval - 1 < today
        
        # need to send
        if day_before_next_email_date < today:
            # send sequence
            print("sending")
            server = connectToServer()
            complete_message = 'Subject: {}\n\n{}'.format(subject, msg)
            server.sendmail(from_addr, to_addrs, complete_message)
            server.quit()
            createLastSentFile(today)
            readConfigFile()
        
        # everything sent as normal, go sleep until the next reminder interval
        else:
            days_to_sec = reminder_interval * 86400
            sleep(days_to_sec)



def createLastSentFile(today):
    # keeps track of the last sent email
    with open(last_sent_path, 'w') as file:
        file.write(f"Last sent: {today}\n")

main()