import schedule
import time
import datetime
import os
import stat
from os import environ as env
from subprocess import run
from OpenSSL import crypto, SSL
#from time import gmtime, mktime

eg_certs = "/etc/letsencrypt/live/aiotes/"
cert_files = ['privkey.pem', 'cert.pem', 'chain.pem']

def create_self_signed_cert():
    CERT_FILE = eg_certs+cert_files[1]
    KEY_FILE = eg_certs+cert_files[0]
    # create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 1024)

    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().O = "AIOTES Instance"
    cert.get_subject().CN = "localhost"
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha1')

    open(CERT_FILE, "wt").write(
        crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    open(KEY_FILE, "wt").write(
        crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

def check_certs_create_eoc():
    print(datetime.datetime.now()," checking certs")
    if (not (os.path.isdir(eg_certs) & os.path.isfile(eg_certs+cert_files[0]))):
        print (datetime.datetime.now()," creating self-signed certificates")
        os.makedirs(eg_certs, mode=0o777, exist_ok=True)
        create_self_signed_cert()

def certonly():
    print (datetime.datetime.now()," Configuring or renewing certificate")
    print (run(["certbot", "certonly","-n", "--standalone",
        "--cert-name", "aiotes", 
        "--keep-until-expiring","--renew-with-new-domains","--agree-tos",
        "--email" , env.get('AIOTES_SYSADMIN_EMAIL'),
        "-d", env.get('AIOTES_HOSTNAME')]))
    check_certs_create_eoc()
    for root, dirs, files in os.walk("/etc/letsencrypt/"):
        for momo in dirs:
            os.chmod(os.path.join(root, momo), stat.S_IRWXU | stat.S_IRWXG | stat.S_IXOTH )
    for file in cert_files:
        os.chmod(eg_certs + file, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH )
    #print (run(["ls", "-lhaR", "/etc/letsencrypt/"]))


    
print(datetime.datetime.now()," Initialising Certbot pySchedule")
certonly()
schedule.every().monday.do(certonly)

while True:
    schedule.run_pending()
    time.sleep(1)
