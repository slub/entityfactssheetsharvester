# entityfactssheetsharvester - EntityFacts sheets harvester

entityfactssheetsharvester is a commandline command (Python3 program) that retrieves [EntityFacts](https://www.dnb.de/EN/Professionell/Metadatendienste/Datenbezug/Entity-Facts/entity-facts_node.html) sheets* from a given CSV with GND identifiers and returns them as line-delimited JSON records

*) EntityFacts are "fact sheets" on entities of the Integrated Authority File ([GND](https://www.dnb.de/EN/Professionell/Standardisierung/GND/gnd_node.html)), which is provided by German National Library ([DNB](https://www.dnb.de/EN/Home/home_node.html))

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

## See Also

* [entityfactspicturesharvester](https://github.com/slub/entityfactspicturesharvester) - a commandline command (Python3 program) that reads depiction information (images URLs) from given EntityFacts sheets (as line-delimited JSON records) and retrieves and stores the pictures and thumbnails contained in this information
* [entityfactspicturesmetadataharvester](https://github.com/slub/entityfactspicturesmetadataharvester) - a commandline command (Python3 program) that reads depiction information (images URLs) from given EntityFacts sheets (as line-delimited JSON records) and retrieves the (Wikimedia Commons file) metadata of these pictures (as line-delimited JSON records)
