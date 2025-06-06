from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import signals
import logging
from scrapy import signals
from core.spiders.GeneralSpider import GeneralSpider
from scrapy.utils.project import get_project_settings
import os
from scrapy.settings import Settings

def setup_crawler(domain):
    spider = GeneralSpider(attributesXMLFilePath=domain)
    settings = get_project_settings()
    Settings.set(settings, 'JOBDIR', "SeenFolders/Apartment/Rent/seen_apartment_rent_districtuae")
    Settings.set(settings, 'LOG_FILE', "LogFiles/Apartment/Rent/apartments_rent_districtuae.log")
    Settings.set(settings, 'LOG_ENABLED', "TRUE")
    Settings.set(settings, 'LOG_LEVEL', "INFO")
    crawler = Crawler(spidercls = GeneralSpider ,settings = settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    #crawler.configure()
    crawler.crawl(domain)
    #crawler.start()


setup_crawler('Websites//ApartmentRent//DistrictUAE//Items.xml')
#log.start()
reactor.run()