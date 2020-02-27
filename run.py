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
self_signed_flag = "self-signed"
self_signed_backup = "bkp"

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
    touch(eg_certs+self_signed_flag)
    f=open(CERT_FILE, "wb")
    f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    f.close()
    f=open(KEY_FILE, "wb")
    f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
    f.close()
    f=open(CA_FILE, "wb")
    f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    f.close()

def backup_dir(src,bkp):
    print (datetime.datetime.now()," Backing up " + src + " to " + bkp)
    os.makedirs(bkp, mode=0o700, exist_ok=True)
    for root, dirs, files in os.walk(src):
        for name in files:
            os.replace(os.path.join(root, name),os.path.join(bkp, name))
            
def recover_dir(src,bkp):
    print (datetime.datetime.now()," Recover from " + bkp + " to " + src)
    for root, dirs, files in os.walk(bkp):
        for name in files:
            os.replace(os.path.join(root, name),os.path.join(src, name))
    os.rmdir(bkp)

def remove_dir(trg):
    for root, dirs, files in os.walk(trg):
        for name in files:
            print(datetime.datetime.now()," removing " + os.path.join(root, name))
            os.remove(os.path.join(root, name))
    print(datetime.datetime.now()," removing dir " + os.path.join(root, name))
    os.rmdir(trg)
    
def check_certs_create_eoc():
    print(datetime.datetime.now()," checking certs")
    if (not (os.path.isdir(eg_certs) & os.path.isfile(eg_certs+cert_files[0]))):
        #if certbot not successful
        if (os.path.isdir(eg_certs+self_signed_backup)):
            #if the backup exist, then recover it
            recover_dir(eg_certs,eg_certs+self_signed_backup)
        else:
            #else create self-signed certificate
            print (datetime.datetime.now()," creating self-signed certificates")
            print ("WARNING: Using self-signed certificates, this may not be secure nor stable")
            os.makedirs(eg_certs, mode=0o700, exist_ok=True)
            create_self_signed_cert()
    elif (os.path.isdir(eg_certs+self_signed_backup)):
        # dir and cert exist (certbot was successful after ssc where backedup) if there is a backup it needs to be removed
        print (datetime.datetime.now()," removing backup of self-signed certificate, no longer needed.")
        remove_dir(eg_certs+self_signed_backup)

def certonly():
    #if the current certificate is self-signed, then back it up before retrying letsencrypt
    if (os.path.isfile(eg_certs+self_signed_flag)):
        backup_dir(eg_certs,eg_certs+self_signed_backup)
    #create or renew certificates with certbot
    print (datetime.datetime.now()," Configuring or renewing certificate")
    print (run(["certbot", "certonly","-n", "--standalone",
        "--cert-name", "aiotes",
        "--keep-until-expiring","--renew-with-new-domains","--agree-tos",
        "--email" , os.getenv('AIOTES_SYSADMIN_EMAIL','a@a.a'),
        "-d", os.getenv('AIOTES_HOSTNAME','localhost')]))
    check_certs_create_eoc()
    #Change access to all dirs
    for root, dirs, files in os.walk("/etc/letsencrypt/"):
        for momo in dirs:
            os.chmod(os.path.join(root, momo), stat.S_IRWXU | stat.S_IRWXG | stat.S_IXOTH )
    #Change acces to certs
    for file in cert_files:
        try:
            os.chmod(eg_certs + file, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH )
        except:
            print(datetime.datetime.now(), "problems with file ", file)
    #print (run(["ls", "-lhaR", "/etc/letsencrypt/"]))


if __name__ == "__main__":
    print(datetime.datetime.now()," Initialising Certbot pySchedule")
    certonly()
    schedule.every().monday.do(certonly)
    while True:
        schedule.run_pending()
        time.sleep(1)
