import os
from aiohttp import web

async def index(request):
    return web.Response(text="Webhook is running!", status=200)

async def web_server():
    app = web.Application()
    app.router.add_get("/", index)
    return app  # Return app instance instead of running it
