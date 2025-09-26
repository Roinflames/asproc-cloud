import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os # Importamos os para manejar rutas de archivo de forma robusta

# --- Definición de Constantes y Rutas ---
SCRIPT_DIR = os.path.dirname(__file__)

TRAIN_FILE_PATH = os.path.join(SCRIPT_DIR, "data", "train.csv")
TEST_FILE_PATH = os.path.join(SCRIPT_DIR, "data", "test.csv")
SUBMISSION_FILE_PATH = os.path.join(SCRIPT_DIR, "submission.csv")

# Definimos las características (features) que usaremos para entrenar el modelo y el objetivo (target).
FEATURES = ['']
TARGET = ''

def load_data(train_path, test_path):
    """
    Carga los archivos CSV de entrenamiento y prueba en DataFrames de pandas.
    """
    print("Paso 1: Cargando datos...")
    try:
        train_df = pd.read_csv(train_path)
        test_df = pd.read_csv(test_path)
        print("Datos cargados exitosamente.")
        return train_df, test_df
    except FileNotFoundError as e:
        print(f"Error: No se encontró el archivo. Asegúrate de que los archivos CSV estén en la ruta correcta: {e}")
        print(f"Ruta de train.csv esperada: {train_path}")
        print(f"Ruta de test.csv esperada: {test_path}")
        exit()
        
def preprocess_data(train_df, test_df):
    """
    Preprocesa los datos para el modelo.
    - Convierte la columna 'Sex' a valores numéricos.
    - Rellena los valores faltantes en 'Age' con la mediana.
    """
    pass

def train_and_evaluate_model(df):
    """
    Entrena y evalúa el modelo de clasificación.
    """
    pass

def generate_submission_file(model, test_df, submission_path):
    """
    Genera el archivo de submission para Kaggle.
    """
    pass

def main():
    """
    Función principal que orquesta todo el proceso.
    """
    # 1. Cargar datos
    train_df, test_df = load_data(TRAIN_FILE_PATH, TEST_FILE_PATH)
    # 2. Preprocesar datos
    train_processed, test_processed = preprocess_data(train_df, test_df)
    # 3. Entrenar y evaluar el modelo (usando solo los datos de entrenamiento procesados)
    trained_model = train_and_evaluate_model(train_processed)
    # 4. Generar el archivo de predicciones (usando el modelo entrenado y los datos de prueba procesados)
    generate_submission_file(trained_model, test_processed, SUBMISSION_FILE_PATH)
    print("\nProceso completado.")

if __name__ == "__main__":
    main()