import psycopg2
params={# it is the database I want
    'host': 'localhost',
    'database': 'Log_base',
    'user':'postgres',
    'password':'554775861',
    'port':5432
}
def connect_to_db(params):
    try:
        conn=psycopg2.connect(**params)
        #print("Database connection successful")
        return conn
    except psycopg2.Error as e:
        #print(f"Error connecting to database: {e}")
        return None
def close_connection(conn):
    if conn:
        conn.commit()
        conn.close()
def initialize(conn):
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS logs(id SERIAL PRIMARY KEY, " \
    "user_email VARCHAR(50)," \
    "user_name VARCHAR(50), log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP , " \
    "pwd VARCHAR(50))")
    cur.execute("INSERT INTO logs(user_email,user_name,pwd) VALUES(%s,%s,%s)",("dongxviu9@gmail.com","admin","123456"))
def operate(order,params,mail=None,user=None,pwd=None):
    conn=connect_to_db(params)
    cur=conn.cursor()
    if order=="signin":
        cur.execute("SELECT * FROM logs WHERE user_name=%s",(user,))
        result=cur.fetchone()
        if result:
            print("pwd db:",result[4]," pwd input:",pwd)
            if result[4]==pwd:
                #print("Login successfulxxxx")
                close_connection(conn)
                return True
            else:
                #print("Incorrect password")
                close_connection(conn)
                return False
        else:
            #print("User does not exist")
            close_connection(conn)
            return False
    elif order=="register":
        cur.execute("SELECT * FROM logs WHERE user_name=%s",(user,))
        result=cur.fetchone()
        if result:
            #print("User already exists")
            close_connection(conn)
            return False
        else:
            cur.execute("INSERT INTO logs(user_email,user_name,pwd) VALUES(%s,%s,%s)",(mail,user,pwd))
            #print("User registered successfully")
            close_connection(conn)
            return True
    elif order=="cancel":
        cur.execute("SELECT * FROM logs WHERE user_name=%s",(user,))
        result=cur.fetchone()
        if result:
            if result[4]==pwd:
               cur.execute("DELETE FROM logs WHERE user_name=%s",(user,))
               #print("User cancelled successfully")
               close_connection(conn)
               return True
            else:
                #print("Incorrect password")
                close_connection(conn)
                return False
        else:
            #print("User does not exist")
            close_connection(conn)
            return False
    close_connection(conn)
    return False
if __name__=="__main__":
    #test examples
    #operate(None,params)
    #print("====1====")
    #operate(None,params)
    #print("====2====")
    #operate("signin",params,"admin","123456")
    #print("====3====")
    #operate("register",params,"adminnn","123456")
    #print("====4====")
    #operate("cancel",params,"adminnn","123456")
    pass