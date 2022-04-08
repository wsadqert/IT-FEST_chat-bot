from aiogram import types, Bot, Dispatcher
from constants import info_text, hashtags, subscribe_text, contacts_text, group_ids
from tokens import TELEGRAM_TOKEN
import database as db

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# Create main menu markup
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons1: tuple[str, ...] = ("Подписаться", "Список подписок")
buttons2: tuple[str, ...] = ('Управление ботом', 'Наши контакты')
markup.add(*buttons1)
markup.add(*buttons2)

empty_markup = types.ReplyKeyboardRemove

section: str = 'main'


# Start/help
@dp.message_handler(commands=['start', 'help'])
async def start(message, res=False):
    if section == 'main':
        await bot.send_message(message.from_user.id, f"Привет, {message.from_user.first_name}! Вот что я умею:")
        await bot.send_message(message.from_user.id, info_text)
        await bot.send_message(message.from_user.id, "Для управления используй кнопки \U0001f447", reply_markup=markup)

        db.init_user(message.from_user.id)
    else:
        await bot.send_message(message.from_user.id, "Ошибка: бот уже запущен!")


async def subscribe(message):
    global section
    section = 'subscribe'

    async def help(message):
        if message.text.strip() == "Помощь":
            await bot.send_photo(message.from_user.id, 'hashtags.png')

    markup_hashtags = types.InlineKeyboardMarkup()
    for hashtag in hashtags:
        markup_hashtags.add(types.InlineKeyboardButton(text=hashtag, callback_data=hashtag[1:]))

    await bot.send_message(message.from_user.id, subscribe_text, reply_markup=markup_hashtags)

    for hashtag in hashtags:
        print(1234567890)
        # мне пришлось юзать `exec`; у меня не было выхода(((
        # простите пж(
        exec(f"""
@dp.callback_query_handler(text=hashtag[1:])
async def answer{hashtags.index(hashtag)}(call: types.CallbackQuery):
	try:
		cur.execute(f"UPDATE data SET {hashtag[1:]} = true WHERE user_id = {message.from_user.id}")
	except:
		await call.bot.send_message({message.from_user.id}, f'Произошла неизвестная ошибка!\u274c\U0001f937')
	else:
		await call.bot.send_message({message.from_user.id}, f'Поздравляю!\U0001f389\U0001f38a Ты успешно подписался на обновления группы вк {group_ids[hashtags.index(hashtag)]}по хэштегу {hashtag}')
	""")


async def unsubscribe(message):
    pass


async def my_subscriptions(message):
    for hashtag in hashtags:
        db.cur.execute(f"").fetchall()
        pass
    pass


@dp.message_handler(content_types=["text"])
async def main(message):
    global section
    if section == 'main':
        txt = message.text.strip()
        if txt == 'Подписаться':
            await subscribe(message)
        elif txt == 'Мои подписки':
            await my_subscriptions(message)
        elif txt == 'Управление ботом':
            await start(message)
        elif txt == 'Наши контакты':
            await bot.send_message(message.chat.id, contacts_text)

    section = 'main'

    # тут сделать бесконечный цикл, вставить парсер
    while True:
        pass
    pass
