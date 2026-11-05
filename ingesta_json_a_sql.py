import json
import pyodbc
import pandas as pd

# 1. Configuración de conexiones
server = r'localhost\SQLEXPRESS'  
database = 'db_ventas_local'  # Usamos la base de datos que creamos en el laboratorio anterior
driver = '{ODBC Driver 17 for SQL Server}' 
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

try:
    # 2. Leer el archivo JSON de pruebas con Python
    print("📖 Leyendo archivo semiestructurado 'nuevas_ventas.json'...")
    with open('nuevas_ventas.json', 'r', encoding='utf-8') as archivo:
        datos_ventas = json.load(archivo)
    
    # 3. Conectarse a SQL Server para preparar la tabla de destino
    print("🔌 Conectando a SQL Server...")
    with pyodbc.connect(conn_str) as conn:
        cursor = conn.cursor()
        
        # Crear la tabla de Ventas si no existe
        cursor.execute("""
            IF OBJECT_ID('Ventas', 'U') IS NOT NULL DROP TABLE Ventas;
            CREATE TABLE Ventas (
                TransaccionID INT PRIMARY KEY,
                Producto VARCHAR(150),
                Monto DECIMAL(18,2),
                ClienteID INT
            )
        """)
        conn.commit()
        print("🏢 Tabla 'Ventas' lista en la base de datos.")

        # 4. Iterar e Insertar los datos del JSON en la tabla SQL (Proceso de Ingesta)
        print("🚀 Insertando registros en la base de datos...")
        for venta in datos_ventas:
            cursor.execute("""
                INSERT INTO Ventas (TransaccionID, Producto, Monto, ClienteID)
                VALUES (?, ?, ?, ?)
            """, venta['TransaccionID'], venta['Producto'], venta['Monto'], venta['ClienteID'])
        
        conn.commit()
        print("✅ ¡Ingesta completada con éxito!")

        # 5. Validación final: Unir tablas usando un SQL JOIN desde Pandas
        print("\n--- 📊 Reporte Consolidado (Ventas + Clientes) ---")
        consulta_sql = """
            SELECT V.TransaccionID, C.Nombre, V.Producto, V.Monto, C.Ciudad
            FROM Ventas V
            INNER JOIN Clientes C ON V.ClienteID = C.ClienteID
        """
        df_reporte = pd.read_sql(consulta_sql, conn)
        print(df_reporte)

except Exception as e:
    print("\n❌ Error durante el proceso de ingesta:", e)
