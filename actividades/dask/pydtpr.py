# main.py
import dask.dataframe as dd

# --- Leer archivos CSV con Dask ---
train = dd.read_csv('dtpr/data/train.csv', sep=';', decimal=',')
test = dd.read_csv('dtpr/data/test.csv', sep=';', decimal=',')

# --- Mostrar las primeras filas ---
print("Primeras filas de train:")
print(train.head())

print("\nPrimeras filas de test:")
print(test.head())

# --- Estadísticas descriptivas ---
print("\nEstadísticas de train:")
print(train.describe().compute())

# --- Filtrado de ejemplo ---
# Mostrar solo transacciones mayores a 200
print("\nTransacciones mayores a 200:")
print(train[train['MONTO_TRANSACCION'] > 200].compute())

# --- Agrupación de ejemplo ---
# Promedio de monto por tipo de tarifa
promedio_tarifa = train.groupby('TIPO_TARIFA')['MONTO_TRANSACCION'].mean().compute()
print("\nPromedio de monto por tipo de tarifa:")
print(promedio_tarifa)
