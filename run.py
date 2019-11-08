import schedule
import time
from os import environ as env
from subprocess import run

def certonly():
    print("Configuring or renewing certificate")
    print run(["certbot", "certonly","-n", "--standalone", "--cert-name", "aiotes", "--keep-until-expiring","--renew-with-new-domains","--agree-tos" "-d", env.get('AIOTES_HOSTNAME')])

certonly()
schedule.every().monday.do(certonly)

while True:
    schedule.run_pending()
    time.sleep(1)