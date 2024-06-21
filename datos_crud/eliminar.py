import mysql.connector

conexion = mysql.connector.connect(user='root', password='19961004Omar.',
                             host='localhost',
                             database='tienda',
                             port='3306')
if conexion.is_connected():
    print("conexion exitosa")
    cursor= conexion.cursor()
    #define la consulta delete
    query = "DELETE FROM marca WHERE ID_Marca IN  (1,2,13)"
    
    cursor.execute(query)
    #confirmar los cambios
    conexion.commit()
    #verifica el numero de registros afectados 
    print(f"{cursor.rowcount} registros eliminados ")
    cursor.close()
    conexion.close()
