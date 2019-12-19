import schedule
import time
import datetime
import os
import stat
from subprocess import run
from OpenSSL import crypto, SSL
import random
#from time import gmtime, mktime

eg_certs = "/etc/letsencrypt/live/aiotes/"
cert_files = ['privkey.pem', 'cert.pem', 'chain.pem']
self-signed-flag = "self-signed"

def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)

def create_self_signed_cert():
    CA_FILE = eg_certs+cert_files[2]
    CERT_FILE = eg_certs+cert_files[1]
    KEY_FILE = eg_certs+cert_files[0]
    # create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)

    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().O = "AIOTES Instance"
    cert.get_subject().CN = os.getenv('AIOTES_HOSTNAME','localhost')
    cert.set_serial_number(random.randint(1001,2147483647))
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha256')
    touch(eg_certs+self-signed-flag)
    f=open(CERT_FILE, "wb")
    f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    f.close()
    f=open(KEY_FILE, "wb")
    f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
    f.close()
    f=open(CA_FILE, "wb")
    f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    f.close()
    

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
        "--email" , os.getenv('AIOTES_SYSADMIN_EMAIL','a@a.a'),
        "-d", os.getenv('AIOTES_HOSTNAME','localhost')]))
    check_certs_create_eoc()
    for root, dirs, files in os.walk("/etc/letsencrypt/"):
        for momo in dirs:
            os.chmod(os.path.join(root, momo), stat.S_IRWXU | stat.S_IRWXG | stat.S_IXOTH )
    for file in cert_files:
        try:
            os.chmod(eg_certs + file, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH )
        except:
            print( "problems with file ", file)
    #print (run(["ls", "-lhaR", "/etc/letsencrypt/"]))


    
print(datetime.datetime.now()," Initialising Certbot pySchedule")
certonly()
schedule.every().monday.do(certonly)

while True:
    schedule.run_pending()
    time.sleep(1)
