# ADB-Tools
ADB is a headache to use manually, so I've automated some of it.
Everything in the repo is for the automation of specific tasks,
like enabling MTP on a phone which doesn't have default usb behavior settings or
automatically connecting over tcp(when the usb cable is plugged in) for easier debugging.


I'll probably add folder sync over TCP in the next decade or so.

## Installation
No additional libraries are currently required.\
Invoke with pythonw, change the setup directory with the "path" argument.\
Example: `main.py path="/test/path/ADB Tools Data"`

The config is **NOT** meant to be edited while the script is running.
## Capabilities:

* USB to TCP handover
* Automatically connect to TCP devices via cache
* Automatically enable MTP when connected via USB