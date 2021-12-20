import sqlite3

def create_db():
    con=sqlite3.connect(database=r'SRM.db')
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS course(cid INTEGER PRIMARY KEY AUTOINCREMENT,name text,duration text,charges text,description text)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS student(roll INTEGER PRIMARY KEY AUTOINCREMENT,name text,email text,gender text,contact text,admission text,course text,state text,city text,address text)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS resulting(rid INTEGER PRIMARY KEY AUTOINCREMENT,roll text,name text,course text,marks text,full_marks text,per text)")
    con.commit()
    con.close()
create_db()