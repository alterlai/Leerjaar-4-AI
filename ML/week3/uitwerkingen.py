import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow import keras

DEFCON_LEVEL = 1

# OPGAVE 1a
def plotImage(img, label):
    # Deze methode krijgt een matrix mee (in img) en een label dat correspondeert met het 
    # plaatje dat in de matrix is weergegeven. Zorg ervoor dat dit grafisch wordt weergegeven.
    # Maak gebruik van plt.cm.binary voor de cmap-parameter van plt.imgshow.

    # YOUR CODE HERE
    plt.imshow(img, cmap=plt.cm.binary)
    plt.xlabel(label)
    plt.show()
    pass


# OPGAVE 1b
def scaleData(X):
    # Deze methode krijgt een matrix mee waarin getallen zijn opgeslagen van 0..m, en hij 
    # moet dezelfde matrix retourneren met waarden van 0..1. Deze methode moet werken voor 
    # alle maximal waarde die in de matrix voorkomt.
    # Deel alle elementen in de matrix 'element wise' door de grootste waarde in deze matrix.
    max = np.amax(X)
    return X/max



# OPGAVE 1c
def buildModel():
    # Deze methode maakt het keras-model dat we gebruiken voor de classificatie van de mnist
    # dataset. Je hoeft deze niet abstract te maken, dus je kunt er van uitgaan dat de input
    # layer van dit netwert alleen geschikt is voor de plaatjes in de opgave (wat is de 
    # dimensionaliteit hiervan?).
    # Maak een model met een input-laag, een volledig verbonden verborgen laag en een softmax
    # output-laag. Compileer het netwerk vervolgens met de gegevens die in opgave gegeven zijn
    # en retourneer het resultaat.

    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Flatten())    # Input layer
    model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    return model


# OPGAVE 2a
def confMatrix(labels, pred):
    # Retourneer de econfusion matrix op basis van de gegeven voorspelling (pred) en de actuele
    # waarden (labels). Check de documentatie van tf.math.confusion_matrix
    
    return tf.math.confusion_matrix(labels, pred)
    pass

# OPGAVE 2b
def confEls(conf, labels): 
    # Deze methode krijgt een confusion matrix mee (conf) en een set van labels. Als het goed is, is 
    # de dimensionaliteit van de matrix gelijk aan len(labels) × len(labels) (waarom?). Bereken de 
    # waarden van de TP, FP, FN en TN conform de berekening in de opgave. Maak vervolgens gebruik van
    # de methodes zip() en list() om een list van len(labels) te retourneren, waarbij elke tupel 
    # als volgt is gedefinieerd:
    #     (categorie:string, tp:int, fp:int, fn:int, tn:int)
 
    # Check de documentatie van numpy diagonal om de eerste waarde te bepalen.
    results = []
    for i in range(len(labels)):
        tp = conf[i][i]
        fp = sum(conf[:,i]) - tp
        fn = sum(conf[i]) - tp
        tn = sum(sum(conf)) - tp - fn - fp
        results.append((labels[i], tp, fp, fn, tn))
    return results

# OPGAVE 2c
def confData(metrics):
    # Deze methode krijgt de lijst mee die je in de vorige opgave hebt gemaakt (dus met lengte len(labels))
    # Maak gebruik van een list-comprehension om de totale tp, fp, fn, en tn te berekenen en
    # bepaal vervolgens de metrieken die in de opgave genoemd zijn. Retourneer deze waarden in de
    # vorm van een dictionary (de scaffold hiervan is gegeven).

    # VERVANG ONDERSTAANDE REGELS MET JE EIGEN CODE

    tp = sum([i[1] for i in metrics])
    fp = sum([i[2] for i in metrics])
    fn = sum([i[3] for i in metrics])
    tn = sum([i[4] for i in metrics])

    # BEREKEN HIERONDER DE JUISTE METRIEKEN EN RETOURNEER DIE
    # ALS EEN DICTIONARY
    tpr = tp/(tp+fn)
    ppv = tp/(tp+fp)
    tnr = tn/(tn+fp)
    fpr = fp/(fp+tn)

    rv = {'tpr':tpr, 'ppv':ppv, 'tnr':tnr, 'fpr':fpr }
    return rv
