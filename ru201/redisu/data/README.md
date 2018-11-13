# RU201 Scripts

## Install
To install the script you'll need npm and Node.js 8.11+. To get the dependencies use:

```
$ npm install
```

in this directory.

## Configuration

First, you will need to create a simple JSON file for your connection credentials. This connection file is based on the node_redis config object allowing you specify host, password, port, etc. In the most basic configuration you would have just those three:

```
{
  "host"  : "localhost",
  "port"  : 6379
}
```

Save this file outside of the path of this repo so you don't accidentally commit it to a public-facing site.

## Running

The `index.js` script will create the schema and database for you from a CSV file (provided). 

When running you'll need to specify:

- `source` **Required.** _The CSV file which will be ingested. `General_Building_Permits.csv` is included_
- `connection` **Required.** _The path to your configuration file._
- `drop` **Optional.** _This will drop the existing permits schema._
- `totaldocs` **Optional.** _This will give you an accurate progress bar. The provided CSV has 121,828 docs_


```
$ node index.js --source ./General_Building_Permits.csv --connection ./connection.json --drop --totaldocs 121828
```

The output should look something like this:

```
Created index. Starting ingest.
Parsed   [▇▇▇▇▇▇▇▇▇▇▇—————————————————————————————————————————————————] 21798/121828 18% 3.5s 19.8s
Ingested [▇▇▇▇▇▇▇▇▇▇▇—————————————————————————————————————————————————] 21613/121828 18% 3.5s 20.0s (Pipeline 185)
Speed    [▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇] 6927 docs/sec, ~6928 doc/sec max
```

## Confirmation

You can check you have the right data by trying the following search from the redis-cli

```
127.0.0.1:6379> ft.search permits garage limit 0 0
1) (integer) 49488
```

## Data

The data file provided (`General_Building_Permits.csv`) is pulled from the [Edmonton Open Data Portal](https://data.edmonton.ca) and is the [General Building Permits](https://data.edmonton.ca/Sustainable-Development/General-Building-Permits/24uj-dj8v) dataset pulled on May 16, 2018. This dataset is frequently updated, however we've frozen the data set in this course to provided a consistent course experience. 
