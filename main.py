from aiohttp import web
from datetime import datetime
import json

ads = []

routes = web.RouteTableDef()

@routes.get('/ads')
async def handle_ads_get(request):
    return web.json_response(ads)

@routes.post('/ads')
async def handle_ads_post(request):
    new_ad = await request.json()
    new_ad['id'] = len(ads) + 1
    new_ad['date'] = str(datetime.now())
    ads.append(new_ad)
    return web.json_response(new_ad, status=201)

@routes.delete('/ads/{ad_id}')
async def handle_ad_delete(request):
    ad_id = int(request.match_info['ad_id'])
    for ad in ads:
        if ad['id'] == ad_id:
            ads.remove(ad)
            return web.json_response({'message': f'ad {ad_id} has been deleted.'})

    return web.json_response({'error': 'ad not found'}, status=404)

app = web.Application()
app.add_routes(routes)
web.run_app(app)
