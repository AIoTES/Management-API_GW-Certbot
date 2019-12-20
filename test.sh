#check if certificates are self-signed
if [ -f "/var/lib/certs/live/aiotes/self-signed" ]; then
    echo "self-signed certificate detected"
	export NODE_EXTRA_CA_CERT=/var/lib/certs/live/aiotes/cert.pem
	echo "NODE_EXTRA_CA_CERT="$(printenv NODE_EXTRA_CA_CERT)
fi
mkdirs /var/lib/certs/live/aiotes/
touch /var/lib/certs/live/aiotes/self-signed
#check if certificates are self-signed
if [ -f "/var/lib/certs/live/aiotes/self-signed" ]; then
    echo "self-signed certificate detected"
	export NODE_EXTRA_CA_CERT=/var/lib/certs/live/aiotes/cert.pem
	echo "NODE_EXTRA_CA_CERT="$(printenv NODE_EXTRA_CA_CERT)
fi