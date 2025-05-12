import asyncio

from django.conf import settings
from django.core.management.base import BaseCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
from sqlalchemy import create_engine, MetaData, select, update

DATABASE_URL = "postgresql://postgres:postgres@pg_db:5432/bot_db"

engine = create_engine(DATABASE_URL)
metadata = MetaData()
metadata.reflect(bind=engine)
custom_user_table = metadata.tables["subscriptions_customuser"]


async def start(update_tg: Update):
    telegram_id = update_tg.effective_user.id
    message_text = update_tg.message.text.strip()
    args = message_text.split()

    if len(args) < 2:
        await update_tg.message.reply_text("Пожалуйста, отправьте номер телефона после команды /start\nПример: /start +71234567890")
        return

    phone = args[1]

    with engine.connect() as conn:
        stmt = select(custom_user_table).where(custom_user_table.c.phone == phone)
        result = conn.execute(stmt).first()

        if result:
            upd = (
                update(custom_user_table)
                .where(custom_user_table.c.phone == phone)
                .values(telegram_id=telegram_id)
            )
            conn.execute(upd)
            conn.commit()
            await update_tg.message.reply_text("Вы успешно зарегистрированы в системе!")
        else:
            await update_tg.message.reply_text("Пользователь с таким номером телефона не найден.")

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.create_task(self.run_bot())
        loop.run_forever()

    async def run_bot(self):
        app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        await app.initialize()
        await app.start()
        await app.updater.start_polling()
