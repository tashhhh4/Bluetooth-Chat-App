# Bluetooth Chat App (still working on the name)


## Development

### Test locally (Linux)
```fish
uv run main.py
```

### Build and Test using buildozer
To speed up development, skip building and deploying when adding additional iterations of existing types of functionality (CRUD operations, new UI designs, new error checks) instead testing locally using `uv run main.py`. Creating and testing a new build should be done after adding entirely new types of functionality to the app, especially things that may interact with the OS such as database, file I/O, bluetooth, or Android permissions.

* Requires Java SDK 17

#### Debug Build
Run:
```fish
./build.sh
```

#### How to test the build
* The phone must be plugged into the computer with a USB cable.
* Enable developer mode by tapping on the build number in Settings.
* Set "Connected Devices > USB > USB Preferences > Use USB for" to "File Transfer".
* May need to disable additional USB security settings.

Run:
```fish
uv run buildozer android deploy run
```