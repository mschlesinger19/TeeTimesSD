# TeeTimesSD

This is an automated Selenium script written in python used to book tee times for the San Diego Tee Time Scheduling system.

## Installation

Python is needed to run this script. I am using version 3.8.2.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Selenium.

```bash
pip install selenium
```

In addition, ensure that the chrome browser driver is in the same folder. The Chrome Browser driver can be found here: <https://sites.google.com/a/chromium.org/chromedriver/downloads>

## Usage

There are 4 parameters necessary for the script to work.
```bash
python golf.py [1] [2] [3] [4] optional[5]
```

1. Golf course name ex. "Torrey Pines South"
2. Number of golfers ex. 2
3. Date formatted as so: "9/28/20"
4. Earliest desired tee time: "16:00" (formatted in 24 hour clock)
5. If you want to wait unitl a certain time to book: "19:00"

You also need to edit the script to input your email and password into the script. See [Desired Changes](#desired-changes)

## Desired Changes <a name="desired-changes"></a>

1. Add other SD courses
2. ~~I am looking to add a flag to wait until 7:00 PM PST for the tee times the following week to open.~~ Done.
3. Config file for credentials
4. Including other GolfNow courses.
