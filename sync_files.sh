#!/bin/bash

###############################################################################
## SYNC FILES
###############################################################################
#
# Synchronize files through SSH using rsync.
#

USER="pi"
DESTINATION_DIR="~/Documents"

PI_MAC_ADDRESS="b8:27:eb:3b:35:0" # eth0
# PI_MAC_ADDRESS="b8:27:eb:6e:60:55" # wlan0
IP_FIND_COMMAND="arp -na | grep -i $PI_MAC_ADDRESS"
IP_ADDRESS="192.168.1.61"
# IP_ADDRESS=$(eval $IP_FIND_COMMAND | grep -Eo '[0-9.]{7,15}')

CONNECTION_STRING="$USER@$IP_ADDRESS:$DESTINATION_DIR"

printf "Attempting connection to %s...\n" $PI_MAC_ADDRESS

# if ssh -qTn -o ConnectTimeout=2 $CONNECTION_STRING; [ $? -eq 255 ]
# then
#     echo "Connection failed. Exiting."
#     exit 1
# fi

# -u, --update skip files that are newer on the receiver
# -r, --recursive recurse into directories
# -l, --links copy symlinks as symlinks
# -t, --times preserve modification times
# -v, --verbose increase verbosity
# --delete delete extraneous files from dest dirs, acts as --delete-during
# lastly, -e is the option that allows you to specify your remote shell, in this case ssh
function dir_sync () {
    rsync -urltv --delete --exclude "transfer.sh" -e ssh $PWD $CONNECTION_STRING
}

# dir_sync
dir_sync; fswatch -o . | while read f; do dir_sync; done

echo "TASK FINISHED."
