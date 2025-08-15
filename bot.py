import logging
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# ====== Cấu hình bot và API ======
BOT_TOKEN = "8414943745:AAH8UWwNTlFcNTorL1SOt4FucwjCrhHY5b4"
CHAT_ID = "7523571828"
PARTNER_ID = "52763223825"
PARTNER_KEY = "fa5a0fca9bc968813195b6da5b64f7d8"

API_URL = "https://gachthe1s.com/chargingws/v2"

# ====== Khởi tạo bot ======
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# ====== Lệnh start ======
@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.reply("Xin chào! Gửi theo định dạng:\n`nhamang menhgia seri mathe`", parse_mode="Markdown")

# ====== Xử lý nạp thẻ ======
@dp.message_handler()
async def handle_card(message: types.Message):
    try:
        parts = message.text.strip().split()
        if len(parts) != 4:
            await message.reply("Sai định dạng!\nVí dụ: `viettel 10000 1234567890 9876543210`", parse_mode="Markdown")
            return

        telco, amount, serial, code = parts

        async with aiohttp.ClientSession() as session:
            payload = {
                "telco": telco,
                "amount": amount,
                "serial": serial,
                "code": code,
                "partner_id": PARTNER_ID,
                "sign": __import__("hashlib").md5(f"{PARTNER_KEY}{code}{serial}".encode()).hexdigest(),
                "command": "charging"
            }
            async with session.post(API_URL, data=payload) as resp:
                result = await resp.json()
                await message.reply(f"Kết quả: {result}")
    except Exception as e:
        await message.reply(f"Lỗi: {e}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)