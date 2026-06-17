# Bluetooth Chat App (still working on the name)


## Development

### Test locally (Linux)
```fish
uv run main.py
```

### Using buildozer
To speed up development, skip building and deploying when adding additional iterations of existing types of functionality (CRUD operations, new UI designs, new error checks) instead testing locally using `uv run main.py`. Creating and testing a new build should be done after adding entirely new types of functionality to the app, especially things that may interact with the OS such as database, file I/O, bluetooth, or Android permissions.

* Requires Java SDK 17

#### Debug Build
Run:
```fish
./build.sh
```

Sometimes pip is not installed when dependencies are managed with uv. But pip is needed for buildozer. To fix:
```fish
uv run python -m ensurepip --upgrade
```

#### How to test the build
* The phone must be plugged into the computer with a USB cable.
* Enable developer mode by tapping on the build number in Settings.
* Set "Connected Devices > USB > USB Preferences > Use USB for" to "File Transfer".
* May need to disable additional USB security settings.

#### Install the app to the phone
Run:
```fish
uv run buildozer android deploy
```

#### Launch the app on the phone
Run:
```fish
uv run buildozer android run
```

#### Clean the build cache
⚠️ Deleting the build cache may cause the next build to take a very long time. But it might fix issues especially after changing around the dependencies.
```fish
uv run buildozer android clean
```

## Building Python with Bluetooth
Python was not installed with bluetooth headers by default on my development machine. The following may not be extremely useful as a tutorial yet, but for now I'm just writing down the steps I took to fix this.

|                 |               |
|-----------------|---------------|
| My system       | CachyOS Linux |
| Package Manager | paru          |
| Shell           | fish          |

#### Install Bluetooth libs
```fish
paru bluez
```
It was already installed:

```shell
6 cachyos-extra-znver4/bluez-libs 5.86-6.1 [0 B 16.19 KiB] [Installed]
   Deprecated libraries for the bluetooth protocol stack
```

#### Verify that the Bluetooth headers exist in the system
These are the files that CPython looks for when deciding whether to enable Bluetooth socket support.
```fish
ls /usr/include/bluetooth/bluetooth.h
# It is there.
ls /usr/include/bluetooth/rfcomm.h
# It is there.
```

At this point I learned that Bluetooth is usually included by default in Python. I installed Python 3.11 globally.
```fish
paru python311
1 cachyos/python311 3.11.14-1 [13.34 MiB 74.12 MiB]
    The Python programming language (version 3.11)
2 aur/python311 3.11.14-1 [+24 ~0.47]
    The Python programming language (version 3.11)
```

I tried (1) and it STILL didn't have the Bluetooth stuff, so I tried (2).

#### Verify that Python's socket library has Bluetooth support enabled
```fish
python3.11
>>> import socket
>>> hasattr(socket, 'AF_BLUETOOTH')
True
```