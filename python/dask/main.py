"""
Computación distribuida y paralela con Dask
"""
import dask.dataframe as dd
import pandas as pd

# 1️⃣ Crear un DataFrame de ejemplo usando Pandas
data = pd.DataFrame([
    {"nombre": "Rodrigo", "edad": 34, "ciudad": "Santiago"},
    {"nombre": "Juan", "edad": 29, "ciudad": "Valparaíso"},
    {"nombre": "Camila", "edad": 40, "ciudad": "Concepción"},
    {"nombre": "Ana", "edad": 25, "ciudad": "Santiago"},
    {"nombre": "Luis", "edad": 38, "ciudad": "Valparaíso"}
])

# 2️⃣ Convertir a DataFrame de Dask (particionado automáticamente)
ddf = dd.from_pandas(data, npartitions=2)

# 3️⃣ Mostrar los datos (ejecuta computación con .compute())
print("📋 DataFrame original:")
print(ddf.compute())

# 4️⃣ Filtrar personas mayores de 30
ddf_mayores = ddf[ddf['edad'] > 30]
print("\n👤 Personas mayores de 30:")
print(ddf_mayores.compute())

# 5️⃣ Calcular edad promedio
edad_promedio = ddf['edad'].mean().compute()
print(f"\n📊 Edad promedio: {edad_promedio}")

# 6️⃣ Agrupar por ciudad y contar
cantidad_por_ciudad = ddf.groupby('ciudad').size().compute()
print("\n🏙️ Cantidad de personas por ciudad:")
print(cantidad_por_ciudad)
