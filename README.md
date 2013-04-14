================================
django stopforumspam middleware
================================

Tired of comment spam, form spam and dumb crawlers? A django application that provides middleware for blocking IPs listed in stopforumspam.com's database. A simple management command is provided for updating the database:

    manage.py sfsupdate [--force]

Using this command, all IPs are stored in Django models. Using django-admin, it's possible to add your own extra IP addresses on a permanent database.

------------
Installation
------------

Install the latest release from pypi:

    sudo pip install stopforumspam

Add this to settings.MIDDLEWARE_CLASSES

    'stopforumspam.middleware.StopForumSpamMiddleware'
    
Then add this to INSTALLED_APPS

    'stopforumspam'

And run

    python manage.py syncdb

To insert all the IPs run this command, which you should make a cronjob (run it every 24h).

    python manage.py sfsupdate

You may remove stopforumspam from your INSTALLED_APPS after, if you do not
wish to see it in your admin pages.


-------------
Configuration
-------------

The following options exist for your project's settings.py file:

To check ALL POST requests:

    SFS_ALL_POST_REQUESTS = True

To ignore some URLS:

    SFS_URLS_IGNORE = ["url_name", "/url/path"]

To only include some URLS (only works if SFS_ALL_POST_REQUEST=False):

    SFS_URLS_INCLUDE = ["url_name", "/url/path"]

### Synching with stopforumspam.com

Be nice to their servers and remember that they have strict enforcements on the files that they offer. So before
you start testing, you could consider using a local file as a test.

To configure where to download the file from (you can MAX download 2 times a day) - see http://www.stopforumspam.com for more resources:

    SFS_SOURCE_ZIP = "http://www.stopforumspam.com/downloads/listed_ip_7.zip"  

But you should really use a local file if you have more than 1 Django project with stopforumspam running from the same IP address. To do this, use a local protocol:

    SFS_SOURCE_ZIP = "file:///path/to/listed_ip_7.zip"

You can control how often at most the update should be performed

    SFS_CACHE_EXPIRE = 1 #day

...and how long back the log should remember the rejection of POSTS and IPs.

    SFS_LOG_EXPIRE = 1 #days

Remember to configure this as well -- it's the name of the file inside the .zip file:

    SFS_ZIP_FILENAME = "listed_ip_7.txt"

For testing you can force all requests to be checked.

    SFS_FORCE_ALL_REQUESTS = True   

---------
Cron Jobs
---------
You probably want to automatically update the list of blocked IP addresses every 24 hours or 48 hours.
To do that, you can insert a line in crontab.

    0 2 * * * python /your/project/path/manage.py sfsupdate

The above would update at 2 AM every night. If you have several projects and sync them with a local file, you can add:

    0 2 * * * wget -O /tmp/listed_ip_7.zip http://www.stopforumspam.com/downloads/listed_ip_7.zip && python /your/project/path/manage.py sfsupdate
