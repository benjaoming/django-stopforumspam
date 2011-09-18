###############################
django stopforumspam middleware
###############################

A django application that provides middleware for blocking IPs listed in
stopforumspam.com's database.

A management command is provided for updating the database:

manage.py sfsupdate [--force]

...and all IPs are stored in Django models so you can add your own as well
(remember to mark them permanent so they don't get deleted!)

###############################
Installation
###############################

Add this to settings.MIDDLEWARE_CLASSES:
    'stopforumspam.middleware.StopForumSpamMiddleware'
    
Then add this to INSTALLED_APPS:
    'stopforumspam'

And run:
    ./manage.py syncdb

The run this command and remember that it takes quite some time (2+ min)
to insert all IPs in your database (there's probably > 20,000).
    ./manage.py sfsupdate

You may remove stopforumspam from your INSTALLED_APPS after, if you do not
wish to see it in your admin pages.