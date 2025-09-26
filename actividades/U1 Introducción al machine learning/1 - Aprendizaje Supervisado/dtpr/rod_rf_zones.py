import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.cluster import KMeans
import os # Importamos os para manejar rutas de archivo de forma robusta
import matplotlib.pyplot as plt
import seaborn as sns

# --- Definición de Constantes y Rutas ---
SCRIPT_DIR = os.path.dirname(__file__)

TRAIN_FILE_PATH = os.path.join(SCRIPT_DIR, "data", "train.csv")
TEST_FILE_PATH = os.path.join(SCRIPT_DIR, "data", "test.csv")
RECAUDO_FILE_PATH = os.path.join(SCRIPT_DIR, "data", "recaudo.csv")
SUBMISSION_FILE_PATH = os.path.join(SCRIPT_DIR, "submission_rf_zones.csv")
PLOT_FILE_PATH = os.path.join(SCRIPT_DIR, "kmeans_clusters.png")
ELBOW_PLOT_FILE_PATH = os.path.join(SCRIPT_DIR, "kmeans_elbow_plot.png")

# Problema de clasificación multiclase.
"""
Clasificación de tipo de tarifa
Objetivo: predecir TIPO_TARIFA a partir de MONTO_TRANSACCION, MEDIO_ACCESO y coordenadas.
Sería similar al Titanic (donde se predice “sobrevive / no sobrevive”), pero ahora el target son categorías de tarifa (ej. escolar, adulto, adulto mayor).
Pros: se ajusta 1:1 a Random Forest, Decision Trees, Logistic Regression, etc.
Requiere: tener bien definidos los códigos de TIPO_TARIFA.
"""

# Definimos las características (features) que usaremos para entrenar el modelo y el objetivo (target).
"""
Features:
TIPO_TARIFA	
    1: Tarifa Adulto
    2: Tarifa TNE
    3: Tarifa TAM
MONTO_TRANSACCION
MEDIO_ACCESO	
    1: Pago con tarjeta sin contacto
    2: Pago con QR
LATITUDE_USO	
LONGITUDE_USO
"""
FEATURES = ['MEDIO_ACCESO', 'ZONA_GEO']
TARGET = 'TIPO_TARIFA'

def load_data(train_path, test_path):
    """
    Carga los archivos CSV de entrenamiento y prueba en DataFrames de pandas.
    """
    print("Paso 1: Cargando datos...")
    try:
        train_df = pd.read_csv(train_path, sep=";", encoding="utf-8")
        test_df = pd.read_csv(test_path, sep=";", encoding="utf-8")
        print("Datos cargados exitosamente.")
        return train_df, test_df
    except FileNotFoundError as e:
        print(f"Error: No se encontró el archivo. Asegúrate de que los archivos CSV estén en la ruta correcta: {e}")
        print(f"Ruta de train.csv esperada: {train_path}")
        print(f"Ruta de test.csv esperada: {test_path}")
        exit()

def plot_clusters(df, kmeans_model, plot_path):
    """
    Visualiza y guarda el gráfico de los clusters de KMeans.
    """
    print("Generando gráfico de clusters...")
    plt.figure(figsize=(12, 8))
    
    sns.scatterplot(data=df, x='LONGITUDE_USO', y='LATITUDE_USO', hue='ZONA_GEO', palette='viridis', s=50, alpha=0.7, legend='full')
    
    centroids = kmeans_model.cluster_centers_
    plt.scatter(centroids[:, 1], centroids[:, 0], s=200, c='red', marker='X', label='Centroides')
    
    plt.title('Visualización de Clusters Geográficos (KMeans)')
    plt.xlabel('Longitud')
    plt.ylabel('Latitud')
    plt.legend(title='Zona Geográfica')
    plt.grid(True)
    
    plt.savefig(plot_path)
    plt.close()
    print(f"Gráfico guardado en: {plot_path}")

def find_optimal_clusters(data, plot_path):
    """
    Calcula y grafica la inercia para diferentes números de clusters (Método del Codo).
    """
    print("Calculando el número óptimo de clusters con el Método del Codo...")
    inertias = []
    k_range = range(1, 16)
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(data)
        inertias.append(kmeans.inertia_)
    
    plt.figure(figsize=(10, 6))
    plt.plot(k_range, inertias, marker='o')
    plt.title('Método del Codo para KMeans')
    plt.xlabel('Número de Clusters (k)')
    plt.ylabel('Inercia')
    plt.xticks(k_range)
    plt.grid(True)
    plt.savefig(plot_path)
    plt.close()
    print(f"Gráfico del Método del Codo guardado en: {plot_path}")

