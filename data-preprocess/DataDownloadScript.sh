#!/bin/bash

### First, run python script to extract and download all relevant pdf links from panynj.gov site
  # mkdir AirlinePDFs
  # python3 ExtractREGURLS.py

### Second, convert pdf files to text files
### The "-f 3" option is used since it was determined that page 3 held all the useful data
### The "-H 444" option is used since it was determined that the table in the top 444 pixels of page 3 contains the useful information
#### If the pdftotext tool runs on the full pdf, errors occur on ~20% of the file conversions
for file in ./AirlinePDFs/*.pdf ./AirlinePDFs/*.PDF; do
  pdftotext -f 3 $file
  # pdftotext -f 3 -y 0 -H 444 $file
done

