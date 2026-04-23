import cv2
import numpy as np
import os
import tensorflow as tf
import tqdm

# Habilitar carga de capas Lambda personalizadas
import keras
try:
    keras.config.enable_unsafe_deserialization()
except:
    pass

from mltu.utils.text_utils import ctc_decoder
from mltu.configs import BaseModelConfigs

class CaptchaPredictor:
    def __init__(self, model_path, configs_path):
        self.configs = BaseModelConfigs.load(configs_path)
        self.model = tf.keras.models.load_model(model_path, compile=False, safe_mode=False)
        self.char_list = self.configs.vocab
        
    def preprocess(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            return None
            
        # Transformación Visual (Propuesta 2: Relleno)
        img_array = 255 - image
        kernel_close = np.ones((3, 3), np.uint8)
        img_array = cv2.morphologyEx(img_array, cv2.MORPH_CLOSE, kernel_close, iterations=1)
        kernel_dilate = np.ones((2, 2), np.uint8)
        img_array = cv2.dilate(img_array, kernel_dilate, iterations=1)
        
        # Resize y normalización implícita (el modelo tiene capa Lambda / 255)
        img_resized = cv2.resize(img_array, (self.configs.width, self.configs.height))
        input_data = np.expand_dims(img_resized, axis=0).astype(np.float32)
        
        return input_data

    def predict(self, image_path):
        processed_image = self.preprocess(image_path)
        if processed_image is None:
            return "FILE_NOT_FOUND"
            
        preds = self.model.predict(processed_image, verbose=0)
        text = ctc_decoder(preds, self.char_list)[0]
        return text