def preprocess_data(train_df, test_df):
    """
    Preprocesa los datos para el modelo.
    - Convierte latitud y longitud a float.
    - Maneja valores faltantes.
    - Crea y grafica zonas geográficas usando KMeans.
    """
    print("Paso 2: Preprocesando datos y creando zonas geográficas...")
    train_df_processed = train_df.copy()
    test_df_processed = test_df.copy()

    # --- Conversión de LAT y LONG ---
    for df in [train_df_processed, test_df_processed]:
        df["LATITUDE_USO"] = df["LATITUDE_USO"].astype(str).str.replace(",", ".", regex=False).astype(float)
        df["LONGITUDE_USO"] = df["LONGITUDE_USO"].astype(str).str.replace(",", ".", regex=False).astype(float)

        df["LATITUDE_USO"].fillna(df["LATITUDE_USO"].median(), inplace=True)
        df["LONGITUDE_USO"].fillna(df["LONGITUDE_USO"].median(), inplace=True)

    # --- Creación de Zonas Geográficas con KMeans ---
    all_coords = pd.concat([
        train_df_processed[['LATITUDE_USO', 'LONGITUDE_USO']],
        test_df_processed[['LATITUDE_USO', 'LONGITUDE_USO']]
    ])

    # --- Encontrar k óptimo con el método del codo ---
    find_optimal_clusters(all_coords, ELBOW_PLOT_FILE_PATH)

    # Usamos n_clusters=6 basado en el hallazgo del usuario
    n_clusters = 6 
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(all_coords)

    train_df_processed['ZONA_GEO'] = kmeans.predict(train_df_processed[['LATITUDE_USO', 'LONGITUDE_USO']])
    test_df_processed['ZONA_GEO'] = kmeans.predict(test_df_processed[['LATITUDE_USO', 'LONGITUDE_USO']])
    print(f"Se han creado {n_clusters} zonas geográficas.")

    # --- Visualización de los Clusters ---
    combined_df_for_plot = pd.concat([train_df_processed, test_df_processed])
    plot_clusters(combined_df_for_plot, kmeans, PLOT_FILE_PATH)

    return train_df_processed, test_df_processed

def train_and_evaluate_model(df):
    """
    Entrena y evalúa el modelo de clasificación.
    """
    # Separar características (X) y objetivo (y)
    X = df[FEATURES]
    y = df[TARGET]

    # Dividir los datos en entrenamiento y validación (80% para entrenar, 20% para validar)
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Datos divididos: {len(X_train)} para entrenamiento, {len(X_val)} para validación.")
    
    clf = RandomForestClassifier(
        n_estimators=100, 
        random_state=42, 
        verbose=1
    )
    
    # Entrenar el modelo
    print("Entrenando el modelo RandomForest con zonas geográficas...")
    clf.fit(X_train, y_train)
    
    # --- Evaluación del Modelo ---
    predictions = clf.predict(X_val)

    accuracy = accuracy_score(y_val, predictions)

    print("-" * 30)
    print("Paso 4: Evaluación del modelo")
    print(f"Precisión (Accuracy) en el conjunto de validación: {accuracy:.2%}")
    print("Explicación: Este valor representa el porcentaje de predicciones correctas que hizo el modelo sobre el conjunto de validación.")
    print("Un valor más alto es mejor. Nos da una idea de cómo se comportará el modelo con datos nuevos.")
    print("-" * 30)

    return clf

def generate_submission_file(model, test_df, submission_path):
    """
    Genera el archivo de submission.
    """
    print("Paso 5: Generando archivo de predicciones...")

    X_test = test_df[FEATURES]

    test_predictions = model.predict(X_test)

    output = pd.DataFrame({
        'TIPO_TARIFA': test_predictions
    })

    output.to_csv(submission_path, index=False)
    print(f"Archivo de predicciones guardado en: {submission_path}")

def main():
    """
    Función principal que orquesta todo el proceso.
    """
    # 1. Cargar datos
    train_df, test_df = load_data(TRAIN_FILE_PATH, TEST_FILE_PATH)
    print(f"Datos de entrenamiento: {train_df.shape}")
    print(f"Datos de prueba: {test_df.shape}")
    # 2. Preprocesar datos
    train_processed, test_processed = preprocess_data(train_df, test_df)
    # 3. Entrenar y evaluar el modelo (usando solo los datos de entrenamiento procesados)
    trained_model = train_and_evaluate_model(train_processed)
    # 4. Generar el archivo de predicciones (usando el modelo entrenado y los datos de prueba procesados)
    generate_submission_file(trained_model, test_processed, SUBMISSION_FILE_PATH)
    print("\nProceso completado.")

if __name__ == "__main__":
    main()
