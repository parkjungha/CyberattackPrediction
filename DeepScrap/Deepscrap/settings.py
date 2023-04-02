# -*- coding: utf-8 -*-

# !!! # Crawl responsibly by identifying yourself (and your website/e-mail) on the user-agent
USER_AGENT = 'Deepscrap'

# settings for spiders
BOT_NAME = 'Deepscrap'
LOG_FILE='log.txt'
LOG_LEVEL = 'WARNING'
DOWNLOAD_HANDLERS = {'s3': None,} # from http://stackoverflow.com/a/31233576/2297751, 

SPIDER_MODULES = ['Deepscrap.spiders']
NEWSPIDER_MODULE = 'Deepscrap.spiders'
ITEM_PIPELINES = {
    'Deepscrap.pipelines.JsonLinesPipeline':1,
}
FEED_FORMAT = 'jsonlines'
FEED_EXPORTERS = {
        'jsonlines': 'scrapy.contrib.exporter.JsonLinesItemExporter',
}
COMMANDS_MODULE = 'Deepscrap.commands'
# 크롤 결과를 저장할 디렉토리 지정
SAVE_USER_PATH = 'C:/Users/jungh/Desktop/getTweetText'