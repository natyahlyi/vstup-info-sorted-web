import aiohttp_jinja2
from aiohttp import web
from .utils import prepare, process, get_rating

from urllib.parse import urlparse
# from aiocache import cached
from aiocache import MemcachedCache
from aiocache.serializers import PickleSerializer

cache = MemcachedCache(serializer=PickleSerializer, endpoint="memcached")


class Home(web.View):
    @aiohttp_jinja2.template('index.html')
    async def get(self):

        return {}

    @aiohttp_jinja2.template('rating.html')
    async def post(self):
        data = await self.request.post()
        url = data.get('url', None)
        url_p = urlparse(url)
        if url_p.netloc not in ('www.vstup.info', 'vstup.info'):
            return {'invalid': True}
        if url:
            key = url_p.path
            records = await cache.get(key=key)
            if records is None:
                records = await get_rating(url=url)
                await cache.set(key, records, 60 * 60 * 2)

            heads = ['№', '#', 'ПІБ', 'П', 'Σ', 'Д']
            ctx = dict(records=records, heads=heads, req_u=url)
            return ctx
        else:
            return {'invalid': True}
