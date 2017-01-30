kivy-browser
=============

Open the Android web browser.  Amazing!  Uses P4A/PyJNIus.

#### Features
None.  Zero.  Zilch.

#### Install
Pre-built application in ```/bin```
adb install -r /bin/BrowserOpener-0.1-debug-unaligned.apk

#### Build
Copy the browser.sh to a P4A dist then run:
```browser.sh my/path/to/app/```
If it doesn't work, edit netcheck.sh to configure P4A to build this.  Need PyJNIus in your dist. 

#### Debuggable
```src/browser/main.py``` It prints the URL to let you know that the call happened.  No more.

#### Docs
Public API.

Contact me for support
