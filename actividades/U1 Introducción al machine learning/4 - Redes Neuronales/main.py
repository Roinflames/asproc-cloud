'''
Aprendizaje supervisado ✅
Redes neuronales ✅ (MLP con PyTorch)
Backpropagation ✅ (loss.backward() + optimizer.step())
Entrenamiento ✅ (ciclo de épocas con forward/loss/backprop/actualización)
Python y Machine Learning ✅ (PyTorch + sklearn)
'''
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 1) Datos sintéticos (no requiere internet)
X, y = make_moons(n_samples=1000, noise=0.25, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val   = scaler.transform(X_val)

X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.long)
X_val   = torch.tensor(X_val, dtype=torch.float32)
y_val   = torch.tensor(y_val, dtype=torch.long)

# 2) Modelo (MLP)
class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2, 16),
            nn.ReLU(),
            nn.Linear(16, 16),
            nn.ReLU(),
            nn.Linear(16, 2)  # 2 clases
        )
    def forward(self, x):
        return self.net(x)

model = MLP()

# 3) Pérdida y optimizador
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3)

# 4) Entrenamiento con backpropagation
for epoch in range(200):
    model.train()
    optimizer.zero_grad()
    logits = model(X_train)           # forward
    loss = criterion(logits, y_train) # compute loss
    loss.backward()                   # <<< backpropagation
    optimizer.step()                  # <<< update pesos

    if (epoch+1) % 40 == 0:
        model.eval()
        with torch.no_grad():
            val_logits = model(X_val)
            val_pred = val_logits.argmax(dim=1)
            acc = (val_pred == y_val).float().mean().item()
        print(f"Epoch {epoch+1:3d} | loss={loss.item():.4f} | val_acc={acc:.3f}")
