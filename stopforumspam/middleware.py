import settings as sfs_settings
import models
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden

class StopForumSpamMiddleware():

    def process_request(self, request):
        
        if sfs_settings.FORCE_ALL_REQUESTS:
            return self.check_request_ip(request)
        
        def compile_paths(path_list):
            paths = []
            for path in path_list:
                if path.starts_with("/"):
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
        
        remote_ip = request.META['REMOTE_ADDR']
        
        if models.Cache.objects.filter(ip=remote_ip).count() > 0:
            if sfs_settings.LOG_SPAM:
                log = models.Log(message = "Spam received from %s" % remote_ip)
                log.save()
            return HttpResponseForbidden("Goodbye, spammer")
    
