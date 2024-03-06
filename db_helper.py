import sqlite3 as sql


class UsernameError(Exception):
    pass


con = sql.connect('eedb.db')
cur = con.cursor()


def registration(username: str, password: str, gender: str):
    try:
        if not (cur.execute(f"""SELECT id FROM Users 
                                    WHERE name = '{username}'""")):
            raise UsernameError
        cur.execute(f"""INSERT INTO Users (name, password, gender, level, dates) 
                                   VALUES ('{username}', '{password}', {int(gender)}, 0, '')""")
        return "!Success"
    except UsernameError:
        return "!UsernameError"
    except Exception as e:
        print(e)
        return "!DatabaseError"
