#  INITIAL PI CONFIG FOR WIFI SENSOR

# SET STATIC IP ADDRESS ON PI
# (THIS IS ALREADY DONE ON DISK IMAGE)
cat <<'HEREDOC' >> /etc/dchpcd.conf
interface eth0
static ip_address=192.168.0.10/24
static routers=192.168.0.1
static domain_name_servers=192.168.0.1
HEREDOC

# CONNECT TO PI VIA SSH
To connect, just run: ssh pi@172.16.181.45
Press enter to skip phassphrase (if prompted), and then enter the login password: raspberry.
 
#  VERIFY DATETIME IS CORRECT
date

#  FOR EXAMPLE HOW TO SET THE CURRENT TIME
sudo date +%T -s "13:14:00"

# LIST PHYSICAL WIFI DEVICES AND ASSOCIATED INTERFACES
# Look for device id (phy0 or phy1 or ph2) that supports monitor mode
iw phy | less
# or try
iw dev

# ADD MONITOR INTERFACE "mon1" TO PHYSICAL DEVICE THAT SUPPORT MONITOR MODE (.E.G phy0)
# Monitor will be name of interface that monitors traffic w/ tshark
sudo iw phy1 interface add mon1 type monitor  

#  BRING MONITOR INTERFACE UP
sudo ip link set dev mon1 up

# USE TSHARK TO SCAN THE MONITOR INTERFACE FOR MAC ADDRESSES
# prints output to terminal
sudo tshark \
-i mon1 \
-I -l -f broadcast \
-Y wlan.fc.subtype==4 \
-T fields \
-e wlan.sa

# SEND SCANNED MAC ADDRESSES TO FILE
sudo tshark \
-i mon2 \
-I -l -f broadcast \
-Y wlan.fc.subtype==4 \
-T fields \
-e wlan.sa \
-e fn/var/tshark/data.log 2>/var/tshark/data.err &

# Add process ID (PID) of last run command to a file
echo $! > /var/tshark/tshark.pid

#  VIEW RUNNING TSHARK PROCESSES
ps aux | grep tshark

#  STOP TSHARK COLLECTION BY PID
sudo kill [PID]

# SYNC TIME BETWEEN TWO COMPUTERS OVER SSH
date --set="$(ssh user@server date)"

###  HELPFUL COMMANDS TO ANALYZE MAC ADDRESS DATA ###
#  GET CURRENT LENGTH OF DATA.LOG
wc -l /var/tshark/data.log

#  GET COUNT OF UNIQUE MAC ADDRESSES IN DATA FILE
#  https://stackoverflow.com/questions/2781491/counting-unique-values-in-a-column-with-a-shell-script
cut -f1 /var/tshark/data.log | sort | uniq | wc -l

# GET COMMON MAC ADDRESSES BETWEEN TWO LOG FILES
comm -12 <(cut -f1 /var/tshark/benwhite.csv | sort -u) <(cut -f1 /var/tshark/oltorf.csv | sort -u) | wc -l

#  COPY LOG DATA FROM PI TO CLIENT
#  run from local machine
scp pi@172.16.181.45:/var/tshark/data.log ./oltorf.log


# From TIANXIN LI
# iw dev without the wifi adaptor information, need to install driver for wifi adap.
# get the mode of wifi adap (e.g., 8192EU)
# get kernel version by command uname -a (e.g., Linux rasp 4.14.56-v7+ #1128 SMP ...)
# google search 8192eu-driver raspberry pi

# Download the driver by command
wget url
# create a dir to save the download file
mkdir d
mv downloadFile d
# unzip
tar -xzf downloadFile
# install driver
./install.sh

# use iw dev check the wifi adap
