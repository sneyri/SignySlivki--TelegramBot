from config import BOT_TOKEN

import telebot

from itd_utils import *
from database import *

bot = telebot.TeleBot(BOT_TOKEN)

users = {}

event_enabled = True

POST_URL = 'https://xn--d1ah4a.com/@sneyriii/post/2bedc019-0d3c-4e66-8148-8ec208c09c1f'

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.send_message(message.chat.id,
    '🌟 <b>ДОБРО ПОЖАЛОВАТЬ В СИГНЫ СЛИВКИ</b> 🌟\n\n'
    '📝 Бот для <b>сигн итд</b>. Для начала нужна регистрация.\n\n'
    '✅ Напишите <b>/register</b> и следуйте инструкции\n\n'
    '⚠️ ВНИМАНИЕ! Бот работает на моем пк и работоспособность бота зависит от моего соединения. К НЕСЧАСТЬЮ в данный период времени у меня плохо работает программа на 3 буквы, поэтому если бот вдруг перестал реагировать на команды СРАЗУ пишите создателю @SneyrIII\n\n'
    '❓ Если нужна помощь — напишите <b>/help</b>',
    parse_mode='HTML')

@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.send_message(message.chat.id,
    '📚 <b>ПОМОЩЬ ПО БОТУ</b> 📚\n\n'
    '<b>📌 КОМАНДЫ:</b>\n'
    '➡️ /start — приветственное сообщение\n'
    '➡️ /register — начать регистрацию\n'
    '➡️ /stop_register — остановить регистрацию\n'
    '➡️ /verify — верификация пользователя\n'
    '➡️ /get — получить сигну\n'
    '➡️ /upload_post — отправить пост с сигной\n'
    '➡️ /check_signa — проверить статус сигны\n'
    '➡️ /cancel — отменить отправку\n'
    '➡️ /help — эта справка\n\n'
    '📞 <b>Контакты:</b>\n'
    '👤 Разработчик: @SneyrIII\n'
    '💬 По всем вопросам обращаться к нему',
    parse_mode='HTML')

@bot.message_handler(commands=['register'])
def register_cmd(message):
    users[message.chat.id] = {
        'is_registered': True,
        'current_user': None,
        'current_user_avatar': None,
    }

    bot.send_message(message.chat.id,
    '📝 <b>РЕГИСТРАЦИЯ</b>\n\n'
    '✏️ Введите ваш <b>итд ник</b>\n\n'
    '⚠️ Убедитесь, что ник введен правильно.\n\n'
    '⚠️ Важное уточнение! Если при вводе вашего ника выводятся несколько пользователей то временно поменяйте отображаемое имя в ИТД! \n\n'
    '🛑 <b>/stop_register</b> — отменить регистрацию',
    parse_mode='HTML')

@bot.message_handler(commands=['stop_register'])
def stop_register_cmd(message):
    if message.chat.id and users:
        del users[message.chat.id]

    bot.send_message(message.chat.id,
    '⛔ <b>РЕГИСТРАЦИЯ ОСТАНОВЛЕНА</b> ⛔\n\n'
    '✅ Теперь вы можете писать сообщения',
    parse_mode='HTML')

@bot.message_handler(commands=['verify'])
def verify_cmd(message):
    if users.get(message.chat.id, False):
        current_user = users[message.chat.id]['current_user']
        current_user_avatar = users[message.chat.id]['current_user_avatar']

        if get_user(current_user):
            bot.send_message(message.chat.id,
            '🔐 <b>ВЕРИФИКАЦИЯ</b> 🔐\n\n'
            '❌ Вы уже зарегистрированы в системе',
            parse_mode='HTML')
        else:
            founded = findCode(current_user, 'сливки')

            if founded:
                add_user(current_user, current_user_avatar, message.chat.id)

                bot.send_message(message.chat.id,
                '✅ <b>ВЫ ЗАПИСАНЫ НА ИВЕНТ!</b> ✅\n\n'
                f'👤 <b>Ник:</b> {current_user}\n\n'
                '⏳ Ожидайте начала ивента.\n'
                '📖 Ознакомьтесь с правилами у разработчика.\n\n'
                'Если хотите отменить — напишите @SneyrIII',
                parse_mode='HTML')
            else:
                bot.send_message(message.chat.id,
                '🔐 <b>ВЕРИФИКАЦИЯ</b> 🔐\n\n'
                '⚠️ <b>Код не найден!</b>\n\n'
                'Проверьте, написали ли вы комментарий "<b>сливки</b>"\n'
                '📍 Под постом: ' + POST_URL,
                parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, '❌ Сначала пройдите <b>/register</b>', parse_mode='HTML')

