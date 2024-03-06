import sqlite3 as sql


class UsernameError(Exception):
    pass


def registration(username: str, password: str, gender: str):
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
        return "!Success"
    except UsernameError:
        return "!UsernameError"
    except Exception as e:
        print(e)
        return "!DatabaseError"
    finally:
        if con:
            con.close()
