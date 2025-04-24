from aiohttp import web

async def handle(request):
    return web.Response(text="✅ Бот активний!")

def web_app():
    app = web.Application()
    app.router.add_get("/", handle)
    return app
