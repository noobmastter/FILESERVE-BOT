import os
from aiohttp import web

async def index(request):
    return web.Response(text="Webhook is running!", status=200)

async def ping(request):
    return web.Response(text="pong", status=200)  # Responds with "pong"

async def web_server():
    app = web.Application()
    app.router.add_get("/", index)
    app.router.add_get("/ping", ping)  # Add this line
    return app
