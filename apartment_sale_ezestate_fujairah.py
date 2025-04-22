from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import signals

from scrapy import  signals
from General_Spider.spiders.GeneralSpider import GeneralSpider
from scrapy.utils.project import get_project_settings
import os
from scrapy.settings import Settings

def setup_crawler(domain):
    spider = GeneralSpider(attributesXMLFilePath=domain)
    settings = get_project_settings()
    Settings.set(settings, 'JOBDIR', "SeenFolders/Apartment/Sale/seen_apartment_sale_ezestate_fujairah")
    crawler = Crawler(spidercls = GeneralSpider ,settings = settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    #crawler.configure()
    crawler.crawl(domain)
    #crawler.start()


setup_crawler('Websites//ApartmentSale//EzestateFujairah//Items.xml')
#log.start()
reactor.run()