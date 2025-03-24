import os
from aiohttp import web

# Get the PORT from environment (default: 8000)
PORT = int(os.getenv("PORT", 8000))

async def index(request):
    """ Health check endpoint for Koyeb """
    return web.Response(text="Webhook is running!", status=200)

async def start_web_server():
    """ Starts the aiohttp web server for webhook handling """
    app = web.Application()
    app.router.add_get("/", index)  # Health check route

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()

    return app  # Returning app in case it's needed elsewhere
