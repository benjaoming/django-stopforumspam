from __future__ import absolute_import, unicode_literals

import re
import zipfile
from io import BytesIO

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from ... import settings as sfs_settings
from ... import compat, models


class Command(BaseCommand):
    help = 'Updates the database with the latest IPs from stopforumspam.com'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            dest='force',
            default=False,
            help='Force update of options',
        )
        parser.add_argument(
            '--quiet', '-q',
            action='store_true',
            dest='quiet',
            default=False,
            help='Do not produce output unless upon failure',
        )

    def handle(self, *args, **options):
        self.quiet = options['quiet']
        self.ensure_updated(force=options['force'])

    def print_output(self, msg):
        if not self.quiet:
            print(msg)

    def ensure_updated(self, force=False, quiet=False):

        last_update = models.Log.objects.filter(
            message=sfs_settings.LOG_MESSAGE_UPDATE).order_by('-inserted')
        do_update = force
        if not do_update and last_update.count() > 0:
            days_ago = timezone.now() - last_update[0].inserted
            if days_ago.days >= sfs_settings.CACHE_EXPIRE:
                do_update = True
        else:
            do_update = True
        if do_update:
            self.print_output("Updating (this may take some time)")
            self.print_output(
                "If you abort this command and want to rebuild, you have to use the --force option!")
            self.do_update()
        else:
            self.print_output("Nothing to update")

    @compat.notrans
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

        # For security purposes we test that each line is actually an IP
        # address
        ip_pattern = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")

        fileobject = None
        if sfs_settings.SOURCE_ZIP.startswith("file://"):
            filename = sfs_settings.SOURCE_ZIP.split("file://")[1]
            self.print_output(" . Using: {}".format(filename))
            fileobject = open(filename, "rb")
        else:
            self.print_output(" ^ Downloading: {}".format(sfs_settings.SOURCE_ZIP))
            response = compat.urllib.urlopen(sfs_settings.SOURCE_ZIP)
            # Necessary because ZipFile needs to do a seek() call on the
            # file object which HttpResponse in python3 doesn't support.
            fileobject = BytesIO(response.read())
        z = zipfile.ZipFile(fileobject)
        self.print_output(" < Extracting: {}".format(sfs_settings.ZIP_FILENAME))
        ips = str(z.read(sfs_settings.ZIP_FILENAME))
        inserted = 0
        total = len(ips)
        objects_to_save = []
        for ip in ip_pattern.findall(ips):
            cache = models.Cache(ip=ip)
            objects_to_save.append(cache)
            inserted = inserted + 1
            if inserted % 100 == 0:
                self.print_output("Object %d of %d found" % (inserted, total))

        self.print_output("====================")
        self.print_output(" Saving to database ")
        self.print_output("====================")

        self.safe_bulk_create(objects_to_save)

        self.print_output("IPs from SFS saved to database")

    def safe_bulk_create(self, objs):
        """Wrapper to overcome the size limitation of standard bulk_create()"""
        if len(objs) == 0:
            return
        if 'sqlite' not in settings.DATABASES['default']['ENGINE']:
            objs[0].__class__.objects.bulk_create(objs)
        else:
            BULK_SIZE = 900 / len(objs[0].__class__._meta.fields)
            for i in range(0, len(objs), BULK_SIZE):
                self.print_output("SQLITE size limits: Bulk inserting %d objects" % BULK_SIZE)
                objs[0].__class__.objects.bulk_create(objs[i:i + BULK_SIZE])
