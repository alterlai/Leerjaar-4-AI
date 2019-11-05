# Dit is het eigen gemaakte neurale netwerk
# Authors: Jeroen van der Laan, Sander van Doorn.
import os
import numpy as np
from PIL import Image
from scipy.sparse import csr_matrix

DATASET_DIR = "./Fundus-data"
INPUT_LAYER_SIZE = 5625     # 75x75
HIDDEN_LAYER_SIZE = 128
NUM_LABELS = 30     # 0 - 29 labels

def load_dataset():
    dataset = np.ndarray((1000, 75, 75))
    y = []
    i = 0
    for dir in os.listdir(DATASET_DIR):
        for image in os.listdir(DATASET_DIR+"/"+dir):
            image = Image.open(DATASET_DIR+"/"+dir+"/"+image).convert("L")
            dataset[i] = np.asarray(image)
            i += 1
            y.append(dir)
    return dataset, np.asarray(y)


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def get_y_matrix(y, m):
    A = [1 for i in range(len(y))]
    groepering = [i for i in
                  range(len(y) + 1)]  # Row in de CSR (voor elke waarde in y moet er een row zijn, dus len(y))
    indices = np.reshape(y - 1, m)  # zet 1-based y om in 0-based JA -> dit is column in de CSR
    return csr_matrix((A, indices, groepering)).toarray()


def predictNumber(Theta1, Theta2, X):
    a1 = np.insert(X, 0, 1, axis=1)
    a2 = sigmoid(np.dot(a1, np.transpose(Theta1)))
    a2 = np.insert(a2, 0, 1, axis=1)
    result = sigmoid(np.dot(a2, np.transpose(Theta2)))

def randInitializeWeights(in_conn, out_conn):
    epsilon_init = 0.12
    # W = rand(L_out, 1 + L_in) * 2 * epsilon_init - epsilon_init;
    W = np.random.rand(out_conn, 1 + in_conn) * 2 * epsilon_init - epsilon_init
    return W

def nnCheckGradients(Theta1, Theta2, X, y):
    # Retourneer de gradiënten van Theta1 en Theta2, gegeven de waarden van X en van y
    # Zie het stappenplan in de opgaven voor een mogelijke uitwerking.

    Delta2 = np.zeros(Theta1.shape)
    Delta3 = np.zeros(Theta2.shape)
    m, n = np.shape(X)  # voorbeeldwaarde; dit moet je natuurlijk aanpassen naar de echte waarde van m
    y_vec = get_y_matrix(y, m)

    for i in range(m):
        a1 = np.insert(X[i], 0, 1)
        z2 = np.dot(Theta1, a1)
        a2 = sigmoid(z2)
        a2 = np.insert(a2, 0, 1)
        a3 = sigmoid(np.dot(a2, np.transpose(Theta2)))

        # stap 2
        d3 = a3 - y_vec[i]
        d2 = np.dot(Theta2.T, d3)[1:] * sigmoidGradient(z2)

        # stap 3
        Delta3 = Delta3 + np.dot(d3, a3)
        Delta2 = Delta2 + np.dot(np.insert(d2, 0, 1), a2)

    Delta2_grad = Delta2 / m
    Delta3_grad = Delta3 / m

    return Delta2_grad, Delta3_grad


def sigmoidGradient(z):
    # Retourneer hier de waarde van de afgeleide van de sigmoïdefunctie.
    # Zie de opgave voor de exacte formule. Zorg ervoor dat deze werkt met
    # scalaire waarden en met vectoren.
    return sigmoid(z) * (1 - sigmoid(z))


X, y = load_dataset()
flatX = X.reshape((1000, 5625))
Theta1 = randInitializeWeights(INPUT_LAYER_SIZE, HIDDEN_LAYER_SIZE)
Theta2 = randInitializeWeights(HIDDEN_LAYER_SIZE, NUM_LABELS)

results = nnCheckGradients(Theta1, Theta2, flatX, y)
pass


