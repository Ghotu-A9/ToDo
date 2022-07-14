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

        self.createdLocalAnalyticalData = False

        def create(conn, error):
            if error is None:
                conn.execute(
                    '''CREATE TABLE IF NOT EXISTS  lat(ID INTEGER PRIMARY KEY AUTOINCREMENT ,Placeholder TEXT NOT NULL,Time REAL NOT NULL,ExtraTime REAL NOT NULL,Programs TEXT NOT NULL,PTime TEXT NOT NULL);''')
                self.createdLocalAnalyticalData = True
            else:
                self.createdLocalAnalyticalData = False
                print(error)

        operateOnConnection(self.LTAF, create)

    def saveLocalAnalyticalData(self, data):

        self.createLocalAnalyticalDatabase()
        self.savedLocalAnalyticalData = False
        self.returnId = None

        def save(conn, error):
            if error is None:
                dataSaved = conn.execute("insert into lat  (Placeholder,Time,ExtraTime,Programs,PTime) values ( ?, ?, ?, ?, ?)", (
                    data.get("placeholder"), data.get("time"), data.get("extra_time"), json.dumps(data.get("programs")),
                    json.dumps(data.get("p_time"))))
                conn.commit()
                self.returnId = dataSaved.lastrowid
                self.savedLocalAnalyticalData = True
            else:
                self.savedLocalAnalyticalData = False
                print(error)

        operateOnConnection(self.LTAF, save)
        return {"saved": self.savedLocalAnalyticalData, "id": self.returnId}

    def getAllLocalAnalyticalData(self):

        self.dataoutlocal = []

        def get(conn, error):
            if error is None:
                cursor = conn.execute("SELECT * from lat")
                for row in cursor:
                    dictData = {
                        "id": row[0],
                        "placeholder": row[1],
                        "time": row[2],
                        "extra_time": row[3],
                        "programs": json.loads(row[4]),
                        "p_time": json.loads(row[5])
                    }
                    self.dataoutlocal.append(dictData)
            else:
                print(error)
                self.dataoutlocal = None

        operateOnConnection(self.LTAF, get)

        return self.dataoutlocal

    def updateLocalAnalyticalData(self, tid, key, data):

        self.createLocalAnalyticalDatabase()
        self.updatedLocalAnalyticalData = False

        def updateProgramTime(conn, error):
            if error is None:
                conn.execute("UPDATE lat SET PTime = ?  WHERE ID = ?",(json.dumps(data), tid))
                conn.commit()
                self.updatedLocalAnalyticalData = True
            else:
                print(error)
                self.updatedLocalAnalyticalData = False

        def updateExtraTime(conn, error):
            if error is None:
                conn.execute("UPDATE lat SET ExtraTime = ?  WHERE ID = ?", (data, tid))
                conn.commit()
                self.updatedLocalAnalyticalData = True
            else:
                print(error)
                self.updatedLocalAnalyticalData = False

        def updatePrograms(conn, error):
            if error is None:
                conn.execute("UPDATE lat SET Programs = ?  WHERE ID = ?", (json.dumps(data), tid))
                conn.commit()
                self.updatedLocalAnalyticalData = True
            else:
                print(error)
                self.updatedLocalAnalyticalData = False

        if key == "programs":
            operateOnConnection(self.LTAF, updatePrograms)
        elif key == "p_time":
            operateOnConnection(self.LTAF, updateProgramTime)
        elif key == "extra_time":
            operateOnConnection(self.LTAF, updateExtraTime)

        return self.updatedLocalAnalyticalData

    def getSingleLocalAnalyticalData(self, tid, key):

        self.createLocalAnalyticalDatabase()

        self.dataSingleLocalOut = None

        def selectProgramTime(conn, error):
            if error is None:
                data = conn.execute("SELECT PTime FROM lat WHERE ID = ?", (tid,))
                for row in data:
                    self.dataSingleLocalOut = json.loads(row[0])
            else:
                print(error)
                return False

        def selectPrograms(conn, error):
            if error is None:
                data = conn.execute("SELECT Programs FROM lat WHERE ID = ?", (tid,))
                for row in data:
                    self.dataSingleLocalOut = json.loads(row[0])
            else:
                print(error)
                return False

        if key == "programs":
            operateOnConnection(self.LTAF, selectPrograms)
        elif key == "p_time":
            operateOnConnection(self.LTAF, selectProgramTime)

        return self.dataSingleLocalOut

    def removeSingleRowLocalAnalyticalData(self, tid):

        self.deletedSingleRowLocalAnalyticalData = False

        def delete(conn, error):
            if error is None:
                conn.execute("DELETE FROM lat WHERE id=?", (tid,))
                conn.commit()
                self.deletedSingleRowLocalAnalyticalData = True
            else:
                print(error)
                self.deletedSingleRowLocalAnalyticalData = False

        operateOnConnection(self.LTAF, delete)
        return self.deletedSingleRowLocalAnalyticalData

    def reorderLocalAnalyticalData(self):
        self.reorderedLocalAnalyticalData = False

        def order(conn, error):
            if error is None:
                conn.execute("VACUUM")
                conn.commit()
                self.reorderedLocalAnalyticalData = True
            else:
                print(error)
                self.reorderedLocalAnalyticalData = False

        operateOnConnection(self.LTAF, order)
        return self.reorderedLocalAnalyticalData

