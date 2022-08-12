import mysql.connector
#Ese code esta para check de la database, para traer datos
conexion1=mysql.connector.connect(host="localhost",
                                  user="root",
                                  passwd="",
                                  database="colegio")
cursor1=conexion1.cursor()
cursor1.execute("SELECT * FROM `estudiantes` ")
for fila in cursor1:
    print(fila)
conexion1.close()


import mysql.connector