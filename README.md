# Plant Recommendation System 🌿

This Streamlit application recommends plants based on a photo of your room and your preferences. It uses computer vision to analyze the room's lighting conditions and combines this information with user input to suggest suitable plants.

## 📋 Prerequisites

Before you begin, ensure you have met the following requirements:

* You have installed Python 3.7 or later.
* You have a Windows/Linux/Mac machine.

## 🚀 Setting Up Plant Recommendation System

To install the Plant Recommendation System, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/Adibvafa/HackThe6ix.git
   cd HackThe6ix
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Download the YOLO weights and configuration files:
   - Download `yolov3.weights` from the official YOLO website.
   - Download `yolov3.cfg` from the YOLO GitHub repository.
   - Place both files in the project root directory.

## 🌟 Using Plant Recommendation System

To use the Plant Recommendation System, follow these steps:

1. Ensure you're in the project directory and your virtual environment is activated (if you're using one).

2. Run the Streamlit app:
   ```
   streamlit run main.py
   ```

3. Open your web browser and go to the URL displayed in your terminal (usually `http://localhost:8501`).

4. Use the app:
   - Take or upload a photo of your room.
   - Answer the questions about sunlight, watering habits, and preferred plant size.
   - Receive personalized plant recommendations!

## 🤝 Contributing to Plant Recommendation System

To contribute to Plant Recommendation System, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

Alternatively, see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## 📬 Contact

If you want to contact the project maintainers, you can reach out through the GitHub repository: [https://github.com/Adibvafa/HackThe6ix](https://github.com/Adibvafa/HackThe6ix)

## 📜 License

This project uses the following license: [MIT License](https://github.com/Adibvafa/HackThe6ix/blob/main/LICENSE).