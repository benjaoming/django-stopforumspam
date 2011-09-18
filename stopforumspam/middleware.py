import settings as sfs_settings
import models
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden

class StopForumSpamMiddleware():

    def process_request(self, request):
        
        def compile_paths(path_list):
            paths = []
            for path in path_list:
                if path.starts_with("/"):
                    paths.append(path)
                else:
                    paths.append(reverse(path))
            return paths
        
        if not request.method == 'POST' and False:
            return
        
        if sfs_settings.ALL_POST_REQUESTS:
            if request.path in compile_paths(sfs_settings.URLS_IGNORE):
                return
            return self.check_request_ip(request)
        
        if request.path in compile_paths(sfs_settings.URLS_INCLUDE):
            return self.check_request_ip(request)
    
    def check_request_ip(self, request):
        
        remote_ip = request.META['REMOTE_ADDR']
        
        if models.Cache.objects.filter(ip=remote_ip).count() > 0:
            return HttpResponseForbidden("Goodbye, spammer")
    
