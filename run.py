import schedule
import time
import datetime
import os
import stat
from os import environ as env
from subprocess import run

def certonly():
    print (datetime.datetime.now()," Configuring or renewing certificate")
    print (run(["certbot", "certonly","-n", "--standalone", "--cert-name", "aiotes", "--keep-until-expiring","--renew-with-new-domains","--agree-tos","--email" , env.get('AIOTES_SYSADMIN_EMAIL'), "-d", env.get('AIOTES_HOSTNAME')]))
    for root, dirs, files in os.walk("/etc/letsencrypt/"):
        for momo in dirs:
            os.chmod(os.path.join(root, momo), stat.S_IRWXU | stat.S_IRWXG | stat.S_IXOTH )
    path = "/etc/letsencrypt/live/aiotes/"
    files = ['privkey.pem', 'cert.pem', 'chain.pem']
    for file in files:
        os.chmod(path + file, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH )
    print (run(["ls", "-lhaR", "/etc/letsencrypt/"]))

print (datetime.datetime.now()," Initialising Certbot pySchedule")
certonly()
schedule.every().monday.do(certonly)

while True:
    schedule.run_pending()
    time.sleep(1)
