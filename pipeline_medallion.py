import os
import pandas as pd

print("🚀 Iniciando Pipeline de Datos (Arquitectura Medallion) 🚀\n")

# ==========================================
# 🥉 PASO 1: LEER DESDE CAPA BRONZE
# ==========================================
print("🥉 Procesando Capa BRONZE...")
ruta_bronze = "datalake/1_bronze/ventas_sucias.csv"

# Leemos el archivo tal cual como llegó del origen
df_bronze = pd.read_csv(ruta_bronze)
print("Datos crudos en Bronze encontrados:")
print(df_bronze, "\n")


# ==========================================
# 🥈 PASO 2: TRANSFORMAR Y GUARDAR EN SILVER
# ==========================================
print("🥈 Transformando datos hacia Capa SILVER...")

# Clonamos el dataframe para limpiarlo sin dañar el original
df_silver = df_bronze.copy()

# 1. Limpieza: Rellenar montos vacíos con el promedio de las ventas
monto_promedio = df_silver['monto_cop'].mean()
df_silver['monto_cop'] = df_silver['monto_cop'].fillna(monto_promedio)

# 2. Limpieza: Rellenar fechas vacías con una fecha por defecto
df_silver['fecha'] = df_silver['fecha'].fillna('2026-11-05')
# Estandarizamos el formato de la fecha para que use guiones (-) y no barras (/)
df_silver['fecha'] = df_silver['fecha'].str.replace('/', '-')

# 3. Estandarización: Colocar nombres y ciudades en Mayúscula Inicial (Title Case)
df_silver['nombre_cliente'] = df_silver['nombre_cliente'].str.title()
df_silver['ciudad'] = df_silver['ciudad'].str.title()

# Guardamos el resultado limpio en la carpeta Silver en formato CSV
ruta_silver = "datalake/2_silver/ventas_limpias.csv"
df_silver.to_csv(ruta_silver, index=False)
print("✅ Datos limpios guardados en SILVER:")
print(df_silver, "\n")


# ==========================================
# 🥇 PASO 3: AGREGAR Y GUARDAR EN GOLD
# ==========================================
print("🥇 Generando analítica para Capa GOLD...")

# Tomamos los datos limpios de Silver para hacer el reporte ejecutivo
df_gold = df_silver.copy()

# Agrupamos por Ciudad y calculamos: Total de ventas y número de transacciones
reporte_ciudades = df_gold.groupby('ciudad').agg(
    Total_Ingresos=('monto_cop', 'sum'),
    Cantidad_Ventas=('id_transaccion', 'count')
).reset_index()

# Guardamos el reporte optimizado en la carpeta Gold
ruta_gold = "datalake/3_gold/reporte_ventas_ciudad.csv"
reporte_ciudades.to_csv(ruta_gold, index=False)
print("🏆 Reporte de Negocio guardado en GOLD:")
print(reporte_ciudades)

print("\n🎉 ¡Pipeline finalizado con éxito de punta a punta! 🎉")
