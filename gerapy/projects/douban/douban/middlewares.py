import random
from douban.settings import USER_AGENT_LIST,PROXY_LIST

# 定义一个中间件类
class RandomUserAgent(object):
    # 随机ua
    def process_request(self,request,spider):
        ua = random.choice(USER_AGENT_LIST)
        request.headers["User-Agent"] = ua
class RandomProxy(object):
    # 随机ip
    def process_request(self,request,spider):
        proxy = random.choice(PROXY_LIST)
        print(proxy)
        request.meta['proxy'] = proxy['ip_port']
