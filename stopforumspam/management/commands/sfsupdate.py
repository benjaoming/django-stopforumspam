from django.core.management.base import BaseCommand
from datetime import datetime

from stopforumspam import models
from stopforumspam import settings as sfs_settings

import re
import urllib
import zipfile
from optparse import make_option

class Command(BaseCommand):
    args = ''
    help = 'Updates the database with the latest IPs from stopforumspam.com'
    option_list = BaseCommand.option_list + (
        make_option('--force',
            dest='force',
            default=False,
            help='Force update of options'),
        )
    
    def handle(self, *args, **options):
        self.ensure_updated(options['force'])
        
    def ensure_updated(self, force=False):
        last_update = models.Log.objects.filter(message=sfs_settings.LOG_MESSAGE_UPDATE)
        do_update = False or force
        if not do_update and last_update.count() > 0:
            last_update = last_update[0].inserted
            days_ago = datetime.now() - last_update
            if days_ago.days >= sfs_settings.CACHE_EXPIRE:
                do_update = True
        else:
            do_update = True
            last_update = None
        if do_update:
            print "Updating (this may take some time)"
            print "If you abort this command and want to rebuild, you have to use the --force option!"
            self.do_update(delete_before=last_update)
        else:
            print "Nothing to update"
            
    def do_update(self, delete_before=None):
        # First log the update
        log = models.Log()
        log.message = sfs_settings.LOG_MESSAGE_UPDATE
        log.save()
        
        # For security purposes we test that each line is actually an IP address
        ip_match = re.compile(r"^(\d+)\.(\d+)\.(\d+)\.(\d+)$")
        
        filename, __ = urllib.urlretrieve(sfs_settings.SOURCE_ZIP)
        z = zipfile.ZipFile(filename)
        ips = z.read(sfs_settings.ZIP_FILENAME)
        ips = ips.split("\n")
        
        for ip in ips:
            if not ip_match.match(ip):
                continue
            cache = models.Cache(ip=ip)
            cache.save(force_insert=True)
        
        # After inserting all these ips, delete the old ones
        if delete_before:
            models.Cache.objects.filter(updated_lte=delete_before, permanent=False).delete()
        
        
    