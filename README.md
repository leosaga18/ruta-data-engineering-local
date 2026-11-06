# 🚀 Sistema de Ingesta y Arquitectura Medallion en la Nube (Simulación Local)

## 📝 Descripción del Proyecto
Este repositorio contiene el diseño, simulación e implementación de un entorno moderno de Ingeniería de Datos empleando las metodologías y conceptos clave del ecosistema corporativo de Microsoft Azure.

El objetivo principal es demostrar habilidades en la ingesta, limpieza, orquestación, procesamiento masivo (Big Data) y servido analítico de datos procedentes de diversas fuentes (estructuradas y semiestructuradas), simulando el comportamiento de un **Azure Data Lake Storage (ADLS)**, **Azure SQL Database**, **Azure Data Factory**, **Azure Synapse Analytics** y **Azure Databricks** directamente en un entorno local controlado, alineado con las competencias de las certificaciones internacionales **AZ-900**, **DP-900** y **DP-203**.

---

## 📐 Arquitectura de la Solución e Integración con Azure

Para asegurar un desarrollo eficiente y libre de costos de infraestructura en fases tempranas, se diseñó un flujo local parametrizado que mapea con total precisión los servicios empresariales en la nube:

| Componente Local | Servicio Replicado en Azure | Rol en la Arquitectura |
| :--- | :--- | :--- |
| **SQL Server (`db_ventas_local`)** | **Azure SQL Database** | Almacenamiento relacional transaccional (Origen de datos). |
| **Estructura de Carpetas `datalake/`** | **Azure Data Lake Storage Gen2 (ADLS)** | Almacenamiento masivo jerárquico de objetos. |
| **`pipeline_medallion.py` (Pandas)** | **Azure Synapse Analytics (Pipelines)** | Motor de procesamiento y transformación clásico (ETL). |
| **`pipeline_databricks_local.py` (PySpark)**| **Azure Databricks (Apache Spark)** | Procesamiento distribuido a gran escala (Big Data) en memoria. |
| **`orquestador_local.py` (Subprocess)** | **Azure Data Factory (ADF)** | Orquestación basada en disparadores por eventos de almacenamiento. |
| **`analitica_synapse_local.py` (DuckDB)** | **Azure Synapse Serverless SQL Pools** | Consultas analíticas directas sobre archivos del Data Lake usando SQL. |
| **Power BI Desktop** | **Power BI Service** | Capa de consumo y visualización analítica (Dashboards / KPIs). |

### 1. Ingesta de Datos Estructurados y Semiestructurados (SQL + JSON)
* **Conexión Segura a Base de Datos:** Implementación de cadenas de conexión parametrizadas (*Connection Strings*) con autenticación integrada de Windows para automatizar la creación de bases de datos relacionales (`db_ventas_local`).
* **Flujo ETL con JSON:** Lectura de estructuras de datos semiestructuradas independientes empleando parámetros seguros (`?`) para mitigar vulnerabilidades críticas de ciberseguridad como la *SQL Injection*.
* **Modelo Relacional:** Inyección controlada y consolidación mediante sentencias avanzadas como `INNER JOIN` para cruzar dimensiones de clientes y hechos de ventas.

### 2. Diseño de Data Lake Moderno bajo Arquitectura Medallón
Simulación del almacenamiento masivo de datos mediante una jerarquía organizada en tres capas de madurez lógica:
* **🥉 Capa Bronze (Datos en Bruto / Raw):** Punto de entrada del lago de datos donde se preserva el historial intacto y crudo del negocio en formato `.csv` (`ventas_sucias.csv`), garantizando la trazabilidad y la posibilidad de reprocesamiento ante fallas.
* **🥈 Capa Silver (Datos Limpios y Validados / Enriched):** Aplicación de ingeniería de características mediante Pandas y Apache Spark. Se realiza la imputación estadística de valores faltantes (media aritmética), estandarización de formatos cronológicos con guiones (`-`) y capitalización uniforme de variables textuales (`Title Case`).
* **🥇 Capa Gold (Datos de Negocio / Agregados):** Creación de KPIs agregados mediante funciones de agrupación (`.groupby()` y `.agg()`). Esta capa genera reportes ejecutivos optimizados listos para su consumo analítico.

### 3. Orquestación Automatizada e Ingeniería de Eventos (DataOps)
El script `orquestador_local.py` actúa conceptualmente como un **Event-Driven Trigger de Azure Data Factory**. Monitorea de manera asíncrona la capa Bronze mediante hilos de tiempo. Al detectar la ingesta de un nuevo archivo, dispara el subproceso del pipeline de transformación de manera 100% automática, garantizando la actualización continua de las capas sin intervención humana.

### 4. Consultas Analíticas y Servido de Datos (Módulo 3: Synapse Analytics)
Con el script `analitica_synapse_local.py`, emulo la capacidad **Serverless SQL Pools de Azure Synapse Analytics**. Utilizando consultas SQL directas vectorizadas sobre archivos planos en el Data Lake sin cargarlos en bases de datos relacionales tradicionales, logrando filtros dinámicos de altas ventas en memoria, cálculos avanzados como el **Ticket Promedio por Ciudad**, y la generación de una estructura final optimizada para **Power BI Desktop**.

