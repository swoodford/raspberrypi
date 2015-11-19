#!/usr/bin/env bash

# Script to build Raspbian bootable SD card from Raspbian img file


# Fail
function fail(){
	tput setaf 1; echo "Failure: $*" && tput sgr0
	exit 1
}

# clear

RASPBIAN=$(find ~/Downloads -type f -name "*raspbian*.img")

if [ -z "$RASPBIAN" ]; then
	ZIPPED=$(find ~/Downloads -type f -name "*raspbian*.zip")
	if [ -z "$ZIPPED" ]; then
		fail "Could not find any Raspbian images."
	else
		echo "List of compressed Raspbian images"
		echo "$ZIPPED"
		fail "Must uncompress image first."
	fi
else
	echo "List of Raspbian images found in Downloads:"
	echo "$RASPBIAN"
	read -rp "Use this Raspbian image? (y/n) " REPLY
	if [[ $REPLY =~ ^[Nn]$ ]]; then
		echo
		read -rp "Enter full path to Raspbian image: " REPLY
		RASPBIAN=$REPLY
	fi
fi
echo
echo "List of mounted disks:"
echo
df -lH
# ls -fl /Volumes/
echo
echo "Full path to disk for your Raspberry Pi MicroSD Card?"
echo "Example: /dev/disk5"
read DISK
read -rp "Proceed to erase and format \"$DISK\" with Raspbian image? (y/n) " REPLY
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
	echo "Unmounting" $DISK
	diskutil unmountDisk $DISK
	echo "Formatting with FAT32"
	sudo diskutil eraseDisk FAT32 RASPBERRYPI MBRFormat $DISK
	echo "Installing the Raspberry Pi image... (this may take some time)"
	UNMOUNT=$(diskutil unmountDisk $DISK)
	if [[ $UNMOUNT = "dd: $DISK: Resource busy" ]]; then
		UNMOUNT=$(diskutil unmountDisk $DISK)
	fi
    sudo dd bs=1m if=$RASPBIAN of=$DISK
fi
echo "Done!"
