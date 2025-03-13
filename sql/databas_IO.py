import pymssql

class db_io:
    def __init__(self):
        self.server = "localhost"
        self.port = 1433
        self.database = "master"
        self.username = "sa"
        self.password = "GreenHorses?!"

    def _connect_to_database(self):
        try:
            conn = pymssql.connect(
                server=self.server,
                port=self.port,
                user=self.username,
                password=self.password,
                database=self.database,
            )
            conn.autocommit(True)
            print("Connection successful!")
            return conn

        except Exception as e:
            print("Error:", e)


    def insert_into_core_count_table(self, data: tuple) -> None:
        conn = self._connect_to_database()
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO watch_research_table (title, price, link, box, papers, watch_creation_date, date_added, movement)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, data)
        conn.close()
        print("Data inserted successfully!")