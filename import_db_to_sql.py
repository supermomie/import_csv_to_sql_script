import time
import json
import pandas as pd
import sqlalchemy
import pymysql
from sys import argv
from termcolor import colored

start = time.time()


# Configuration serveur
DATABASESERVERIP      = "localhost" #OR 127.0.0.1
DATABASEUSERNAME      = "root"
DATABASEUSERPASSWORD  = ""

# Nom de la base de donnee et nom de la table
DB_NAME    = 'GOT2'
TABLE_NAME = 'FORTESTING'

# Chemin du ficher CSV
PATHFILE   = '/home/fakhredine/Documents/microsoft/DB/JSON/game-of-thrones-srt' # TODO put in ARGV PLZ!!

# Nom du fichier
NAME       = 'season1.json' # TODO put in ARGV PLZ!!

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


def read_CSV(pathfile, name, encoding, sep):
    # Lecture du fichier csv
    data = pd.read_csv(pathfile +'/'+ name, encoding=encoding, sep=sep, dtype='object')
    columnsName = [col for col in data.columns] # OR columnsName = data.columns
    ratings = pd.read_csv(pathfile +'/'+ name, encoding=encoding, 
                            usecols=columnsName, sep=sep, dtype='object')
    return ratings

def read_JSON(pathfile, name):
    # Lecture du ficher json
    data = pd.read_json(pathfile + '/' + name)
    return data


def error_MSG():
    return colored("ERR... ARG MISSING", "red", attrs=["bold", "reverse"])


def all_process(databaseUserName, databaseServerIP, databaseUserPassword, 
                            tableName, dbName, pathfile, name, encoding, sep):
    if len(argv) <= 1:
        print(error_MSG())
        exit()
    
    print("IMPORT DATABASE")
    engine, _ = connection(databaseUserName, databaseServerIP, databaseUserPassword, dbName)
    create_DB(databaseUserName, databaseServerIP, databaseUserPassword, dbName)
    if argv[1] == "csv":
        ratings = read_CSV(pathfile, name, encoding, sep)
        ratings.to_sql(tableName, con=engine, if_exists='append', index=False, chunksize=1)
    
    if argv[1] == "json":
        data = read_JSON(pathfile, name)
        data.to_sql(tableName, con=engine, if_exists='append', index=True, chunksize=1)
    
    print("IMPORT TERMINER")


all_process(DATABASEUSERNAME, DATABASESERVERIP, DATABASEUSERPASSWORD, 
                TABLE_NAME, DB_NAME, PATHFILE, NAME, ENCODING, SEP)
end = time.time()
print("time {}s".format(end-start))
