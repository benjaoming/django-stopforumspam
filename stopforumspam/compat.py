"""Abstraction layer to deal with Django related changes in order to keep
compatibility with several Django versions simultaneously."""
from __future__ import absolute_import, unicode_literals

from django.db import transaction


try:
    notrans = transaction.non_atomic_requests
except:
    notrans = transaction.commit_manually  # @UndefinedVariable


try:
    # Python 2
    import urllib2 as urllib
except ImportError:
    from urllib import request as urllib  # noqa @UnusedImport
