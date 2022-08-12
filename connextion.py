import mysql.connector


class DataBase:
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="colegio"
    )
    cursor = conexion.cursor()
