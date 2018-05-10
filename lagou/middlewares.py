# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
import requests
from scrapy import signals
from fake_useragent import UserAgent  # 提供随机的UserAgent
from lagou.proxies import Proxy
from lagou.settings import API_URL


class RandomUserAgentMiddleware(object):
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)

        user_agent_random = get_ua()
        request.headers.setdefault('User-Agent', user_agent_random)


class ProxyMiddleWare(object):
    PROXIES = None

    def get_proxies(self):
        pro = Proxy()
        ProxyMiddleWare.PROXIES = ["{protocol}://{ip}:{port}".format(
            protocol=proxy_tuple[-1].lower(),
            ip=proxy_tuple[0],
            port=proxy_tuple[1]) for proxy_tuple in pro.get_access_ip(size=200)]

    # def get_random_proxy(self):
    #     if not ProxyMiddleWare.PROXIES:
    #         self.get_proxies()
    #     # proxy_tuple = random.choice(ProxyMiddleWare.PROXIES)
    #     # proxy = "{protocol}://{ip}:{port}".format(protocol=proxy_tuple[-1].lower(), ip=proxy_tuple[0],
    #     #                                           port=proxy_tuple[1])
    #     return random.choice(ProxyMiddleWare.PROXIES)
    def get_random_proxy_from_api(self):
        return 'http://' + requests.get('http://{api_url}/get/'.format(api_url=API_URL)).content.decode("utf-8")

    def get_random_proxy_from_txt(self):
        if not ProxyMiddleWare.PROXIES:
            with open('F:\GraduationProject\lagou\lagou\proxies.txt', 'r') as f:
                ProxyMiddleWare.PROXIES = f.readlines()
        proxy = random.choice(ProxyMiddleWare.PROXIES).strip()
        return 'https://' + proxy

    def process_request(self, request, spider):
        if request.method.lower() == 'get':
            return None
        # proxy = self.get_random_proxy_from_txt()
        proxy = self.get_random_proxy_from_api()
        print("this is request ip:" + proxy)
        request.meta['proxy'] = proxy
        request.meta['download_timeout'] = 10

    def process_response(self, request, response, spider):
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            # proxy = self.get_random_proxy_from_txt()
            proxy = self.get_random_proxy_from_api()
            print("this is response ip:" + proxy)
            request.meta['proxy'] = proxy
            return request
        return response


class LagouSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class LagouDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
