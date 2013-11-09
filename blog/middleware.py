#coding:utf-8
import time
import logging

from utils.cache import cache

logger = logging.getLogger(__name__)


class OnlineMiddleware(object):
    print("=============================================================middeware is comeing now")
    start_time= time.time()
    def process_request(self, request):
        self.start_time = time.time()

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        处理当前在线人数
        整个逻辑很简单，每一个用户访问，我都会把用户的ip作为key放到memcache，然后有一个 online_ips 的key，用来存放所有的ip。
        每次请求都会进行如下步骤，先取出 online_ips的所有值，然后再根据这个这个list来从memcache中取出依然存在的ip，
        然后再次存入 online_ips 。
        """
        http_user_agent = request.META.get('HTTP_USER_AGENT')
        if 'Spider' in http_user_agent or 'spider' in http_user_agent:
            return

        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        online_ips = cache.get("online_ips", [])

        if online_ips:
            online_ips = cache.get_many(online_ips).keys()

        cache.set(ip, 0, 5 * 60)

        if ip not in online_ips:
            online_ips.append(ip)

        cache.set("online_ips", online_ips)

    def process_response(self, request, response):
        cast_time = time.time() - self.start_time
        response.content = response.content.replace('<!!LOAD_TIMES!!>', str(cast_time)[:5])
        return response
