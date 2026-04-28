import os
import asyncio
import aiohttp
from aiohttp import web

BOTPRESS_TOKEN = os.environ.get("BOTPRESS_TOKEN")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

async def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    async with aiohttp.ClientSession() as session:
        await session.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text
        })

async def handle_webhook(request):
    data = await request.json()
    
    try:
        msg = data.get("payload", {}).get("text", "")
        if "COMANDĂ NOUĂ" in msg or "Comanda ta pentru" in msg:
            await send_telegram(f"🛍 COMANDĂ NOUĂ HydroPeptide\n\n{msg}")
    except:
        pass
    
    return web.Response(text="OK")

app = web.Application()
app.router.add_post("/webhook", handle_webhook)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, port=port)
