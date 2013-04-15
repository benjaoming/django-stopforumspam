from django.db import transaction
from django.core.management.base import BaseCommand

try:
    from django.utils import timezone
except ImportError:
    from datetime import datetime as timezone

from stopforumspam import models
from stopforumspam import settings as sfs_settings
from django.conf import settings

import re
import urllib
import zipfile
from optparse import make_option

def safe_bulk_create(objs):
    """Wrapper to overcome the size limitation of standard bulk_create()"""
    if len(objs) == 0: return
    if not 'sqlite' in settings.DATABASES['default']['ENGINE']:
        objs[0].__class__.objects.bulk_create(objs)
    else:
        BULK_SIZE = 900/len(objs[0].__class__._meta.fields)
        for i in range(0,len(objs),BULK_SIZE):
            print "SQLITE size limits: Bulk inserting %d objects" % BULK_SIZE
            objs[0].__class__.objects.bulk_create(objs[i:i+BULK_SIZE])

class Command(BaseCommand):
    args = '--force'
    help = 'Updates the database with the latest IPs from stopforumspam.com'
    option_list = BaseCommand.option_list + (
        make_option('--force', '-f', dest='force', default=False,
                    action='store_true',
                    help='Force update of options'),
        )
    
    def handle(self, *args, **options):
        self.ensure_updated(options['force'])
        
    def ensure_updated(self, force=False):
        last_update = models.Log.objects.filter(message=sfs_settings.LOG_MESSAGE_UPDATE).order_by('-inserted')
        do_update = force
        if not do_update and last_update.count() > 0:
            days_ago = timezone.now() - last_update[0].inserted
            if days_ago.days >= sfs_settings.CACHE_EXPIRE:
                do_update = True
        else:
            do_update = True
        if do_update:
            print "Updating (this may take some time)"
            print "If you abort this command and want to rebuild, you have to use the --force option!"
            self.do_update()
        else:
            print "Nothing to update"
    
    
    @transaction.commit_manually()
    def do_update(self):
        try:
            self._do_update()
            transaction.commit()
        except Exception:
            transaction.rollback()
            raise

    def _do_update(self):
        # Delete old cache
        models.Cache.objects.filter(permanent=False).delete()
        
        # First log the update
        log = models.Log()
        log.message = sfs_settings.LOG_MESSAGE_UPDATE
        log.save()
        
        # For security purposes we test that each line is actually an IP address
        ip_match = re.compile(r"^(\d+)\.(\d+)\.(\d+)\.(\d+)$")
        
        if sfs_settings.SOURCE_ZIP.startswith("file://"):
            filename = sfs_settings.SOURCE_ZIP.split("file://")[1]
        else:
            filename, __ = urllib.urlretrieve(sfs_settings.SOURCE_ZIP)
        z = zipfile.ZipFile(filename)
        ips = z.read(sfs_settings.ZIP_FILENAME)
        ips = ips.split("\n")
        ips = filter(lambda x: ip_match.match(x), ips)
        inserted = 0
        total = len(ips)
        objects_to_save = []
        for ip in ips:
            cache = models.Cache(ip=ip)
            objects_to_save.append(cache)
            inserted = inserted + 1
            if inserted % 100 == 0:
                print "Object %d of %d found" % (inserted, total)
        
        print "===================="
        print " Saving to database "
        print "===================="

        if hasattr(models.Cache.objects, 'bulk_create'):
            print "New django with bulk_create detected. Inserting everyting at once!"
            safe_bulk_create(objects_to_save)
        else:
            print "Django<1.5, inserting one object at a time..."
            for cnt,cache in enumerate(objects_to_save):
                cache.save()
                if cnt % 100 == 0:
                    print "Object %d of %d saved" % (inserted, total)

    
