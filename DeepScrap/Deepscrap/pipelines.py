# -*- coding: utf-8 -*-
import os
from scrapy.exceptions import DropItem
import logging
import json
import time

from scrapy import signals
from Deepscrap.items import Tweet, User
from Deepscrap.utils import mkdirs
from scrapy.exporters import JsonLinesItemExporter
from scrapy.utils.project import get_project_settings
settings =get_project_settings()

logger = logging.getLogger(__name__)
class JsonLinesPipeline(object):
    def __init__(self):
        self.files = {}
      

    def open_spider(self, spider):
        print(spider.name, 'open spider')
        self.name = spider.name
        print(self.name)
        self.time = spider.start
        self.saveUserPath = settings['SAVE_USER_PATH']
        mkdirs(self.saveUserPath)
        
        file = open(f'{self.saveUserPath}/{self.name}.json', 'wb')
        self.files[spider] = file
        
        self.exporter = JsonLinesItemExporter(file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()
    
    def close_spider(self, spider):
        print(spider.name, self.name)
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()
        logger.warning(f'{self.name} finish {time.time() - self.time}')

    def process_item(self, item, spider):
        if item['usernameTweet'] == self.name:
            self.exporter.export_item(item)
            return item
