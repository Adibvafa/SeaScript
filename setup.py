import matlab.engine
from pymongo import MongoClient
import os
from dotenv import load_dotenv

def setup_resources():
    # Load environment variables
    load_dotenv()

    # Database constants
    MONGO_URI = os.getenv("mongodb_uri")
    DATABASE_NAME = "matlab"
    COLLECTION_NAME = "matlab"

    # Create MongoDB client and get collection
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    # Start MATLAB engine
    matlab_engine = matlab.engine.start_matlab()

    return matlab_engine, collection, mongo_client

if __name__ == "__main__":
    matlab_engine, collection, mongo_client = setup_resources()
    print("Resources set up successfully.")
    print("Don't forget to close these resources when you're done!")