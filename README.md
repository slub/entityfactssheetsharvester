# entityfactssheetsharvester - EntityFacts sheets harvester

entityfactssheetsharvester is a commandline command (Python3 program) that retrieves EntityFacts sheets from a given CSV with GND identifiers and returns them as line-delimited JSON records

## Usage

It eats CSV with GND identifiers (i.e. GND identifier per line) from *stdin*.

It puts the EntityFacts sheets one by one as line-delimited JSON record to *stdout*.

```
entityfactssheetsharvester

optional arguments:
  -h, --help                           show this help message and exit
```

* example:
    ```
    entityfactssheetsharvester < [INPUT CSV FILE WITH GND IDENTIFIERS] > [PATH TO THE OUTPUT LINE-DELIMITED JSON RECORDS FILE]
    ```
## Run

* clone this git repo or just download the [entityfactssheetsharvester.py](entityfactssheetsharvester/entityfactssheetsharvester.py) file
* run ./entityfactssheetsharvester.py
* for a hackish way to use entityfactssheetsharvester system-wide, copy to /usr/local/bin

### Install system-wide via pip

```
sudo -H pip3 install --upgrade [ABSOLUTE PATH TO YOUR LOCAL GIT REPOSITORY OF ENTITYFACTSSHEETSHARVESTER]
```
(which provides you ```entityfactssheetsharvester``` as a system-wide commandline command)
