import pymysql

def conecta_db():
   con =  pymysql.connect(host="localhost",
                        database="credSim",
                        user='root',
                        password="",
                        port=3306)  
   return con