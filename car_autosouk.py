from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import  signals
from General_Spider.spiders.GeneralSpider import GeneralSpider
from scrapy.utils.project import get_project_settings
import os
from scrapy.settings import Settings

def setup_crawler(domain):
    spider = GeneralSpider(attributesXMLFilePath=domain)
    settings = get_project_settings()
    Settings.set(settings, 'JOBDIR', "SeenFolders/Car/Sale/seen_car_autosouk")
    Settings.set(settings, 'LOG_FILE', "LogFiles/Car/Sale/cars_autosouk.log")
    Settings.set(settings, 'LOG_LEVEL', "DEBUG")
    crawler = Crawler(spidercls = spider ,settings = settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    #crawler.configure()
    crawler.crawl(domain)
#crawler.starts()

setup_crawler('Websites//Cars//Autosouk//Items.xml')
#log.start()
reactor.run()