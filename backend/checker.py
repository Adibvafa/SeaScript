import matlab.engine
import numpy as np
import tempfile
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

def handle_grading(func_name, func_source):
    mongo_uri = os.getenv("mongodb_uri")
    database_name = "matlab"
    collection_name = "matlab"

    model_answer, model_input = get_model_answer_and_input(mongo_uri, database_name, collection_name, func_name)

    if model_answer != None and model_input != None:
        return evaluate_matlab_function(func_source, func_name, model_answer, model_input)
    # raise "No model answer found" # Commented out for demo
    return True, None


def get_model_answer_and_input(mongo_uri, database_name, collection_name, func_name_value):
    client = MongoClient(mongo_uri)
    
    # Access the database
    db = client.get_database(database_name)
    
    # Access the collection
    collection = db[collection_name]
    
    # Query the collection for the item with the specific func_name key
    query = {"id": func_name_value}
    item = collection.find_one(query)
    
    # Get the model_answer attribute
    if item:
        model_answer = item.get("answer")
        model_input = item.get("test")
        return model_answer, model_input
    else:
        return None, None


def evaluate_matlab_function(matlab_func_str, func_name, model_answer, *args):
    # Start MATLAB engine
    eng = matlab.engine.start_matlab()
    
    try:
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a temporary .m file with the function code
            file_path = os.path.join(temp_dir, f"{func_name}.m")
            with open(file_path, 'w') as f:
                f.write(matlab_func_str)
            
            # Add the temporary directory to MATLAB's path
            eng.addpath(temp_dir)
            
            # Get the MATLAB function
            matlab_func = getattr(eng, func_name)
            
            # Execute the MATLAB function
            result = matlab_func(*args)
            
            # Convert result to numpy array if it's a MATLAB array
            if isinstance(result, matlab.double):
                result = np.array(result)
            
            # Compare the result with the model answer
            if isinstance(model_answer, (list, np.ndarray)):
                is_correct = np.allclose(result, model_answer)
            else:
                is_correct = np.isclose(result, model_answer)
            
            return is_correct, result

    except:
        return False, None
    
    finally:
        # Stop MATLAB engine
        eng.quit()


if __name__ == "__main__":
    handle_grading("1", "sin")
