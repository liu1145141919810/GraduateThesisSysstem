import psycopg2

# 连接数据库
def connect_db():
    try:
        conn = psycopg2.connect(database="db_evn", user="postgres", password="123", host="localhost", port="5432")
    except Exception as e:
        print("connect db error:", e)
    else:
        return conn
    return None

# 提交数据库语句并断开数据库连接
def close_db_connection(conn):
    conn.commit()  # 提交语句
    conn.close()   # 关闭与数据库的连接
    close_db_connection(conn)  # 提交并关闭连接
    print("successfully operation database")