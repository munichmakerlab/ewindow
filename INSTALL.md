* Grab and extract Tarballs for Janus and PeerVPN
* Install uv4l/asoundrc to /etc
* Disable uv4l_raspicam and uv4l_uvc in systemd
* Configure PeerVPN IPs and stuff

=== SETUP LOG / PRE-BOOT

Write 2016-05-27-raspbian-jessie-lite.img to SD card

Edit /etc/hostname to ewindow-*
Also Change local hostname in /etc/hosts

Add Local network to /etc/wpa_supplicant/wpa_supplicant.conf

=== POST-BOOT

ssh pi@ewindow-X.local

sudo apt-get update
sudo apt-get install git daemontools-run python-requests

git clone https://github.com/munichmakerlab/ewindow

cp -r ewindow/service/* /etc/service/
chown -R pi:pi /etc/service/uv4l /etc/service/janus # Hand to user, so he can control these services

=== UV4L Installtion, Taken from http://linux-projects.org/uv4l/installation

curl http://www.linux-projects.org/listing/uv4l_repo/lrkey.asc | sudo apt-key add -

cat >> /etc/apt/sources.list << EOF
deb http://www.linux-projects.org/listing/uv4l_repo/raspbian/ jessie main
EOF

apt-get update
apt-get install uv4l-uvc uv4l-webrtc

sudo systemctl disable uv4l_raspicam uv4l_uvc@ # Disable auto-start
# TODO: This does not seem to work, find out how to stop that shit

=== Setup Janus

sudo apt-get install libnice10 libsofia-sip-ua0 libmicrohttpd10 libjansson4 libsrtp0

Copy janus-build*.tar.xz from buildserver # TODO: Setup buildserver
Or use ewindow/janus/build.sh
sudo tar xJvf janus=build*.tar.xz  -C /

=== Setup Peervpn


git clone https://github.com/peervpn/peervpn
cd peervpn
sudo apt-get install libssl-dev
make
cp peervpn /etc/service/peervpn/

# Edit /etc/service/peervpn/peervpn-client.conf
# Enter PSK, Edit IP
