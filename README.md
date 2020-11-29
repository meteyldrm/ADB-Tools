# ADB-Tools
ADB is a headache to use manually, so I've automated some of it. Everything in the repo is for the automation of specific tasks, like enabling MTP on a phone which doesn't have default usb behavior settings or automatically connecting over tcp(when usb is plugged in) for easier debugging.

The script will create some icons and a config file in the folder that it's in, it's best to put it in a new folder and run it that way.

This is intended to be run in the background without launching a terminal. Preferably invoke it with pythonw on startup.
The config file allows for runtime behavior changes, possible keys and values will be commented in the generated ini file.
On Windows and macOS you can access the process/config as a tray icon also.

### Capabilities:

* Reconnect to device over TCP
* Enable MTP