from database_utils import db_query
import random

def get_signa_username(chat_id):
    username = db_query(
        "SELECT signa_user FROM users WHERE chat_id = %s",
        (chat_id,),
        fetch=True)
    
    if username:
        return username
    else:
        return None

def check_signa(chat_id):
    has_signa = db_query(
        "SELECT * FROM users WHERE chat_id = %s AND signa_user = 'NOBODY'",
        (chat_id,),
        fetch=True)
    
    if has_signa:
        return True
    else:
        return False

def get_signa(chat_id):
    users = db_query(
        'SELECT * FROM users WHERE used = 0 AND chat_id != %s',
        (chat_id,),
        fetch_all=True
    )

    if not users or len(users) <= 0:
        return None
    
    user = random.choice(users)

    db_query('UPDATE users SET used = 1 WHERE username = %s', (user['username'],))
    db_query('UPDATE users SET signa_user = %s WHERE chat_id = %s', (user['username'], chat_id))

    return user

def get_signa_without_update(chat_id):
    result = db_query(
        'SELECT signa_user FROM users WHERE chat_id = %s AND signa_user != "NOBODY"',
        (chat_id,),
        fetch=True
    )
    
    if result and result.get('signa_user'):
        user = db_query(
            'SELECT username, avatar FROM users WHERE username = %s',
            (result['signa_user'],),
            fetch=True
        )
        return user
    return None

def get_current_signa(chat_id):
    result = db_query(
        'SELECT signa_user FROM users WHERE chat_id = %s',
        (chat_id,),
        fetch=True
    )
    
    if result and result.get('signa_user') and result['signa_user'] != 'NOBODY':
        user = db_query(
            'SELECT username, avatar FROM users WHERE username = %s',
            (result['signa_user'],),
            fetch=True
        )
        return user
    return None

def get_user_by_id(chat_id):
    return db_query(
        'SELECT * FROM users WHERE chat_id = %s',
        (chat_id,),
        fetch=True
    )

def get_user(username):
    return db_query(
        'SELECT * FROM users WHERE username = %s',
        (username,),
        fetch=True
    )

def add_user(user, avatar, chat_id):
    db_query('INSERT INTO users (username, avatar, used, chat_id, signa_user) VALUES (%s, %s, %s, %s, %s)', 
             (user, avatar, 0, chat_id, 'NOBODY'))
    
def upload_post(post_id, chat_id):
    db_query('UPDATE users SET signa_url = %s WHERE chat_id = %s', (post_id, chat_id))

def check_signa_for_user(username):
    result = db_query(
        'SELECT chat_id, signa_url FROM users WHERE signa_user = %s AND signa_url != "NONE"',
        (username,),
        fetch=True
    )
    
    if result and result.get('signa_url') and result['signa_url'] != 'NONE':
        return result
    return None