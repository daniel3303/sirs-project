import json
import sqlite3
import os
from database.DatabaseInterface import DatabaseInterface
from Logger import ConsoleLogger

class SQLiteDatabase(DatabaseInterface):
    def __init__(self):
        self.logger = ConsoleLogger()
        with open("config/storage.json") as configFile:
            self.config = json.loads(configFile.read())

        self.schema = None

        # Opens the main connection
        self.connection = sqlite3.connect(self.config["db_name"])
        self.checkSchema(self.connection)

        #Opens a new connection for each replica
        self.replicas = []
        for index in range(0, len(self.config["replicas"])):
            newReplica = self.config["replicas"][index]
            self.replicas.append(newReplica)

            # Make the path if not exists
            os.makedirs(os.path.dirname(newReplica["db_name"]), exist_ok=True)
            self.replicas[index]["connection"] =  sqlite3.connect(newReplica["db_name"])
            self.checkSchema(newReplica["connection"])




    def tableExists(self, tableName, connection):
        tableName = (tableName, )
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", tableName)
        if(len(cursor.fetchall()) == 0):
            return False
        else:
            return True

    def checkSchema(self, connection):
        if(self.tableExists("migrations", connection) == False):
            self.createSchema(connection)


    def createSchema(self, connection):
        # Load schema if not loaded yet
        if(self.schema == None):
            with open("database/schema.json") as schemaFile:
                self.schema = json.loads(schemaFile.read())


        # Execute the schema
        cursor = connection.cursor()
        for query in self.schema:
            cursor.execute(query["up"])

        self.logger.info("Created schema for database "+self.getDatabaseName(connection))

    def getDatabaseName(self, connection):
        cursor = connection.cursor()
        cursor.execute("PRAGMA database_list;")
        return cursor.fetchone()[2]
