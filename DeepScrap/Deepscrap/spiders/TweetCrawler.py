from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy import http
from scrapy.shell import inspect_response  # for debugging
import re
import json
import time
import logging
from lxml import html
import urllib.parse
from random import seed
from random import randint

try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+

from datetime import datetime
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

from Deepscrap.items import Tweet, User

logger = logging.getLogger(__name__)


class Deepscrap(CrawlSpider):
    name = 'Deepscrap'
    allowed_domains = ['twitter.com']

    def __init__(self, query='', lang='', crawl_user=False, top_tweet=False):
        # print(query)
        self.name = query.replace('from:', '')
        self.start = time.time()
        super(CrawlSpider, self)
        self.query = query
        self.tweetcount = 0
        self.url = "https://twitter.com/i/search/timeline?l={}".format(lang)
        # self.url = "https://twitter.com/search?vertical=default&q={}".format(lang)
        if not top_tweet:
            self.url = self.url + "&f=tweets"

        self.url = self.url + "&q=%s&src=typed&max_position=%s"

        self.crawl_user = crawl_user

    def start_requests(self):
        url = self.url % (quote(self.query), '')
        # seed(1)
        # value=randint(10,15)
        # time.sleep(value)
        print("userID start")
        self.tweetcount = 0
        yield http.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        # inspect_response(response, self)
        # handle current page
        # print(response.body)
        data = json.loads(response.body.decode("utf-8"))

        for item in self.parse_tweets_block(data['items_html']):
            yield item

        # get next page
        min_position = data['min_position']
        min_position = min_position.replace("+", "%2B")
        url = self.url % (quote(self.query), min_position)
        seed(1)
        value = randint(1, 1)
        time.sleep(value)
        print(url)
        yield http.Request(url, callback=self.parse_page)

    def parse_tweets_block(self, html_page):
        page = Selector(text=html_page)

        ### for text only tweets
        items = page.xpath('//li[@data-item-type="tweet"]/div')
        for item in self.parse_tweet_item(items):
            yield item

    def parse_tweet_item(self, items):
        for item in items:
            try:
                self.tweetcount = self.tweetcount + 1

                tweet = Tweet()
                tweet['usernameTweet'] = \
                item.xpath('.//span[@class="username u-dir u-textTruncate"]/b/text()').extract()[0]
                ID = item.xpath('.//@data-tweet-id').extract()
                if not ID:
                    self.tweetcount = self.tweetcount - 1
                    continue
                tweet['ID'] = ID[0]

                ### get text content
                p_txt = item.xpath('.//div[@class="js-tweet-text-container"]/p').extract()
                p_txt = " ".join(p_txt)
                p = html.fromstring(p_txt)
                a_links = p.xpath("//p/a")
                for a in a_links:
                    if 'twitter-atreply' in a.attrib['class']:
                        # user tag
                        txt = "@" + a.attrib['href'].split("/")[1]
                        for child in list(a):
                            a.remove(child)
                        a.text = txt
                    elif 'twitter-hashtag' in a.attrib['class']:
                        # hash tag
                        txt = urllib.parse.unquote(a.attrib['href'])
                        txt = "#" + txt.split("?")[0].split("/")[2]
                        for child in list(a):
                            a.remove(child)
                        a.text = txt
                    elif 'twitter-timeline-link u-hidden' in a.attrib['class']:
                        # twitter redirect url whitespace
                        # txt = ' '.join([child.text for child in list(a)])
                        txt = ''
                        for child in list(a):
                            if child.text is not None:
                                txt += child.text
                            a.remove(child)
                        a.text = txt
                    elif 'twitter-timeline-link' in a.attrib['class'] and 'data-expanded-url' in a.attrib:
                        # embedded url in raw text
                        txt = a.attrib['data-expanded-url']
                        for child in list(a):
                            a.remove(child)
                        a.text = txt
                text = p.xpath("//p//text()")
                tweet['text'] = ' '.join(text)
                # print(tweet['text'])
                if tweet['text'] == '':
                    # If there is not text, we ignore the tweet
                    self.tweetcount = self.tweetcount - 1
                    continue

                tweet['datetime'] = datetime.fromtimestamp(int(
                    item.xpath('.//div[@class="stream-item-header"]/small[@class="time"]/a/span/@data-time').extract()[
                        0])).strftime('%Y-%m-%d %H:%M:%S')

                ### get photo
                has_cards = item.xpath('.//@data-card-type').extract()
                if has_cards and has_cards[0] == 'photo':
                    tweet['has_image'] = True
                    tweet['images'] = item.xpath('.//*/div/@data-image-url').extract()
                elif has_cards:
                    logger.debug('Not handle "data-card-type":\n%s' % item.xpath('.').extract()[0])

                ### get animated_gif
                has_cards = item.xpath('.//@data-card2-type').extract()
                if has_cards:
                    if has_cards[0] == 'player':
                        tweet['has_video'] = True
                        tweet['videos'] = item.xpath('.//*/source/@video-src').extract()
                    elif has_cards[0] == 'summary_large_image':
                        tweet['has_media'] = True
                        tweet['medias'] = item.xpath('.//*/div/@data-card-url').extract()
                    elif has_cards[0] == 'amplify':
                        tweet['has_media'] = True
                        tweet['medias'] = item.xpath('.//*/div/@data-card-url').extract()
                    elif has_cards[0] == 'summary':
                        tweet['has_media'] = True
                        tweet['medias'] = item.xpath('.//*/div/@data-card-url').extract()
                    elif has_cards[0] == 'animated_gif':
                        tweet['has_media'] = True
                        tweet['medias'] = item.xpath('.//*/div/@data-card-url').extract()
                    elif has_cards[0] == '__entity_video':
                        pass  # TODO
                        # tweet['has_media'] = True
                        # tweet['medias'] = item.xpath('.//*/div/@data-src').extract()
                    else:  # there are many other types of card2 !!!!
                        logger.debug('Not handle "data-card2-type":\n%s' % item.xpath('.').extract()[0])
                        # tweet['has_media'] = True
                        # tweet['medias'] = item.xpath('.//.*/div/@data-card-url').extract()

                yield tweet

                if self.crawl_user:
                    ### get user info
                    user = User()
                    user['ID'] = tweet['user_id']
                    user['name'] = item.xpath('.//@data-name').extract()[0]
                    user['screen_name'] = item.xpath('.//@data-screen-name').extract()[0]
                    user['avatar'] = \
                        item.xpath('.//div[@class="content"]/div[@class="stream-item-header"]/a/img/@src').extract()[0]
                    yield user
                print("\t tweetcount = ", self.tweetcount)
            except:
                logger.error("Error tweet:\n%s" % item.xpath('.').extract()[0])
                # raise
        logger.warning(f'tweetcount = {self.tweetcount}')

    def extract_one(self, selector, xpath, default=None):
        extracted = selector.xpath(xpath).extract()
        if extracted:
            return extracted[0]
        return default

