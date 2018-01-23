from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import signals
from scrapy import log
from scrapy import log, signals
from General_Spider.spiders.GeneralSpider import GeneralSpider
from scrapy.utils.project import get_project_settings
import os
from scrapy.settings import Settings

def setup_crawler(domain):
    spider = GeneralSpider(attributesXMLFilePath=domain)
    settings = get_project_settings()
    Settings.set(settings, 'JOBDIR', "SeenFolders/Apartment/Sale/seen_apartment_sale_propertyfinder")
    Settings.set(settings, 'LOG_FILE', "LogFiles/Apartment/Sale/apartments_sale_propertyfinder.log")
    Settings.set(settings, 'LOG_ENABLED', "TRUE")
    Settings.set(settings, 'LOG_LEVEL', "INFO")
    crawler = Crawler(spidercls=spider, settings=settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    # crawler.configure()
    # crawler.crawl(spider)
    crawler.crawl(domain)

setup_crawler('Websites//ApartmentSale//PropertyFinder//Items.xml')
# log.start()
reactor.run()