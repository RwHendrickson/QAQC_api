## 1) Set up Server on remote Google Cloud Run 

Set up a [Google Cloud Run Build](https://cloud.google.com/run/docs/continuous-deployment-with-cloud-build) using the GitHub repository:

RwHendrickson/QAQC_api

Select Dockerfile as your build type. Allow unauthenticated invocations.

Then you will need to update the db_credentials_template.txt with your own credentials somehow... 

I think this can be done at ide.cloud.google.com 

## 2) TO DO Another Time... Set up Secure Virtual Machine (See old_west_main.py)

# Cloud Run Setup

Here is a "how to" set up a remote machine for the Community Air Monitoring Project

## Download the code (WRONG)

On you remote machine, download the code with something like this line:

wget -m https://github.com/RTGS-Lab/QualityAirQualityCities/trunk/api

