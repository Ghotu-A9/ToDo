import json
import os.path

class StoreTUtility:

    def __init__(self):
        self.DataStorage = "../assets/data/database.json"


        if not os.path.exists(self.DataStorage):
            f = open(self.DataStorage, "w")
            f.write("[]")
            f.close()

        print("Initialized Todo Database")

    def saveToStore(self, data):
        loaded = self.getDatabase()
        loaded.append(data)
        self.localWrite(loaded)

    def removeFromStoreByIndex(self, index):
        loaded = self.getDatabase()
        if index is not None and index < len(loaded):
            del loaded[index]
        self.localWrite(loaded)

    def removeFromStoreByValue(self, value):
        loaded = self.getDatabase()
        if value and value in loaded:
            loaded.remove(value)
        self.localWrite(loaded)

    def localWrite(self, data):
        file2 = open(self.DataStorage, 'w')
        file2.write(json.dumps(data))
        file2.close()

    def modifyTodoStoreProperty(self, index, option, value):
        loaded = self.getDatabase()
        loaded[index][option] = value
        self.localWrite(loaded)

    def getDatabase(self):
        file = open(self.DataStorage, 'r')
        loaded = json.load(file)
        file.close()
        return loaded
