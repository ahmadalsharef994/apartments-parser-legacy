BOT_NAME = 'General_Spider'

SPIDER_MODULES = ['General_Spider.spiders']
NEWSPIDER_MODULE = 'General_Spider.spiders'
DUPEFILTER_CLASS = 'General_Spider.CustomFilter.CustomFilter'
FEED_EXPORTERS = {
    'jsonlines': 'scrapy.exporters.JsonLinesItemExporter',
}

FEED_FORMAT = 'jsonlines'
ITEM_PIPELINES = {
    'General_Spider.defaultAttributesPipeline.defaultAttributesPipeline':800,
    # 'General_Spider.pipelines.JsonWriterPipeline': 900,
    'General_Spider.pipelines.ActionsPipeline' : 700,
    'General_Spider.pipelines.Yzerproperty' : 690,
    #'General_Spider.pipelines.CordinatesPipeline' : 710,
    'General_Spider.pipelines.DubizzlePipeline': 701,
    'General_Spider.MasterDataPipeline.MasterDataPipeline' : 901,
    'General_Spider.pipelines.DataNormalisation': 702,
    # 'General_Spider.pipelines.AddCombinedField': 703,
}
DOWNLOADER_MIDDLEWARES = {
    'General_Spider.middlewares.CustomProxyMiddleware': 199,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 200
}

DOWNLOAD_DELAY = 1


REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
