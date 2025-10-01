from pyspark.sql import SparkSession
from pyspark.sql.functions import col

import findspark
findspark.init()

# 1. Crear la sesión de Spark
spark = SparkSession.builder \
    .appName("Ejemplo PySpark") \
    .getOrCreate()

# 2. Crear un DataFrame desde una lista de diccionarios
data = [
    {"nombre": "Rodrigo", "edad": 34, "ciudad": "Santiago"},
    {"nombre": "Juan", "edad": 29, "ciudad": "Valparaíso"},
    {"nombre": "Camila", "edad": 40, "ciudad": "Concepción"}
]

df = spark.createDataFrame(data)

print("📋 DataFrame original:")
df.show()

# 3. Filtrar personas mayores de 30
df_filtrado = df.filter(col("edad") > 30)

print("👤 Personas mayores de 30:")
df_filtrado.show()

# 4. Calcular edad promedio
df.groupBy().avg("edad").show()

# 5. Registrar como vista temporal y ejecutar SQL
df.createOrReplaceTempView("personas")
resultado_sql = spark.sql("SELECT ciudad, COUNT(*) as cantidad FROM personas GROUP BY ciudad")
print("🏙️ Cantidad de personas por ciudad:")
resultado_sql.show()
