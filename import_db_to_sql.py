import time
import json
import pandas as pd
import sqlalchemy
import pymysql
from sys import argv


start = time.time()


# Configuration serveur
DATABASESERVERIP      = "localhost" #OR 127.0.0.1
DATABASEUSERNAME      = "root"
DATABASEUSERPASSWORD  = ""

# Nom de la base de donnee et nom de la table
DB_NAME    = ''
TABLE_NAME = ''

# Chemin du ficher CSV
PATHFILE   = '' # TODO put in ARGV PLZ!!

# Nom du fichier
NAME       = '' # TODO put in ARGV PLZ!!

ENCODING = 'utf-8'
SEP      = ','

def connection(databaseUserName, databaseServerIP, databaseUserPassword, dbName):
    # Connection a mysql
    engine = sqlalchemy.create_engine('mysql+pymysql://'+databaseUserName+':@'+databaseServerIP+'/'+ dbName)
    connectionInstance = pymysql.connect(host=databaseServerIP, user=databaseUserName, password=databaseUserPassword,charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
    return engine, connectionInstance

def create_DB(databaseUserName, databaseServerIP, databaseUserPassword, dbName):
    # Instructions SQL
    _, connectionInstance = connection(databaseUserName, databaseServerIP, databaseUserPassword, dbName)
    cursorInsatnce = connectionInstance.cursor()
    sqlStatement = "CREATE DATABASE "+ dbName
    cursorInsatnce.execute(sqlStatement)
    return cursorInsatnce

def read_CSV(pathfile, name, encoding, sep):
    # Lecture du fichier csv
    data = pd.read_csv(pathfile +'/'+ name, encoding=encoding, sep=sep, dtype='object')
    columnsName = [col for col in data.columns]
    ratings = pd.read_csv(pathfile +'/'+ name, encoding=encoding, usecols=columnsName, sep=sep, dtype='object')
    return ratings

def read_JSON(pathfile, name):
    data = pd.read_json(pathfile + '/' + name)
    data = data['Game Of Thrones S01E01 Winter Is Coming.srt']
    return data

def all_process(databaseUserName, databaseServerIP, databaseUserPassword, dbName, pathfile, name, encoding, sep):
    print("IMPORT DATABASE")
    
    if argv[1] == "csv":
    
        engine, _ = connection(databaseUserName, databaseServerIP, databaseUserPassword, dbName)
        create_DB(databaseUserName, databaseServerIP, databaseUserPassword, dbName)
        ratings = read_CSV(pathfile, name, encoding, sep)
        # Execution de tralala
        ratings.to_sql(TABLE_NAME, con=engine, if_exists='append', index=False, chunksize=1)
    
    if argv[1] == "json":
    
        engine, _ = connection(databaseUserName, databaseServerIP, databaseUserPassword, dbName)
        cursorInsatnce = create_DB(databaseUserName, databaseServerIP, databaseUserPassword, dbName)
        data = read_JSON(pathfile, name)
        #cursorInsatnce.execute("INSERT INTO json_col VALUES (" + str(data) + ")")
        data.to_sql(TABLE_NAME, con=engine, if_exists='append', index=False, chunksize=1)
    
    print("IMPORT TERMINER")


all_process(DATABASEUSERNAME, DATABASESERVERIP, DATABASEUSERPASSWORD, DB_NAME, PATHFILE, NAME, ENCODING, SEP)
read_JSON(PATHFILE, NAME)
end = time.time()
print("time {}".format(end-start))
