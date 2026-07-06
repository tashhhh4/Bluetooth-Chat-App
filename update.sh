#!/bin/fish

# Get the list of connected devices.
set DEVICES (adb devices | awk 'NR>1 && $2=="device" {print $1}')

# Require exactly one connected device.
if test (count $DEVICES) -ne 1
    echo "Error: Expected exactly one connected ADB device, found "(count $DEVICES)
    echo
    adb devices
    exit 1
end

set DEVICE_ID $DEVICES[1]
set LASTUPDATE_FILE "_lastupdate_$DEVICE_ID.txt"

# Create the timestamp file if it doesn't exist.
if not test -f $LASTUPDATE_FILE
    touch -t 197001010000 $LASTUPDATE_FILE
end

# Find all Python files modified since the last update and run push.sh on them.
find . -type f -name "*.py" -newer $LASTUPDATE_FILE -print0 | while read -z file
    echo "Processing: $file"
    ./push.sh "$file"
end

# Update the timestamp file to the current time.
touch $LASTUPDATE_FILE

./restart.sh