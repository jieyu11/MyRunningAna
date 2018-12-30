**Analyze my personal running data**
====================================

* Install fitparse
  - check the fitparse in python: https://github.com/dtcooper/python-fitparse
  - check also below as reference: http://dtcooper.github.io/python-fitparse/
  - do: pip install fitparse

* Bulk Export of data from strava
  - As of May 25th, 2018, Strava provides the option to export an archive of your account.
    Find here: https://support.strava.com/hc/en-us/articles/216918437-Exporting-your-Data-and-Bulk-Export

    1. Log into the account on Strava.com that you wish to delete.
    2. Hover over your name in the upper right-hand corner of the Strava page. Choose "Settings," then find the "My Account" tab from the menu listed on the Left.
    3. Select "Get Started" under "Download or Delete Your Account."
    4. Select "Request your archive" on the next page. You will receive an email with a link to download your data (this may take a few hours.)
      For this reason, it's important that you have access to the email account attached to your Strava profile.

  - Your data archive will contain the following
    1. A zipped folder with your activities in their original file format. (.fit as from garmin?)
    2. A folder with all the photos you've uploaded to Strava.
    3. A folder with routes you've created in GPX format.
    4. CSV files that include the following
       + All the posts and comments you've posted.
       + Contacts you've synced to Strava.
       + Clubs and events you've created
       + The information in your profile including your gear and goals.
       + Actions you've performed including kudos given and routes or segments you've starred.


* Run Analysis of one single run (.fit)
  - python2.7 read_fit.py data/test.fit OUTDIR

* Run Analysis of multiple runs in a folder InputDIR or a input file with each line the (.fit) input name.
  - python2.7 anal.py data OUTDIR
  - python2.7 anal.py inputs.txt OUTDIR
