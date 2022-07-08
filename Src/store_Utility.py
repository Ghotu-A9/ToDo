import json
import sqlite3
from sqlite3 import Error


def operateOnConnection(file, fun):
    conn = None
    try:
        conn = sqlite3.connect(file)
        fun(conn, None)
    except Error as e:
        fun(None, e)
    finally:
        if conn:
            conn.close()


class StoreUtility:

    def __init__(self):
        self.LTAF = '../assets/data/ltaf.db'
        self.OTAF = '../assets/data/otaf.db'
        self.LocalAnalyticsTableName = "lat"
        self.OnlineAnalyticsTableName = "oat"

        self.LocalAnalyticsActiveProgramTableName = "laapt"

    def testDatabase(self):
        def testFun(connection):
            print(connection)

        operateOnConnection(self.LTAF, testFun)
        operateOnConnection(self.OTAF, testFun)

    def createLocalAnalyticalDatabase(self):
        def create(conn, error):
            if conn is not None:
                conn.execute(
                    '''CREATE TABLE IF NOT EXISTS  lat(ID integer primary key autoincrement,Placeholder TEXT NOT NULL,Time REAL NOT NULL,ExtraTime REAL NOT NULL,Programs TEXT NOT NULL,PNames TEXT NOT NULL);''')
            else:
                print(error)

        operateOnConnection(self.LTAF, create)

    def saveLocalAnalyticalData(self, data):


        self.createLocalAnalyticalDatabase()


        def save(conn, error):
            if conn is not None:
                conn.execute("insert into lat  (Placeholder,Time,ExtraTime,Programs,PNames) values ( ?, ?, ?, ?, ?)", (data.get("placeholder"), data.get("time"), data.get("extra_time"), json.dumps(data.get("programs")), json.dumps(data.get("p_names"))))
                conn.commit()
            else:
                print(error)

        operateOnConnection(self.LTAF, save)

    def getAllLocalAnalyticalData(self):

        self.dataoutlocal = []

        def get(conn, error):
            if conn is not None:
                cursor = conn.execute("SELECT * from lat")
                for row in cursor:
                    dictData = {
                        "id": row[0],
                        "placeholder": row[1],
                        "time": row[2],
                        "extra_time": row[3],
                        "programs": json.loads(row[4]),
                        "p_names": json.loads(row[5])
                    }
                    self.dataoutlocal.append(dictData)
            else:
                print(error)
                self.dataoutlocal = None

        operateOnConnection(self.LTAF, get)

        return self.dataoutlocal


