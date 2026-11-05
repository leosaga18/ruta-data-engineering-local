# 🚀 Sistema de Ingesta y Arquitectura Medallion en la Nube (Simulación Local)

## 📝 Descripción del Proyecto
Este repositorio contiene el diseño, simulación e implementación de un entorno moderno de Ingeniería de Datos empleando las metodologías y conceptos clave del ecosistema corporativo de Microsoft Azure.

El objetivo principal es demostrar habilidades en la ingesta, limpieza, orquestación, modelado relacional y agregación de datos procedentes de diversas fuentes (estructuradas y semiestructuradas), simulando el comportamiento de un **Azure Data Lake Storage (ADLS)**, **Azure SQL Database** y **Azure Data Factory** directamente en un entorno local controlado, alineado con las competencias de las certificaciones internacionales **AZ-900**, **DP-900** y **DP-203**.

---

## 📐 Arquitectura de la Solución e Integración con Azure

Para asegurar un desarrollo eficiente y libre de costos de infraestructura en fases tempranas, se diseñó un flujo local parametrizado que mapea con total precisión los servicios empresariales en la nube:

| Componente Local | Servicio Replicado en Azure | Rol en la Arquitectura |
| :--- | :--- | :--- |
| **SQL Server (`db_ventas_local`)** | **Azure SQL Database** | Almacenamiento relacional transaccional (Origen de datos). |
| **Estructura de Carpetas `datalake/`** | **Azure Data Lake Storage Gen2 (ADLS)** | Almacenamiento masivo jerárquico de objetos. |
| **`pipeline_medallion.py` (Pandas)** | **Azure Synapse / Azure Databricks** | Motor de procesamiento, limpieza y transformación (ETL). |
| **`orquestador_local.py` (Subprocess)** | **Azure Data Factory (ADF)** | Orquestación basada en disparadores por eventos de almacenamiento. |
| **Power BI Desktop** | **Power BI Service** | Capa de consumo y visualización analítica (Dashboards / KPIs). |

### 1. Ingesta de Datos Estructurados y Semiestructurados (SQL + JSON)
* **Conexión Segura a Base de Datos:** Implementación de cadenas de conexión parametrizadas (*Connection Strings*) con autenticación integrada de Windows para automatizar la creación de bases de datos relacionales (`db_ventas_local`).
* **Flujo ETL con JSON:** Lectura de estructuras de datos semiestructuradas independientes empleando parámetros seguros (`?`) para mitigar vulnerabilidades críticas de ciberseguridad como la *SQL Injection*.
* **Modelo Relacional:** Inyección controlada y consolidación mediante sentencias avanzadas como `INNER JOIN` para cruzar dimensiones de clientes y hechos de ventas.

### 2. Diseño de Data Lake Moderno bajo Arquitectura Medallón
Simulación del almacenamiento masivo de datos mediante una jerarquía organizada en tres capas de madurez lógica:
* **🥉 Capa Bronze (Datos en Bruto / Raw):** Punto de entrada del lago de datos donde se preserva el historial intacto y crudo del negocio en formato `.csv` (`ventas_sucias.csv`), garantizando la trazabilidad y la posibilidad de reprocesamiento ante fallas.
* **🥈 Capa Silver (Datos Limpios y Validados / Enriched):** Aplicación de ingeniería de características mediante Pandas:
  * Tratamiento de valores nulos o faltantes (`.fillna()`) usando imputación estadística (media aritmética).
  * Normalización y estandarización de variables de texto plano a formato título (`.str.title()`).
  * Homogeneización y formato estandarizado de campos temporales/fechas usando guiones (`-`).
* **🥇 Capa Gold (Datos de Negocio / Agregados):** Creación de KPIs agregados mediante funciones de agrupación (`.groupby()` y `.agg()`). Esta capa genera reportes ejecutivos optimizados listos para su consumo analítico en tableros de control de Inteligencia de Negocios (como Power BI) o modelos de Machine Learning.

### 3. Orquestación Automatizada e Ingeniería de Eventos (DataOps)
El script `orquestador_local.py` actúa conceptualmente como un **Event-Driven Trigger de Azure Data Factory**. Monitorea de manera asíncrona la capa Bronze mediante hilos de tiempo. 

Al detectar la ingesta de un nuevo archivo en el almacenamiento, rompe de inmediato el estado de espera en la terminal, aísla el lote de datos entrante y dispara el subproceso del pipeline de transformación de manera 100% automática, garantizando la actualización automática y fluida de las capas Silver y Gold sin intervención humana.

---

## 🛠️ Tecnologías y Librerías Utilizadas
* **Idioma principal:** Python 3.13+
* **Entorno de Desarrollo:** Visual Studio Code (VS Code)
* **Motor de Base de Datos:** SQL Server (`localhost\SQLEXPRESS`)
* **Librerías de Procesamiento y Automatización:**
  * **Pandas:** Manipulación de datos, limpieza, indexación y agregaciones.
  * **PyODBC:** Conector nativo entre scripts de Python y el motor de SQL Server.
  * **JSON:** Mapeo y lectura de archivos semiestructurados.
  * **Subprocess & OS:** Gestión del sistema operativo, inyección de variables de entorno y ejecución asíncrona de scripts en segundo plano.

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
├── orquestador_local.py            # Orquestador automatizado basado en eventos de carpeta
└── README.md                       # Documentación técnica del proyecto
```

---

## 📈 Resultados Obtenidos
El pipeline automatizado procesa los datos sucios y consolida métricas críticas de rendimiento comercial en milisegundos, entregando el siguiente esquema analítico en la capa final (**Gold**):

| Ciudad | Total_Ingresos (COP) | Cantidad_Ventas |
| :--- | :--- | :--- |
| Bogotá | 380,000.0 | 2 |
| Girardot | 600,000.0 | 2 |
| Medellín | 320,000.0 | 1 |

---

## 💡 Bitácora de Ingeniería y Solución de Problemas (Troubleshooting)

Durante el despliegue operativo del entorno de automatización local en sistemas Windows, se documentó y solucionó el siguiente reto de infraestructura de software:

* **Incidente:** `UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f680'`. Los scripts de transformación colapsaban abruptamente al intentar imprimir registros decorados con emojis en la consola debido a restricciones de codificación heredadas del sistema operativo (`cp1252`).
* **Solución Aplicada:** En lugar de purgar los logs decorativos del código fuente, se modificó el entorno de ejecución en `orquestador_local.py` para inyectar dinámicamente variables del sistema (`PYTHONUTF8 = 1`) y forzar la ejecución del proceso secundario (`subprocess.run`) bajo el estándar universal **UTF-8**, haciendo que la tubería automatizada de datos sea tolerante a fallas por caracteres especiales.
