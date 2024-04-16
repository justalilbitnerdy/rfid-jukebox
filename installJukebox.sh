#!/bin/bash

# We need sudo for various parts of this
if [ "$(id -u)" != "0" ]; then
    echo "This script requires root privileges. Restarting with sudo..."
    sudo "$0" "$@"
    exit $?
fi

# make sure we have our dependencies
apt update
apt install python3-mutagen python3-yaml

# Get the actual software and pull in dependency modules
git clone https://github.com/justalilbitnerdy/rfid-jukebox.git /etc/jukebox
pushd /etc/jukebox
git submodule update --init --recursive

#install the software to /etc/jukebox
mv rfid-jukebox /etc/jukebox

#setup our systemd service
cp jukebox.service /etc/systemd/system/
systemctl enable jukebox
systemctl start jukebox

popd

chmod 777 /etc/jukebox

# Make sure sound works
echo "Setting up audio to use headphone port."
card_number=$(cat /proc/asound/cards | grep '\[Headpho' | awk '{print $1}')
echo "defaults.pcm.card $card_number" >> /etc/asound.conf

echo "Installation done, rebooting."
sleep 2
shutdown -r 0