import re
import requests
from peewee import PostgresqlDatabase
import time
from lagou.settings import DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD


class Proxy(object):
    first_insert = None

    def __init__(self):
        self.req = requests.Session()
        self.headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Referer': 'http://www.xicidaili.com/nn/',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Ubuntu Chromium/60.0.3112.113 Chrome/60.0.3112.113 Safari/537.36'}
        self.proxyHeaders = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Ubuntu Chromium/60.0.3112.113 Chrome/60.0.3112.113 Safari/537.36',
        }
        self.db = PostgresqlDatabase(database=DB_DATABASE,
                                     host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     autocommit=True,
                                     autorollback=True)

    def get_page(self, url):
        page = self.req.get(url, headers=self.headers).text
        return page

    def parse_page(self, text):
        time.sleep(2)
        pattern = re.compile('<tr class=".*?">.*?<td class="country">'
                             '<img.*?/></td>.*?<td>(\d+\.\d+\.\d+\.\d+)</td>.*?<td>(\d+)</td>.*?'
                             '<td>.*?'
                             '<a href=".*?">(.*?)</a>.*?'
                             '</td>.*?'
                             '<td class="country">(.*?)</td>.*?'
                             '<td>([A-Z]+)</td>.*?'
                             '</tr>',
                             re.S)
        return re.findall(pattern, text)

    def get_url(self, page_num):
        url = 'http://www.xicidaili.com/nn/'+str(page_num)
        return url

    def insert(self, datas):
        print("插入{}条".format(len(datas)))
        for data in datas:
            self.db.execute_sql("INSERT INTO ipool(ip,port,protocol) "
                                "VALUES ('{ip}','{port}','{protocol}')".
                                format(ip=data[0], port=data[1], protocol=data[-1]))

    def select_all(self):
        cursor = self.db.execute_sql("SELECT * FROM ipool")
        datas = cursor.fetchall()
        return datas

    def get_access_ip(self, size=1):
        results = self.select_all()
        available_ips = []
        for i in results:
            if len(available_ips) == size:
                return available_ips
            try:
                self.req.get("https://www.lagou.com/", proxies={
                    "{}".format(i[2]): "{}://{}:{}".format(i[2], i[0], i[1])},
                             timeout=5)
                print('Ip available')
                available_ips.append(i)
            except Exception:
                print("{} is valid".format(i))
        print(available_ips)

    def get_newip_to_db(self, clear_old_data=False):
        if clear_old_data:
            self.db.execute_sql("DELETE FROM ipool")

        for i in range(10):
            page = self.get_page(self.get_url(i))
            p.insert(self.parse_page(page))


if __name__ == '__main__':
    p = Proxy()
    p.get_newip_to_db(clear_old_data=True)
    # print(p.get_access_iP(size=10))
