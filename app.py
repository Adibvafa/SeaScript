import streamlit as st
import cv2
import numpy as np
import os
from PIL import Image
from sklearn.cluster import KMeans


# Define functions for image processing
def load_and_preprocess_image(image):
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    image = cv2.resize(image, (640, 480))  # Resize for consistency
    return image


def detect_windows_and_calculate_light(image):
    cfg_path = "yolov3.cfg"
    weights_path = "yolov3.weights"

    if not os.path.exists(cfg_path) or not os.path.exists(weights_path):
        raise FileNotFoundError("YOLO configuration or weight files not found. Please check the file paths.")

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
        for detected_layer in detection:
            if isinstance(detected_layer, np.ndarray):
                for detected_obj in detected_layer:
                    if detected_obj.ndim == 2 and detected_obj.shape[1] > 0:
                        for obj in detected_obj:
                            obj = obj.flatten()
                            if len(obj) > 5:
                                scores = obj[5:]
                                class_id = np.argmax(scores)
                                confidence = scores[class_id]
                                if confidence > 0.5 and class_id == 1:  # Assuming class_id 1 is a window
                                    center_x = int(obj[0] * width)
                                    center_y = int(obj[1] * height)
                                    w = int(obj[2] * width)
                                    h = int(obj[3] * height)
                                    window_area = w * h
                                    total_window_area += window_area
                                    cv2.rectangle(image, (center_x - w // 2, center_y - h // 2),
                                                  (center_x + w // 2, center_y + h // 2), (0, 255, 0), 2)

    return image, total_window_area


def analyze_colors(image, k=3):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_rgb = image_rgb.reshape((image_rgb.shape[0] * image_rgb.shape[1], 3))

    kmeans = KMeans(n_clusters=k)
    kmeans.fit(image_rgb)
    colors = kmeans.cluster_centers_

    return colors


def suggest_plants(sunlight, watering, size, window_area, dominant_colors):
    plant_suggestions = []

    if window_area > 100000:
        plant_suggestions.append("Fiddle Leaf Fig 🌿")
        plant_suggestions.append("Snake Plant 🌵")
    else:
        plant_suggestions.append("ZZ Plant 🪴")
        plant_suggestions.append("Pothos 🍃")

    if dominant_colors[0][0] > 200:
        plant_suggestions.append("Peace Lily 🌸")

    if sunlight.lower() in ["high", "bright"]:
        plant_suggestions.append("Fiddle Leaf Fig 🌿")
    else:
        plant_suggestions.append("ZZ Plant 🪴")

    if watering.lower() in ["weekly", "bi-weekly"]:
        plant_suggestions.append("Pothos 🍃")
    else:
        plant_suggestions.append("Cactus 🌵")

    if size.lower() in ["small", "medium"]:
        plant_suggestions.append("Peace Lily 🌸")
    else:
        plant_suggestions.append("Rubber Plant 🌳")

    plant_suggestions = list(set(plant_suggestions))
    plant_suggestions.sort()

    return plant_suggestions


def main_page():
    st.markdown("""
    <style>
    .main-container {
        background-color: #ffebf2;
        padding: 40px;
        border-radius: 25px;
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
        text-align: center;
        font-family: 'Lobster', cursive;
    }
    .title {
        color: #ff6f61;
        font-size: 40px;
        font-weight: bold;
    }
    .subtitle {
        color: #ff9a8b;
        font-size: 28px;
    }
    .button {
        background-color: #ff9a8b;
        color: #fff;
        border: none;
        padding: 15px 35px;
        border-radius: 20px;
        cursor: pointer;
        font-size: 20px;
        font-family: 'Lobster', cursive;
    }
    .button:hover {
        background-color: #ff6f61;
    }
    .icon {
        vertical-align: middle;
        margin-right: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<div class="title">🌸 UwU Plant Recommendation System 🌿</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Capture or Upload a Photo of Your Room 📸</div>', unsafe_allow_html=True)

    photo_file = st.camera_input("Take a photo of your room")

    if photo_file:
        st.session_state.photo = photo_file
        image = Image.open(photo_file)
        st.image(image, caption="Captured Photo ✨", use_column_width=True)

        st.session_state.image = image
        st.session_state.page = "quiz"

    if st.button("Proceed to Quiz 📝", key="proceed_button"):
        if "photo" in st.session_state:
            st.session_state.page = "quiz"
        else:
            st.warning("Please capture or upload a photo first. 🛑")

    st.markdown('</div>', unsafe_allow_html=True)


def display_quiz_page():
    st.markdown("""
    <style>
    .quiz-container {
        background-color: #ffebf2;
        padding: 40px;
        border-radius: 25px;
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
        font-family: 'Lobster', cursive;
    }
    .question {
        color: #ff6f61;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .form-submit-button {
        background-color: #ff9a8b;
        color: #fff;
        border: none;
        padding: 15px 35px;
        border-radius: 20px;
        cursor: pointer;
        font-size: 20px;
        font-family: 'Lobster', cursive;
    }
    .form-submit-button:hover {
        background-color: #ff6f61;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
    st.markdown('<div class="question">✨ Quiz Time! ✨</div>', unsafe_allow_html=True)
    st.markdown('<div class="question">Answer the following questions to get plant suggestions 💬</div>',
                unsafe_allow_html=True)

    with st.form(key='quiz_form'):
        sunlight = st.text_input("How much sunlight does your room get? ☀️", key="sunlight")
        watering = st.text_input("How often are you available to water the plants? 💧", key="watering")
        size = st.text_input("What size of plants are you interested in? 🌿", key="size")

        submit_button = st.form_submit_button("Save Answers ✅")

        if submit_button:
            if sunlight and watering and size:
                image_cv = load_and_preprocess_image(st.session_state.image)
                image_with_windows, total_window_area = detect_windows_and_calculate_light(image_cv)
                dominant_colors = analyze_colors(image_with_windows)

                plant_suggestions = suggest_plants(sunlight, watering, size, total_window_area, dominant_colors)

                st.write("🌟 Based on your photo and quiz responses, here are some plant suggestions: 🌟")
                for plant in plant_suggestions:
                    st.write(f"- {plant}")

                st.session_state.page = "main"
            else:
                st.write("Please answer all the questions. 🛑")

    st.markdown('</div>', unsafe_allow_html=True)


# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = "main"

# Display the current page based on session state
if st.session_state.page == "main":
    main_page()
elif st.session_state.page == "quiz":
    display_quiz_page()
