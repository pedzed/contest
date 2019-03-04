#!/bin/bash

###############################################################################
## SSH CONNECT
###############################################################################
#
# Automatically find the Raspberry Pi address and connect through SSH.
#

function cls() {
    printf "\033c"
}

cls

nmap -sP 192.168.1.0/24
echo ""

echo "Finding possible IP addresses..."

USER="pi"

IP_FIND_COMMAND="arp -na | grep -i b8:27:eb" # Pi's have these MAC segments in common
# IP_FIND_COMMAND="arp -na"
IP_FIND_OUTPUT=$(eval $IP_FIND_COMMAND | grep -Eo '[0-9.]{7,15}')
IP_ADDRESSES=($IP_FIND_OUTPUT)

if [ -z "$IP_FIND_OUTPUT" ]
then
    echo "No IP found. Aborting."
    exit 1
fi

printf "IP Address found: %s\n" "${IP_ADDRESSES[@]}"
printf "\n"

connectionString=""

while read -r ipAddress; do
    echo "Attempting IP: $ipAddress"
    echo "Connecting through SSH..."

    connectionString="${USER}@${ipAddress}"

    if ssh -qTn -o ConnectTimeout=2 $connectionString "echo ''"; [ $? -eq 255 ]
    then
        echo "Connection failed."
        echo ""
    else
        break
    fi
done <<< "$IP_FIND_OUTPUT"

ssh -q $connectionString
