from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log
from scrapy import log, signals
from General_Spider_code_version_7.spiders.AltimateSpider import AltimateSpider
from scrapy.utils.project import get_project_settings
import os
from scrapy.settings import Settings

def setup_crawler(domain):
    spider = AltimateSpider(attributesXMLFilePath=domain)
    settings = get_project_settings()
    Settings.set(settings, 'JOBDIR', "SeenFolders/Car/Sale/seen_car_yallamotor")
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()

setup_crawler('Websites/Cars/Yallamotor/Items.xml')
log.start()
reactor.run()
