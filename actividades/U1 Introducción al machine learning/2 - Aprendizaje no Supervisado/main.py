import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import os

# --- Constantes ---
SCRIPT_DIR = os.path.dirname(__file__)
DATA_FILE_PATH = os.path.join(SCRIPT_DIR, "customer_segmentation.csv")
SUBMISSION_FILE_PATH = os.path.join(SCRIPT_DIR, "submission.csv")
FEATURES = ["purchase_frequency", "average_purchase", "loyalty_points", "months_active"]


def load_data(path):
    print("Paso 1: Cargando datos...")
    return pd.read_csv(path)


def preprocess_data(df):
    print("Paso 2: Escalando datos...")
    X = df[FEATURES].values
    scaler = StandardScaler()
    return scaler.fit_transform(X)


def train_kmeans(X, k=3):
    print(f"Paso 3: Entrenando KMeans con k={k}...")
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(X)
    return kmeans, labels


def evaluate_model(X, labels, kmeans):
    print("Paso 4: Evaluando modelo...")
    inertia = kmeans.inertia_
    sil_score = silhouette_score(X, labels) if len(set(labels)) > 1 else None
    return inertia, sil_score


def export_results(kmeans, labels, inertia, sil_score, path):
    print("Paso 5: Exportando resultados...")
    rows = []
    sizes = np.bincount(labels)
    for i, centroid in enumerate(kmeans.cluster_centers_):
        for j, val in enumerate(centroid):
            rows.append([f"cluster{i}_center_{FEATURES[j]}", round(val, 2)])
        rows.append([f"cluster{i}_size", float(sizes[i])])

    rows.append(["inertia", round(inertia, 2)])
    if sil_score is not None:
        rows.append(["silhouette_score", round(sil_score, 2)])

    df_out = pd.DataFrame(rows, columns=["ID", "value"])
    df_out.to_csv(path, index=False)
    print(f"✅ Archivo '{path}' generado con éxito.")


def main():
    df = load_data(DATA_FILE_PATH)
    X_scaled = preprocess_data(df)
    kmeans, labels = train_kmeans(X_scaled, k=3)
    inertia, sil_score = evaluate_model(X_scaled, labels, kmeans)
    export_results(kmeans, labels, inertia, sil_score, SUBMISSION_FILE_PATH)


if __name__ == "__main__":
    main()
