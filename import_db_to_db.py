import os, re
import time
import json
import pandas as pd
import sqlalchemy
import pymysql
import pymongo
from sys import argv
from termcolor import colored
from pathlib import Path
from menu import Menu
from tqdm import tqdm

start = time.time()


validArg = ["-db", "-d", '-tn', '-cn', '-a']
arg = Menu().men(validArg)


# Configuration serveur
DATABASESERVERIP      = "localhost" #OR 127.0.0.1
DATABASEUSERNAME      = "root"
DATABASEUSERPASSWORD  = ""

# Nom de la base de donnee et nom de la table
DB_NAME    = arg['-tn']

# Chemin du ficher CSV
PATHFILE   = arg['-d']

# Nom de la colone
TABLE_NAME = Path(PATHFILE).stem

# Nom du fichier
FILE_NAME = os.path.basename(PATHFILE)

EXTENSION  = Path(PATHFILE).suffix

# Encodage et Separateur
ENCODING = 'utf-8'
SEP      = ','


#TODO create class for reading files in folder and solo FILE_NAME


class readbases():
    
    def __init__():
        print("a")

    def read_CSV():
        print("c") 


class sql():
    
    def __init__(self, DATABASEUSERNAME, DATABASESERVERIP, DATABASEUSERPASSWORD, 
                    TABLE_NAME, DB_NAME, PATHFILE, ENCODING, SEP):
        self.all_process(DATABASEUSERNAME, DATABASESERVERIP, DATABASEUSERPASSWORD, 
                    TABLE_NAME, DB_NAME, PATHFILE, ENCODING, SEP)


    def connection(self, databaseUserName, databaseServerIP, databaseUserPassword, dbName):
        # Connection a mysql
        engine = sqlalchemy.create_engine('mysql+pymysql://'+databaseUserName+':@'+databaseServerIP+'/'+ dbName)
        connectionInstance = pymysql.connect(host=databaseServerIP, 
                                            user=databaseUserName, 
                                            password=databaseUserPassword,
                                            charset="utf8mb4", 
                                            cursorclass=pymysql.cursors.DictCursor)
        return engine, connectionInstance


    def create_DB(self, databaseUserName, databaseServerIP, databaseUserPassword, dbName):
        # Instructions SQL
        _, connectionInstance = self.connection(databaseUserName, databaseServerIP, 
                                                databaseUserPassword, dbName)
        cursorInsatnce = connectionInstance.cursor()
        try :
            sqlStatement = "CREATE DATABASE "+ dbName
            cursorInsatnce.execute(sqlStatement)
        except :
            return cursorInsatnce
        return cursorInsatnce


    def read_CSV(self, pathfile, encoding, sep):
        # Lecture du fichier csv
        data = pd.read_csv(pathfile, encoding=encoding, sep=sep)
        columnsName = [col for col in data.columns] # OR columnsName = data.columns
        ratings = pd.read_csv(pathfile, encoding=encoding, 
                                usecols=columnsName, sep=sep)
        return ratings


    def read_JSON(self, pathfile):
        # Lecture du ficher json
        #data = pd.read_json(pathfile)
        with open(pathfile) as f:
            data = json.load(f)
        return data


    def all_process(self, databaseUserName, databaseServerIP, databaseUserPassword, 
                                tableName, dbName, pathfile, encoding, sep):
        
        print("IMPORT DATABASE")
        engine, _ = self.connection(databaseUserName, databaseServerIP, databaseUserPassword, dbName)
        self.create_DB(databaseUserName, databaseServerIP, databaseUserPassword, dbName)
        
        if EXTENSION == ".csv":
            ratings = self.read_CSV(pathfile, encoding, sep)
            ratings.to_sql(tableName, con=engine, if_exists='append', index=False, chunksize=1)
        
        if EXTENSION == ".json":
            data = self.read_JSON(pathfile)
            data.to_sql(tableName, con=engine, if_exists='append', index=True, chunksize=1)
        
        print("IMPORT TERMINER")



class mongo():

    def __init__(self, pathfile, dbName, tableName):
        self.all_process(pathfile, dbName, tableName)


    def connections(self):
        myclient = pymongo.MongoClient()
        return myclient
    
    def create_DB(self, dbName, tableName):
        myclient = self.connections()
        db = myclient[dbName]
        collection = db[tableName]
        #print(collection)
        #print(collection.count())
        if collection.count() == 0:
            return collection
        elif collection.count() > 0:
            collection.drop()
    
    def insert(self, pathfile, dbName, tableName):
        collection = self.create_DB(dbName, tableName)
        collection.insert_one(self.read_JSON(pathfile))
    
    def read_JSON(self, pathfile):
       # Lecture du ficher json
       with open(pathfile) as f:
           data = json.load(f)
           #for item in data:
           #     print(Path(item).stem)
       #exit()
       return data



    def all_process(self, pathfile, dbName, tableName):
        myclient = self.connections()
        self.create_DB(dbName, tableName)
        self.insert(pathfile, dbName, tableName)
        myclient.close()

        print(myclient.list_database_names())




if __name__ == '__main__':
    if arg['-db'] == "mysql":
        sql(DATABASEUSERNAME, DATABASESERVERIP, DATABASEUSERPASSWORD, 
                    TABLE_NAME, DB_NAME, PATHFILE, ENCODING, SEP)
    if arg['-db'] == "mongo":
        mongo(PATHFILE, DB_NAME, TABLE_NAME)


end = time.time()
print("time {}s".format(end-start))
