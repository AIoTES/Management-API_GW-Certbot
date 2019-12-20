#check if certificates are self-signed
FILE=./self-signed
if [ -f "$FILE" ]; then
    echo "self-signed certificate detected"
	export NODE_EXTRA_CA_CERT=/var/lib/certs/live/aiotes/cert.pem
	echo "NODE_EXTRA_CA_CERT="$(printenv NODE_EXTRA_CA_CERT)
fi
#mkdir $FILE
touch $FILE
#check if certificates are self-signed
if [ -f "$FILE" ]; then
    echo "self-signed certificate detected"
	export NODE_EXTRA_CA_CERT=/var/lib/certs/live/aiotes/cert.pem
	echo "NODE_EXTRA_CA_CERT="$(printenv NODE_EXTRA_CA_CERT)
fi
