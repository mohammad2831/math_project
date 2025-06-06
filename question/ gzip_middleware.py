import gzip
from io import BytesIO
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.utils.encoding import smart_bytes
import re

class GZipAPIResponseMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
    

        if re.match(r'^/question-app/\d+/$', request.path) or re.match(r'^/question-web/\d+/$', request.path):
            
            
               
            gzipped_buffer = BytesIO()
            gzipper = gzip.GzipFile(mode='wb', fileobj=gzipped_buffer)
            gzipper.write(smart_bytes(response.content))
            gzipper.close()
            response.content = gzipped_buffer.getvalue()
            response['Content-Encoding'] = 'gzip'
            response['Content-Length'] = len(response.content)
            return response
        else:
            return response