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
