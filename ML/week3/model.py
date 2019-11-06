# Dit is het eigen gemaakte neurale netwerk
# Authors: Jeroen van der Laan, Sander van Doorn.
import os
import numpy as np
from PIL import Image
from scipy.sparse import csr_matrix
import scipy.optimize

DATASET_DIR = "./Fundus-data"
INPUT_LAYER_SIZE = 5625     # 75x75
HIDDEN_LAYER_SIZE = 128
NUM_LABELS = 39     # 0 - 39 labels
name_mapping = []

def load_dataset():
    dataset = np.ndarray((1000, 75, 75))
    y = []
    i = 0
    for dir in os.listdir(DATASET_DIR):
        name_mapping.append(dir)
        for image in os.listdir(DATASET_DIR+"/"+dir):
            image = Image.open(DATASET_DIR+"/"+dir+"/"+image).convert("L")
            dataset[i] = np.asarray(image)
            y.append(len(name_mapping) -1)
            i += 1
    return dataset, np.asarray(y)


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def get_y_matrix(y, m):
    rows = [i for i in range(len(y) + 1)]
    columns = y
    data = [1 for i in y]
    y_vec = csr_matrix((data, columns, rows)).toarray()
    return y_vec


def predictNumber(Theta1, Theta2, X):
    a1 = np.insert(X, 0, 1, axis=1)
    a2 = sigmoid(np.dot(a1, np.transpose(Theta1)))
    a2 = np.insert(a2, 0, 1, axis=1)
    result = sigmoid(np.dot(a2, np.transpose(Theta2)))
    return result

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


def nnCostFunction(Thetas, X, y):
    global INPUT_LAYER_SIZE, HIDDEN_LAYER_SIZE, NUM_LABELS
    size = HIDDEN_LAYER_SIZE * (1 + INPUT_LAYER_SIZE)  # +1 want de bias-node zit wel in de matrix
    Theta1 = Thetas[:size].reshape(HIDDEN_LAYER_SIZE, INPUT_LAYER_SIZE + 1)
    Theta2 = Thetas[size:].reshape(NUM_LABELS, HIDDEN_LAYER_SIZE + 1)
    J = computeCost(Theta1, Theta2, X, y)
    grad1, grad2 = nnCheckGradients(Theta1, Theta2, X, y)
    return J, np.concatenate((grad1.flatten(), grad2.flatten()))

def callbackF(Xi):
    global itr
    print("iteration {}".format(itr))
    itr += 1


def computeCost(Theta1, Theta2, X, y):
    predictions = predictNumber(Theta1, Theta2, X)
    y_vec = get_y_matrix(y, len(X))

    # kost = (-1/len(X))*(sum(y_mat*np.log(np.transpose(predictions)) + (1-y_mat)*np.log(1-np.transpose(predictions))))
    return (1 / len(X)) * sum(
        sum(-y_vec * np.log(predictions) - (1 - y_vec) * np.log(1 - predictions)))


X, y = load_dataset()
flatX = X.reshape((1000, 5625))
Theta1 = randInitializeWeights(INPUT_LAYER_SIZE, HIDDEN_LAYER_SIZE)
Theta2 = randInitializeWeights(HIDDEN_LAYER_SIZE, NUM_LABELS)

init_params = np.concatenate((Theta1.flatten(), Theta2.flatten()))
args = (X, y)
res = scipy.optimize.minimize(nnCostFunction, init_params, args=args, method='CG', callback=callbackF, jac=True,
               options={'maxiter': 30, 'disp': True})
size = HIDDEN_LAYER_SIZE * (
            INPUT_LAYER_SIZE + 1)  # voor de bias-node die wel in de matrix zit maar niet geplot moet worden
res_Theta1 = res['x'][:size].reshape(HIDDEN_LAYER_SIZE, INPUT_LAYER_SIZE + 1)
res_Theta2 = res['x'][size:].reshape(NUM_LABELS, HIDDEN_LAYER_SIZE + 1)

cost = computeCost(res_Theta1, res_Theta2, X, y)
print("Totale cost is nu:", cost)
pred = np.argmax(predictNumber(res_Theta1, res_Theta2, X), axis=1) + 1
pass