### 5. Computación Distribuida y Big Data (Módulo 4: Azure Databricks / Spark)
A través de `pipeline_databricks_local.py`, el entorno migra hacia un motor de procesamiento paralelo masivo utilizando **PySpark**:
* **Evaluación Perezosa (Lazy Evaluation):** Construcción de grafos de ejecución optimizados (DAG) antes de computar los datos en los nodos esclavos.
* **Almacenamiento Columnar Delta/Parquet:** Los datos transformados de la capa Silver se escriben particionados en formato binario estructurado `.parquet`, reduciendo drásticamente el espacio en disco y acelerando los tiempos de lectura para analítica avanzada de Big Data.

---

## 🛠️ Tecnologías y Librerías Utilizadas
* **Idioma principal:** Python 3.13+
* **Framework de Big Data:** Apache Spark 3.5+ (PySpark) y Java JRE/JDK 17
* **Entorno de Desarrollo:** Visual Studio Code (VS Code)
* **Motor de Base de Datos:** SQL Server (`localhost\SQLEXPRESS`)
* **Librerías de Procesamiento y Automatización:**
  * **Pandas:** Manipulación de datos, limpieza, indexación y agregaciones básicas.
  * **DuckDB:** Simulación analítica ultrarrápida de consultas SQL en memoria sobre archivos del Data Lake.
  * **PyODBC & JSON:** Conectividad relacional y mapeo de archivos semiestructurados.
  * **Subprocess & OS:** Gestión del sistema operativo, inyección de variables de entorno y orquestación por eventos.

---

## 📂 Estructura del Repositorio
```text
ruta-data-engineering-local/
│
├── datalake/                       # Simulación de Azure Data Lake Storage (ADLS)
│   ├── 1_bronze/                   # Archivos crudos de origen (Raw Data)
│   │   └── ventas_sucias.csv
│   ├── 2_silver/                   # Archivos limpios y estandarizados
│   │   ├── ventas_limpias.csv
│   │   └── ventas_pyspark_parquet/ # Carpeta de almacenamiento distribuido Parquet (Big Data)
│   └── 3_gold/                     # Reportes finales y KPIs consolidados
│       ├── reporte_ventas_ciudad.csv
│       └── kpis_entregables.csv    # Dataset optimizado para Power BI
│
├── ingenieria_datos_local.py       # Script de creación de BD relacional e ingesta SQL
├── ingesta_json_a_sql.py           # Pipeline ETL para conversión de JSON a tablas SQL
├── pipeline_medallion.py           # Pipeline completo del Data Lake (Bronze -> Silver -> Gold)
├── pipeline_databricks_local.py    # Pipeline de Big Data con Apache Spark / Databricks
├── orquestador_local.py            # Orquestador automatizado basado en eventos de carpeta
├── analitica_synapse_local.py      # Simulador de Azure Synapse Serverless SQL Pools
└── README.md                       # Documentación técnica del proyecto
```

---

## 📈 Resultados Obtenidos (Capa de Servido Gold)
El pipeline analítico consolida métricas críticas de rendimiento comercial, entregando el siguiente esquema en la capa final entregable para Inteligencia de Negocios (**Gold**):

| Ciudad | Total_Ingresos | Cantidad_Ventas | Ticket_Promedio_Ciudad |
| :--- | :--- | :--- | :--- |
| Girardot | 600,000.0 | 2 | 300,000.0 |
| Bogotá | 380,000.0 | 2 | 190,000.0 |
| Medellín | 320,000.0 | 1 | 320,000.0 |

---

## 💡 Bitácora de Ingeniería y Solución de Problemas (Troubleshooting)

Durante el despliegue operativo del entorno de automatización local en sistemas Windows, se documentaron y solucionaron los siguientes retos de infraestructura de software:

* **Incidente 1 (Unicode):** `UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f680'`. Los scripts de transformación colapsaban al imprimir emojis en consola por la codificación nativa de Windows (`cp1252`).
  * **Solución:** Se modificó el entorno de ejecución en `orquestador_local.py` para inyectar dinámicamente variables del sistema (`PYTHONUTF8 = 1`) forzando el estándar universal **UTF-8**.
* **Incidente 2 (Big Data Runtime Error):** Spark bloqueaba el controlador debido a una desincronización entre el hilo maestro de ejecución de Python y los binarios de Hadoop (`Hadoop bin directory does not exist: C:\Hadoop\bin\bin`).
  * **Solución de Infraestructura:** Se depuraron las variables globales del sistema, reestructurando la variable raíz `HADOOP_HOME=C:\hadoop` e integrando explícitamente en las propiedades del sistema las variables `PYSPARK_PYTHON` y `PYSPARK_DRIVER_PYTHON` apuntando al intérprete nativo de Python 3.13, logrando la perfecta inicialización de la JVM y la compilación distribuida de Spark sobre Windows.
