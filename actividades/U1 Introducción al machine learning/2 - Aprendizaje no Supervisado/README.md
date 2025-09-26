1️⃣ Preparar y estandarizar los datos
Objetivo: Que todas las variables tengan la misma escala antes del clustering.

Supongamos que tienes en columnas:

B: Frecuencia de compra

C: Valor promedio de compra

D: Puntos de fidelidad

E: Tiempo como cliente

Para cada variable:

Calcular la media y desviación estándar.

Calcular el valor estandarizado con:

(Valor - Media) / DesviaciónEstándar
Guardar esos datos estandarizados en nuevas columnas (por ejemplo, F a I).

2️⃣ Configurar el K-means en Excel
Idea: Vamos a tener una tabla con:

Datos estandarizados de cada cliente

Coordenadas de los centros de los clusters

Asignación de cada cliente al cluster más cercano

Pasos:

Crear una tabla con k filas (número de clusters que quieras probar, p. ej. 3) y columnas para cada variable estandarizada → estos serán los centroides.

En cada fila de datos de clientes:

Calcular la distancia euclidiana a cada centroide:

Distancia = RAIZ( (X1 - Centroide1)^2 + (X2 - Centroide2)^2 + ... )
Asignar el cliente al cluster con menor distancia (usando =MIN y =COINCIDIR).

3️⃣ Usar Solver para optimizar
Objetivo: Minimizar la suma total de distancias cuadradas → equivalente a minimizar la inercia.

En Solver:

Objetivo: Celda con la suma total de distancias cuadradas.

Minimizar esa celda.

Cambiando: las coordenadas de los centroides.

Restricciones: Ninguna (a menos que quieras limitar rango de valores).

Ejecutar Solver → ajustará los centroides.

4️⃣ Calcular métricas
Después de tener los clusters finales:

Inercia: suma de distancias cuadradas cliente-centroide.

Silhouette Score:

No es trivial en Excel, pero puedes calcularlo:

Para cada cliente, a = media de distancias a clientes de su mismo cluster.

b = mínima media de distancias a clientes de otros clusters.

Silhouette = (b - a) / MAX(a, b)

Media de todos los silhouette = puntuación final.

Tamaño de cada cluster: contar clientes asignados.

5️⃣ Justificar número de clusters
Puedes probar distintos valores de k (2, 3, 4, etc.) y ver:

Gráfico de codo (inercia vs. k).

Silhouette (cuanto más alto, mejor).

El k con mejor balance suele ser el elegido.

6️⃣ Formar el CSV de submission
Poner en una columna todos los pares ID,value en el orden requerido:

cluster0_center_x,<valor>
cluster0_center_y,<valor>
cluster1_center_x,<valor>
cluster1_center_y,<valor>
cluster2_center_x,<valor>
cluster2_center_y,<valor>
inertia,<valor>
silhouette_score,<valor>
cluster0_size,<valor>
cluster1_size,<valor>
cluster2_size,<valor>
Asegurarte de usar punto . como separador decimal (Excel > Preferencias > Editar).

Unir columnas ID y value en una sola con =A1 & "," & B1.

Copiar → pegar valores → borrar columnas originales.

Guardar como .csv y subir.