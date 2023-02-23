import sqlite3 as mc

def create_TB():
    conn = mc.connect("SPACE.db") 
    cursor = conn.cursor() 

    # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # q = "pragma table_info('score');"
    create_tb = "CREATE TABLE IF NOT EXISTS 'score' ( RANK INT NOT NULL PRIMARY KEY,PLAYER_NAME VARCHAR(15) NOT NULL,SCORE INT NOT NULL);"  
    cursor.execute(create_tb)
    # print("Table!")
    conn.commit()
    conn.close()
    
# create_TB()
