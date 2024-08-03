def get_styles():
    return """
    <style>
    .stApp {
        background-color: white;
    }
    .stApp > header {
        background-color: transparent;
    }
    .stApp .block-container {
        max-width: 800px !important;
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    /* Style for the main container */
    .stApp .element-container:first-child {
        background-color: #ffebf2;
        border-radius: 25px;
        padding: 2rem;
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
        margin: 0 auto;
        max-width: 100%;
    }
    /* Center all content */
    .stApp .element-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    .title {
        margin-bottom: 30px;
        color: #ff6f61;
        font-size: 40px;
        font-weight: bold;
        font-family: 'Lobster', cursive;
        width: 100%;
    }
    .subtitle {
        margin-bottom: 20px;
        color: #ff9a8b;
        font-size: 28px;
        font-family: 'Lobster', cursive;
        width: 100%;
    }
    .stButton > button {
        background-color: #ff9a8b;
        color: #fff;
        border: none;
        padding: 15px 40px;
        border-radius: 20px;
        cursor: pointer;
        font-size: 22px;
        font-family: 'Lobster', cursive;
        width: 100%;
        max-width: 300px;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #ff6f61;
    }
    .question {
        color: #ff6f61;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
        font-family: 'Lobster', cursive;
        width: 100%;
    }
    .stForm {
        width: 100%;
        max-width: 500px;
    }
    .stForm > button {
        background-color: #ff9a8b;
        color: #fff;
        border: none;
        padding: 15px 35px;
        border-radius: 20px;
        cursor: pointer;
        font-size: 20px;
        font-family: 'Lobster', cursive;
        width: 100%;
        transition: background-color 0.3s ease;
    }
    .stForm > button:hover {
        background-color: #ff6f61;
    }
    .stTextInput > div > div > input {
        font-family: 'Lobster', cursive;
        text-align: center;
    }
    .stTextInput > label {
        font-family: 'Lobster', cursive;
        color: #ff6f61;
    }
    .stImage {
        display: flex;
        justify-content: center;
    }
    .stImage > img {
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        max-width: 100%;
        height: auto;
    }
    /* Ensure all elements respect max-width */
    .element-container, .stTextInput, .stButton, div[data-testid="stForm"] {
        max-width: 100%;
    }
    /* Center camera input */
    .stCamera {
        display: flex;
        justify-content: center;
        width: 100%;
    }
    .stCamera > div {
        max-width: 350px;
    }
    </style>
    """