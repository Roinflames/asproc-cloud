import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import os # Importamos os para manejar rutas de archivo de forma robusta

# --- Definición de Constantes y Rutas ---
SCRIPT_DIR = os.path.dirname(__file__)

TRAIN_FILE_PATH = os.path.join(SCRIPT_DIR, "data", "train.csv")
TEST_FILE_PATH = os.path.join(SCRIPT_DIR, "data", "test.csv")
RECAUDO_FILE_PATH = os.path.join(SCRIPT_DIR, "data", "recaudo.csv")
SUBMISSION_FILE_PATH = os.path.join(SCRIPT_DIR, "submission_xgboost.csv")

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
FEATURES = ['MEDIO_ACCESO', 'LATITUDE_USO', 'LONGITUDE_USO']
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
        
def preprocess_data(train_df, test_df):
    """
    Preprocesa los datos para el modelo.
    - Convierte latitud y longitud a float.
    - Maneja valores faltantes.
    - Elimina TIPO_TARIFA en el test set.
    """
    train_df_processed = train_df.copy()
    test_df_processed = test_df.copy()

    # --- Conversión de LAT y LONG ---
    for df in [train_df_processed, test_df_processed]:
        df["LATITUDE_USO"] = df["LATITUDE_USO"].astype(str).str.replace(",", ".", regex=False).astype(float)
        df["LONGITUDE_USO"] = df["LONGITUDE_USO"].astype(str).str.replace(",", ".", regex=False).astype(float)

        df["LATITUDE_USO"].fillna(df["LATITUDE_USO"].median(), inplace=True)
        df["LONGITUDE_USO"].fillna(df["LONGITUDE_USO"].median(), inplace=True)

    # --- Eliminar columna objetivo en test ---
    if TARGET in test_df_processed.columns:
        test_df_processed = test_df_processed.drop(columns=[TARGET])

    print("Datos preprocesados (lat/long convertidos a float, test sin target).")
    return train_df_processed, test_df_processed

def train_and_evaluate_model(df):
    """
    Entrena y evalúa el modelo de clasificación.
    """
    # Separar características (X) y objetivo (y)
    X = df[FEATURES]
    y = df[TARGET]

    # Codificar la variable objetivo (target) para que empiece en 0
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    num_class = len(le.classes_)

    # Dividir los datos en entrenamiento y validación (80% para entrenar, 20% para validar)
    X_train, X_val, y_train, y_val = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    print(f"Datos divididos: {len(X_train)} para entrenamiento, {len(X_val)} para validación.")
    
    # Instanciar el clasificador XGBoost
    clf = xgb.XGBClassifier(
        objective='multi:softmax', 
        num_class=num_class, 
        n_estimators=100, 
        random_state=42, 
        use_label_encoder=False, 
        eval_metric='mlogloss'
    )
    
    # Entrenar el modelo
    print("Entrenando el modelo XGBoost...")
    clf.fit(X_train, y_train)
    
    # --- Evaluación del Modelo ---
    # Hacemos predicciones en el conjunto de validación (datos que el modelo no ha visto)
    predictions_encoded = clf.predict(X_val)

    # Decodificar las predicciones para calcular la precisión con las etiquetas originales si es necesario
    # predictions = le.inverse_transform(predictions_encoded)

    # Calculamos la precisión (accuracy)
    accuracy = accuracy_score(y_val, predictions_encoded)

    print("-" * 30)
    print("Paso 4: Evaluación del modelo")
    print(f"Precisión (Accuracy) en el conjunto de validación: {accuracy:.2%}")
    print("Explicación: Este valor representa el porcentaje de predicciones correctas que hizo el modelo sobre el conjunto de validación.")
    print("Un valor más alto es mejor. Nos da una idea de cómo se comportará el modelo con datos nuevos.")
    print("-" * 30)

    return clf, le

def generate_submission_file(model, test_df, submission_path, label_encoder):
    """
    Genera el archivo de submission.
    """
    print("Paso 5: Generando archivo de predicciones...")

    # Asegurarse de que el DataFrame de prueba tenga las mismas columnas que se usaron para entrenar
    X_test = test_df[FEATURES]

    # Realizar predicciones
    test_predictions_encoded = model.predict(X_test)
    
    # Decodificar las predicciones para tener las etiquetas originales (1, 2, 3)
    test_predictions = label_encoder.inverse_transform(test_predictions_encoded)

    # Crear el DataFrame para el archivo de submission
    output = pd.DataFrame({
        # 'PassengerId': test_df.PassengerId, 
        'TIPO_TARIFA': test_predictions
    })

    # Guardar el archivo en formato CSV
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
    trained_model, label_encoder = train_and_evaluate_model(train_processed)
    # 4. Generar el archivo de predicciones (usando el modelo entrenado y los datos de prueba procesados)
    generate_submission_file(trained_model, test_processed, SUBMISSION_FILE_PATH, label_encoder)
    print("\nProceso completado.")

if __name__ == "__main__":
    main()
