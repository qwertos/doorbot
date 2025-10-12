#!/bin/bash
RESOURCE=frontdoor
AUTHHOST=auth.makeitlabs.com
URL=https://${AUTHHOST}/authit/api/v1/resources/${RESOURCE}/acl
PWFILE=/home/pi/doorbot/databases/curlpw
OUTFILE=/home/pi/doorbot/databases/rfid/acl.json

outdir="$(dirname $OUTFILE)"
if [[ ! -d "$outdir" ]] ; then
	mkdir -p "$outdir"
fi

curl --silent --fail --output ${OUTFILE} --netrc-file ${PWFILE} ${URL}

