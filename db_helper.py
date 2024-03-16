import sqlite3 as sql


# error classes
class UsernameError(Exception):
    pass


# registration method
def registration(username: str, password: str, gender: str):
    print('!r method is working...')
    con = sql.connect('eedb.db')
    try:
        cur = con.cursor()
        if (cur.execute(f"""SELECT id FROM Users 
                                    WHERE name = '{username}'""").fetchall()):
            raise UsernameError
        cur.execute(f"""INSERT INTO Users (name, password, gender, level, dates) 
                                   VALUES ('{username}', '{password}', {int(gender)}, 0, '')""")
        con.commit()
        cur.close()
        con.close()
        print('!Success')
        return "!Success"
    except UsernameError:
        print('!Error')
        return "!UsernameError"
    except Exception as e:
        print('!Error')
        print(e)
        return "!DatabaseError"
    finally:
        if con:
            con.close()


def get_all_info(username):
    print("!gai method is working...")
    con = sql.connect('eedb.db')
    try:
        cur = con.cursor()
        info = cur.execute(f"""SELECT * FROM Users WHERE name = '{username}'""").fetchall()
        cur.close()
        con.close()
        print('!Success')
        return f'!gai {"!".join(map(str, list(info[0])))}'
    except Exception as e:
        print('!Error')
        print(e)
        return "!DatabaseError"
    finally:
        if con:
            con.close()


def update_image(username, image):
    print('!ui method is working...')
    con = sql.connect('eedb.db')
    try:
        cur = con.cursor()
        cur.execute(f"""UPDATE Users SET avatar = {image} WHERE name = {username}""")
        con.commit()
        cur.close()
        con.close()
        print("!Success")
        return '!Success'
    except Exception as e:
        print('!Error')
        print(e)
        return "!DatabaseError"
    finally:
        if con:
            con.close()


def update_progress(username, progress):
    print('!up method is working...')
    con = sql.connect('eedb.db')
    try:
        cur = con.cursor()
        cur.execute(f"""UPDATE Users SET dates = {progress} WHERE name = {username}""")
        con.commit()
        cur.close()
        con.close()
        print("!Success")
        return '!Success'
    except Exception as e:
        print('!Error')
        print(e)
        return "!DatabaseError"
    finally:
        if con:
            con.close()
