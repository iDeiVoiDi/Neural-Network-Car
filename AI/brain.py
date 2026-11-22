
import numpy as np


class Brain:

    def __init__(self):
        # Pesos inicializados con He
        self.W1 = np.random.randn(7, 64).astype(np.float32) * np.sqrt(2 / 7)
        self.b1 = np.zeros((1, 64), dtype=np.float32)

        self.W2 = np.random.randn(64, 32).astype(np.float32) * np.sqrt(2 / 64)
        self.b2 = np.zeros((1, 32), dtype=np.float32)

        self.W3 = np.random.randn(32, 1).astype(np.float32) * np.sqrt(2 / 32)
        self.b3 = np.zeros((1, 1), dtype=np.float32)

    def forward(self, inputs):

        # Primera capa
        z1 = inputs @ self.W1 + self.b1
        a1 = np.maximum(0, z1)

        # Segunda capa
        z2 = a1 @ self.W2 + self.b2
        a2 = np.maximum(0, z2)

        # Salida
        z3 = a2 @ self.W3 + self.b3
        output = np.tanh(z3)

        return output

    def predict(self, sensors):

        sensors = np.asarray(
            sensors, dtype=np.float32
        ).reshape(1, 7)

        return float(self.forward(sensors)[0, 0])

    def save(self, path):
        np.savez_compressed(
            path,
            W1=self.W1, b1=self.b1,
            W2=self.W2, b2=self.b2,
            W3=self.W3, b3=self.b3
        )

    def load(self, path):
        data = np.load(path)

        self.W1 = data["W1"]
        self.b1 = data["b1"]
        self.W2 = data["W2"]
        self.b2 = data["b2"]
        self.W3 = data["W3"]
        self.b3 = data["b3"]
