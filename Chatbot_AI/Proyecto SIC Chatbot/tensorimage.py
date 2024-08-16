#!pip install tensorflow
#!pip install keras

from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
import numpy as np
from scipy.spatial import distance
import os

def image_comparison(img_path):
    # Load the ResNet50 model
    model = ResNet50(weights='imagenet')
    # Load the image you want to compare
    img_to_compare = image.load_img(img_path, target_size=(224, 224))
    img_to_compare = image.img_to_array(img_to_compare)
    img_to_compare = np.expand_dims(img_to_compare, axis=0)
    img_to_compare = preprocess_input(img_to_compare)
    # Extract feature vector for the image
    feature_vec_to_compare = model.predict(img_to_compare)
    # Iterate over all images in the folder
    folder_path = "/content/imgcomp"
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg"):
            # Load and preprocess the image
            img = image.load_img(os.path.join(folder_path, filename), target_size=(224, 224))
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            img = preprocess_input(img)
            # Extract feature vector for the image
            feature_vec = model.predict(img)
            # Compute distance between the feature vectors
            dist = distance.euclidean(feature_vec_to_compare, feature_vec)
            if dist == 0:
                return "Existe el producto"
                break
            else:
                return "no tenemos de ese producto"

