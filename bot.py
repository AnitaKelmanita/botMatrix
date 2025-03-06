from nio import AsyncClient, LoginResponse
import asyncio
from datetime import datetime

# Настройки бота
HOMESERVER = "https://matrix.org"  # Сервер Matrix
BOT_USERNAME = "@bot8812:matrix.org"  # Логин бота
PASSWORD = "Bot8812))!!!!"  # Ваш пароль для авторизации
DEVICE_ID = "matrix_bot_8812"  # Уникальный ID устройства

# Чаты и соответствующие сообщения
ROOM_MESSAGES = {
    # "!wFqTIrwJqxJcCQuagM:matrix.org": ("11:00", "Good morning! Please call all your Appointments and update comments, and if you have Hot traffic - open Call everyday filter and call from there "),  # ESP
    # "!qBBbiNQAqkOOVqpQpl:matrix.org": ("11:00", "Good morning! Please call all your Appointments and update comments, and if you have Hot traffic - open Call everyday filter and call from there "),  # ENG
    # "!TvIFvXtrdTDFyaByFd:matrix.org": ("11:00", "Good morning! Please call all your Appointments and update comments, and if you have Hot traffic - open Call everyday filter and call from there "),  # PL
    # "!aAwTPgNEMgYwtFlkvv:matrix.org": ("11:00", "Доброе утро, обновите комментарии на Appointment "),  # RU    
    # "!SYNwohtdvpFkrntNoz:matrix.org": ("11:00", "Доброе утро, обновите комментарии на Appointment "),  # OUTSOURCE    
    # "!wFqTIrwJqxJcCQuagM:matrix.org": ("14:00", "Please call Hot traffic if you have n/ And update Appointments"),  # ESP
    # "!qBBbiNQAqkOOVqpQpl:matrix.org": ("14:00", "Please call Hot traffic if you have n/ And update Appointments"),  # ENG
    # "!TvIFvXtrdTDFyaByFd:matrix.org": ("14:00", "Please call Hot traffic if you have n/ And update Appointments"),  # PL
    "!wFqTIrwJqxJcCQuagM:matrix.org": ("19:30", "reminding to send your talk time"),  # ESP
    "!qBBbiNQAqkOOVqpQpl:matrix.org": ("19:30", "reminding to send your talk time"),  # ENG
    "!TvIFvXtrdTDFyaByFd:matrix.org": ("19:30", "reminding to send your talk time"),  # PL
    "!aAwTPgNEMgYwtFlkvv:matrix.org": ("19:30", "напоминаю отправить разговорное"),  # RU    
    "!SYNwohtdvpFkrntNoz:matrix.org": ("19:30", "напоминаю отправить разговорное")  # OUTSOURCE  
        }

class MatrixBot(AsyncClient):
    def __init__(self):
        super().__init__(HOMESERVER, BOT_USERNAME, device_id=DEVICE_ID)
        self.sent_today = set()

    async def start(self):
        try:
            response = await self.login(PASSWORD)
            if isinstance(response, LoginResponse):
                print("✅ Бот успешно авторизован!")
            else:
                print(f"❌ Ошибка при авторизации: {response}")
                return
            
            asyncio.create_task(self.send_auto_messages())
            print("🔄 Запуск синхронизации...")
            await self.sync_forever(timeout=30000)

        except Exception as e:
            print(f"❌ Ошибка при запуске бота: {e}")

    async def send_auto_messages(self):
        print("📢 Запущена авто-рассылка сообщений.")
        while True:
            now = datetime.now().strftime("%H:%M")
            
            for room_id, (time, message) in ROOM_MESSAGES.items():
                if now == time and (room_id, time) not in self.sent_today:
                    print(f"📨 Отправка сообщения в {room_id}: {message}")
                    try:
                        await self.room_send(
                            room_id,
                            message_type="m.room.message",
                            content={"msgtype": "m.text", "body": message}
                        )
                        self.sent_today.add((room_id, time))
                    except Exception as e:
                        print(f"❌ Ошибка при отправке сообщения в {room_id}: {e}")
            
            if now == "00:00":
                self.sent_today.clear()

            await asyncio.sleep(60)

async def main():
    bot = MatrixBot()
    await bot.start()

asyncio.run(main())
