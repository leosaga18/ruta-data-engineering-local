import pyodbc
import pandas as pd

# 1. Configuración de la conexión local
# Intentamos con la instancia estándar de SQL Express. Si no conecta, probamos con 'localhost'
server = r'localhost\SQLEXPRESS'  
database = 'master'   
driver = '{ODBC Driver 17 for SQL Server}' 

# Cadena de conexión usando Autenticación de Windows
conn_str_master = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

try:
    print("Conectando al servidor SQL local...")
    # 2. Conectarse para crear la base de datos simulada de Azure
    conn = pyodbc.connect(conn_str_master, autocommit=True)
    cursor = conn.cursor()
    
    # Borramos la base de datos si ya existe para evitar errores y la creamos limpia
    cursor.execute("IF EXISTS (SELECT name FROM sys.databases WHERE name = 'db_ventas_local') ALTER DATABASE db_ventas_local SET SINGLE_USER WITH ROLLBACK IMMEDIATE; DROP DATABASE IF EXISTS db_ventas_local")
    cursor.execute("CREATE DATABASE db_ventas_local")
    print("¡Base de datos 'db_ventas_local' creada exitosamente!")
    conn.close()

    # 3. Conectarse directamente a la nueva base de datos de datos de ventas
    conn_str_db = f'DRIVER={driver};SERVER={server};DATABASE=db_ventas_local;Trusted_Connection=yes;'
    with pyodbc.connect(conn_str_db) as conn_node:
        cursor = conn_node.cursor()
        
        # Crear una tabla de datos estructurados (Simulación de Ingesta)
        print("Creando tabla de clientes...")
        cursor.execute("""
            CREATE TABLE Clientes (
                ClienteID INT PRIMARY KEY,
                Nombre VARCHAR(100),
                Ciudad VARCHAR(50),
                FechaRegistro DATE
            )
        """)
        
        # Insertar registros de prueba usando SQL
        cursor.execute("INSERT INTO Clientes VALUES (1, 'Alejandro Gomez', 'Girardot', '2026-11-04')")
        cursor.execute("INSERT INTO Clientes VALUES (2, 'Maria Claudia', 'Bogota', '2026-11-01')")
        cursor.execute("INSERT INTO Clientes VALUES (3, 'Carlos Mendoza', 'Medellin', '2026-10-15')")
        conn_node.commit()
        print("¡Datos insertados correctamente en SQL Server!")
        
        # 4. Extracción y Análisis de datos usando Pandas (Data Engineering básico)
        print("\n--- Leyendo datos con Pandas desde Python ---")
        df = pd.read_sql("SELECT * FROM Clientes", conn_node)
        print(df)

except Exception as e:
    print("\n❌ Ocurrió un error en el proceso:", e)
    print("💡 Si el error es de conexión, probaremos cambiando la línea 6 por: server = 'localhost'")
