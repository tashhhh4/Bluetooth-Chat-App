#!/bin/fish

set FILE $argv[1]

if test -z "$FILE"
    echo "Usage: push <path/to/file>"
    exit 1
end

adb push $FILE /data/local/tmp/$FILE; or exit 1
adb shell run-as com.blu2chat.blu2chat cp -f /data/local/tmp/$FILE files/app/$FILE; or exit 1
echo "Pushed $FILE."
adb shell rm /data/local/tmp/$FILE
echo "Cleaned up tmp dir."