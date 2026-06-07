import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

config = DB_CONFIG

def create_connection():
    try:
        conn = mysql.connector.connect(**config)

        if conn.is_connected():
            return conn
    except Error as e:
        print(f'Ошибка при подключении к базе данных: {e}')
        return None

def db_query(query, values=None, fetch=False, fetch_all=False):
    conn = create_connection()
    
    if not conn:
        return None
    
    cursor = conn.cursor(dictionary=True, buffered=True)
    
    try:
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        
        result = None
        
        if fetch or fetch_all:
            if fetch_all:
                result = cursor.fetchall()
            else:
                result = cursor.fetchone()
            
            while cursor.nextset():
                pass
        
        if not fetch and not fetch_all:
            conn.commit()
            result = cursor.lastrowid
        
        return result
    except Error as err:
        print(f"Ошибка БД: {err}")
        if not fetch and not fetch_all:
            conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()