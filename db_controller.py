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

    def check_if_resident(self, tel_id):
        list_tel_id = self.select(['tel_id'], key_word='tel_id', value=tel_id)
        return False if list_tel_id == [] else True

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

    def select(self, columns: list, key_word: str, value):
        """
        :param columns: list; resident_id, apartment_id, tel_id, ph_num, user_type, *
        :param resident_id:
        :return:
        """
        return self._cursor.execute(f"""SELECT ({','.join(columns)}) FROM {self._table_name} WHERE {key_word} = ?""",
                                    (value,)).fetchall()


class Transport(Database):
    _table_name = 'transport'

    def select(self, columns: list, key_word: str, value):
        """
        :param columns: list, transport_id, apartment_id, transport_num, *
        :param key_word: str, transport_id, apartment_id, transport_num
        :param value:
        :return:
        """
        return self._cursor.execute(
            f"""SELECT {','.join(columns)} FROM {self._table_name} WHERE {key_word} = ?""",
            (value,)).fetchall()

    def update(self, transport_num_old: str, transport_num_new: str):
        self._cursor.execute(f"""UPDATE {self._table_name}
                                SET transport_num = ?
                                WHERE transport_num = ?""", (transport_num_new.lower(), transport_num_old.lower(),))
        self._connect.commit()

    def delete(self, key_word: str, value):
        """
        :param key_word: str, transport_id, apartment_id, transport_num
        :param value:
        """

        self._cursor.execute(f'''DELETE FROM {self._table_name}
                                WHERE {key_word} = ?''', (value,))
        self._connect.commit()

    def insert(self, apartment_id: int, transport_num: str):
        all_transport = self.select(['transport_num', ], 'apartment_id', apartment_id)
        valid_apartment_id = self._cursor.execute("""SELECT * FROM apartments
                                                    WHERE apartment_id = ?""", (apartment_id,)).fetchone()
        if valid_apartment_id:
            if len(all_transport) <= 5:
                self._cursor.execute(f"""INSERT INTO {self._table_name} (apartment_id, transport_num) VALUES (?,?)""",
                                     (apartment_id, transport_num,))
                self._connect.commit()
            else:
                # todo change to answer, not an error
                raise ValueError("Transport limit exceeded. Must be 5 or less per one apartment_id.")
        else:
            raise ValueError("Invalid apartment_id")


class TypesOfUsers(Database):
    _table_name = 'types_of_users'

    def insert(self, type_name):
        self._cursor.execute(f"INSERT INTO {self._table_name} (user_type, type_name) VALUES (NULL, ?)", (type_name,))
        self._connect.commit()

    def update(self, user_type, type_name):
        self._cursor.execute(f"UPDATE {self._table_name} SET type_name=? WHERE user_type=?", (type_name, user_type,))
        self._connect.commit()

    def delete(self, user_type):
        self._cursor.execute(f"DELETE FROM {self._table_name} WHERE user_type=?", (user_type,))
        self._connect.commit()

    def select(self, columns: list, user_type):
        """
        :param columns: list, user_type, type_name, *
        :param user_type:
        :return:
        """
        return self._cursor.execute(f"SELECT {','.join(columns)} FROM {self._table_name} WHERE user_type=?",
                                    (user_type,)).fetchall()

    class Payments(Database):
        _table_name = "payments"

        def insert(self, apartment_id, date, amount):
            self._cursor.execute(f"""INSERT INTO {self._table_name} (apartament_id, date, sum) VALUES (?,?,?)""",
                                 (apartment_id, date, amount))
            self._connect.commit()

        def update(self, payment_id, new_amount):
            self._cursor.execute(f"""UPDATE {self._table_name} SET sum = ? WHERE payment_id = ?""",
                                 (new_amount, payment_id))
            self._connect.commit()

        def delete(self, payment_id):
            self._cursor.execute(f"""DELETE FROM {self._table_name} WHERE payment_id = ?""", (payment_id,))
            self._connect.commit()

        def select(self, payment_id):
            self._cursor.execute(f"""SELECT * FROM {self._table_name} WHERE payment_id = ?""", (payment_id,))
            return self._cursor.fetchall()


class Apartments(Database):
    _table_name = 'apartments'

    def insert(self, apartment_code):
        self._cursor.execute(
            f"""INSERT INTO {self._table_name}
            (apartment_id, apartment_code) VALUES (NULL,?)""",
            (apartment_code,))
        self._connect.commit()

    def update(self, apartment_id, apartment_code):
        self._cursor.execute(
            f"""UPDATE {self._table_name} SET apartment_code=? WHERE apartment_id = ?""",
            (apartment_id, apartment_code))
        self._connect.commit()

    def delete(self, apartment_id):
        self._cursor.execute(F"""DELETE * FROM {self._table_name} WHERE apartment_id = ?""", (apartment_id,))
        self._connect.commit()

    def select(self, columns: list, key_word: str, value):
        """
        :param columns: list, apartment_id, apartment_code, *
        :param apartment_id:
        :return:
        """
        return self._cursor.execute(
            f"""SELECT {','.join(columns)} FROM {self._table_name} WHERE {key_word} = ?""",
            (value,)).fetchall()

    def select_apt_code(self, apt_id):
        res = self._cursor.execute(f"""SELECT apartment_code FROM {self._table_name} WHERE apartment_id = ?""",
                                   (apt_id,)).fetchall()[0]
        print(res)
        return res[0]
