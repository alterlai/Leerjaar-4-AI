import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix


# ==== OPGAVE 1 ====
def plotNumber(nrVector):
    # Let op: de manier waarop de data is opgesteld vereist dat je gebruik maakt
    # van de Fortran index-volgorde – de eerste index verandert het snelst, de 
    # laatste index het langzaamst; als je dat niet doet, wordt het plaatje 
    # gespiegeld en geroteerd. Zie de documentatie op 
    # https://docs.scipy.org/doc/numpy/reference/generated/numpy.reshape.html

    nrVector = np.reshape(nrVector, (20, 20), 'F')  # Mogelijk 3e param 'F' megeven voor Fortran index volgorde
    plt.matshow(nrVector)
    plt.show()


# ==== OPGAVE 2a ====
def sigmoid(z):
    # Maak de code die de sigmoid van de input z teruggeeft. Zorg er hierbij
    # voor dat de code zowel werkt wanneer z een getal is als wanneer z een
    # vector is.
    # Maak gebruik van de methode exp() in NumPy.

    return 1 / (1 + np.exp(-z))


# ==== OPGAVE 2b ====
def get_y_matrix(y, m):
    # Gegeven een vector met waarden y_i van 1...x, retourneer een (ijle) matrix
    # van m×x met een 1 op positie y_i en een 0 op de overige posities.
    # Let op: de gegeven vector y is 1-based en de gevraagde matrix is 0-based,
    # dus als y_i=1, dan moet regel i in de matrix [1,0,0, ... 0] zijn, als
    # y_i=10, dan is regel i in de matrix [0,0,...1] (in dit geval is de breedte
    # van de matrix 10 (0-9), maar de methode moet werken voor elke waarde van 
    # y en m

    # elke waarde in y-1 is de index voor 1 en de rest is 0
    A = [1 for i in range(len(y))]
    groepering = [i for i in
                  range(len(y) + 1)]  # Row in de CSR (voor elke waarde in y moet er een row zijn, dus len(y))
    indices = np.reshape(y - 1, m)  # zet 1-based y om in 0-based JA -> dit is column in de CSR
    return csr_matrix((A, indices, groepering)).todense()


# ==== OPGAVE 2c ==== 
# ===== deel 1: =====
def predictNumber(Theta1, Theta2, X):
    # Deze methode moet een matrix teruggeven met de output van het netwerk
    # gegeven de waarden van Theta1 en Theta2. Elke regel in deze matrix 
    # is de waarschijnlijkheid dat het sample op die positie (i) het getal
    # is dat met de kolom correspondeert.

    # De matrices Theta1 en Theta2 corresponderen met het gewicht tussen de
    # input-laag en de verborgen laag, en tussen de verborgen laag en de
    # output-laag, respectievelijk. 

    # Een mogelijk stappenplan kan zijn:

    #    1. voeg enen toe aan de gegeven matrix X; dit is de input-matrix a1
    a1 = np.insert(X, 0, 1, axis=1)
    #    2. roep de sigmoid-functie van hierboven aan met a1 als actuele
    #       parameter: dit is de variabele a2
    a2 = sigmoid(np.dot(a1, np.transpose(Theta1)))
    #    3. voeg enen toe aan de matrix a2, dit is de input voor de laatste
    #       laag in het netwerk
    a2 = np.insert(a2, 0, 1, axis=1)
    #    4. roep de sigmoid-functie aan op deze a2; dit is het uiteindelijke
    #       resultaat: de output van het netwerk aan de buitenste laag.
    result = sigmoid(np.dot(a2, np.transpose(Theta2)))

    # Voeg enen toe aan het begin van elke stap en reshape de uiteindelijke
    # vector zodat deze dezelfde dimensionaliteit heeft als y in de exercise.
    return result


# ===== deel 2: =====
def computeCost(Theta1, Theta2, X, y):
    # Deze methode maakt gebruik van de methode predictNumber() die je hierboven hebt
    # geïmplementeerd. Hier wordt het voorspelde getal vergeleken met de werkelijk 
    # waarde (die in de parameter y is meegegeven) en wordt de totale kost van deze
    # voorspelling (dus met de huidige waarden van Theta1 en Theta2) berekend en
    # geretourneerd.
    # Let op: de y die hier binnenkomt is de m×1-vector met waarden van 1...10. 
    # Maak gebruik van de methode get_y_matrix() die je in opgave 2a hebt gemaakt
    # om deze om te zetten naar een matrix. 
    predictions = predictNumber(Theta1, Theta2, X)
    y_mat = get_y_matrix(y, len(X))
    print(y_mat.shape)
    print(predictions.shape)
    kost = (-1/len(X))*(sum(y_mat*np.log(np.transpose(predictions)) + (1-y_mat)*np.log(1-np.transpose(predictions))))
    return kost


# ==== OPGAVE 3a ====
def sigmoidGradient(z):
    # Retourneer hier de waarde van de afgeleide van de sigmoïdefunctie.
    # Zie de opgave voor de exacte formule. Zorg ervoor dat deze werkt met
    # scalaire waarden en met vectoren.
    return sigmoid(z)*(1-sigmoid(z))


# ==== OPGAVE 3b ====
def nnCheckGradients(Theta1, Theta2, X, y):
    # Retourneer de gradiënten van Theta1 en Theta2, gegeven de waarden van X en van y
    # Zie het stappenplan in de opgaven voor een mogelijke uitwerking.

    Delta2 = np.zeros(Theta1.shape)
    Delta3 = np.zeros(Theta2.shape)
    m = len(X)

    # Stap 1
    predictions = predictNumber(Theta1, Theta2, X)

    # Stap 2
    y_vec = get_y_matrix(y, m)
    d3 = predictions - y_vec

    # Stap 3
    error = np.transpose(Theta2) * np.transpose(d3) * sigmoidGradient(X)

    # TODO: plz halp Stap 4
    print(np.shape(sum(np.transpose(error))))
    print(np.shape(Theta2))
    print(np.shape(Theta1))

    # d2 = (np.dot(d3, Theta2)) * sigmoidGradient(d3)

    for i in range(m):
        pass

    Delta2_grad = Delta2 / m
    Delta3_grad = Delta3 / m

    return Delta2_grad, Delta3_grad
