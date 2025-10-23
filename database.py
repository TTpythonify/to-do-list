import psycopg2

def connect():
    return psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='12345',
        host='localhost',
        port='5432'
    )

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


def get_or_create_user(username):
    with connect() as conn:
        with conn.cursor() as cur:
            # Try to find existing user
            cur.execute("SELECT id FROM to_do_list_table_username WHERE username = %s;", (username,))
            user = cur.fetchone()
            
            if user:
                return user[0]  # Return existing user ID
            else:
                # Insert new user
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
                INSERT INTO to_do_list_table_usertask (username,task_name,task_info,task_date,status)
                VALUES (%s,%s,%s,%s,%s)
                """, (
                    users_task["username"],
                    users_task["task_name"],
                    users_task["task_info"],
                    users_task["task_date"],
                    users_task["task_status"],
                ))


def get_users_task(username):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM to_do_list_table_usertask 
                WHERE username = %s
                """, (username,))
            items = cur.fetchall()
            return items 