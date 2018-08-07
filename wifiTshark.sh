#!/bin/bash
sudo ifconfig wlan1 down
sudo iwconfig wlan1 mode monitor
sudo ifconfig wlan1 up

sudo tshark -a duration:60 -i wlan1 -l -f broadcast -Y wlan.fc.subtype==4 -T fields -e wlan.sa -e frame.time_epoch > "pi$(date +"%Y%m%d%I%M").txt"
