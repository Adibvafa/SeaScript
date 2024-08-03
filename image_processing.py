import cv2
import numpy as np
from sklearn.cluster import KMeans

def load_and_preprocess_image(image):
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    image = cv2.resize(image, (640, 480))  # Resize for consistency
    return image

def detect_windows_and_calculate_light(image, cfg_path, weights_path):
    net = cv2.dnn.readNetFromDarknet(cfg_path, weights_path)
    
    layer_names = net.getLayerNames()
    output_layer_indices = net.getUnconnectedOutLayers() - 1
    output_layers = [layer_names[i] for i in output_layer_indices]

    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    detections = net.forward(output_layers)

    height, width, channels = image.shape
    total_window_area = 0

    for detection in detections:
        for detected_obj in detection:
            scores = detected_obj[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and class_id == 1:  # Assuming class_id 1 is a window
                center_x, center_y, w, h = (detected_obj[0:4] * np.array([width, height, width, height])).astype(int)
                window_area = w * h
                total_window_area += window_area
                cv2.rectangle(image, (center_x - w // 2, center_y - h // 2), (center_x + w // 2, center_y + h // 2), (0, 255, 0), 2)

    return image, total_window_area

def analyze_colors(image, k=3):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_rgb = image_rgb.reshape((-1, 3))
    
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(image_rgb)
    colors = kmeans.cluster_centers_
    
    return colors