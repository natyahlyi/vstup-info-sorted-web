import aiohttp_jinja2
from aiohttp import web
from utils import get_rating

from urllib.parse import urlparse, urlunparse

from aiocache import MemcachedCache
from aiocache.serializers import PickleSerializer

cache = MemcachedCache(serializer=PickleSerializer,
                       endpoint="memcached"
                       )


class Home(web.View):
    @aiohttp_jinja2.template('index.html')
    async def get(self):

        return {}

    @aiohttp_jinja2.template('rating.html')
    async def post(self):
        data = await self.request.post()
        url = data.get('url', None)
        url_p = urlparse(url)
        netloc = url_p.netloc or url_p.path.split('/')[0]
        if url_p.scheme not in ('http', 'https'):
            url = 'http://' + urlunparse(url_p)
        if netloc not in ('www.vstup.info', 'vstup.info'):
            return {'invalid': True}
        if url:
            key = url_p.path
            data = await cache.get(key=key)
            if data is None:
                try:
                    data = await get_rating(url=url)
                except:
                    return {'invalid': True}
                await cache.set(key, data, 60 * 60 * 2)

            ctx = dict(records=data[0], s_title=data[1], stats=data[2], req_u=url)
            return ctx
        else:
            return {'invalid': True}
