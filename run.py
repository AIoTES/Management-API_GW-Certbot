import schedule
import time
import datetime
from os import environ as env
from subprocess import run

def certonly():
    print (datetime.datetime.now()," Configuring or renewing certificate")
    print (run(["certbot", "certonly","-n", "--standalone", "--cert-name", "aiotes", "--keep-until-expiring","--renew-with-new-domains","--agree-tos","--email" , env.get('AIOTES_SYSADMIN_EMAIL'), "-d", env.get('AIOTES_HOSTNAME')]))
#    print (run(["ls", "-lhaR", "/etc/letsencrypt"]))

print(datetime.datetime.now()," Initialising Certbot pySchedule")
certonly()
schedule.every().monday.do(certonly)

while True:
    schedule.run_pending()
    time.sleep(1)
