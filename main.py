from smtplib import SMTP_SSL
import json

# TODO refactor into nice functions :)
with open("config.json", 'r') as f:
    config = json.load(f)

password = config["password"]
from_addr = config["from"]
to_addrs = config["to"]
is_test = config["isTest"]
subject = config["subject"]
msg = config["body"]
smtp_server = config["smtpServer"]
reminder_interval = config["reminderInterval"]  # TODO implement logic
mileage_due = config["mileageDue"]
date_due = config["dateDue"]
current_mileage = config["currentMileage"]

days_left = 0 # TODO implement logic

if is_test.lower() == "true":
    print("TEST VERSION")
    to_addrs = from_addr

lines = [f"From: {from_addr}", f"To: {', '.join(to_addrs)}", ""]

# TODO make recurring every day (or add to log file)
print(f"Sending message:\n{msg}\n Days until sending: {days_left}.\n\n")

server = SMTP_SSL(smtp_server)
server.login(from_addr, password)
server.set_debuglevel(1)
server.sendmail(from_addr, to_addrs, msg)
server.quit()