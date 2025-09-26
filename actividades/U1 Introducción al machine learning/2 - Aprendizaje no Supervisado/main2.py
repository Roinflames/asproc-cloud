'''
Aprendizaje no supervisado
Entrenamiento
Python y Machine Learning
'''
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 1️⃣ Cargar datos
df = pd.read_csv("customer_segmentation.csv")

# Variables para clustering
features = ["purchase_frequency", "average_purchase", "loyalty_points", "months_active"]

X = df[features].values

# 2️⃣ Estandarizar variables
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3️⃣ Entrenar K-means
k = 3
kmeans = KMeans(n_clusters=k, random_state=42)
labels = kmeans.fit_predict(X_scaled)

# 4️⃣ Métricas
inertia = kmeans.inertia_
sil_score = silhouette_score(X_scaled, labels)
sizes = np.bincount(labels)
centroids = kmeans.cluster_centers_

# 5️⃣ PCA para graficar
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
centroids_pca = pca.transform(centroids)

# 7️⃣ Exportar CSV en formato requerido
rows = []
for i in range(k):
    rows.append([f"cluster{i}_center_x", round(centroids[i, 0], 2)])
    rows.append([f"cluster{i}_center_y", round(centroids[i, 1], 2)])
rows.append(["inertia", round(inertia, 2)])
rows.append(["silhouette_score", round(sil_score, 2)])
for i in range(k):
    rows.append([f"cluster{i}_size", float(sizes[i])])

df_out = pd.DataFrame(rows, columns=["ID", "value"])
df_out.to_csv("submission.csv", index=False)
print("✅ Archivo 'submission.csv' generado con éxito.")

# 6️⃣ Gráfico de clusters
plt.figure(figsize=(8, 6))
sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=labels, palette="Set2", s=60, alpha=0.8)
plt.scatter(centroids_pca[:, 0], centroids_pca[:, 1], c="red", marker="X", s=200, label="Centroides")
plt.title(f"K-means Clustering (k={k})\nSilhouette={sil_score:.2f} | Inertia={inertia:.2f}")
plt.xlabel("Componente Principal 1")
plt.ylabel("Componente Principal 2")
plt.legend()
plt.show()