@bot.message_handler(commands=['get'])
def get_cmd(message):
    if event_enabled == True:
        current_signa = get_current_signa(message.chat.id)
        
        if current_signa:
            bot.send_message(message.chat.id,
            f'📌 <b>АКТИВНАЯ СИГНА</b> 📌\n\n'
            f'👤 <b>Ваш пользователь:</b> {current_signa["username"]} {current_signa["avatar"]}\n\n'
            f'📝 <b>Текст поста:</b>\n'
            f'<code>#сигнысливки</code>\n\n'
            f'🔗 После публикации отправьте ссылку:\n'
            f'<b>/upload_post</b>',
            parse_mode='HTML')
        else:
            signa = get_signa(message.chat.id)
            
            if signa == None:
                bot.send_message(message.chat.id,
                '😔 <b>НЕТ ДОСТУПНЫХ УЧАСТНИКОВ</b> 😔\n\n'
                'К сожалению, не нашлось людей.\n'
                'Попробуйте позже.',
                parse_mode='HTML')
            else:
                bot.send_message(message.chat.id,
                f'🎯 <b>НОВАЯ СИГНА</b> 🎯\n\n'
                f'👤 <b>Вам выпал пользователь:</b>\n'
                f'{signa["username"]} {signa["avatar"]}\n\n'
                f'📝 <b>Текст для поста:</b>\n'
                f'<code>#сигнысливки</code>\n\n'
                f'📤 После публикации:\n'
                f'<b>/upload_post</b>',
                parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, '⏳ <b>Ивент еще не начался</b>', parse_mode='HTML')

@bot.message_handler(commands=['upload_post'])
def upload_post_cmd(message):
    signa = get_signa_username(message.chat.id)
    
    if not signa or signa == None or signa['signa_user'] == 'NOBODY':
        bot.send_message(message.chat.id, '❌ У вас нет активной сигны. Используйте <b>/get</b>', parse_mode='HTML')
        return
    
    if message.chat.id not in users:
        users[message.chat.id] = {}
    
    users[message.chat.id]['waiting_for_post'] = True
    users[message.chat.id]['signa_user'] = signa['signa_user']
    
    bot.send_message(message.chat.id,
    '📎 <b>РЕЖИМ ОТПРАВКИ ПОСТА</b> 📎\n\n'
    'Просто <b>отправьте ссылку</b> на ваш пост\n\n'
    '📋 <b>Пример:</b>\n'
    '<code>https://xn--d1ah4a.com/@user/post/123</code>\n\n'
    '🚫 <b>/cancel</b> — выйти из режима',
    parse_mode='HTML')

@bot.message_handler(commands=['cancel'])
def cancel_cmd(message):
    if message.chat.id in users and users[message.chat.id].get('waiting_for_post'):
        users[message.chat.id]['waiting_for_post'] = False
        bot.send_message(message.chat.id,
        '✅ Режим отправки <b>отменен</b>',
        parse_mode='HTML')
    else:
        bot.send_message(message.chat.id,
        '❌ Вы <b>не в режиме</b> отправки',
        parse_mode='HTML')

@bot.message_handler(func=lambda message: message.chat.id in users and users[message.chat.id].get('waiting_for_post'))
def handle_post_link(message):
    text = message.text.strip()
    post_id = None
    
    if '/post/' in text:
        post_id = text.split('/post/')[-1]
        post_id = post_id.split('?')[0].split('#')[0]
    else:
        bot.send_message(message.chat.id, 
        '❌ <b>ОШИБКА</b>\n\n'
        'Ссылка должна содержать <b>/post/</b>\n\n'
        'Отправьте правильную ссылку или <b>/cancel</b>',
        parse_mode='HTML')
        return
    
    signa_username = users[message.chat.id].get('signa_user')
    
    bot.send_message(message.chat.id, '⏳ <b>Проверяю пост...</b>', parse_mode='HTML')
    
    try:
        has_post = checkPost(post_id)
        
        if has_post:
            upload_post(post_id, message.chat.id)
            users[message.chat.id]['waiting_for_post'] = False
            
            bot.send_message(message.chat.id,
            '✅ <b>ПОСТ ПРИНЯТ</b> ✅\n\n'
            'Ваш пост <b>успешно сохранен</b>',
            parse_mode='HTML')
        else:
            bot.send_message(message.chat.id,
            f'❌ <b>ОШИБКА</b> ❌\n\n'
            f'Текст на посте <b>не соответствует</b>\n\n'
            f'Нужно написать:\n'
            f'<code>#сигнысливки</code>\n\n'
            f'Отправьте правильную ссылку или <b>/cancel</b>',
            parse_mode='HTML')
    except Exception as e:
        bot.send_message(message.chat.id, f'❌ <b>Ошибка:</b> {str(e)}', parse_mode='HTML')

