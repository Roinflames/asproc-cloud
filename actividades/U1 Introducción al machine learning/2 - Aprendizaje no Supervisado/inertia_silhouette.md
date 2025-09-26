🔹 1. Inercia (Within-Cluster Sum of Squares - WCSS)

Mide la compacidad de los clústeres: qué tan cerca están los puntos de sus centroides.

Siempre es un valor positivo y disminuye a medida que aumentamos el número de clústeres k.

No tiene un valor “ideal” absoluto → se usa en conjunto con el método del codo (Elbow Method):

Se grafica inercia vs k.

El punto donde la curva deja de decrecer bruscamente (el “codo”) suele ser un buen valor de k.

👉 Regla: Menor inercia = mejor, pero cuidado con elegir un k demasiado alto que sobreajuste.

🔹 2. Silhouette Score

Varía entre -1 y 1:

Cerca de 1 → Los clústeres están bien definidos y separados.

Cerca de 0 → Los clústeres se traslapan o los puntos están en el borde entre grupos.

Negativo (< 0) → Muchos puntos están mal asignados a su clúster.

Regla práctica:

> 0.5 → Bueno, clústeres bien formados.

0.25 – 0.5 → Aceptable, pero hay traslape.

< 0.25 → Mala separación, probablemente k no es adecuado.