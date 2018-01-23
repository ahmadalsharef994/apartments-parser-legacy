import os
import re
from urlparse import urlparse
from scrapy.dupefilters import RFPDupeFilter
from scrapy.utils.request import request_fingerprint
import logging
class CustomFilter(RFPDupeFilter):
    def request_seen(self, request):
        fp = request.url
        if fp in self.fingerprints: #if this condition is true, we have visited this url before
            logging.log(logging.DEBUG, "Ignoring url=%r" % request.url)
            return True
        else: #if this condition is true, we are about to scrap a details page url
            self.fingerprints.add(fp)
            logging.log(logging.DEBUG, "Scrpaing url=%r" % request.url )
            if self.file:
                self.file.write(fp + os.linesep)
            return False 