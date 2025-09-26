'''
Aprendizaje supervisado
Entrenamiento
Python y Machine Learning
'''
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from tqdm import tqdm

tqdm.pandas()  # Permite usar .progress_apply() en pandas

print("📂 Leyendo archivos CSV...")
train = pd.read_csv("titanic/train.csv")
test = pd.read_csv("titanic/test.csv")
print("✅ Archivos cargados")

print("🔄 Preprocesando datos...")
train['Sex'] = train['Sex'].map({'male': 0, 'female': 1})
test['Sex'] = test['Sex'].map({'male': 0, 'female': 1})

train['Age'] = train['Age'].fillna(train['Age'].median())
test['Age'] = test['Age'].fillna(train['Age'].median())
print("✅ Preprocesamiento completado")

X = train[['Pclass', 'Sex', 'Age']]
y = train['Survived']

print("🤖 Entrenando modelo...")
clf = RandomForestClassifier(n_estimators=100, verbose=1, n_jobs=-1)
clf.fit(X, y)
print("✅ Modelo entrenado")

print("📊 Generando predicciones...")
pred = clf.predict(test[['Pclass', 'Sex', 'Age']])

output = pd.DataFrame({'PassengerId': test.PassengerId, 'Survived': pred})
output.to_csv('submission.csv', index=False)
print("💾 Archivo 'submission.csv' guardado correctamente")
