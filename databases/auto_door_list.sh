#!/bin/bash

. config

outdir="$(dirname $OUTFILE)"
if [[ ! -d "$outdir" ]] ; then
	mkdir -p "$outdir"
fi

curl --silent --fail --output ${OUTFILE} --netrc-file ${PWFILE} ${URL}

