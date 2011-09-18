###############################
django stopforumspam middleware
###############################

A django application that provides middleware for blocking IPs listed in
stopforumspam.com's database.

A management command is provided for updating the database:

manage.py sfsupdate [--force]

...and all IPs are stored in Django models so you can add your own as well
(remember to mark them permanent so they don't get deleted!)

************
Installation
************

Install by running:

    sudo pip install stopforumspam

Add this to settings.MIDDLEWARE_CLASSES

    'stopforumspam.middleware.StopForumSpamMiddleware'
    
Then add this to INSTALLED_APPS

    'stopforumspam'

And run

    ./manage.py syncdb

To insert all the IPs run this command, which you should make a cronjob (run it every 24h).

    ./manage.py sfsupdate

You may remove stopforumspam from your INSTALLED_APPS after, if you do not
wish to see it in your admin pages.


*************
Configuration
*************

The following options exist for your project's settings.py file:

To check ALL POST requests:

    SFS_ALL_POST_REQUESTS = True

To ignore some URLS:

    SFS_URLS_IGNORE = ["url_name", "/url/path"]

To only include some URLS (only works if SFS_ALL_POST_REQUEST=False):

    SFS_URLS_INCLUDE = ["url_name", "/url/path"]

To configure where to download the file from (you can MAX download 2 times a day) - see http://www.stopforumspam.com for more resources:

    SFS_SOURCE_ZIP = "http://www.stopforumspam.com/downloads/listed_ip_7.zip"  

Remember to configure this as well -- it's the name of the file inside the .zip file:

    SFS_ZIP_FILENAME = "listed_ip_7.txt"

For testing you can force all requests to be checked.

    SFS_FORCE_ALL_REQUESTS = True   

