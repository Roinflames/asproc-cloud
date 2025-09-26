"""
Aprendizaje Supervisado - Ejemplo Titanic
Refactorizado para fines educativos.

Este script realiza los siguientes pasos:
 1. Carga los datos de entrenamiento y prueba del Titanic.
 2. Preprocesa los datos para convertirlos a un formato numérico y manejar valores faltantes.
 3. Divide los datos de entrenamiento para poder evaluar el modelo.
 4. Entrena un modelo de clasificación (Random Forest).
 5. Evalúa el rendimiento del modelo usando la métrica de precisión (accuracy).
 6. Genera un archivo de predicciones para la competencia de Kaggle.
"""
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os # Importamos os para manejar rutas de archivo de forma robusta

# --- 1. Definición de Constantes y Rutas ---
# Es una buena práctica definir las rutas y variables importantes en un solo lugar.
# Usamos os.path.join y os.path.dirname(__file__) para construir rutas robustas
# que funcionen sin importar desde dónde se ejecute el script.
SCRIPT_DIR = os.path.dirname(__file__)
TRAIN_FILE_PATH = os.path.join(SCRIPT_DIR, "titanic", "train.csv")
TEST_FILE_PATH = os.path.join(SCRIPT_DIR, "titanic", "test.csv")
SUBMISSION_FILE_PATH = os.path.join(SCRIPT_DIR, "submission.csv")
    
    # Definimos las características (features) que usaremos para entrenar el modelo y el objetivo (target).
FEATURES = ['Pclass', 'Sex', 'Age']
TARGET = 'Survived'
    
    
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
    print("Paso 2: Preprocesando datos...")

    # Hacemos una copia para evitar advertencias de SettingWithCopyWarning
    train_df_processed = train_df.copy()
    test_df_processed = test_df.copy()

    # Convertir 'Sex' a 0 y 1.
    sex_mapping = {'male': 0, 'female': 1}
    train_df_processed['Sex'] = train_df_processed['Sex'].map(sex_mapping)
    test_df_processed['Sex'] = test_df_processed['Sex'].map(sex_mapping)

    # Rellenar valores faltantes en 'Age'.
    # ¡Importante! Usamos la mediana del conjunto de entrenamiento para rellenar AMBOS conjuntos.
    # Esto evita la "fuga de datos" (data leakage) del conjunto de prueba al de entrenamiento.
    median_age = train_df_processed['Age'].median()
    print(f"La edad media para rellenar valores faltantes es: {median_age:.2f}")
    train_df_processed['Age'] = train_df_processed['Age'].fillna(median_age)
    test_df_processed['Age'] = test_df_processed['Age'].fillna(median_age)

    print("Datos preprocesados.")
    return train_df_processed, test_df_processed
    
    
def train_and_evaluate_model(df):
    """
    Entrena y evalúa el modelo de clasificación.
    """
    print("Paso 3: Entrenando y evaluando el modelo...")

    # Separar características (X) y objetivo (y)
    X = df[FEATURES]
    y = df[TARGET]

    # Dividir los datos en entrenamiento y validación (80% para entrenar, 20% para validar)
    # random_state asegura que la división sea siempre la misma, para reproducibilidad.
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    print(f"Datos divididos: {len(X_train)} para entrenamiento, {len(X_val)} para validación.")

    # Inicializar el clasificador
    clf = RandomForestClassifier(n_estimators=100, random_state=42, verbose=0)

    # Entrenar el modelo
    print("Entrenando el modelo RandomForest...")
    clf.fit(X_train, y_train)

    # --- Evaluación del Modelo ---
    # Hacemos predicciones en el conjunto de validación (datos que el modelo no ha visto)
    predictions = clf.predict(X_val)

    # Calculamos la precisión (accuracy)
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
    Genera el archivo de submission para Kaggle.
    """
    print("Paso 5: Generando archivo de predicciones...")

    # Asegurarse de que el DataFrame de prueba tenga las mismas columnas que se usaron para entrenar
    X_test = test_df[FEATURES]

    # Realizar predicciones
    test_predictions = model.predict(X_test)

    # Crear el DataFrame para el archivo de submission
    output = pd.DataFrame({'PassengerId': test_df.PassengerId, 'Survived': test_predictions})

    # Guardar el archivo en formato CSV
    output.to_csv(submission_path, index=False)
    print(f"Archivo de predicciones guardado en: {submission_path}")


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