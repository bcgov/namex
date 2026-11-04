#!/bin/bash
max_attempts=3
wait_time=15
url=https://bcgov.github.io/sso-requests-sandbox
code=301
if [ $(curl --output /dev/null --silent --head -X GET --retry ${max_attempts} --fail --retry-all-errors --retry-delay ${wait_time} --retry-max-time 240 -w "%{response_code}\n" ${url}) -eq ${code} ]; then
	echo "Connection Success!"
else
	echo "Failed Connection!"
        exit 1
fi
