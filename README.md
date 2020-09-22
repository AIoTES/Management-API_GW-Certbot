# AIoTES Certbot Certificate Manager

A certbot client for Express Gateway automatically managing certificates with Letsencrypt.

## Getting stated / Use
Certbot is automatically bundled with AIoTES core components since V2.0 onwards.

Certbot will attempt to manage certificates in the following order of preference
1. certificates provided by the user
2. certificates generated through letsencrypt service
3. self signed certificates

This will ensure Express gateway communications are always encrypted, and (in cases 1 and 2) using valid acceptable certificates.

## How to build, install, or deploy it
build the docker image
```
docker build -t certbot .
```

Run it with:
1. port 80 accessible from the public internet (for letsencrypt challenge, see below for details)
2. `AIOTES_HOSTNAME` environment variable with the fully qualified domain name (FQDN) of your server
3. `AIOTES_SYSADMIN_EMAIL` with your email, required for letsencrypt service. Only notifications on missed renewals are sent.
4. volume at `/etc/letsencrypt` which should be share with the volume at `/var/lib/certs/` of express gateway. 

Certbot assumes the following configuration in Express Gateway (_gateway.config.yml_):

```
  tls: 
    "default": 
      key: /var/lib/certs/live/aiotes/privkey.pem
      cert: /var/lib/certs/live/aiotes/cert.pem
      ca:
        - /var/lib/certs/live/aiotes/chain.pem
```

## Testing
There are 2 unit testing procedures, one in python (_test.py_) and another for bash shell (_test.sh_).

Once the container is running the certificate management process can be monitored through logs.

## Further Information

### using provided certificates
When you own certificates signed by a trusted CA, that is because you either paid for them, or your entity provides a CA who issues certificates for your servers, you need to put these certificates for the AIOTES instance to use. Ensure the certificates used are addressed to the correct DNS address AIOTES Will be using (set up as AIOTES_HOSTNAME variable).
The certificates are injected into a running instance through these commands:

```
docker cp <path-to-privatekey-file> <certbot-container-name>:/etc/letsencrypt/live/aiotes/privkey.pem
docker cp <path-to-certificate-file> <certbot-container-name>:/etc/letsencrypt/live/aiotes/cert.pem
docker cp <path-to-CA-chain-file> <certbot-container-name>:/etc/letsencrypt/live/aiotes/chain.pem
```

<certbot-container-name> can be determined by using Portainer, and locating the certbot service; or you may use the id resulting from running:
```
docker service ps express-gateway_certbot
```

The exact name of the certbot container is different in each deployment. To obtain the name, go to “Containers” and look for any running container of the image docker-activage.satrd.es/certbot.

To apply the changes, update the express-gw service (go to “stacks”, select the API stack, then select express-gw service and click “update”).

### Using Letsencryipt service
To ensure that correctly signed certificates are used the letsencrypt service is used to issue trusted certificates. The default challenge to get the certificates is the HTTP-01 challenge, Which means there are a couple of prerequisites on the network to ensure it works correctly:

* Your DNS server (or DNS provider) should have a DNS entry pointing to your server. This DNS will later be assigned to variable AIOTES_HOSTNAME.
* Your network and firewalls should allow port 80(http) to be reached on your server from outside (specifically from the letsencrypt server).
* Port 80  will be exposed by the AIOTES deployment by default, however you can reverse proxy the “.well-known/” http path to the AIOTES deployment if you have any other web server running on the server.
* Although not necessary, it is highly recommended that your DNS (or DNS provider) has a CAA entry set up to allow letsencrypt issuance of certificates.

Letsencrypt issues trusted certificates with 90 days expirancy, they need your email to contact you when the certificate is about to expire (set as AIOTES_SYSADMIN_EMAIL global variable). AIoTES will automatically attempt renewal every monday, and renew the certificate if there are less than 30 days to expirancy.

If letsencrypt service fails to provide trusted certificates, AIoTES will resort to self-signed certificates, and although this is a secure way to ensure communications are encrypted, many clients will reject the connection due to certificates not being signed by a trusted Certificate Authority (CA). Check the logs of the certbot container for more details. If a trusted certificate cannot be generated automatically, it is recommended to try to obtain a trusted certificate by other means and install it manually (see the “Using your own certificates” section).

## Contributing
Pull requests are always appreciated.
## Credits
This template is been created by:
Alejandro Medrano <amedrano@lst.tfo.upm.es>
## License
```
Copyright 2020 Universidad Politécnica de Madrid

Licensed under the Apache License, Version 2.0 (the "License"); 
you may not use this file except in compliance with the License. 
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
See the License for the specific language governing permissions and 
limitations under the License.
```
