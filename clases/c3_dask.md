Dask es una biblioteca de Python para computación paralela y distribuida, pensada para manejar datos más grandes que la memoria o acelerar operaciones que normalmente harías con Pandas, NumPy o Python puro.

# 🔹 Conceptos clave

## DataFrames paralelos

Dask tiene dask.dataframe → muy parecido a Pandas, pero divide los datos en particiones y las procesa en paralelo.

Puedes trabajar con datasets enormes sin cargarlos enteros en RAM.

## Arrays paralelos

dask.array → similar a NumPy, pero distribuido y “lazy”, ideal para matrices grandes.

## Computación lazy

Todas las operaciones no se ejecutan inmediatamente.

Se construye un grafo de tareas, y se ejecuta cuando llamas a .compute().

Esto permite optimizar y paralelizar automáticamente.

## Distribuido

Dask puede correr en una sola máquina usando todos los núcleos, o en clústeres de decenas/hasta miles de nodos.

Compatible con SLURM, Kubernetes, Hadoop YARN, etc.

## Integración con Python nativo

Compatible con Pandas, NumPy, Scikit-Learn, XGBoost, etc.

No necesitas aprender un lenguaje nuevo como con Spark SQL.

🔹 Casos de uso comunes

| Caso                    | Por qué Dask es útil                                                |
| ----------------------- | ------------------------------------------------------------------- |
| CSV/Parquet muy grandes | Puedes leer y procesar archivos de GB o TB sin quedarte sin memoria |
| DataFrames tipo Pandas  | Mismo código que Pandas pero distribuido                            |
| Computación científica  | Arrays y álgebra lineal paralela con Dask Array                     |
| Machine Learning        | Integración con Scikit-Learn para entrenar modelos distribuidos     |
| Pipelines ETL           | Procesos paralelos de transformación de datos grandes               |


💡 Resumen rápido:

Dask es como un “Pandas y NumPy distribuido y paralelo” para Python. Te permite trabajar con datos grandes y ejecutar operaciones en múltiples núcleos o nodos, sin cambiar demasiado tu código.