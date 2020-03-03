import time
import pandas as pd
import sqlalchemy
import pymysql

start = time.time()


# Configuration serveur
DATABASESERVERIP      = "localhost" #OR 127.0.0.1
DATABASEUSERNAME      = "root"
DATABASEUSERPASSWORD  = ""

# Nom de la base de donnee et nom de la table
DB_NAME    = ''
TABLE_NAME = ''

# Chemin du ficher CSV
PATHFILE   = ''

# Nom du fichier
NAME       = ''

ENCODING = 'utf-8'
SEP      = ';'

def connection(databaseUserName, databaseServerIP, dbName):
    # Connection a mysql
    engine = sqlalchemy.create_engine('mysql+pymysql://'+databaseUserName+':@'+databaseServerIP+'/'+ dbName)
    connectionInstance = pymysql.connect(host=databaseServerIP, user=databaseUserName, password=databaseUserPassword,charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)

def create_DB(dbName):
    # Instructions SQL
    cursorInsatnce = connectionInstance.cursor()
    sqlStatement = "CREATE DATABASE "+ dbName
    cursorInsatnce.execute(sqlStatement)


def read_CSV(pathfile, name, encoding, sep):
    # Lecture du fichier csv
    data = pd.read_csv(pathfile +'/'+ name, encoding=encoding, sep=sep, dtype='object')
    columnsName = [col for col in data.columns]
    ratings = pd.read_csv(pathfile +'/'+ name, encoding=encoding, usecols=columnsName, sep=sep, dtype='object')


def all_process(databaseUserName, databaseServerIP, dbName, pathfile, name, encoding, sep):
    print("IMPORT DATABASE")
    connection(DATABASEUSERNAME, databaseServerIP, dbName)
    createDB(dbName)
    readCsv(pathfile, name, encoding, sep)

    # Execution de tralala
    ratings.to_sql(TABLE_NAME, con=engine, if_exists='append', index=False, chunksize=1)

    print("IMPORT TERMINER")


all_process(DATABASEUSERNAME, DATABASESERVERIP, DB_NAME, PATHFILE, NAME, ENCODING, SEP)
end = time.time()
print("time {}".format(end-start))
