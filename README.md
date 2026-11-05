# 🚀 Sistema de Ingesta y Arquitectura Medallion en la Nube (Simulación Local)

## 📝 Descripción del Proyecto
Este repositorio contiene el diseño, simulación e implementación de un entorno moderno de **Ingeniería de Datos** empleando las metodologías y conceptos clave del ecosistema corporativo de **Microsoft Azure**. 

El objetivo principal es demostrar habilidades en la ingesta, limpieza, modelado relacional y agregación de datos procedentes de diversas fuentes (estructuradas y semiestructuradas), simulando el comportamiento de un **Azure Data Lake Storage (ADLS)** y de **Azure SQL Database** directamente en un entorno local controlado.

---

## 🛠️ Tecnologías y Librerías Utilizadas
* **Lenguaje Principal:** Python 3.x
* **Entorno de Desarrollo:** Visual Studio Code (VS Code)
* **Motor de Base de Datos:** SQL Server (`localhost\SQLEXPRESS`)
* **Librerías de Procesamiento de Datos:** 
  * `Pandas` (Manipulación de datos, limpieza, indexación y agregaciones)
  * `PyODBC` (Conector nativo entre scripts de Python y el motor de SQL Server)
  * `JSON` (Mapeo y lectura de archivos semiestructurados)

---

## 📐 Arquitectura de la Solución (Procesos ETL / ELT)

### 1. Ingesta de Datos Estructurados y Semiestructurados (`SQL + JSON`)
* **Conexión Seguro a Base de Datos:** Implementación de cadenas de conexión parametrizadas (`Connection Strings`) con autenticación integrada de Windows para automatizar la creación de bases de datos relacionales (`db_ventas_local`).
* **Flujo ETL con JSON:** Lectura de estructuras de datos semiestructuradas independientes empleando parámetros seguros (`?`) para mitigar vulnerabilidades críticas de ciberseguridad como la *Inyección SQL*.
* **Modelo Relacional:** Inyección controlada y consolidación mediante sentencias avanzadas como `INNER JOIN` para cruzar dimensiones de clientes y hechos de ventas.

### 2. Diseño de Data Lake Moderno bajo Arquitectura Medallion
Simulación del almacenamiento masivo de datos mediante una jerarquía organizada en tres capas de madurez lógica:

* **🥉 Capa Bronze (Datos en Bruto / Raw):** Punto de entrada del lago de datos donde se preserva el historial intacto y crudo del negocio en formato `.csv` (`ventas_sucias.csv`), garantizando la trazabilidad y la posibilidad de reprocesamiento ante fallas.
* **🥈 Capa Silver (Datos Limpios y Validados / Enriched):** Aplicación de ingeniería de características mediante `Pandas`:
  * Tratamiento de valores nulos o faltantes (`.fillna()`) usando imputación estadística (media aritmética).
  * Normalización y estandarización de variables de texto plano a formato título (`.str.title()`).
  * Homogeneización y formateo de campos temporales/fechas.
* **🥇 Capa Gold (Datos de Negocio / Agregados):** Creación de KPIs agregados mediante funciones de agrupación (`.groupby()` y `.agg()`). Esta capa genera reportes ejecutivos optimizados listos para su consumo analítico en tableros de control de Inteligencia de Negocios (como *Power BI*) o modelos de Machine Learning.

---

## 📂 Estructura del Repositorio
```text
ruta-data-engineering-local/
│
├── datalake/                       # Simulación de Azure Data Lake Storage (ADLS)
│   ├── 1_bronze/                   # Archivos crudos de origen (Raw Data)
│   │   └── ventas_sucias.csv
│   ├── 2_silver/                   # Archivos limpios y estandarizados
│   │   └── ventas_limpias.csv
│   └── 3_gold/                     # Reportes finales y KPIs consolidados
│       └── reporte_ventas_ciudad.csv
│
├── ingenieria_datos_local.py       # Script de creación de BD relacional e ingesta SQL
├── ingesta_json_a_sql.py           # Pipeline ETL para conversión de JSON a tablas SQL
├── pipeline_medallion.py           # Pipeline completo del Data Lake (Bronze -> Silver -> Gold)
└── README.md                       # Documentación técnica del proyecto
```

---

## 📈 Resultados Obtenidos
El pipeline procesa los datos sucios y consolida métricas críticas de rendimiento comercial en milisegundos, entregando el siguiente esquema analítico en la capa final (**Gold**):

| Ciudad | Total Ingresos (COP) | Cantidad Ventas |
| :--- | :---: | :---: |
| Bogotá | 380,000.0 | 2 |
| Girardot | 600,000.0 | 2 |
| Medellín | 320,000.0 | 1 |

---
