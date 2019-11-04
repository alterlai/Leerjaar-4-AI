# Dit is het eigen gemaakte neurale netwerk
# Authors: Jeroen van der Laan, Sander van Doorn.
import os
import numpy as np
from PIL import Image

DATASET_DIR = "./Fundus-data"

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

dataset, y = load_dataset()
pass
