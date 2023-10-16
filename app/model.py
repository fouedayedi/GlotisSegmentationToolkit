from tensorflow.keras.models import load_model
from PIL import Image
import os
import tensorflow as tf
from tensorflow.keras.metrics import MeanIoU
from PIL import Image
import numpy as np
import cv2

def preprocess_image(img_path):
    img = Image.open(img_path).convert("L")
    img = img.resize((256, 256))
    img_array = np.array(img).astype(np.float32) / 255.0
    return np.expand_dims(img_array, axis=0)  # shape will be (1, 256, 256, 1)


def iou_metric(y_true, y_pred, smooth=1e-6):
    y_pred = tf.cast(y_pred > 0.5, dtype=tf.float32)
    intersection = tf.reduce_sum(y_true * y_pred)
    union = tf.reduce_sum(y_true) + tf.reduce_sum(y_pred) - intersection
    return (intersection + smooth) / (union + smooth)


def iou_metric_2(y_true, y_pred, smooth=1e-6):
    intersection = np.sum(y_true * y_pred)
    union = np.sum(y_true) + np.sum(y_pred) - intersection
    return (intersection + smooth) / (union + smooth)

def dice_loss(y_true, y_pred):
    smooth = 1e-6
    y_pred = tf.cast(y_pred > 0.5, dtype=tf.float32)
    intersection = tf.reduce_sum(y_true * y_pred)
    return 1 - (2. * intersection + smooth) / (tf.reduce_sum(y_true) + tf.reduce_sum(y_pred) + smooth)




def calculate_surface(mask_path):
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    _, binary_mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
    white_pixels = np.sum(binary_mask == 255)
    return white_pixels

def calculate_iou(true_mask_path, predicted_mask_path):
    true_mask = cv2.imread(true_mask_path, cv2.IMREAD_GRAYSCALE)
    predicted_mask = cv2.imread(predicted_mask_path, cv2.IMREAD_GRAYSCALE)
    # Convert to binary masks
    true_mask = (true_mask > 127).astype(np.uint8)
    predicted_mask = (predicted_mask > 127).astype(np.uint8)

    return iou_metric_2(true_mask, predicted_mask)




MODEL_PATH = './model/unet_model_batchsize_8_epochs_15_data_0.4.hdf5'
model = load_model(MODEL_PATH, custom_objects={"iou_metric": iou_metric, "dice_loss": dice_loss})


def segment_image(input_filepath, filename, output_folder,selected_model="Unet"):
    
    output_filepath = os.path.join(output_folder, f'seg_{filename}')
    if selected_model== "Unet" :
        img = preprocess_image(input_filepath)
        segmented_image_array = model.predict(img)
        single_image_array = np.squeeze(segmented_image_array[0])
        single_image_array = (single_image_array * 255).astype(np.uint8)
        segmented_image = Image.fromarray(single_image_array)
        
        
    elif selected_model== "kmeans":
        print("kmeans")
    else :
        print("meanshift")
    segmented_image.save(output_filepath)
    return(output_filepath)


