import sys
import os
from run import touch
from run import create_self_signed_cert
from run import backup_dir
from run import recover_dir
from run import remove_dir
from run import check_certs_create_eoc
from run import certonly

eg_certs = "/etc/letsencrypt/live/aiotes/"
backup = "bkp"

#test touch
test_touch="test"
exist_before=os.path.isfile(test_touch)
touch(test_touch)
exist_after=os.path.isfile(test_touch)
touch(test_touch)
if (exist_before or not exist_after):
    sys.exit(-1)

#test create_self_signed_cert
check_certs_create_eoc()
#This should run in the case there is nothing, and generate self signed certificates
if (not os.path.isfile(eg_certs+'privkey.pem') and 
    not os.path.isfile(eg_certs+'cert.pem') and 
    not os.path.isfile(eg_certs+'chain.pem') and 
    not os.path.isfile(eg_certs+'self-signed') ):
    sys.exit(-1)
#TODO: check cert and chain are the same

#test bakcup
backup_dir(eg_certs,eg_certs+backup)
if (os.path.isfile(eg_certs+'privkey.pem') and 
    os.path.isfile(eg_certs+'cert.pem') and 
    os.path.isfile(eg_certs+'chain.pem') and 
    os.path.isfile(eg_certs+'self-signed') and
    not os.path.isdir(eg_certs+bkp)):
    sys.exit(-1)

recover_dir(eg_certs,eg_certs+backup)
if (not os.path.isfile(eg_certs+'privkey.pem') and 
    not os.path.isfile(eg_certs+'cert.pem') and 
    not os.path.isfile(eg_certs+'chain.pem') and 
    not os.path.isfile(eg_certs+'self-signed') and
    os.path.isdir(eg_certs+backup)):
    sys.exit(-1)

backup_dir(eg_certs,eg_certs+backup)
remove_dir(eg_certs+backup)
if (os.path.isfile(eg_certs+'privkey.pem') and 
    os.path.isfile(eg_certs+'cert.pem') and 
    os.path.isfile(eg_certs+'chain.pem') and 
    os.path.isfile(eg_certs+'self-signed') and
    os.path.isdir(eg_certs+backup)):
    sys.exit(-1)
