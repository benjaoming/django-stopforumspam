from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


from . import settings as sfs_settings



# Create your models here.
class Cache(models.Model):

    updated = models.DateTimeField(auto_now=True, verbose_name=_(u"Updated"))
    ip = models.GenericIPAddressField(verbose_name=_(u"IP address"),)
    permanent = models.BooleanField(
        default=False, verbose_name=_(u"Permanent"))

    class Meta:
        verbose_name = _(u"Cache entry")
        verbose_name_plural = _(u"Cache")


class Log(models.Model):
    inserted = models.DateTimeField(
        auto_now_add=True, verbose_name=_(u"inserted"))
    message = models.CharField(max_length=1024, verbose_name=_(u"message"))

    def save(self):
        super(Log, self).save()
        # Delete old log messages
        Log.objects.filter(
            inserted__lt=timezone.now() - timedelta(days=sfs_settings.LOG_EXPIRE)).delete()

    class Meta:
        ordering = ('-inserted',)
        verbose_name = _(u"Log message")
        verbose_name_plural = _(u"Log")
