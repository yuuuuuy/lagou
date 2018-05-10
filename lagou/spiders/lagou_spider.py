import scrapy
import json
from lagou.items import LagouItem


class LaGouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']
    start_urls = ['https://www.lagou.com/']
    post_url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false'
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "www.lagou.com",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36",
        "Referer": "https://www.lagou.com/"}
    # 爬取热门城市招聘岗位
    city_list = ['北京',
                 '上海',
                 '广州',
                 '深圳',
                 '杭州',
                 '成都',
                 '南京',
                 '武汉',
                 '西安',
                 '厦门',
                 '长沙',
                 '苏州',
                 '天津',
                 '重庆',
                 '郑州']
    key_list = []  # 保存关键字信息 {'firsy_type': '后端开发', 'second_types': ['Java', 'Python']}
    total_page_count = None
    curpage = 1  # 当前页
    direction_index = 0  # 一级分类关下标
    key_index = 0   # 二级分类下标
    key_words = None  # 二级分类
    key = None  # 关键字
    city = None  # 城市关键字
    city_index = 0

    def parse(self, response):
        post_headers = self.headers.copy()

        post_headers.update({'Origin': 'https://www.lagou.com',
                             'Referer': 'https://www.lagou.com/jobs/list_'
                             })

        for sel in response.xpath("//div[@class='mainNavs']/div[1]/div[@class='menu_sub dn']/dl"):
            first_type = sel.xpath("dt/span/text()").extract()[0]  # 一级分类
            _temp_list = []
            for _type in sel.xpath("dd/a/text()").extract():  # 二级分类
                _temp_list.append(_type)
            self.key_list.append({'first_type': first_type, 'second_types': _temp_list[:-1]})

        self.key_words = self.key_list[self.direction_index]['second_types']
        self.key = self.key_words[self.key_index]
        self.city = self.city_list[self.city_index]
        yield scrapy.FormRequest.from_response(response,
                                               method='POST',
                                               url='{post_url}&city={city}'.format(
                                                   post_url=self.post_url,
                                                   city=self.city),
                                               headers=post_headers,
                                               formdata={'pn': str(self.curpage),
                                                         'first': 'true',
                                                         'kd': self.key},
                                               callback=self.parse_position)

    def parse_position(self, response):
        post_headers = self.headers.copy()

        post_headers.update({'Origin': 'https://www.lagou.com',
                             'Referer': 'https://www.lagou.com/jobs/list_'
                             })
        try:
            jdict = json.loads(response.body)
            print(jdict)
        except json.decoder.JSONDecodeError:
            yield scrapy.http.FormRequest(url='{post_url}&city={city}'.format(
                                                   post_url=self.post_url,
                                                   city=self.city),
                                          headers=post_headers,
                                          formdata={'pn': str(self.curpage),
                                                    'first': 'true',
                                                    'kd': self.key},
                                          dont_filter=True,
                                          callback=self.parse_position)

        if not jdict.get('success', None):
            print('Spiders are identified')
            yield scrapy.http.FormRequest(url='{post_url}&city={city}'.format(
                                                   post_url=self.post_url,
                                                   city=self.city),
                                          headers=post_headers,
                                          formdata={'pn': str(self.curpage),
                                                    'first': 'true',
                                                    'kd': self.key},
                                          dont_filter=True,
                                          callback=self.parse_position)
        else:
            item = LagouItem()
            jcontent = jdict['content']
            jposresult = jcontent["positionResult"]
            positions = jposresult["result"]
            for _position in positions:
                item['city'] = _position['city']  # 城市
                item['position_name'] = _position['positionName']  # 职位名称
                item['business_zones'] = _position['businessZones'] or ['']  # 工作区域
                item['company_full_name'] = _position['companyFullName']  # 公司全称
                item['company_short_name'] = _position['companyShortName']  # 公司简称
                item['company_lable_list'] = _position['companyLabelList'] or ['']  # 公司福利
                item['company_size'] = _position['companySize']  # 公司规模
                item['education'] = _position['education']  # 学历要求
                item['finance_stage'] = _position['financeStage'] or None  # 融资状况
                item['first_type'] = self.key_list[self.direction_index]['first_type']  # 一级分类
                item['industry_field'] = _position['industryField'] or None  # 公司领域
                item['job_nature'] = _position['jobNature'] or None  # 工作性质
                item['position_lables'] = _position['positionLables'] or ['']  # 职位标签
                item['salary'] = _position['salary']  # 薪资范围
                temp_list = _position['salary'].split('-')
                if len(temp_list) == 1:
                    item['salary_max'] = int(temp_list[0][:temp_list[0].find('k')])
                else:
                    item['salary_max'] = int(temp_list[1][:temp_list[1].find('k')])
                item['salary_min'] = int(temp_list[0][:temp_list[0].find('k')])
                item['salary_avg'] = (item['salary_max'] + item['salary_min']) / 2
                item['second_type'] = self.key
                item['work_year'] = _position['workYear']
                yield item
            if not self.total_page_count:
                self.total_page_count = jposresult['totalCount'] // 15 + 1
                print(self.total_page_count)
                # self.total_page_count = 30 if self.total_page_count > 30 else self.total_page_count
            if self.curpage < self.total_page_count - 1:
                self.curpage += 1
                print('Turn pages to ', self.curpage)
                yield scrapy.http.FormRequest(url='{post_url}&city={city}'.format(
                                                   post_url=self.post_url,
                                                   city=self.city),
                                              headers=post_headers,
                                              formdata={'pn': str(self.curpage),
                                                        'first': 'true',
                                                        'kd': self.key},
                                              callback=self.parse_position)
            elif self.city_index < len(self.city_list) - 1:
                self.city_index += 1
                self.curpage = 1
                self.key = self.key_words[self.key_index]
                self.city = self.city_list[self.city_index]
                print('Change the city to ', self.city)
                yield scrapy.http.FormRequest(url=self.post_url + '&city={}'.format(self.city),
                                              headers=post_headers,
                                              formdata={'pn': str(self.curpage),
                                                        'first': 'true',
                                                        'kd': self.key},
                                              callback=self.parse_position)
            elif self.key_index < len(self.key_words) - 1:
                self.curpage = 1
                self.key_index += 1
                self.city_index = 0
                self.city = self.city_list[self.city_index]
                self.key = self.key_words[self.key_index]
                print('Change the keyword to ', self.key)
                yield scrapy.http.FormRequest(url='{post_url}&city={city}'.format(
                                                   post_url=self.post_url,
                                                   city=self.city),
                                              headers=post_headers,
                                              formdata={'pn': str(self.curpage),
                                                        'first': 'true',
                                                        'kd': self.key},
                                              callback=self.parse_position)
            else:
                self.direction_index += 1
                self.curpage = 1
                self.city_index = 0
                self.key_index = 0
                self.key_words = self.key_list[self.direction_index]['second_types']
                self.city = self.city_list[self.city_index]
                self.key = self.key_words[self.key_index]
                yield scrapy.http.FormRequest(url='{post_url}&city={city}'.format(
                                                   post_url=self.post_url,
                                                   city=self.city),
                                              headers=post_headers,
                                              formdata={'pn': str(self.curpage),
                                                        'first': 'true',
                                                        'kd': self.key},
                                              callback=self.parse_position)
