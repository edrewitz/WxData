# Contributing Guidelines

For those who would like to contribute to the WxData Project, please take note of the following guidelines. 

In order for your pull request to be accepted, you must comply with the following guidelines:

1) Your addition must work on VPN/PROXY server connections and allow users to pass in their PROXY settings. The `requests` package is recommended for this.
2) If you are building an end-to-end pipeline client used for automation, your addition must have a scanner to prevent repetitive downloads.
3) If creating an API interface that requires an API Key, DO NOT include the API Key in your code. Make a variable called API Key in the function and have the user pass in their own API Key. Anything related to API Keys and passwords are considered secrets and are not allowed in code. If you submit a PR with secrets in it, your PR will be rejected until those secrets are removed. 
4) If you are building a new end-to-end pipeline client, your addition must automatically organize the files and re-map the GRIB keys into plain-language like all existing end-to-end pipeline clients.
5) Do not plagerize anyone else's work - cite any new dependencies.
6) You are not allowed to use packages that are not available on BOTH Anaconda and PYPI (pip) (i.e. pygrib is not allowed and users must use xarray with cfgrib for post-processing)
    - This project must be available on PYPI in addition to Anaconda to maximize access for use.
7) The use of setup.py files is forbidden due to security vulerabilities associated with the use of setup.py. We use pyproject.toml for building our recipe.
8) If you are adding data access for a new data source or using new packages not already used in WxData, please cite the data source/package at the following:
     - [packages](https://github.com/edrewitz/WxData?tab=readme-ov-file#citations)
     - [data sources](https://github.com/edrewitz/WxData?tab=readme-ov-file#data-sources)
9) Be willing to accept feedback and constructive criticism.
10) Be respectful.
11) Have fun!
    
