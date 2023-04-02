import os
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
from scrapy.commands import ScrapyCommand
from scrapy.utils.python import without_none_values
from scrapy.exceptions import UsageError


class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Run many instances of a spider'

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_option('-a', '-a', metavar="NAME=VALUE", help="set spider argument (may be repeated)")
        parser.add_option('-f', '--input-file', metavar='FILE', help='file to load arguments from')
        parser.add_option('-o', '--output', metavar='FILE', help='dump scraped items into FILE (use - for stdout)')
        parser.add_option('-t', '--output-format', metavar='FORMAT', help='format to use for dumping items with -o')

    def process_options(self, args, opts):
        ScrapyCommand.process_options(self, args, opts)

    def run(self, args, opts):
        if args:
            raise UsageError()
        handle = opts.a
        names = handle.split(',')
        for name in names:
            if name.strip():
                self.crawler_process.crawl('Deepscrap', query=f"from:{name}")
        self.crawler_process.start()
