#!/bin/bash

if [ "$1" == alpha ]; then
    ssh root@10.38.95.50 reboot
elif [ "$1" == beta ]; then
    ssh root@10.38.95.51 reboot
else
    echo "No input bitch"
fi
