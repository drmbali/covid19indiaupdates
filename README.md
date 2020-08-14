# covid19indiaupdates | community service project

This project is done as a community service project by two of the IIT Kharagpur students, meant to provide information at better level to the common people. Using the publicly available APIs of covid19india.org the data is updated on daily basis. Also scraping of few other internet sources is done in order to keep a better track of the cases.

## Old version (heroku-push)

the older version of the project is depreciated now as the sources of the data changes and the we have done the migration of our data to aws s3 bucket, anyone needing the geojson file for the same can connect us.

## New version
the newer version code is also made public, with removing the confidential credentials, the complete code is written in python3 and only a few libraries are used namely: **boto3, pandas, numpy, fuzzywuzzy (for partial string matching), requests, collections** and a few more basic libraries which are available in python by default.

## Mentions and thanking notes

We are thankful to **Mapbox** team who allowed us to use their javascript API free of cost for 6 months, also a big thanks to **https://covid19india.org** for keeping their APIs public, otherwise scarping data from the web would have been a hectic and time taking task.

### Live project links:

link with geolocation fetching feature: https://grv.codes/coronavirus
link without geolocation fetching feature: http://projects.shevya.codes/coronavirus

![demo-version1](https://dl-model-bucket-101.s3.amazonaws.com/corona.gif)
