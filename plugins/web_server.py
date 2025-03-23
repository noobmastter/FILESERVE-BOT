from aiohttp import web

async def index(request):
    return web.Response(text="Webhook is running!", status=200)

async def web_server():
    app = web.Application()
    app.router.add_get("/", index)

    # Use port 8000 for Koyeb health checks
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8000)
    await site.start()

    return app
