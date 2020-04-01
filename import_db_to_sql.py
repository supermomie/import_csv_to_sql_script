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


start = time.time()

# Configuration serveur
DATABASESERVERIP      = "localhost" #OR 127.0.0.1
DATABASEUSERNAME      = "root"
DATABASEUSERPASSWORD  = ""

# Nom de la base de donnee et nom de la table

validArg = ["-db", "-d", '-tn', '-cn', '-a']
arg = Menu().men(validArg)

DB_NAME    = arg
print(DB_NAME)
exit()

# Chemin du ficher CSV
PATHFILE   = argv[1]

# Nom de la colone
TABLE_NAME = Path(PATHFILE).stem

# Nom du fichier
FILE_NAME = os.path.basename(PATHFILE)

EXTENSION  = Path(PATHFILE).suffix

# Encodage et Separateur
ENCODING = 'utf-8'
SEP      = ','



def connection(databaseUserName, databaseServerIP, databaseUserPassword, dbName):
    # Connection a mysql
    engine = sqlalchemy.create_engine('mysql+pymysql://'+databaseUserName+':@'+databaseServerIP+'/'+ dbName)
    connectionInstance = pymysql.connect(host=databaseServerIP, 
                                        user=databaseUserName, 
                                        password=databaseUserPassword,
                                        charset="utf8mb4", 
                                        cursorclass=pymysql.cursors.DictCursor)
    return engine, connectionInstance


def create_DB(databaseUserName, databaseServerIP, databaseUserPassword, dbName):
    # Instructions SQL
    _, connectionInstance = connection(databaseUserName, databaseServerIP, 
                                            databaseUserPassword, dbName)
    cursorInsatnce = connectionInstance.cursor()
    try :
        sqlStatement = "CREATE DATABASE "+ dbName
        cursorInsatnce.execute(sqlStatement)
    except :
        return cursorInsatnce
    return cursorInsatnce


def read_CSV(pathfile, encoding, sep):
    # Lecture du fichier csv
    data = pd.read_csv(pathfile, encoding=encoding, sep=sep)
    columnsName = [col for col in data.columns] # OR columnsName = data.columns
    ratings = pd.read_csv(pathfile, encoding=encoding, 
                            usecols=columnsName, sep=sep)
    return ratings


def read_JSON(pathfile):
    # Lecture du ficher json
    #data = pd.read_json(pathfile)
    with open(pathfile) as f:
        data = json.load(f)
    return data


def error_MSG():
    msgLinux = colored("ERR ARG MISSING", "red")
    msgWin = "ERR ARG MISSING"
    msg = os.system(msgWin if os.name == 'nt' else msgLinux)
    return msg


def all_process(databaseUserName, databaseServerIP, databaseUserPassword, 
                            tableName, dbName, pathfile, encoding, sep):
    if len(argv) <= 1:
        print(error_MSG())
        exit()
    
    print("IMPORT DATABASE")
    engine, _ = connection(databaseUserName, databaseServerIP, databaseUserPassword, dbName)
    create_DB(databaseUserName, databaseServerIP, databaseUserPassword, dbName)
    
    if EXTENSION == ".csv":
        ratings = read_CSV(pathfile, encoding, sep)
        ratings.to_sql(tableName, con=engine, if_exists='append', index=False, chunksize=1)
    
    if EXTENSION == ".json":
        data = read_JSON(pathfile)
        data.to_sql(tableName, con=engine, if_exists='append', index=True, chunksize=1)
    
    print("IMPORT TERMINER")



#all_process(DATABASEUSERNAME, DATABASESERVERIP, DATABASEUSERPASSWORD, 
#                TABLE_NAME, DB_NAME, PATHFILE, ENCODING, SEP)




myclient = pymongo.MongoClient()

db = myclient[DB_NAME]
collection = db[TABLE_NAME]
collection.insert_one(read_JSON(PATHFILE))

print(myclient.list_database_names())

myclient.close()


end = time.time()
print("time {}s".format(end-start))
