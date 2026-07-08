# Bluetooth Chat App (still working on the name)


## Development

### The different development environments
#### Local
_Runs on my local development machine, (CachyOS Linux with KDE desktop environment)._
- A window pops up over the desktop when this version is run.
- Bluetooth adapters and permissions libraries for Android are excluded from this build.
- Useful for rapid development/debugging of the UI widgets.
Command to test the app:
```fish
uv run main.py
```

#### Debug
1. Build the app:
```fish
# Sets the appropriate JDK version and runs buildozer
./build.sh
```

1.5 Push individual files (much faster than creating a new build):
```fish
# Replaces the exact file specified using adb push and adb shell ... cp
./push.sh path/of/file.py
```

2. Check if the device is connected:
```fish
adb devices
```

3. Perform streamed install
```fish
# Runs buildozer deploy (very slow and sometimes fails)
./deploy.sh
```

3.5 Perform faster streamed install
```fish
# Reinstall AND RESET runtime permissions and user data
adb install bin/latest-version-of-debug.apk
# Reinstall WITHOUT resetting runtime permissions or user data
adb install -r bin/latest-version-of-debug.apk
```

3.75 Uninstall through adb
```fish
# Combine with the above command to quickly reinstall the app after a new build.
adb uninstall com.blu2chat.blu2chat
```

4. Activate the logs, filtering for logs coming from the Python app:
```fish
adb logcat | grep python
```

5. Make the app on the phone start:
_You can also click on the app from the phone._
```fish
buildozer android run
```

5.5 Restart the app through adb:
```fish
# Runs force-stop and start through adb
./restart.sh
```

#### Troubleshooting
_Fixes for issues encountered while developing._

###### pip
Sometimes pip is not installed when dependencies are managed with uv. But pip is needed for buildozer. To fix:
```fish
uv run python -m ensurepip --upgrade
```

###### USB Bridge Setup
* The phone must be plugged into the computer with a USB cable.
* Enable developer mode by tapping on the build number in Settings.
* Set "Connected Devices > USB > USB Preferences > Use USB for" to "File Transfer".
* May need to disable additional USB security settings.


###### Clean the build cache
⚠️ Deleting the build cache may cause the next build to take a very long time. But it might fix issues especially when changing the specific version of a dependency.
⚠️ After running clean, a lot of random dependencies are sometimes deleted and need to be manually reinstalled. Make sure to fix these with `uv pip install ...` instead of `uv add ...`, to keep the project dependency list in check.
```fish
uv run buildozer android clean
```

###### Building Python with Bluetooth
Python was not installed with bluetooth headers by default on my development machine. The following may not be extremely useful as a tutorial yet, but for now I'm just writing down the steps I took to fix this.

|                 |               |
|-----------------|---------------|
| My system       | CachyOS Linux |
| Package Manager | paru          |
| Shell           | fish          |

**Install Bluetooth libs**
```fish
paru bluez
```
It was already installed:

```shell
6 cachyos-extra-znver4/bluez-libs 5.86-6.1 [0 B 16.19 KiB] [Installed]
   Deprecated libraries for the bluetooth protocol stack
```

**Verify that the Bluetooth headers exist in the system**
These are the files that CPython looks for when deciding whether to enable Bluetooth socket support.
```fish
ls /usr/include/bluetooth/bluetooth.h
# It is there.
ls /usr/include/bluetooth/rfcomm.h
# It is there.
```

**Obtaining a complete version of Python 3.11**
_At this point I learned that Bluetooth is usually included by default in Python. The main issue seems to be that a version without Bluetooth headers was installed when using uv to set the project's Python version to 3.11. The fix is to install Python 3.11 from my OS's robust and well-maintained default package list, and then make sure the local interpreter for the project is using that one._
```fish
paru python311
1 cachyos/python311 3.11.14-1 [13.34 MiB 74.12 MiB]
    The Python programming language (version 3.11)
2 aur/python311 3.11.14-1 [+24 ~0.47]
    The Python programming language (version 3.11)
```

_I tried (1) and it STILL didn't have the Bluetooth stuff, so I tried (2)._

###### Verify Bluetooth socket support
```fish
python3.11
>>> import socket
>>> hasattr(socket, 'AF_BLUETOOTH')
True
```

**Note**
This entire sidequest of updating the local interpreter with Python3.11 with Bluetooth support is ONLY RELEVANT to the "local" version of the project, as a completely different Python runtime is used to actually build the final app when buildozer pulls from the "python-for-android" GitHub repository.