# Trademarks Loader

_September 2018_

This document describes the python script that is used to load the trademarks data into the Solr cores. At the time of
writing, the data arrived on seven DVDs containing 26 GB of zip files.

The python script has two variables that may be configured:

 - `SOURCE_DIRECTORY` (default `C:\TEMP\Trademarks`) defines the location of the zip files. All zip files in all
   subdirectories will be extracted, so it is important that only the trademarks files are under this directory.
 - `DESTINATION_DIRECTORY` (default `C:\TEMP\Trademarks.output`) the directory where the XML files are written to.

Check the log file for ERROR items and handle as needed.

Once the XML files have been generated, they must be copied to the servers (rsync will use tar if you don't have rsync
in your path):

```
C:\TEMP> oc rsync CA-TMK-GLOBAL_2018-06-16 solr-<POD_ID>:/opt/solr/trademarks_data
WARNING: rsync command not found in path. Download cwRsync for Windows and add it to your PATH.
```

In the pod terminal for Solr swap the link to point to the new data. Note that two sets of data may not fit on the
volume.

```
$ cd /opt/solr/trademarks_data
$ rm latest
$ ln -s latest CA-TMK-GLOBAL_2018-06-16
```

#### Room for improvement
1. If you used a built-in library rather than untangle, there would be no required packages
1. Proper logging would be nice
1. Perhaps its better to read from the zip than unzip them all
1. The hokey JUMP functionality would be nice if it has min and max application (filename) values
1. The matches.sort() call is a NOP, it needs to sort numerically
