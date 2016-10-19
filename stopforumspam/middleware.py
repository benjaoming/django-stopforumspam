from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils import ipv6

from . import settings as sfs_settings
from . import models


class StopForumSpamMiddleware():

    def process_request(self, request):

        if sfs_settings.FORCE_ALL_REQUESTS:
            return self.check_request_ip(request)

        def compile_paths(path_list):
            paths = []
            for path in path_list:
                if path.startswith("/"):
                    paths.append(path)
                else:
                    paths.append(reverse(path))
            return paths

        if not request.method == 'POST':
            return

        if sfs_settings.ALL_POST_REQUESTS:
            if request.path in compile_paths(sfs_settings.URLS_IGNORE):
                return
            return self.check_request_ip(request)

        if request.path in compile_paths(sfs_settings.URLS_INCLUDE):
            return self.check_request_ip(request)

    def check_request_ip(self, request):

        remote_ip = ipv6._unpack_ipv4(request.META[sfs_settings.HEADER])

        cache_entries = models.Cache.objects.filter(ip=remote_ip)

        if cache_entries.count() > 0:
            if sfs_settings.LOG_SPAM:
                log = models.Log(message="Spam received from {}".format(remote_ip))
                log.save()

            return render(
                request,
                'stopforumspam/denied.html',
                {"cache_entries": cache_entries},
                status=403
            )
