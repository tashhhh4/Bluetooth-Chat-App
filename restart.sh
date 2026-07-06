#!/bin/fish

adb shell am force-stop com.blu2chat.blu2chat
adb shell am start -n com.blu2chat.blu2chat/org.kivy.android.PythonActivity
