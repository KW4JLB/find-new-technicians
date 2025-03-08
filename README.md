[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# find-new-license-grants

## Description
A Python Script to download the weekly FCC ULS Amateur Radio License Database, extract licenses for the state of Georgia, and then filter new License Grants by zipcode. 

## Installation and Usage

### Windows

1. Open a command prompt
2. Navigate to where you downloaded this repository
3. Run the following commands to setup the environment
```
python3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
4. To Run the Script use the command `.\.venv\Scripts\python.exe .\find-new-license-grants.py -d --zipcode 12345 --months 1`
5. When you are done, close the command prompt. 

### OS X and Linux
1. Open a Terminal
2. Navigate to where you downloaded this repository
3. Run the following commands to setup the environment
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
4. To Run the Script use the command `python3 find-new-license-grants.py -d --zipcode 12345 --months 1`
5. When you are done, run the command `deactivate`
6. Close the Terminal

## Usage

```
usage: [-h] [-z ZIPCODE [ZIPCODE ...]] [-m MONTHS [MONTHS ...]] [-D] [-d]

Search the FCC ULS to find newly licensed individuals

options:
  -h, --help            show this help message and exit
  -z ZIPCODE [ZIPCODE ...], --zipcode ZIPCODE [ZIPCODE ...]
                        What Zip Code To Search
  -m MONTHS [MONTHS ...], --months MONTHS [MONTHS ...]
                        How Many Months from today to search for
  -D, --download-only   Only Download the FCC ULS Database Files
  -d, --download        Download the FCC ULS Database Files

Developed and maintained by KW4JLB.
```