import sqlite3


class DBlite:
    """
    Interacts with sqlite3 in python
    """

    def __init__(self, db_name):
        """
        Init Database connection
        """
        self.db_name = db_name
        self.db = sqlite3.connect(db_name)

    def add_table(self, table_name, **columns):
        """
        Insert new Tables in Database
        """
        cols = ""
        for col_name, col_type in columns.items():
            cols += col_name + " " + col_type + ","
        cols = cols[0 : len(cols) - 1]
        command = "CREATE TABLE IF NOT EXISTS {}({})".format(table_name, cols)
        self.db.execute(command)

    def insert(self, table_name, *data):
        """
        Insert new Attributes
        """
        ins_data = ""
        for value in data:
            ins_data += '"' + value + '"' + ","
        ins_data = ins_data[0 : len(ins_data) - 1]
        self.db.execute("INSERT INTO {} values({})".format(table_name, ins_data))
        self.db.commit()

    def remove(self, table_name, where):
        """
        Remove Attributes with a condition
        """
        self.where = where
        self.db.execute("DELETE FROM {} WHERE {}".format(table_name, self.where))
        self.db.commit()

    def update_data(self, table_name, where, changes):
        """
        Update Attributes with a condition
        """
        sets = ""
        for (col, data), num in zip(changes.items(), range(len(changes))):
            data = data.replace('"', "'")
            data = data.replace('”', "'")
            print("data: ", data)
            sets += '{}="{}"'.format(col, data)
            if num + 1 != len(changes):
                sets += ", "
        command = "UPDATE {} SET {} WHERE {}".format(table_name, sets, where)
        self.db.execute(command)
        self.db.commit()

    def get_items(self, table_name, where):
        """
        Get Attributes with a condition
        """
        if table_name:
            command = "SELECT * FROM {} WHERE {}".format(table_name, where)
            items = self.db.execute(command)
            self.db.commit()
            return list(items)
        else:
            return []

    def get_items_query(self, query):
        """
        Get Attributes with Custom Query
        """
        self.items = self.db.execute(query)
        self.db.commit()
        return list(self.items)

    def get_tables(self):
        """
        Get all tables in the database
        """
        self.tables = self.db.execute("SELECT name FROM sqlite_master")
        return list(self.tables)

    def query(self, query_string):
        """
        Commit custom query
        """
        self.db.execute(query_string)
        self.db.commit()

    def search(self, table_name, query):
        command = "SELECT * FROM {} WHERE {}".format(table_name, where)
        self.items = self.db.execute()
        self.db.commit()
        return list(self.items)

    def close_connection(self):
        """
        close database connection
        """
        self.db.close()
