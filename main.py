import streamlit as st
import os
from PIL import Image
from image_processing import load_and_preprocess_image, detect_windows_and_calculate_light, analyze_colors
from plant_recommendation import suggest_plants
from styles import get_styles


def main_page():
    st.markdown(get_styles(), unsafe_allow_html=True)
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
    st.markdown(get_styles(), unsafe_allow_html=True)
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
                process_quiz_answers(sunlight, watering, size)
            else:
                st.write("Please answer all the questions. 🛑")

    st.markdown('</div>', unsafe_allow_html=True)


def process_quiz_answers(sunlight, watering, size):
    image_cv = load_and_preprocess_image(st.session_state.image)
    cfg_path = "yolov3.cfg"
    weights_path = "yolov3.weights"

    if not os.path.exists(cfg_path) or not os.path.exists(weights_path):
        st.error("YOLO configuration or weight files not found. Please check the file paths.")
        return

    image_with_windows, total_window_area = detect_windows_and_calculate_light(image_cv, cfg_path, weights_path)
    dominant_colors = analyze_colors(image_with_windows)

    plant_suggestions = suggest_plants(sunlight, watering, size, total_window_area, dominant_colors)

    st.write("🌟 Based on your photo and quiz responses, here are some plant suggestions: 🌟")
    for plant in plant_suggestions:
        st.write(f"- {plant}")

    st.session_state.page = "main"


def main():
    if 'page' not in st.session_state:
        st.session_state.page = "main"

    if st.session_state.page == "main":
        main_page()
    elif st.session_state.page == "quiz":
        display_quiz_page()


if __name__ == "__main__":
    main()
