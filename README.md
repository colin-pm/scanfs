# Scanfs
Embedded Linux Root Filesystem Analysis Tool

## Design Goals
* Initially loads filesystem layout into memory
  * Assoicates files with the block device they're stored on
* Size can be calculated dynamically

* Contents can be output to CSV or sqlite3 database

* Tool can load data from a CSV or sqlite3 database

* Tool can diff different files

* Tool can generate HTML reports with graphs