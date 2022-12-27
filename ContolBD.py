import sqlite3


class ControlDataBase:
    def __init__(self):
        self.con = sqlite3.connect('db_for_game.db', check_same_thread=False)  # подключение БД
        tabl1 = '''CREATE TABLE IF NOT EXISTS BestPlayers (
                   ID             INTEGER  PRIMARY KEY NOT NULL,
                   name           TEXT     NOT NULL,
                   time           DATETIME NOT NULL,
                   generation_key INTEGER);'''
        tabl2 = '''CREATE TABLE IF NOT EXISTS OpenWorlds (
    ID             INTEGER  PRIMARY KEY
                            NOT NULL
                            UNIQUE,
    time           DATETIME,
    generation_key INTEGER,
    name           STRING,
    x              INTEGER,
    y              INTEGER
);
'''
        self.con.execute(tabl1)
        self.con.execute(tabl2)
        self.con.commit()

    def add_world(self, name, time, generation_key, x, y, rud):
        self.con.cursor().execute(f'''INSERT INTO OpenWorlds (name, time, generation_key, x, y, rud) 
        VALUES ('{name}', '{time}', {generation_key}, {x}, {y}, {rud})''')
        self.con.commit()
        return self.get_worlds()[-1][0]

    def add_record(self, name, time, generation_key):
        self.con.cursor().execute(f'''INSERT INTO BestPlayers (name, time, generation_key) 
        VALUES ('{name}', '{time}', {generation_key})''')
        self.con.commit()

    def get_worlds(self):
        return self.con.cursor().execute(f'SELECT id, name, time, generation_key, x, y FROM OpenWorlds').fetchall()

    def get_record(self):
        return self.con.cursor().execute(f'SELECT name, time, generation_key FROM BestPlayers').fetchall()

    def is_name_world(self, name):
        return len(self.con.cursor().execute(f"""SELECT ID FROM OpenWorlds WHERE name='{name}'""").fetchall()) != 0

    def remove_time_world(self, name, time):
        self.con.cursor().execute(f'''UPDATE OpenWorlds SET time = '{time}' WHERE name = \'{name}\'''')
        self.con.commit()

    def get_info_of_name_world(self, name):
        return self.con.cursor().execute(f"""SELECT ID, generation_key, x, y, time, rud
         FROM OpenWorlds WHERE name='{name}'""").fetchone()

    def del_world(self, ID):
        self.con.cursor().execute(f'''DELETE from OpenWorlds WHERE ID = {ID}''')
        self.con.commit()

# control = ControlDataBase()
# control.add_world('II0', '100', 201)
# control.add_record('YY0', '200', 101)
# print(control.get_record())
# print(control.get_worlds())
# print(control.is_name_world('78'))