@bot.message_handler(commands=['check_signa'])
def check_signa_cmd(message):
    user_data = get_user_by_id(message.chat.id)
    
    if not user_data or not user_data.get('username'):
        bot.send_message(message.chat.id,
        '❌ Сначала зарегистрируйтесь: <b>/register</b>',
        parse_mode='HTML')
        return
    
    username = user_data.get('username')
    
    result = check_signa_for_user(username)
    
    if not result:
        bot.send_message(message.chat.id,
        f'🔍 <b>ПРОВЕРКА СИГНЫ</b> 🔍\n\n'
        f'👤 <b>Пользователь:</b> {username}\n\n'
        '❌ Пока <b>никто не сделал</b> вам сигну\n'
        '💡 Ожидайте, когда вас получат в <b>/get</b>',
        parse_mode='HTML')
        return
    
    chat_id = result['chat_id']
    post_id = result['signa_url']
    
    user_info = db_query(
        'SELECT username, avatar FROM users WHERE chat_id = %s',
        (chat_id,),
        fetch=True
    )
    
    if user_info:
        post_url = f'https://xn--d1ah4a.com/@{user_info["username"]}/post/{post_id}'
        
        bot.send_message(message.chat.id,
        f'✅ <b>ВАМ СДЕЛАЛИ СИГНУ</b> ✅\n\n'
        f'👤 <b>От:</b> {user_info["username"]} {user_info["avatar"]}\n'
        f'🔗 <b>Ссылка на пост:</b>\n'
        f'<a href="{post_url}">▶ Открыть пост ◀</a>',
        parse_mode='HTML',
        disable_web_page_preview=True)
    else:
        bot.send_message(message.chat.id,
        f'✅ <b>ВАМ СДЕЛАЛИ СИГНУ</b> ✅\n\n'
        f'📝 ID поста: <code>{post_id}</code>',
        parse_mode='HTML')

@bot.message_handler()
def msg(message):
    user_data = users.get(message.chat.id)

    if user_data and user_data.get('is_registered'):
        search_query = message.text.strip()
        
        if not search_query:
            bot.send_message(message.chat.id,
            '❌ <b>Ошибка</b>\n\nВведите <b>ник</b> для поиска',
            parse_mode='HTML')
            return
        
        found_users = getUsers(search_query)

        if found_users:
            if len(found_users) == 1:
                user = found_users[0]
                bot.send_message(message.chat.id,
                f'✅ <b>ПОЛЬЗОВАТЕЛЬ НАЙДЕН</b> ✅\n\n'
                f'👤 <b>Ник:</b> <code>@{user.username}</code>\n'
                f'📛 <b>Имя:</b> <code>{user.display_name}</code>\n'
                f'🖼️ <b>Аватар:</b> {user.avatar}\n\n'
                f'📢 <b>ДЛЯ ПОДТВЕРЖДЕНИЯ</b>\n\n'
                f'Напишите комментарий:\n'
                f'<code>сливки</code>\n\n'
                f'📍 <b>Под этим постом:</b>\n'
                f'{POST_URL}\n\n'
                f'🔑 <b>После этого пропишите команду</b> <b>/verify</b>',
                parse_mode='HTML')

                users[message.chat.id]['current_user'] = user.username
                users[message.chat.id]['current_user_avatar'] = user.avatar
            else:
                user_list = ""
                for i, user in enumerate(found_users[:10], 1):
                    user_list += f'{i}. <b>@{user.username}</b> — <code>{user.display_name}</code>\n'
                
                if len(found_users) > 10:
                    user_list += f'\n...и еще <b>{len(found_users) - 10}</b> пользователей'
                
                bot.send_message(message.chat.id,
                f'🔍 <b>НАЙДЕНО ПОЛЬЗОВАТЕЛЕЙ:</b> {len(found_users)}\n\n'
                f'{user_list}\n\n'
                f'📝 <b>Уточните поиск</b>\n'
                f'🔄 Введите более точный ник или имя\n'
                f'🛑 <b>/stop_register</b> — отменить',
                parse_mode='HTML')
        else:
            bot.send_message(message.chat.id,
            f'❌ <b>ПОЛЬЗОВАТЕЛЬ НЕ НАЙДЕН</b> ❌\n\n'
            f'🔍 <b>Запрос:</b> <code>{search_query}</code>\n\n'
            f'💡 Проверьте <b>правильность написания</b>\n'
            f'📞 Свяжитесь с разработчиком: @SneyrIII\n\n'
            f'🛑 <b>/stop_register</b> — отменить',
            parse_mode='HTML')
    else:
        if message.text.startswith('/'):
            return
        
        bot.send_message(message.chat.id,
        '🌟 <b>Добро пожаловать!</b> 🌟\n\n'
        'Используйте <b>/register</b> для начала',
        parse_mode='HTML')

if __name__ == "__main__":
    bot.polling(none_stop=True)