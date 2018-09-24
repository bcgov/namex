# Trademarks Loader

_September 2018_

This document describes the python scripts that are used to load the trademarks data into the Solr _trademarks_ core. At
the time of writing, the data arrived from the Canadian Intellectual Property Office (CIPO) on seven DVDs, and contain
26 GB of zip files.

The python script `trademarks_parser.py` has one variable that can be configured:

 - `SOURCE_DIRECTORY` (default `C:\TEMP\Trademarks`) defines the location of the CIPO zip files. All zip files in all
   subdirectories will be extracted, so it is important that only the CIPO files are under this directory.

When running the script, a log will be written to the console as well as to the `.log` file in the same directory. After
processing, search the log file for:
1. `ERROR`: to indicate errors that happened during processing.
1. `DESCRIPTION`: to indicate trademarks that are missing their description element. These should be investigated as
   we may want to exclude them from the core data.

The primary output of the script is the `.json` file in the same directory. This file is loaded by running
`trademarks_loader.py`. The loader needs to be configured for a particular environment by setting `SOLR_BASE_URL`.

Until a better place can be found, the `.log` and `.json` outputs should be archived in
`N:\BCAP2\6450 Projects\20-Mainframe Migration\Names Examination\trademarks`.

#### Room for improvement
1. Proper logging would be nice
1. Perhaps its better to read from the zip than unzip them all
1. The hokey JUMP functionality would be nice if it had min and max application (filename) values
1. The matches.sort() call is a NOP, it needs to sort numerically
1. If solr_loader is converting string to JSON and then back to string, then prevent that
1. The solr_loader should be multi-threaded to decrease the load time
