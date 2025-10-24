import os
import psycopg2
import time

def connect(retries=5, delay=2):
    """
    Connects to Postgres, retrying if the database is not ready.
    :param retries: number of attempts
    :param delay: seconds to wait between attempts
    """
    while retries > 0:
        try:
            return psycopg2.connect(
                dbname=os.getenv("POSTGRES_DB", "postgres"),
                user=os.getenv("POSTGRES_USER", "postgres"),
                password=os.getenv("POSTGRES_PASSWORD", "password"),
                host=os.getenv("DB_HOST", "db"),
                port=os.getenv("DB_PORT", "5432")
            )
        except psycopg2.OperationalError:
            retries -= 1
            print(f"Postgres not ready, retrying in {delay} seconds... ({retries} attempts left)")
            time.sleep(delay)
    raise Exception("Could not connect to Postgres after several retries")

def create_table():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS to_do_list_table_username (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL
                )
            """)
            conn.commit()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS to_do_list_table_usertask (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    task_name VARCHAR(255) NOT NULL,
                    task_info TEXT,
                    task_date TIMESTAMP,
                    status BOOLEAN DEFAULT FALSE
                )
            """)
            conn.commit()

def get_or_create_user(username):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM to_do_list_table_username WHERE username = %s;", (username,))
            user = cur.fetchone()
            if user:
                return user[0]
            else:
                cur.execute("""
                    INSERT INTO to_do_list_table_username (username)
                    VALUES (%s)
                    RETURNING id;
                """, (username,))
                new_id = cur.fetchone()[0]
                conn.commit()
                return new_id

def add_users_task(users_task):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO to_do_list_table_usertask (username, task_name, task_info, task_date, status)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, username, task_name, task_info, task_date, status
            """, (
                users_task["username"],
                users_task["task_name"],
                users_task["task_info"],
                users_task["task_date"],
                users_task["task_status"],
            ))
            return cur.fetchone()

def get_users_task(username):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM to_do_list_table_usertask 
                WHERE username = %s
            """, (username,))
            return cur.fetchall()
