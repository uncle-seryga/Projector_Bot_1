import sqlite3


class Database:
    _table_name = "database"
    _columns = []

    def __init__(self):
        self._connect = sqlite3.connect("data_base.db", check_same_thread=False)
        self._cursor = self._connect.cursor()

        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS apartments
                (apartment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                apartment_code TEXT UNIQUE)""")

        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS residents
                (resident_id INTEGER PRIMARY KEY AUTOINCREMENT,
                apartment_id INTEGER,
                tel_id INTEGER,
                ph_num TEXT,
                user_type INTEGER,
                FOREIGN KEY (apartment_id) REFERENCES apartments (apartment_id),
                FOREIGN KEY (user_type) REFERENCES types_of_users (user_type))""")

        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS requests(
                request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                apartment_id INTEGER,
                request_type TEXT,
                license_plate TEXT,
                time_of_requests TEXT,
                FOREIGN KEY (apartment_id) REFERENCES apartments (apartment_id))
        """)

        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS transport
                (transport_id INTEGER PRIMARY KEY AUTOINCREMENT,
                apartment_id INTEGER,
                transport_num TEXT,
                FOREIGN KEY (apartment_id) REFERENCES apartments (apartment_id)
            )
        """)

        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS types_of_users
                (user_type INTEGER PRIMARY KEY AUTOINCREMENT,
                type_name TEXT
            )
        """)

    def insert(self, **kwargs):
        pass

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass

    def select(self, **kwargs):
        pass


class Residents(Database):
    _table_name = 'residents'

    def insert(self, apartment_id, tel_id, ph_num, user_type=0):
        self._cursor.execute(
            f"""INSERT INTO {self._table_name} 
            (resident_id, apartment_id, tel_id, ph_num, user_type) VALUES (NULL,?,?,?,?)""",
            (apartment_id, tel_id, ph_num, user_type))
        self._connect.commit()

    def update(self, resident_id, apartment_id, tel_id, ph_num, user_type):
        self._cursor.execute(
            f"""UPDATE {self._table_name} SET apartment_id=?, tel_id=?, ph_num=?, user_type=? WHERE resident_id = ?""",
            (apartment_id, tel_id, ph_num, user_type, resident_id))
        self._connect.commit()

    def delete(self, resident_id):
        self._cursor.execute(F"""DELETE * FROM {self._table_name} WHERE resident_id = ?""", (resident_id,))
        self._connect.commit()

    def select(self, columns: list, resident_id):
        """
        :param columns: list, resident_id, apartment_id, tel_id, ph_num, user_type, *
        :param resident_id:
        :return:
        """
        return self._cursor.execute(f"""SELECT ({','.join(columns)}) FROM {self._table_name} WHERE resident_id = ?""",
                                    (resident_id,))
